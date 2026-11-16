"""
HR Recruitment & Applicant Tracking System (ATS)
Enterprise-grade Web Application built with Python, Streamlit, Pandas, and Plotly.
Supports arbitrary numbers of uploaded sheets with custom headers and zero default dummy data.
"""

import io
import html
import re
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

import data_parser
import sample_data

# ==============================================================================
# 1. PAGE CONFIGURATION & CUSTOM STYLING
# ==============================================================================
st.set_page_config(
    page_title="HR ATS | Recruitment & Applicant Tracking System",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
}

.block-container {
    padding-top: 1.2rem;
    padding-bottom: 2.5rem;
    padding-left: 2rem;
    padding-right: 2rem;
    max-width: 98% !important;
}

/* App Brand Header */
.brand-container {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.85rem 1.4rem;
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    border-radius: 14px;
    color: white;
    margin-bottom: 1.2rem;
    box-shadow: 0 4px 15px rgba(15, 23, 42, 0.15);
}
.brand-left {
    display: flex;
    align-items: center;
    gap: 12px;
}
.brand-logo-icon {
    background: linear-gradient(135deg, #3b82f6 0%, #6366f1 100%);
    color: white;
    font-weight: 800;
    font-size: 1.3rem;
    width: 44px;
    height: 44px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 10px;
    box-shadow: 0 4px 10px rgba(99, 102, 241, 0.35);
}
.brand-title {
    font-size: 1.35rem;
    font-weight: 800;
    letter-spacing: -0.5px;
    margin: 0;
    line-height: 1.2;
}
.brand-subtitle {
    font-size: 0.8rem;
    color: #94a3b8;
    font-weight: 500;
    margin: 0;
}
.brand-badge {
    background: rgba(59, 130, 246, 0.15);
    color: #60a5fa;
    border: 1px solid rgba(59, 130, 246, 0.3);
    padding: 4px 10px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
}

/* Zero State Cards */
.feature-card {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 1.2rem;
    height: 100%;
}
.feature-card h4 {
    margin: 0 0 6px 0;
    color: #0f172a;
    font-size: 0.95rem;
    font-weight: 700;
}
.feature-card p {
    margin: 0;
    color: #64748b;
    font-size: 0.82rem;
    line-height: 1.5;
}

/* Dynamic Job Header Banner */
.job-banner {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-left: 6px solid #3b82f6;
    border-radius: 12px;
    padding: 1.1rem 1.4rem;
    margin-bottom: 1.2rem;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}
.job-banner-title-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 10px;
    margin-bottom: 8px;
}
.job-banner-title {
    font-size: 1.3rem;
    font-weight: 700;
    color: #0f172a;
    margin: 0;
}
.status-badge {
    font-size: 0.75rem;
    font-weight: 700;
    padding: 4px 12px;
    border-radius: 20px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    display: inline-flex;
    align-items: center;
    gap: 5px;
}
.status-badge-open {
    background: #ecfdf5;
    color: #059669;
    border: 1px solid #a7f3d0;
}
.status-badge-progress {
    background: #eff6ff;
    color: #2563eb;
    border: 1px solid #bfdbfe;
}
.status-badge-closed {
    background: #fef2f2;
    color: #dc2626;
    border: 1px solid #fecaca;
}
.status-badge-default {
    background: #f1f5f9;
    color: #475569;
    border: 1px solid #cbd5e1;
}

/* Job Metadata Chips */
.metadata-chips-row {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    align-items: center;
}
.meta-chip {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-size: 0.82rem;
    color: #475569;
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    padding: 4px 10px;
    border-radius: 8px;
    font-weight: 500;
}
.meta-chip b {
    color: #0f172a;
}

/* Kanban Column Headers */
.kanban-col-header {
    padding: 10px 14px;
    border-radius: 10px 10px 0 0;
    font-weight: 700;
    font-size: 0.85rem;
    letter-spacing: 0.5px;
    color: #ffffff;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 12px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.08);
}
.kanban-count-pill {
    background: rgba(255, 255, 255, 0.25);
    color: white;
    padding: 2px 8px;
    border-radius: 12px;
    font-size: 0.75rem;
    font-weight: 800;
}

/* Candidate Kanban Cards */
.candidate-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 14px;
    margin-bottom: 14px;
    box-shadow: 0 3px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -2px rgba(0, 0, 0, 0.03);
    transition: transform 0.15s ease, box-shadow 0.15s ease, border-color 0.15s ease;
}
.candidate-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 16px -2px rgba(0, 0, 0, 0.08), 0 4px 6px -3px rgba(0, 0, 0, 0.04);
    border-color: #cbd5e1;
}
.candidate-header-row {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 8px;
    margin-bottom: 4px;
}
.candidate-name {
    font-weight: 700;
    font-size: 0.98rem;
    color: #0f172a;
    margin: 0;
    line-height: 1.3;
}
.source-tag {
    font-size: 0.65rem;
    font-weight: 700;
    text-transform: uppercase;
    padding: 2px 6px;
    border-radius: 6px;
    background: #f1f5f9;
    color: #475569;
    border: 1px solid #e2e8f0;
    white-space: nowrap;
}
.candidate-role {
    font-size: 0.8rem;
    font-weight: 600;
    color: #2563eb;
    margin-bottom: 8px;
    display: flex;
    align-items: center;
    gap: 4px;
}

