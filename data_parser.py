"""
data_parser.py - Ultra-Flexible Multi-File & Multi-Sheet Ingestion Engine for PAMOHI ATS.
Supports any number of uploaded files/sheets with diverse custom headers,
automatic header row detection, fuzzy synonym mapping, dynamic column preservation,
and robust ATS stage classification.
"""

import io
import re
import pandas as pd
import numpy as np


# ==============================================================================
# 1. FUZZY COLUMN SYNONYM DICTIONARIES
# ==============================================================================

SYNONYMS = {
    # Candidate Tracker Standard Fields
    "Candidate Name": [
        "candidate name", "candidate", "name", "applicant name", "applicant",
        "full name", "talent name", "consultant name", "consultant", "employee name"
    ],
    "Position": [
        "position", "position title", "role", "job title", "designation",
        "profile", "job role", "requirement", "title", "job name", "technology", "tech stack"
    ],
    "Phone Number": [
        "phone number", "phone", "mobile", "mobile no", "mobile number",
        "contact", "contact number", "contact no", "cell", "calling no", "contact details"
    ],
    "Email": [
        "email.id", "email id", "email", "e-mail", "mail id", "mail",
        "email address", "e mail", "email_id"
    ],
    "Total Experience": [
        "total experience", "total exp", "experience", "exp", "total years of exp",
        "work exp", "relevant exp", "overall exp", "exp (years)", "exp in yrs"
    ],
    "Current CTC": [
        "current ctc", "currentctc", "cctc", "present ctc", "current salary",
        "fixed ctc", "current package", "c.ctc", "curr ctc", "present package"
    ],
    "Expected CTC": [
        "expected ctc", "expectedctc", "ectc", "exp ctc", "expected salary",
        "package expected", "e.ctc", "exp package", "expected compensation"
    ],
    "Notice Period": [
        "notice period", "notice", "np", "availability", "serving notice",
        "joining time", "lwd", "last working day", "notice (days)", "notice period (days)"
    ],
    "Status / Follow-up": [
        "candidate status (time/ date)", "candidate status", "status", "current status",
        "recruitment status", "follow up", "next follow up", "follow-up date",
        "next follow-up date", "stage", "hiring status", "sub status", "pipeline status"
    ],
    "Interview Feedback": [
        "interview feedback", "feedback", "client feedback", "internal feedback",
        "screening feedback", "evaluation", "interview remarks", "comments",
        "l1 feedback", "l2 feedback", "assessment", "technical feedback"
    ],
    "Remark": [
        "remark", "remarks", "notes", "recruiter remarks", "hr remarks",
        "comments", "client remark", "next step", "additional notes", "action item"
    ],
    "Google Calendar": [
        "google calender", "google calendar", "calendar", "meeting link",
        "meet link", "zoom link", "teams link", "interview link", "interview url"
    ],
    "Date Added": [
        "date added", "date", "added date", "sourcing date", "profile shared date",
        "created at", "timestamp", "entry date", "received date"
    ],

    # Open Positions Standard Fields
    "Position ID": [
        "position id", "pos id", "requisition id", "req id", "job id", "pos_id",
        "req_id", "vacancy id", "opening id"
    ],
    "Position Title": [
        "position title", "job title", "position", "role title", "designation",
        "opening title", "title"
    ],
    "Company Name": [
        "company name", "company", "client name", "client", "account",
        "customer", "organization", "client company"
    ],
    "Location": [
        "location", "city", "job location", "work location", "base location",
        "preferred location", "country"
    ],
    "JD Link": [
        "jd link", "jd", "job description", "jd url", "description link",
        "drive link", "jd document"
    ],
    "No. of Openings": [
        "no. of openings", "no of openings", "openings", "vacancies", "count",
        "open positions", "headcount", "vacancy count", "no of vacancy"
    ],
    "Budget": [
        "budget", "budget min", "budget max", "ctc range", "salary budget",
        "offered ctc", "budget (lpa)", "salary", "package"
    ],
    "Experience Required": [
        "experience required", "experience", "exp required", "required exp",
        "min experience", "exp range", "experience (years)"
    ],
    "Priority": [
        "priority", "urgency", "criticality", "importance"
    ],
    "Position Status": [
        "position status", "status", "job status", "req status", "opening status"
    ],
}


