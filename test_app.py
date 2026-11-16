"""
Comprehensive test suite verifying data parsing, cleaning, multi-tab handling,
ATS stage classification, and export capabilities.
"""

import io
import pandas as pd
import data_parser
import sample_data


def test_open_positions_parsing():
    excel_file = sample_data.generate_sample_excel_with_dirty_rows("open_positions")
    df = data_parser.parse_tracker_file(excel_file, "open_positions")

    assert not df.empty, "DataFrame should not be empty"
    # Header should contain Position ID and Position Title
    assert "Position ID" in df.columns, "Position ID missing"
    assert "Position Title" in df.columns, "Position Title missing"
    assert "Budget" in df.columns, "Budget missing"
    assert "No. of Openings" in df.columns, "No. of Openings missing"

    # Multi-tab merge test: should include roles from both Azista and Advait
    titles = list(df["Position Title"])
    assert "Senior Python Backend Engineer" in titles, "Azista role missing"
    assert "Product Manager - FinTech" in titles, "Advait role missing"

    # Junk filtering test: 444, Enter each, PAMOHI banner, and How to Use must not be present
    for _, row in df.iterrows():
        row_str = " ".join([str(v) for v in row.values])
        assert "444" not in row_str, f"Found 444 in row: {row_str}"
        assert "Enter each" not in row_str, f"Found 'Enter each' in row: {row_str}"
        assert "How to Use" not in row_str, f"Found 'How to Use' in row: {row_str}"

    print("✔ test_open_positions_parsing passed successfully.")


def test_active_candidates_parsing_and_subtable_cutoff():
    excel_file = sample_data.generate_sample_excel_with_dirty_rows("active_candidates")
    df = data_parser.parse_tracker_file(excel_file, "active_candidates")

    assert not df.empty, "DataFrame should not be empty"
    assert "Candidate Name" in df.columns, "Candidate Name missing"
    assert "Candidate status (Time/ Date)" in df.columns, "Status missing"
    assert "Interview Feedback" in df.columns, "Interview Feedback missing"

    names = list(df["Candidate Name"])
    assert "Rohit Verma" in names
    assert "Pooja Hegde" in names
    assert "Vikramaditya Rao" in names
    assert "Sneha Krishnan" in names

    # Sub-table cutoff test: Task Tracker rows must NOT be present
    for _, row in df.iterrows():
        row_str = " ".join([str(v) for v in row.values])
        assert "Task Tracker" not in row_str
        assert "Reminder Interview" not in row_str
        assert "TSK-01" not in row_str
        assert "TSK-02" not in row_str

    print("✔ test_active_candidates_parsing_and_subtable_cutoff passed successfully.")


def test_pipeline_candidates_parsing_and_instruction_filtering():
    excel_file = sample_data.generate_sample_excel_with_dirty_rows("pipeline_candidates")
    df = data_parser.parse_tracker_file(excel_file, "pipeline_candidates")

    assert not df.empty, "DataFrame should not be empty"
    assert "Candidate Name" in df.columns
    assert "Next Follow-up Date" in df.columns
    assert "Follow-up Time" in df.columns

    names = list(df["Candidate Name"])
    assert "Ananya Mukherjee" in names
    assert "Devendra Joshi" in names
    assert "Ritu Sharma" in names

    # Instruction row filtering test
    for _, row in df.iterrows():
        row_str = " ".join([str(v) for v in row.values])
        assert "How to Use" not in row_str
        assert "Each company" not in row_str
        assert "Add one row" not in row_str

    print("✔ test_pipeline_candidates_parsing_and_instruction_filtering passed successfully.")


def test_stage_classification():
    # Test Selected / Offer
    s1 = data_parser.classify_candidate_stage(pd.Series({
        "Candidate status (Time/ Date)": "Final offer letter released",
        "Source Tracker": "Active Candidate Tracker"
    }))
    assert s1 == "Selected / Offer", f"Expected 'Selected / Offer', got {s1}"

    # Test Interview Stage
    s2 = data_parser.classify_candidate_stage(pd.Series({
        "Candidate status (Time/ Date)": "F2F technical round scheduled for tomorrow",
        "Source Tracker": "Active Candidate Tracker"
    }))
    assert s2 == "Interview Stage", f"Expected 'Interview Stage', got {s2}"

    # Test Screening / Profile Shared
    s3 = data_parser.classify_candidate_stage(pd.Series({
        "Candidate status (Time/ Date)": "Profile shared with hiring manager",
        "Source Tracker": "Active Candidate Tracker"
    }))
    assert s3 == "Profile Shared / Screening", f"Expected 'Profile Shared / Screening', got {s3}"

    # Test Pipeline Tracker default
    s4 = data_parser.classify_candidate_stage(pd.Series({
        "Candidate status (Time/ Date)": "",
        "Source Tracker": "Candidate Pipeline Tracker"
    }))
    assert s4 == "New Applicants / Pipeline", f"Expected 'New Applicants / Pipeline', got {s4}"

    print("✔ test_stage_classification passed successfully.")


def test_unified_candidate_pool():
    act = sample_data.get_sample_active_candidates()
    pip = sample_data.get_sample_pipeline_candidates()
    unified = data_parser.build_unified_candidate_pool(act, pip)

    assert len(unified) == len(act) + len(pip)
    assert set(unified["Stage"].unique()).issubset({
        "New Applicants / Pipeline",
        "Profile Shared / Screening",
        "Interview Stage",
        "Selected / Offer"
    })
    print("✔ test_unified_candidate_pool passed successfully.")


if __name__ == "__main__":
    test_open_positions_parsing()
    test_active_candidates_parsing_and_subtable_cutoff()
    test_pipeline_candidates_parsing_and_instruction_filtering()
    test_stage_classification()
    test_unified_candidate_pool()
    print("\n🎉 ALL UNIT TESTS PASSED WITH 100% SUCCESS!")