.card-meta-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 6px;
    margin-bottom: 10px;
    background: #f8fafc;
    border: 1px solid #f1f5f9;
    padding: 8px;
    border-radius: 8px;
}
.meta-item {
    font-size: 0.75rem;
    color: #64748b;
    line-height: 1.3;
}
.meta-item b {
    color: #1e293b;
    display: block;
    font-weight: 600;
}

.card-status-box {
    font-size: 0.75rem;
    padding: 8px 10px;
    border-radius: 8px;
    line-height: 1.4;
    margin-top: 6px;
    border-left: 3px solid;
}
.status-box-blue {
    background: #eff6ff;
    border-left-color: #2563eb;
    color: #1e40af;
}
.status-box-orange {
    background: #fff7ed;
    border-left-color: #ea580c;
    color: #9a3412;
}
.status-box-red {
    background: #fef2f2;
    border-left-color: #dc2626;
    color: #991b1b;
}
.status-box-teal {
    background: #ecfeff;
    border-left-color: #0891b2;
    color: #155e75;
}

.card-contact-row {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: 8px;
    padding-top: 8px;
    border-top: 1px dashed #e2e8f0;
    font-size: 0.72rem;
    color: #64748b;
}
.card-contact-row a {
    color: #2563eb;
    text-decoration: none;
    font-weight: 500;
}