def _match_synonym(col_name: str, target_field: str) -> bool:
    """Checks if a column name matches any synonym for target_field."""
    c_clean = re.sub(r'[^a-zA-Z0-9]', ' ', str(col_name)).lower().strip()
    syns = SYNONYMS.get(target_field, [])
    for syn in syns:
        syn_clean = re.sub(r'[^a-zA-Z0-9]', ' ', syn).lower().strip()
        if c_clean == syn_clean:
            return True
        if len(syn_clean) >= 4 and syn_clean in c_clean:
            return True
    return False


def _find_header_row_smart(df_raw: pd.DataFrame) -> int:
    """
    Intelligently locates the real header row by scoring rows based on
    the number of recognized HR terminology keywords they contain.
    """
    if df_raw.empty:
        return 0

    best_row_idx = 0
    max_score = 0

    all_keywords = set()
    for syn_list in SYNONYMS.values():
        for syn in syn_list:
            all_keywords.add(syn.lower())

    scan_limit = min(25, len(df_raw))
    for idx in range(scan_limit):
        row = df_raw.iloc[idx]
        score = 0
        non_empty = 0
        for val in row.values:
            if pd.notna(val):
                val_str = str(val).strip().lower()
                if val_str and val_str != "nan":
                    non_empty += 1
                    for kw in all_keywords:
                        if kw in val_str or val_str in kw:
                            score += 2
                            break
        if non_empty >= 2 and score > max_score:
            max_score = score
            best_row_idx = idx

    return best_row_idx


def _clean_column_names(columns) -> list:
    """Clean and deduplicate column names."""
    cleaned = []
    seen = {}
    for col in columns:
        col_str = str(col).strip() if pd.notna(col) else "Unnamed"
        col_str = re.sub(r'\s+', ' ', col_str)
        if col_str in ["", "nan", "None"]:
            col_str = "Unnamed"
        if col_str in seen:
            seen[col_str] += 1
            col_str = f"{col_str}_{seen[col_str]}"
        else:
            seen[col_str] = 0
        cleaned.append(col_str)
    return cleaned


def _row_contains_any(row: pd.Series, keywords: list) -> bool:
    """Checks if any cell in row contains any of the specified keywords."""
    for val in row.values:
        if pd.notna(val):
            val_lower = str(val).lower()
            for kw in keywords:
                if kw.lower() in val_lower:
                    return True
    return False


def detect_sheet_type(df_raw: pd.DataFrame, sheet_name: str = "") -> str:
    """
    Automatically detects whether a raw sheet is:
    - 'positions' (Job Openings / Requisitions Tracker)
    - 'candidates' (Candidate Tracker: Active / Pipeline / Sourced)
    """
    s_name_lower = str(sheet_name).lower()

    if df_raw.empty:
        return "candidates"

    hdr_idx = _find_header_row_smart(df_raw)
    hdr_vals = " ".join([str(v).lower() for v in df_raw.iloc[hdr_idx].values if pd.notna(v)])

    # Score positions
    pos_score = 0
    if "position id" in hdr_vals or "pos id" in hdr_vals or "job id" in hdr_vals or "req id" in hdr_vals:
        pos_score += 6
    if "opening" in hdr_vals or "vacanc" in hdr_vals:
        pos_score += 4
    if "jd" in hdr_vals or "budget" in hdr_vals:
        pos_score += 3
    if any(k in s_name_lower for k in ["position", "job", "opening", "requisition", "req"]):
        pos_score += 4

    # Score candidates
    cand_score = 0
    if "candidate name" in hdr_vals or "applicant name" in hdr_vals or "candidate" in hdr_vals or "applicant" in hdr_vals:
        cand_score += 6
    if "ctc" in hdr_vals or "salary" in hdr_vals:
        cand_score += 4
    if "notice" in hdr_vals:
        cand_score += 4
    if "phone" in hdr_vals or "mobile" in hdr_vals or "email" in hdr_vals:
        cand_score += 4
    if any(k in s_name_lower for k in ["candidate", "pipeline", "active", "screening", "applicant"]):
        cand_score += 4

    if pos_score > cand_score and "candidate" not in hdr_vals:
        return "positions"
    else:
        return "candidates"


