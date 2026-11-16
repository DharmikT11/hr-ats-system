# HR Recruitment & Applicant Tracking System (ATS)

A modern, production-ready ATS web application built with Python, Streamlit, Pandas, and Plotly.

---

## 🚀 Key Features

### 1. Flexible Multi-Sheet & Custom Header Ingestion
- **Arbitrary Number of Spreadsheets**: Upload 1, 2, 5, 10 or more Excel (`.xlsx`, `.xls`) or CSV files at once.
- **Dynamic Header & Synonym Detection**: Intelligent fuzzy-matching automatically recognizes diverse column headers across different client templates (e.g., *Full Name*, *Candidate*, *Applicant*, *Tech Stack*, *Role*, *CCTC*, *Current Package*, *Notice*, *Availability*, *Recruiter Notes*, etc.).
- **Zero Pre-loaded Dummy Data**: Opens with a clean, welcoming state ready for your real spreadsheets. No mock data is shown unless you explicitly click the optional sample preview.
- **Custom Column Preservation**: Any unique or custom column present in your client spreadsheets (e.g., *Skills*, *Degree*, *College*, *Preferred Location*, *SPOC*) is fully preserved and accessible in the dynamic chart builder, search table, candidate cards, and CSV export.
- **Banner & Noise Removal**: Automatically locates the true header row, ignores top banner titles, filters out repeated headers, blank rows, and filler rows containing `"PAMOHI"`, `"Enter each"`, or `"444"`.
- **Sub-Table Truncation**: Intelligently stops reading rows in candidate sheets when secondary sub-tables like `"Task Tracker"` or `"Reminder Interview"` appear below the main data.

### 2. Modern Visual ATS Kanban Board
- **4 Color-Coded Pipeline Stages**:
  - 🔵 **New Applicants / Pipeline** (`#2563eb`) — Default for Sheet 3.
  - 🟠 **Profile Shared / Screening** (`#ea580c`) — Default for Sheet 2.
  - 🔴 **Interview Stage** (`#dc2626`) — Auto-classified via keywords (`"interview"`, `"f2f"`, `"vc"`, `"round"`, `"schedule"`, `"screening ok"`).
  - 🟢 **Selected / Offer** (`#0891b2`) — Auto-classified via keywords (`"selected"`, `"hired"`, `"offer"`, `"joined"`, `"shortlisted"`).
- **Top Control Bar**: Filter by any job position dynamically, or search across any candidate attribute with instant live filtering.
- **Dynamic Job Banner**: Shows real-time metadata (Client, Location, Budget, Experience Required, Openings, Priority, JD Link).
- **Executive Candidate Cards**: Styled white cards with subtle shadow, contact details, notice period, CTC, and highlighted status/interview feedbacks.

### 3. Open Positions & Recruitment KPIs
- Real-time KPI summary: Total Openings, Active Roles, In Progress, Closed Roles, Candidate Depth.
- Filterable interactive table of all client positions with client dossiers.

### 4. Interactive Analytics & Future-Proof Dynamic Chart Builder
- Candidate stage donut chart, roles bar chart, client positions, and notice period charts.
- **Dynamic Chart Builder**: Automatically scans and detects all existing and newly added columns in future spreadsheets, letting users create Bar, Line, Pie, Scatter, Box, or Histogram charts on the fly.

### 5. Master Candidate Database & One-Click CSV Export
- Searchable and filterable table combining all candidates across Sheet 2 and Sheet 3.
- One-click CSV download of filtered candidate lists.

---

## 🛠️ Quick Start Guide

### 1. Prerequisites
Ensure Python 3.9+ is installed on your machine.

### 2. Activate the Virtual Environment
A dedicated virtual environment (`venv`) has already been created with all dependencies installed.

In PowerShell:
```powershell
.\venv\Scripts\Activate.ps1
```
*(Or in Command Prompt: `.\venv\Scripts\activate.bat`)*

### 3. Launch the Application
```powershell
streamlit run app.py
```

> **Direct Launch Without Manual Activation:**
> You can also run the app directly using the venv's Python binary:
> ```powershell
> .\venv\Scripts\streamlit.exe run app.py
> ```

The web application will open in your default browser at `http://localhost:8501`.

---

## 📁 Project Structure

```
c:\Users\Dharmik\Desktop\HR_Analytics\
├── app.py                      # Main Streamlit ATS web application
├── data_parser.py              # Robust parser, regex cleaning & ATS stage classification
├── sample_data.py              # Sample test datasets & Excel generator
├── test_app.py                 # Automated unit tests for parsers & classification
├── requirements.txt            # Dependency specification
└── .streamlit/
    └── config.toml             # Custom theme and telemetry configuration
```