.kpi-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 1.1rem;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.03);
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}
.kpi-label {
    font-size: 0.78rem;
    font-weight: 600;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
.kpi-value {
    font-size: 1.8rem;
    font-weight: 800;
    color: #0f172a;
    margin: 4px 0;
}
.kpi-sub {
    font-size: 0.75rem;
    color: #94a3b8;
}

.empty-column {
    background: #f8fafc;
    border: 1.5px dashed #cbd5e1;
    border-radius: 10px;
    padding: 2.5rem 1rem;
    text-align: center;
    color: #94a3b8;
    font-size: 0.85rem;
    font-weight: 500;
}

[data-testid="stSidebar"] {
    background-color: #f8fafc;
    border-right: 1px solid #e2e8f0;
}
</style>
""", unsafe_allow_html=True)


# Custom helper to render HTML with zero leading indentation to prevent Markdown code block glitches
def render_clean_html(html_str: str):
    """Strips all leading and trailing indentation from HTML lines so Markdown never treats it as code."""
    compact = "".join([line.strip() for line in html_str.splitlines() if line.strip()])
    st.markdown(compact, unsafe_allow_html=True)


# ==============================================================================
# 2. STATE INITIALIZATION (ZERO DUMMY DATA BY DEFAULT)
# ==============================================================================
if "df_positions" not in st.session_state:
    st.session_state.df_positions = pd.DataFrame()
if "df_unified" not in st.session_state:
    st.session_state.df_unified = pd.DataFrame()
if "parsed_sheets_info" not in st.session_state:
    st.session_state.parsed_sheets_info = []
if "data_loaded" not in st.session_state:
    st.session_state.data_loaded = False
if "is_demo" not in st.session_state:
    st.session_state.is_demo = False


def reset_all_data():
    """Completely resets application state to empty."""
    st.session_state.df_positions = pd.DataFrame()
    st.session_state.df_unified = pd.DataFrame()
    st.session_state.parsed_sheets_info = []
    st.session_state.data_loaded = False
    st.session_state.is_demo = False


def process_uploaded_files(files_list):
    """Processes any uploaded list of files and updates application state."""
    if not files_list:
        return
    all_parsed_results = []
    for file_item in files_list:
        file_results = data_parser.parse_any_uploaded_file(file_item, file_item.name)
        all_parsed_results.extend(file_results)

    if all_parsed_results:
        pos_df, cand_df = data_parser.consolidate_parsed_sheets(all_parsed_results)
        st.session_state.df_positions = pos_df
        st.session_state.df_unified = cand_df
        st.session_state.parsed_sheets_info = [
            {
                "filename": item["filename"],
                "sheet_name": item["sheet_name"],
                "sheet_type": item["sheet_type"],
                "row_count": item["row_count"],
                "columns": item["columns"],
            }
            for item in all_parsed_results
        ]
        st.session_state.data_loaded = True
        st.session_state.is_demo = False


def load_demo_data():
    """Loads realistic sample datasets on explicit user request only."""
    pos = sample_data.get_sample_open_positions()
    act = sample_data.get_sample_active_candidates()
    pip = sample_data.get_sample_pipeline_candidates()
    cand = pd.concat([act, pip], ignore_index=True)
    if "Stage" not in cand.columns:
        cand["Stage"] = cand.apply(data_parser.classify_candidate_stage, axis=1)

    st.session_state.df_positions = pos
    st.session_state.df_unified = cand
    st.session_state.parsed_sheets_info = [
        {"filename": "Sample_Positions.xlsx", "sheet_name": "Open Positions", "sheet_type": "positions", "row_count": len(pos)},
        {"filename": "Sample_Active_Candidates.xlsx", "sheet_name": "Active Candidates", "sheet_type": "candidates", "row_count": len(act)},
        {"filename": "Sample_Pipeline.xlsx", "sheet_name": "Pipeline Tracker", "sheet_type": "candidates", "row_count": len(pip)},
    ]
    st.session_state.data_loaded = True
    st.session_state.is_demo = True


# ==============================================================================
# 3. SIDEBAR: MULTI-FILE UPLOADER & CONTROLS
# ==============================================================================
with st.sidebar:
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 12px;">
        <div style="background: #2563eb; color: white; font-weight: 800; font-size: 1.1rem; width: 36px; height: 36px; display: flex; align-items: center; justify-content: center; border-radius: 8px;">💼</div>
        <div>
            <h3 style="margin: 0; font-size: 1.1rem; font-weight: 800; color: #0f172a;">HR ATS Engine</h3>
            <span style="font-size: 0.72rem; color: #64748b; font-weight: 500;">Multi-Sheet Dynamic Tracker</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("#### 📂 Upload Spreadsheets")
    st.caption("Upload any number of files (`.xlsx`, `.xls`, `.csv`). Headers and sheets are detected dynamically.")

    sidebar_files = st.file_uploader(
        "Upload Spreadsheets",
        type=["xlsx", "xls", "csv"],
        accept_multiple_files=True,
        help="Upload 1 or more Excel/CSV sheets with any custom headers.",
        key="sidebar_uploader",
        label_visibility="collapsed"
    )

    if sidebar_files:
        process_uploaded_files(sidebar_files)

    if st.session_state.data_loaded:
        if st.session_state.is_demo:
            st.info("ℹ️ **Active Source**: Sample Test Datasets", icon="💼")
        else:
            st.success(f"✅ **Loaded**: {len(st.session_state.parsed_sheets_info)} Sheet(s)", icon="📁")

        if st.button("🧹 Clear All Data", use_container_width=True, help="Remove all uploaded data"):
            reset_all_data()
            st.rerun()

    if st.session_state.parsed_sheets_info:
        st.markdown("---")
        st.markdown("#### 📑 Detected Sheets")
        for info in st.session_state.parsed_sheets_info:
            icon = "💼" if info["sheet_type"] == "positions" else "👥"
            type_label = "Positions" if info["sheet_type"] == "positions" else "Candidates"
            st.markdown(f"""
            <div style="background: white; border: 1px solid #e2e8f0; border-radius: 8px; padding: 6px 10px; margin-bottom: 6px; font-size: 0.75rem;">
                <b>{icon} {html.escape(info['sheet_name'])}</b> <span style="color:#64748b;">({type_label})</span><br/>
                <span style="color: #2563eb; font-weight: 600;">{info['row_count']} records</span> &bull; <span style="color: #64748b;">{html.escape(info['filename'])}</span>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    with st.expander("🧪 Demo & Templates (Optional)"):
        st.caption("Preview the ATS with sample data if you do not have files ready:")
        if st.button("Load Sample Preview Data", use_container_width=True):
            load_demo_data()
            st.rerun()

        st.caption("Download formatted Excel templates:")
        pos_buf = sample_data.generate_sample_excel_with_dirty_rows("open_positions")
        st.download_button(
            "📄 Positions Template (.xlsx)",
            data=pos_buf,
            file_name="Positions_Template.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
        cand_buf = sample_data.generate_sample_excel_with_dirty_rows("active_candidates")
        st.download_button(
            "📄 Candidates Template (.xlsx)",
            data=cand_buf,
            file_name="Candidates_Template.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )


# ==============================================================================
# 4. TOP APP BANNER
# ==============================================================================
st.markdown("""
<div class="brand-container">
    <div class="brand-left">
        <div class="brand-logo-icon">💼</div>
        <div>
            <h1 class="brand-title">RECRUITMENT & APPLICANT TRACKING SYSTEM (ATS)</h1>
            <p class="brand-subtitle">Multi-Sheet Dynamic Engine & Candidate Pipeline Manager</p>
        </div>
    </div>
    <div style="display: flex; gap: 8px; align-items: center;">
        <span class="brand-badge">⚡ Live ATS Engine</span>
        <span class="brand-badge" style="background: rgba(16, 185, 129, 0.15); color: #34d399; border-color: rgba(16, 185, 129, 0.3);">● Dynamic Header Mapping</span>
    </div>
</div>
""", unsafe_allow_html=True)


# ==============================================================================
# 5. ZERO-STATE SCREEN (CLEAN, NO RAW HTML/CODE DISPLAYED)
# ==============================================================================
if not st.session_state.data_loaded or (st.session_state.df_positions.empty and st.session_state.df_unified.empty):
    st.markdown("<h2 style='text-align: center; color: #0f172a; margin-top: 1rem;'>Welcome to Recruitment & Applicant Tracking System</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #64748b; font-size: 1rem; max-width: 650px; margin: 0 auto 1.5rem auto;'>Upload your candidate trackers or job requisition spreadsheets to immediately launch your visual ATS Kanban board.</p>", unsafe_allow_html=True)

    # Center-Screen Direct File Upload Box
    center_files = st.file_uploader(
        "Upload your spreadsheets here (.xlsx, .xls, .csv)",
        type=["xlsx", "xls", "csv"],
        accept_multiple_files=True,
        key="center_uploader",
        help="Upload single or multiple spreadsheets with any headers."
    )
    if center_files:
        process_uploaded_files(center_files)
        st.rerun()

    st.markdown("---")

    # Native Feature Highlights Grid
    f_col1, f_col2, f_col3, f_col4 = st.columns(4)
    with f_col1:
        st.markdown("""
        <div class="feature-card">
            <h4>🔄 Multi-Sheet Upload</h4>
            <p>Upload 1, 2, 5, or more sheets at once. Multi-tab workbooks are automatically merged.</p>
        </div>
        """, unsafe_allow_html=True)
    with f_col2:
        st.markdown("""
        <div class="feature-card">
            <h4>🔍 Any Custom Headers</h4>
            <p>Smart fuzzy-matching recognizes variations like <i>Full Name</i>, <i>Tech Stack</i>, <i>CCTC</i>, <i>Package</i>, <i>Notice</i>, etc.</p>
        </div>
        """, unsafe_allow_html=True)
    with f_col3:
        st.markdown("""
        <div class="feature-card">
            <h4>🧹 Auto-Sanitization</h4>
            <p>Banners, blank lines, instructions, and secondary sub-tables (like Task Trackers) are stripped out automatically.</p>
        </div>
        """, unsafe_allow_html=True)
    with f_col4:
        st.markdown("""
        <div class="feature-card">
            <h4>📌 Dynamic Kanban Board</h4>
            <p>Candidates are auto-classified into 4 color-coded stages with custom columns preserved.</p>
        </div>
        """, unsafe_allow_html=True)

    st.stop()


# ==============================================================================
# 6. ACTIVE DATASET VARIABLES
# ==============================================================================
df_positions = st.session_state.df_positions
df_unified = st.session_state.df_unified

pos_options = ["All Open Positions"]
known_positions = set()

if not df_positions.empty and "Position Title" in df_positions.columns:
    for p in df_positions["Position Title"].dropna().unique():
        p_str = str(p).strip()
        if p_str and p_str.lower() != "nan":
            known_positions.add(p_str)

if not df_unified.empty and "Position" in df_unified.columns:
    for p in df_unified["Position"].dropna().unique():
        p_str = str(p).strip()
        if p_str and p_str.lower() != "nan":
            known_positions.add(p_str)

pos_options.extend(sorted(list(known_positions)))


# ==============================================================================
# 7. TOP CONTROL BAR (JOB POSITION DROPDOWN + QUICK SEARCH)
# ==============================================================================
ctrl_col1, ctrl_col2 = st.columns([1.8, 1.2])

with ctrl_col1:
    selected_position = st.selectbox(
        "🎯 Select Job Position",
        options=pos_options,
        index=0,
        help="Filter the entire Kanban ATS board and analytics by specific job role."
    )

with ctrl_col2:
    search_query = st.text_input(
        "🔍 Quick Search Candidates",
        placeholder="Search name, phone, email, status, keywords, skills...",
        help="Instant multi-field search across all standard and custom columns"
    )


# ==============================================================================
# 8. DYNAMIC JOB HEADER BANNER
# ==============================================================================
if selected_position == "All Open Positions":
    total_cand = len(df_unified)
    total_roles = len(df_positions) if not df_positions.empty else len(known_positions)
    openings_sum = 0
    if not df_positions.empty and "No. of Openings" in df_positions.columns:
        for val in df_positions["No. of Openings"]:
            try:
                openings_sum += int(float(str(val).strip()))
            except Exception:
                pass
    if openings_sum == 0 and total_roles > 0:
        openings_sum = total_roles

    client_count = df_positions["Company Name"].nunique() if not df_positions.empty and "Company Name" in df_positions.columns else 1

    render_clean_html(f"""
    <div class="job-banner">
        <div class="job-banner-title-row">
            <div>
                <h3 class="job-banner-title">🌐 Master Recruitment Pipeline (All Roles)</h3>
            </div>
            <div>
                <span class="status-badge status-badge-open">● FULL PORTFOLIO ACTIVE</span>
            </div>
        </div>
        <div class="metadata-chips-row">
            <span class="meta-chip">🏢 Client Accounts: <b>{client_count} Portfolio(s)</b></span>
            <span class="meta-chip">💼 Active Positions: <b>{total_roles} Roles</b></span>
            <span class="meta-chip">🎯 Total Openings: <b>{openings_sum} Vacancies</b></span>
            <span class="meta-chip">👥 Total Candidate Pool: <b>{total_cand} Candidates</b></span>
            <span class="meta-chip">📄 Uploaded Sheets: <b>{len(st.session_state.parsed_sheets_info)} Sheet(s)</b></span>
        </div>
    </div>
    """)
else:
    pos_meta = None
    if not df_positions.empty and "Position Title" in df_positions.columns:
        matches = df_positions[df_positions["Position Title"].str.lower() == selected_position.lower()]
        if not matches.empty:
            pos_meta = matches.iloc[0]

    company_name = pos_meta.get("Company Name", "Client Mandate") if pos_meta is not None else "Client Mandate"
    location = pos_meta.get("Location", "Flexible / Hybrid") if pos_meta is not None else "Flexible"
    budget = pos_meta.get("Budget", "Competitive / Market Standard") if pos_meta is not None else "Not specified"
    exp_req = pos_meta.get("Experience Required", "Relevant experience") if pos_meta is not None else "Not specified"
    openings = pos_meta.get("No. of Openings", "1") if pos_meta is not None else "1"
    status_val = str(pos_meta.get("Position Status", "OPEN") if pos_meta is not None else "OPEN").upper()
    priority = pos_meta.get("Priority", "Standard") if pos_meta is not None else "Standard"
    jd_link = pos_meta.get("JD Link", "") if pos_meta is not None else ""

    if "OPEN" in status_val:
        badge_cls = "status-badge-open"
    elif "PROGRESS" in status_val or "ACTIVE" in status_val:
        badge_cls = "status-badge-progress"
    elif "CLOSE" in status_val:
        badge_cls = "status-badge-closed"
    else:
        badge_cls = "status-badge-default"

    jd_html = f'<a href="{jd_link}" target="_blank" style="color:#2563eb; text-decoration:underline;">View JD ↗</a>' if jd_link and str(jd_link).startswith("http") else ""

    render_clean_html(f"""
    <div class="job-banner">
        <div class="job-banner-title-row">
            <div>
                <h3 class="job-banner-title">💼 {html.escape(selected_position)}</h3>
            </div>
            <div>
                <span class="status-badge {badge_cls}">● {html.escape(status_val)}</span>
            </div>
        </div>
        <div class="metadata-chips-row">
            <span class="meta-chip">🏢 Company: <b>{html.escape(str(company_name))}</b></span>
            <span class="meta-chip">📍 Location: <b>{html.escape(str(location))}</b></span>
            <span class="meta-chip">💰 Budget: <b>{html.escape(str(budget))}</b></span>
            <span class="meta-chip">⏳ Experience: <b>{html.escape(str(exp_req))}</b></span>
            <span class="meta-chip">🎯 Openings: <b>{html.escape(str(openings))}</b></span>
            <span class="meta-chip">⚡ Priority: <b>{html.escape(str(priority))}</b></span>
            {f'<span class="meta-chip">📄 {jd_html}</span>' if jd_html else ''}
        </div>
    </div>
    """)


# ==============================================================================
# 9. FILTER CANDIDATES FOR KANBAN
# ==============================================================================
filtered_df = df_unified.copy()

if selected_position != "All Open Positions" and not filtered_df.empty and "Position" in filtered_df.columns:
    filtered_df = filtered_df[filtered_df["Position"].str.lower() == selected_position.lower()]

if search_query.strip() and not filtered_df.empty:
    q = search_query.strip().lower()

    def row_matches(r):
        for val in r.values:
            if pd.notna(val) and q in str(val).lower():
                return True
        return False

    filtered_df = filtered_df[filtered_df.apply(row_matches, axis=1)]


# ==============================================================================
# 10. NAVIGATION TABS
# ==============================================================================
tab_kanban, tab_kpis, tab_charts, tab_master = st.tabs([
    "📋 Kanban Candidate Board",
    "🏢 Open Positions & KPIs",
    "📈 Charts & Custom Analytics",
    "📑 Master Candidate Search & Export",
])


# ==============================================================================
# TAB 1: KANBAN CANDIDATE BOARD
# ==============================================================================
with tab_kanban:
    stages_config = [
        {
            "id": "New Applicants / Pipeline",
            "title": "NEW APPLICANTS / PIPELINE",
            "color": "#2563eb",
            "bg_box": "status-box-blue",
            "icon": "📥",
        },
        {
            "id": "Profile Shared / Screening",
            "title": "PROFILE SHARED / SCREENING",
            "color": "#ea580c",
            "bg_box": "status-box-orange",
            "icon": "📤",
        },
        {
            "id": "Interview Stage",
            "title": "INTERVIEW STAGE",
            "color": "#dc2626",
            "bg_box": "status-box-red",
            "icon": "🎯",
        },
        {
            "id": "Selected / Offer",
            "title": "SELECTED / OFFER",
            "color": "#0891b2",
            "bg_box": "status-box-teal",
            "icon": "🏆",
        },
    ]

    kanban_cols = st.columns(4)

    for i, stage in enumerate(stages_config):
        with kanban_cols[i]:
            if not filtered_df.empty and "Stage" in filtered_df.columns:
                stage_cands = filtered_df[filtered_df["Stage"] == stage["id"]]
            else:
                stage_cands = pd.DataFrame()

            stage_count = len(stage_cands)

            render_clean_html(f"""
            <div class="kanban-col-header" style="background-color: {stage['color']};">
                <span>{stage['icon']} {stage['title']}</span>
                <span class="kanban-count-pill">{stage_count}</span>
            </div>
            """)

            if stage_count == 0:
                render_clean_html("""
                <div class="empty-column">
                    <p style="margin: 0; font-size: 1.1rem; opacity: 0.6;">📭</p>
                    <p style="margin: 4px 0 0 0;">No candidates in this stage</p>
                </div>
                """)
            else:
                all_stage_names = [s["id"] for s in stages_config]
                for orig_idx, cand in stage_cands.iterrows():
                    cand_name = cand.get("Candidate Name", "Unknown Candidate")
                    cand_role = cand.get("Position", "Role Unspecified")
                    cand_exp = cand.get("Total Experience", "N/A")
                    c_ctc = cand.get("Current CTC", "N/A")
                    e_ctc = cand.get("Expected CTC", "N/A")
                    notice = cand.get("Notice Period", "N/A")
                    date_added = cand.get("Date Added", "")
                    source_tracker = cand.get("Source Tab", "") or cand.get("Source File", "Sheet")
                    phone = cand.get("Phone Number", "")
                    email = cand.get("Email", "")
                    calendar_url = cand.get("Google Calendar", "")

                    status_text = cand.get("Status / Follow-up", "")
                    feedback_text = cand.get("Interview Feedback", "")
                    remark_text = cand.get("Remark", "")

                    highlight_msg = []
                    if status_text:
                        highlight_msg.append(f"<b>Status:</b> {html.escape(str(status_text))}")
                    if feedback_text:
                        highlight_msg.append(f"<b>Feedback:</b> {html.escape(str(feedback_text))}")
                    if remark_text:
                        highlight_msg.append(f"<b>Note:</b> {html.escape(str(remark_text))}")

                    combined_highlight = "<br/>".join(highlight_msg) if highlight_msg else "Profile in progress"

                    contact_items = []
                    if phone:
                        contact_items.append(f"📞 <span>{html.escape(str(phone))}</span>")
                    if email:
                        contact_items.append(f"✉️ <a href='mailto:{html.escape(str(email))}'>{html.escape(str(email))}</a>")
                    if calendar_url and str(calendar_url).startswith("http"):
                        contact_items.append(f"📅 <a href='{html.escape(str(calendar_url))}' target='_blank'>Meet Link ↗</a>")

                    contact_html = f"<div class='card-contact-row'>{' &bull; '.join(contact_items)}</div>" if contact_items else ""
                    added_html = f"<div style='font-size: 0.68rem; color: #94a3b8; margin-top: 6px; text-align: right;'>Added: {html.escape(str(date_added))}</div>" if date_added else ""

                    card_markup = (
                        f'<div class="candidate-card" style="margin-bottom: 6px;">'
                        f'<div class="candidate-header-row">'
                        f'<h4 class="candidate-name">{html.escape(str(cand_name))}</h4>'
                        f'<span class="source-tag">{html.escape(str(source_tracker))}</span>'
                        f'</div>'
                        f'<div class="candidate-role"><span>💼</span> {html.escape(str(cand_role))}</div>'
                        f'<div class="card-meta-grid">'
                        f'<div class="meta-item"><b>Experience</b> {html.escape(str(cand_exp))}</div>'
                        f'<div class="meta-item"><b>Notice Period</b> {html.escape(str(notice))}</div>'
                        f'<div class="meta-item"><b>Current CTC</b> {html.escape(str(c_ctc))}</div>'
                        f'<div class="meta-item"><b>Expected CTC</b> {html.escape(str(e_ctc))}</div>'
                        f'</div>'
                        f'<div class="card-status-box {stage["bg_box"]}">{combined_highlight}</div>'
                        f'{contact_html}'
                        f'{added_html}'
                        f'</div>'
                    )
                    render_clean_html(card_markup)

                    # Interactive Stage Changer dropdown directly on each card!
                    cur_idx = all_stage_names.index(stage["id"]) if stage["id"] in all_stage_names else 0
                    c_sel1, c_sel2 = st.columns([1, 1.8])
                    with c_sel1:
                        st.caption("Change Stage:")
                    with c_sel2:
                        new_stage = st.selectbox(
                            "Move candidate",
                            options=all_stage_names,
                            index=cur_idx,
                            key=f"card_stage_select_{orig_idx}_{stage['id']}",
                            label_visibility="collapsed"
                        )
                        if new_stage != stage["id"]:
                            st.session_state.df_unified.at[orig_idx, "Stage"] = new_stage
                            st.rerun()

                    st.markdown("<div style='margin-bottom: 12px;'></div>", unsafe_allow_html=True)


# ==============================================================================
# TAB 2: OPEN POSITIONS & KPIS
# ==============================================================================
with tab_kpis:
    st.markdown("### 🏢 Open Positions & Recruitment KPI Dashboard")

    total_positions_count = len(df_positions) if not df_positions.empty else len(known_positions)
    active_roles_count = total_positions_count
    closed_roles_count = 0
    total_vacancies = 0

    if not df_positions.empty and "Position Status" in df_positions.columns:
        closed_roles_count = len(df_positions[df_positions["Position Status"].astype(str).str.upper().str.contains("CLOSE")])
        active_roles_count = total_positions_count - closed_roles_count

    if not df_positions.empty and "No. of Openings" in df_positions.columns:
        for v in df_positions["No. of Openings"]:
            try:
                total_vacancies += int(float(str(v).strip()))
            except Exception:
                pass
    if total_vacancies == 0:
        total_vacancies = total_positions_count

    total_pipeline_pool = len(df_unified)

    k1, k2, k3, k4, k5 = st.columns(5)
    with k1:
        st.markdown(f"""
        <div class="kpi-card" style="border-top: 4px solid #2563eb;">
            <span class="kpi-label">Total Openings</span>
            <div class="kpi-value">{total_vacancies}</div>
            <span class="kpi-sub">Across active mandates</span>
        </div>
        """, unsafe_allow_html=True)
    with k2:
        st.markdown(f"""
        <div class="kpi-card" style="border-top: 4px solid #10b981;">
            <span class="kpi-label">Active Roles</span>
            <div class="kpi-value">{active_roles_count}</div>
            <span class="kpi-sub">Open & in progress</span>
        </div>
        """, unsafe_allow_html=True)
    with k3:
        st.markdown(f"""
        <div class="kpi-card" style="border-top: 4px solid #f59e0b;">
            <span class="kpi-label">Closed / Filled</span>
            <div class="kpi-value">{closed_roles_count}</div>
            <span class="kpi-sub">Successfully closed</span>
        </div>
        """, unsafe_allow_html=True)
    with k4:
        st.markdown(f"""
        <div class="kpi-card" style="border-top: 4px solid #6366f1;">
            <span class="kpi-label">Total Candidates</span>
            <div class="kpi-value">{total_pipeline_pool}</div>
            <span class="kpi-sub">Across all uploaded sheets</span>
        </div>
        """, unsafe_allow_html=True)
    with k5:
        avg_depth = round(total_pipeline_pool / max(total_positions_count, 1), 1)
        st.markdown(f"""
        <div class="kpi-card" style="border-top: 4px solid #0891b2;">
            <span class="kpi-label">Candidate Depth</span>
            <div class="kpi-value">{avg_depth}</div>
            <span class="kpi-sub">Avg candidates per role</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### 📋 Open Position Master Tracker")

    if df_positions.empty:
        st.info("No dedicated position requisition sheet was detected. If you upload a file containing 'Position ID' or 'Openings', it will appear here automatically.")
    else:
        f_col1, f_col2, f_col3 = st.columns(3)
        with f_col1:
            comps = ["All Companies"] + sorted([c for c in df_positions["Company Name"].unique() if c])
            selected_comp = st.selectbox("Filter by Company", comps, index=0)
        with f_col2:
            prios = ["All Priorities"] + sorted([p for p in df_positions["Priority"].unique() if p])
            selected_prio = st.selectbox("Filter by Priority", prios, index=0)
        with f_col3:
            stats = ["All Statuses"] + sorted([s for s in df_positions["Position Status"].unique() if s])
            selected_stat = st.selectbox("Filter by Status", stats, index=0)

        disp_pos = df_positions.copy()
        if selected_comp != "All Companies":
            disp_pos = disp_pos[disp_pos["Company Name"] == selected_comp]
        if selected_prio != "All Priorities":
            disp_pos = disp_pos[disp_pos["Priority"] == selected_prio]
        if selected_stat != "All Statuses":
            disp_pos = disp_pos[disp_pos["Position Status"] == selected_stat]

        st.dataframe(
            disp_pos,
            use_container_width=True,
            hide_index=True,
            column_config={
                "JD Link": st.column_config.LinkColumn("JD Link", display_text="Open JD ↗"),
            }
        )


# ==============================================================================
# TAB 3: CHARTS & CUSTOM ANALYTICS (DYNAMIC BUILDER)
# ==============================================================================
with tab_charts:
    st.markdown("### 📈 ATS Pipeline Analytics & Dynamic Visualizer")

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.markdown("##### 🎯 Pipeline Stage Distribution")
        if not df_unified.empty and "Stage" in df_unified.columns:
            stg_counts = df_unified["Stage"].value_counts().reset_index()
            stg_counts.columns = ["Stage", "Count"]

            c_map = {
                "New Applicants / Pipeline": "#2563eb",
                "Profile Shared / Screening": "#ea580c",
                "Interview Stage": "#dc2626",
                "Selected / Offer": "#0891b2",
            }
            colors = [c_map.get(s, "#94a3b8") for s in stg_counts["Stage"]]

            fig_donut = go.Figure(data=[go.Pie(
                labels=stg_counts["Stage"],
                values=stg_counts["Count"],
                hole=0.55,
                marker=dict(colors=colors),
                textinfo="label+value",
                hoverinfo="label+value+percent",
            )])
            fig_donut.update_layout(
                margin=dict(t=20, b=20, l=10, r=10),
                height=300,
                showlegend=False,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)"
            )
            st.plotly_chart(fig_donut, use_container_width=True)
        else:
            st.info("No candidates available to chart.")

    with chart_col2:
        st.markdown("##### 💼 Candidates by Job Role")
        if not df_unified.empty and "Position" in df_unified.columns:
            r_counts = df_unified["Position"].value_counts().head(8).reset_index()
            r_counts.columns = ["Position", "Candidates"]

            fig_bar = px.bar(
                r_counts,
                x="Candidates",
                y="Position",
                orientation="h",
                text="Candidates",
                color="Candidates",
                color_continuous_scale="Blues",
            )
            fig_bar.update_layout(
                margin=dict(t=20, b=20, l=10, r=10),
                height=300,
                coloraxis_showscale=False,
                yaxis=dict(autorange="reversed"),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
            )
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.info("No role data available to chart.")

    # ==========================================================================
    # DYNAMIC COLUMN CHART BUILDER (DETECTS ANY NEW OR CUSTOM COLUMNS)
    # ==========================================================================
    st.markdown("---")
    st.markdown("#### 🛠️ Dynamic Column Chart Builder")
    st.caption("Automatically scans all columns in your uploaded sheets (including all custom columns) and lets you build custom Plotly charts instantly.")

    dataset_options = ["Candidates Pool (All Sheets)"]
    if not df_positions.empty:
        dataset_options.append("Open Positions")

    chosen_ds = st.selectbox("1. Select Dataset", options=dataset_options)
    target_data = df_unified if chosen_ds == "Candidates Pool (All Sheets)" else df_positions

    if target_data.empty:
        st.warning("Selected dataset is currently empty.")
    else:
        all_cols = list(target_data.columns)
        dc1, dc2, dc3, dc4 = st.columns(4)
        with dc1:
            x_col = st.selectbox("X-Axis Column", options=all_cols, index=0)
        with dc2:
            y_col = st.selectbox("Y-Axis / Metric", options=["(Count of Records)"] + all_cols, index=0)
        with dc3:
            c_type = st.selectbox("Chart Type", ["Bar Chart", "Line Chart", "Pie / Donut", "Scatter Plot", "Histogram", "Box Plot"])
        with dc4:
            grp_col = st.selectbox("Color / Group By", ["None"] + all_cols, index=0)

        try:
            plot_df = target_data.copy().replace("", np.nan).dropna(subset=[x_col])
            color_arg = grp_col if grp_col != "None" else None

            if y_col == "(Count of Records)":
                if c_type in ["Bar Chart", "Histogram"]:
                    fig_d = px.histogram(plot_df, x=x_col, color=color_arg, barmode="group", title=f"Count of Records by {x_col}", color_discrete_sequence=px.colors.qualitative.Bold)
                elif c_type == "Pie / Donut":
                    cnts = plot_df[x_col].value_counts().reset_index()
                    cnts.columns = [x_col, "Count"]
                    fig_d = px.pie(cnts, names=x_col, values="Count", hole=0.45, title=f"Distribution of {x_col}", color_discrete_sequence=px.colors.qualitative.Bold)
                elif c_type == "Line Chart":
                    cnts = plot_df.groupby(x_col).size().reset_index(name="Count")
                    fig_d = px.line(cnts, x=x_col, y="Count", markers=True, title=f"Count Trend across {x_col}")
                else:
                    fig_d = px.histogram(plot_df, x=x_col, color=color_arg, title=f"Distribution of {x_col}")
            else:
                plot_df["_numeric_y"] = pd.to_numeric(plot_df[y_col].astype(str).str.replace(r"[^\d.]", "", regex=True), errors="coerce")
                y_val = "_numeric_y" if plot_df["_numeric_y"].notna().sum() > 0 else y_col

                if c_type == "Bar Chart":
                    fig_d = px.bar(plot_df, x=x_col, y=y_val, color=color_arg, title=f"{y_col} by {x_col}")
                elif c_type == "Line Chart":
                    fig_d = px.line(plot_df, x=x_col, y=y_val, color=color_arg, markers=True, title=f"{y_col} vs {x_col}")
                elif c_type == "Scatter Plot":
                    fig_d = px.scatter(plot_df, x=x_col, y=y_val, color=color_arg, title=f"Scatter: {y_col} vs {x_col}")
                elif c_type == "Box Plot":
                    fig_d = px.box(plot_df, x=x_col, y=y_val, color=color_arg, title=f"Box Plot: {y_col} across {x_col}")
                else:
                    fig_d = px.bar(plot_df, x=x_col, y=y_val, color=color_arg, title=f"{y_col} by {x_col}")

            if fig_d:
                fig_d.update_layout(margin=dict(t=40, b=20, l=10, r=10), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
                st.plotly_chart(fig_d, use_container_width=True)
        except Exception as e:
            st.warning(f"Could not automatically plot chart with selected columns: {e}")


# ==============================================================================
# TAB 4: MASTER CANDIDATE SEARCH & EXPORT
# ==============================================================================
with tab_master:
    st.markdown("### 📑 Master Candidate Database (All Uploaded Sheets)")
    st.caption("Consolidated talent pool from all uploaded spreadsheets with custom columns preserved, multi-field search, and instant CSV export.")

    if df_unified.empty:
        st.info("No candidates available in master pool. Upload spreadsheets in the sidebar to populate.")
    else:
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            stg_f = st.selectbox("Filter by Stage", ["All Stages"] + sorted(list(df_unified["Stage"].unique())), index=0)
        with m2:
            role_f = st.selectbox("Filter by Position", ["All Roles"] + sorted([r for r in df_unified["Position"].unique() if r]), index=0)
        with m3:
            src_f = st.selectbox("Filter by Source Sheet", ["All Sources"] + sorted(list(df_unified["Source Tracker"].unique())), index=0)
        with m4:
            m_q = st.text_input("Search In Master Table", placeholder="Type anything to filter...")

        m_filtered = df_unified.copy()
        if stg_f != "All Stages":
            m_filtered = m_filtered[m_filtered["Stage"] == stg_f]
        if role_f != "All Roles":
            m_filtered = m_filtered[m_filtered["Position"] == role_f]
        if src_f != "All Sources":
            m_filtered = m_filtered[m_filtered["Source Tracker"] == src_f]
        if m_q.strip():
            mq_low = m_q.strip().lower()
            m_filtered = m_filtered[m_filtered.apply(
                lambda r: any(pd.notna(v) and mq_low in str(v).lower() for v in r.values), axis=1
            )]

        dl1, dl2 = st.columns([2, 1])
        with dl1:
            st.markdown(f"**Showing {len(m_filtered)} of {len(df_unified)} candidates**")
        with dl2:
            csv_bytes = m_filtered.to_csv(index=False).encode("utf-8")
            st.download_button(
                "📥 Download Filtered Candidates (CSV)",
                data=csv_bytes,
                file_name="Candidate_Export.csv",
                mime="text/csv",
                use_container_width=True
            )

        st.dataframe(
            m_filtered,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Email": st.column_config.LinkColumn("Email", display_text="Send Email ✉️"),
                "Google Calendar": st.column_config.LinkColumn("Google Calendar", display_text="Open Meet ↗"),
            }
        )


# ==============================================================================
# FOOTER
# ==============================================================================
st.markdown("---")
st.markdown("""
<div style="display: flex; justify-content: space-between; align-items: center; font-size: 0.78rem; color: #94a3b8; padding: 0.5rem 0;">
    <div>
        <b>HR RECRUITMENT & APPLICANT TRACKING SYSTEM (ATS)</b> &bull; Production Ready
    </div>
    <div>
        Dynamic Header Mapping &bull; Multi-Sheet Engine
    </div>
</div>
""", unsafe_allow_html=True)