def map_and_clean_candidate_sheet(df_raw: pd.DataFrame, source_file: str = "", source_tab: str = "") -> pd.DataFrame:
    """
    Parses any candidate sheet with arbitrary headers:
    1. Finds header row dynamically.
    2. Drops sub-tables (e.g. 'Task Tracker', 'Reminder Interview') and instruction notes.
    3. Maps recognized columns to standard names while preserving ALL original custom columns.
    4. Automatically classifies each candidate into the 4 ATS stages.
    """
    if df_raw.empty:
        return pd.DataFrame()

    hdr_idx = _find_header_row_smart(df_raw)
    raw_headers = df_raw.iloc[hdr_idx].values
    clean_cols = _clean_column_names(raw_headers)

    df_data = df_raw.iloc[hdr_idx + 1:].copy()
    df_data.columns = clean_cols

    # Stop reading if a secondary sub-table appears
    stop_idx = None
    for idx, row in df_data.iterrows():
        if _row_contains_any(row, ["task tracker", "reminder interview", "task id", "pending tasks"]):
            stop_idx = idx
            break

    if stop_idx is not None:
        df_data = df_data.loc[:stop_idx].iloc[:-1]

    # Filter out banner/instruction rows
    instr_mask = df_data.apply(
        lambda r: _row_contains_any(r, ["How to Use", "Each company", "Add one", "PAMOHI RECRUITMENT", "CONFIDENTIAL -"]),
        axis=1
    )
    df_data = df_data[~instr_mask]

    # Drop repeated header rows
    if len(df_data.columns) > 0:
        first_col = df_data.columns[0]
        df_data = df_data[df_data[first_col].astype(str).str.lower() != str(first_col).lower()]

    # Synonym mapping
    col_mapping = {}
    used_targets = set()

    for col in df_data.columns:
        for target in ["Candidate Name", "Position", "Phone Number", "Email", "Total Experience",
                       "Current CTC", "Expected CTC", "Notice Period", "Status / Follow-up",
                       "Interview Feedback", "Remark", "Google Calendar", "Date Added"]:
            if target not in used_targets and _match_synonym(col, target):
                col_mapping[col] = target
                used_targets.add(target)
                break

    # If Candidate Name was not matched, find best text column
    if "Candidate Name" not in used_targets:
        for col in df_data.columns:
            if "name" in col.lower():
                col_mapping[col] = "Candidate Name"
                used_targets.add("Candidate Name")
                break

    # Rename recognized columns while keeping all extra custom columns intact
    df_data = df_data.rename(columns=col_mapping)

    # Ensure Candidate Name column exists
    if "Candidate Name" not in df_data.columns:
        if len(df_data.columns) > 0:
            df_data = df_data.rename(columns={df_data.columns[0]: "Candidate Name"})
        else:
            return pd.DataFrame()

    # Ensure required standard fields exist for consistent display
    for std_field in ["Position", "Phone Number", "Email", "Total Experience",
                      "Current CTC", "Expected CTC", "Notice Period", "Status / Follow-up",
                      "Interview Feedback", "Remark", "Google Calendar", "Date Added"]:
        if std_field not in df_data.columns:
            df_data[std_field] = ""

    # Legacy & synonym aliases for compatibility
    if "Candidate status (Time/ Date)" not in df_data.columns:
        df_data["Candidate status (Time/ Date)"] = df_data["Status / Follow-up"]
    if "Next Follow-up Date" not in df_data.columns:
        df_data["Next Follow-up Date"] = df_data["Status / Follow-up"]
    if "Follow-up Time" not in df_data.columns:
        df_data["Follow-up Time"] = ""

    # Drop rows where Candidate Name is empty or filler
    name_mask = df_data["Candidate Name"].notna() & \
                (df_data["Candidate Name"].astype(str).str.strip() != "") & \
                (df_data["Candidate Name"].astype(str).str.strip().str.lower() != "nan") & \
                (~df_data["Candidate Name"].astype(str).str.lower().str.contains("candidate name|444|total", na=False))
    df_data = df_data[name_mask].copy()

    # Metadata tags
    df_data["Source File"] = source_file or "Uploaded Sheet"
    df_data["Source Tab"] = source_tab or "Default"
    df_data["Source Tracker"] = f"{source_file} ({source_tab})" if source_tab else (source_file or "Uploaded Tracker")

    # Clean string values
    for col in df_data.columns:
        df_data[col] = df_data[col].apply(
            lambda x: str(x).strip() if pd.notna(x) and str(x).strip().lower() not in ["nan", "none"] else ""
        )

    # Auto-classify into 4 ATS stages
    df_data["Stage"] = df_data.apply(classify_candidate_stage, axis=1)

    return df_data.reset_index(drop=True)


def map_and_clean_position_sheet(df_raw: pd.DataFrame, source_file: str = "", source_tab: str = "") -> pd.DataFrame:
    """
    Parses any job requisitions/positions sheet with arbitrary headers.
    """
    if df_raw.empty:
        return pd.DataFrame()

    hdr_idx = _find_header_row_smart(df_raw)
    raw_headers = df_raw.iloc[hdr_idx].values
    clean_cols = _clean_column_names(raw_headers)

    df_data = df_raw.iloc[hdr_idx + 1:].copy()
    df_data.columns = clean_cols

    # Filter out banner and filler rows
    junk_mask = df_data.apply(
        lambda r: _row_contains_any(r, ["PAMOHI", "Enter each", "444", "How to Use", "Template"]),
        axis=1
    )
    df_data = df_data[~junk_mask]

    # Synonym mapping
    col_mapping = {}
    used_targets = set()
    for col in df_data.columns:
        for target in ["Position ID", "Position Title", "Company Name", "Location", "JD Link",
                       "No. of Openings", "Budget", "Experience Required", "Priority", "Position Status",
                       "Last Follow-up Date", "Next Follow-up Date", "Remarks", "Date Received"]:
            if target not in used_targets and _match_synonym(col, target):
                col_mapping[col] = target
                used_targets.add(target)
                break

    # Fallback for Position Title
    if "Position Title" not in used_targets:
        for col in df_data.columns:
            if any(k in col.lower() for k in ["title", "role", "position", "profile"]):
                col_mapping[col] = "Position Title"
                used_targets.add("Position Title")
                break

    df_data = df_data.rename(columns=col_mapping)

    # Ensure Position Title exists
    if "Position Title" not in df_data.columns:
        if len(df_data.columns) > 1:
            df_data = df_data.rename(columns={df_data.columns[1]: "Position Title"})
        elif len(df_data.columns) == 1:
            df_data = df_data.rename(columns={df_data.columns[0]: "Position Title"})
        else:
            return pd.DataFrame()

    # Standard fields default
    for std_field in ["Position ID", "Company Name", "Location", "JD Link", "No. of Openings",
                      "Budget", "Experience Required", "Priority", "Position Status", "Remarks", "Date Received"]:
        if std_field not in df_data.columns:
            df_data[std_field] = ""

    # Ensure Position Title is not null
    title_mask = df_data["Position Title"].notna() & \
                 (df_data["Position Title"].astype(str).str.strip() != "") & \
                 (df_data["Position Title"].astype(str).str.strip().str.lower() != "nan") & \
                 (~df_data["Position Title"].astype(str).str.lower().str.contains("position title|title|444", na=False))
    df_data = df_data[title_mask].copy()

    # If Company Name is blank, use tab name
    if source_tab and "Company Name" in df_data.columns:
        df_data["Company Name"] = df_data["Company Name"].apply(
            lambda v: source_tab if (pd.isna(v) or str(v).strip() in ["", "nan", "None"]) else str(v).strip()
        )

    # Clean strings
    for col in df_data.columns:
        df_data[col] = df_data[col].apply(
            lambda x: str(x).strip() if pd.notna(x) and str(x).strip().lower() not in ["nan", "none"] else ""
        )

    df_data["Position Status"] = df_data["Position Status"].apply(
        lambda s: "OPEN" if not s or s.lower() == "open" else s.upper()
    )
    df_data["Source File"] = source_file or "Uploaded Sheet"
    df_data["Source Tab"] = source_tab or "Default"

    return df_data.reset_index(drop=True)


def classify_candidate_stage(row: pd.Series) -> str:
    """
    Intelligently classifies candidate into one of 4 Kanban stages:
    1. 'New Applicants / Pipeline' (Blue #2563eb)
    2. 'Profile Shared / Screening' (Orange #ea580c)
    3. 'Interview Stage' (Red #dc2626)
    4. 'Selected / Offer' (Teal #0891b2)
    """
    # 0. If user explicitly provided a Stage column in their sheet, honor it first!
    raw_stage = str(row.get("Stage", "") or row.get("Current Stage", "") or "").strip().lower()
    if raw_stage and raw_stage != "nan":
        if any(k in raw_stage for k in ["offer", "selected", "hired", "joined", "shortlisted"]):
            return "Selected / Offer"
        elif any(k in raw_stage for k in ["interview", "f2f", "vc", "round"]):
            return "Interview Stage"
        elif any(k in raw_stage for k in ["screening", "shared", "review"]):
            return "Profile Shared / Screening"
        elif any(k in raw_stage for k in ["pipeline", "applicant", "new", "lead"]):
            return "New Applicants / Pipeline"

    text_pieces = []
    for col in ["Status / Follow-up", "Interview Feedback", "Remark", "Candidate status (Time/ Date)", "Remarks", "Notes", "Status"]:
        if col in row and pd.notna(row[col]):
            text_pieces.append(str(row[col]))

    combined_text = " ".join(text_pieces).lower()
    source_info = f"{row.get('Source Tracker', '')} {row.get('Source Tab', '')} {row.get('Source File', '')}".lower()

    # 1. Selected / Offer
    offer_kw = ["selected", "hired", "offer", "joined", "onboard", "offer released", "offer accepted", "shortlisted", "final select"]
    if any(k in combined_text for k in offer_kw):
        return "Selected / Offer"

    # 2. Interview Stage
    interview_kw = ["interview", "f2f", "vc", "round", "schedule", "screening ok", "l1", "l2", "technical", "client round", "manager round", "discussion scheduled"]
    if any(k in combined_text for k in interview_kw):
        return "Interview Stage"

    # 3. Profile Shared / Screening
    screening_kw = ["profile shared", "shared with client", "shared", "screening", "submitted", "in review", "under review", "sent to client"]
    if any(k in combined_text for k in screening_kw):
        return "Profile Shared / Screening"

    # 4. Pipeline / New Applicants
    if any(k in source_info for k in ["pipeline", "lead", "applicant", "sourced"]) or "follow" in combined_text:
        return "New Applicants / Pipeline"

    if row.get("Interview Feedback", ""):
        return "Profile Shared / Screening"

    return "New Applicants / Pipeline"


def parse_any_uploaded_file(file_obj, filename: str = None, force_type: str = None) -> list:
    """
    Parses any uploaded file (.xlsx, .xls, .csv).
    Returns a list of parsed sheet dicts:
    [
        {
            "filename": str,
            "sheet_name": str,
            "sheet_type": 'candidates' | 'positions',
            "df": pd.DataFrame,
            "row_count": int,
            "columns": list
        },
        ...
    ]
    """
    if file_obj is None:
        return []

    fname = filename or getattr(file_obj, "name", "uploaded_file")
    is_csv = fname.lower().endswith(".csv")

    results = []

    if is_csv:
        if hasattr(file_obj, "seek"):
            file_obj.seek(0)
        try:
            df_raw = pd.read_csv(file_obj, header=None, dtype=str)
        except Exception:
            if hasattr(file_obj, "seek"):
                file_obj.seek(0)
            df_raw = pd.read_csv(file_obj, header=None, encoding="latin1", dtype=str)

        if not df_raw.empty:
            sheet_type = force_type or detect_sheet_type(df_raw, fname)
            if sheet_type == "positions":
                cleaned_df = map_and_clean_position_sheet(df_raw, source_file=fname, source_tab="CSV")
            else:
                cleaned_df = map_and_clean_candidate_sheet(df_raw, source_file=fname, source_tab="CSV")

            if not cleaned_df.empty:
                results.append({
                    "filename": fname,
                    "sheet_name": "CSV",
                    "sheet_type": sheet_type,
                    "df": cleaned_df,
                    "row_count": len(cleaned_df),
                    "columns": list(cleaned_df.columns),
                })
        return results

    # Excel file
    if hasattr(file_obj, "seek"):
        file_obj.seek(0)
    try:
        xls = pd.ExcelFile(file_obj)
    except Exception:
        if hasattr(file_obj, "seek"):
            file_obj.seek(0)
        xls = pd.ExcelFile(file_obj, engine="openpyxl")

    for s_name in xls.sheet_names:
        s_low = s_name.strip().lower()
        if "how to use" in s_low or "template" in s_low or "readme" in s_low:
            continue

        df_raw = pd.read_excel(xls, sheet_name=s_name, header=None, dtype=str)
        if df_raw.empty:
            continue

        sheet_type = force_type or detect_sheet_type(df_raw, s_name)
        if sheet_type == "positions":
            cleaned_df = map_and_clean_position_sheet(df_raw, source_file=fname, source_tab=s_name)
        else:
            cleaned_df = map_and_clean_candidate_sheet(df_raw, source_file=fname, source_tab=s_name)

        if not cleaned_df.empty:
            results.append({
                "filename": fname,
                "sheet_name": s_name,
                "sheet_type": sheet_type,
                "df": cleaned_df,
                "row_count": len(cleaned_df),
                "columns": list(cleaned_df.columns),
            })

    return results


def consolidate_parsed_sheets(parsed_results: list) -> tuple:
    """
    Consolidates parsed sheet results into:
    (df_positions_combined, df_candidates_combined)
    Preserves all dynamic/custom columns across sheets!
    """
    pos_dfs = []
    cand_dfs = []

    for item in parsed_results:
        stype = item.get("sheet_type")
        df = item.get("df")
        if df is not None and not df.empty:
            if stype == "positions":
                pos_dfs.append(df)
            else:
                cand_dfs.append(df)

    # Combine positions
    if pos_dfs:
        df_positions = pd.concat(pos_dfs, ignore_index=True)
    else:
        df_positions = pd.DataFrame()

    # Combine candidates
    if cand_dfs:
        df_candidates = pd.concat(cand_dfs, ignore_index=True)
        if "Stage" not in df_candidates.columns:
            df_candidates["Stage"] = df_candidates.apply(classify_candidate_stage, axis=1)
    else:
        df_candidates = pd.DataFrame()

    return df_positions, df_candidates


# Backward compatibility wrappers
def parse_tracker_file(file_source, tracker_type: str = "") -> pd.DataFrame:
    force = "positions" if tracker_type == "open_positions" else ("candidates" if tracker_type in ["active_candidates", "pipeline_candidates"] else None)
    res = parse_any_uploaded_file(file_source, force_type=force)
    if not res:
        return pd.DataFrame()
    if force == "positions":
        pos_df, _ = consolidate_parsed_sheets(res)
        return pos_df
    else:
        _, cand_df = consolidate_parsed_sheets(res)
        return cand_df


def build_unified_candidate_pool(df_active: pd.DataFrame = None, df_pipeline: pd.DataFrame = None) -> pd.DataFrame:
    dfs = [d for d in [df_active, df_pipeline] if d is not None and not d.empty]
    if not dfs:
        return pd.DataFrame()
    unified = pd.concat(dfs, ignore_index=True)
    if "Stage" not in unified.columns:
        unified["Stage"] = unified.apply(classify_candidate_stage, axis=1)
    return unified
