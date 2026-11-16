"""
sample_data.py - Sample realistic HR recruitment datasets.
Also generates multi-tab test Excel files with dirty headers, sub-tables, and instruction tabs
to demonstrate automatic parsing and cleaning.
"""

import io
import pandas as pd
import openpyxl


def get_sample_open_positions() -> pd.DataFrame:
    """Returns realistic open positions dataset."""
    data = [
        {
            "Position ID": "PAM-POS-101",
            "Date Received": "2026-10-15",
            "Company Name": "Azista Industries",
            "Position Title": "Senior Python Backend Engineer",
            "Location": "Bangalore / Hybrid",
            "JD Link": "https://drive.google.com/jd/pam-pos-101",
            "No. of Openings": "3",
            "Budget": "24 - 32 LPA",
            "Experience Required": "5 - 8 Years",
            "Priority": "High",
            "Position Status": "OPEN",
            "Last Follow-up Date": "2026-11-10",
            "Next Follow-up Date": "2026-11-18",
            "Remarks": "Client urgently needs FastAPI + PostgreSQL + AWS expertise.",
        },
        {
            "Position ID": "PAM-POS-102",
            "Date Received": "2026-10-18",
            "Company Name": "Azista Industries",
            "Position Title": "DevOps & Cloud Architect",
            "Location": "Bangalore / Remote",
            "JD Link": "https://drive.google.com/jd/pam-pos-102",
            "No. of Openings": "2",
            "Budget": "30 - 40 LPA",
            "Experience Required": "7 - 11 Years",
            "Priority": "Critical",
            "Position Status": "OPEN",
            "Last Follow-up Date": "2026-11-12",
            "Next Follow-up Date": "2026-11-19",
            "Remarks": "Kubernetes, Terraform, Multi-cloud CI/CD pipeline automation.",
        },
        {
            "Position ID": "PAM-POS-103",
            "Date Received": "2026-10-22",
            "Company Name": "Advait Technologies",
            "Position Title": "Frontend Lead (React / Next.js)",
            "Location": "Hyderabad / Hybrid",
            "JD Link": "https://drive.google.com/jd/pam-pos-103",
            "No. of Openings": "2",
            "Budget": "22 - 28 LPA",
            "Experience Required": "6 - 9 Years",
            "Priority": "Medium",
            "Position Status": "IN PROGRESS",
            "Last Follow-up Date": "2026-11-08",
            "Next Follow-up Date": "2026-11-17",
            "Remarks": "Strong UI/UX taste, micro-frontends and state management.",
        },
        {
            "Position ID": "PAM-POS-104",
            "Date Received": "2026-10-25",
            "Company Name": "Advait Technologies",
            "Position Title": "Product Manager - FinTech",
            "Location": "Mumbai / On-site",
            "JD Link": "https://drive.google.com/jd/pam-pos-104",
            "No. of Openings": "1",
            "Budget": "28 - 35 LPA",
            "Experience Required": "4 - 7 Years",
            "Priority": "High",
            "Position Status": "OPEN",
            "Last Follow-up Date": "2026-11-14",
            "Next Follow-up Date": "2026-11-20",
            "Remarks": "B2B payment gateways and merchant onboarding experience preferred.",
        },
        {
            "Position ID": "PAM-POS-105",
            "Date Received": "2026-11-01",
            "Company Name": "Nexa LifeSciences",
            "Position Title": "HR Business Partner (Talent & Culture)",
            "Location": "Pune / On-site",
            "JD Link": "https://drive.google.com/jd/pam-pos-105",
            "No. of Openings": "1",
            "Budget": "16 - 20 LPA",
            "Experience Required": "4 - 6 Years",
            "Priority": "Medium",
            "Position Status": "OPEN",
            "Last Follow-up Date": "2026-11-11",
            "Next Follow-up Date": "2026-11-21",
            "Remarks": "Employee engagement, appraisal cycles and compliance knowledge.",
        },
        {
            "Position ID": "PAM-POS-106",
            "Date Received": "2026-09-20",
            "Company Name": "Zenith Retail",
            "Position Title": "Supply Chain & Operations Manager",
            "Location": "Delhi NCR / On-site",
            "JD Link": "https://drive.google.com/jd/pam-pos-106",
            "No. of Openings": "2",
            "Budget": "18 - 25 LPA",
            "Experience Required": "5 - 8 Years",
            "Priority": "Low",
            "Position Status": "CLOSED",
            "Last Follow-up Date": "2026-10-30",
            "Next Follow-up Date": "2026-11-30",
            "Remarks": "Position successfully closed with 2 candidate joinings.",
        },
    ]
    return pd.DataFrame(data)


def get_sample_active_candidates() -> pd.DataFrame:
    """Returns realistic active candidates dataset (Sheet 2)."""
    data = [
        {
            "Date Added": "2026-10-28",
            "Candidate Name": "Rohit Verma",
            "Position": "Senior Python Backend Engineer",
            "Phone Number": "+91 98230 45112",
            "Email.id": "rohit.verma.tech@gmail.com",
            "Total Experience": "6.5 Years",
            "Current CTC": "20 LPA",
            "Expected CTC": "27 LPA",
            "Notice Period": "30 Days",
            "Candidate status (Time/ Date)": "F2F Technical Round Cleared (14 Nov)",
            "Google Calender": "https://calendar.google.com/event?eid=pam-rohit-01",
            "Interview Feedback": "Interview stage: Exceptional in system design and database indexing. Manager round scheduled for 18 Nov.",
            "Remark": "Strong candidate, high likelihood of offer release.",
            "Source Tracker": "Active Candidate Tracker",
            "Source Tab": "Azista Industries",
        },
        {
            "Date Added": "2026-11-02",
            "Candidate Name": "Pooja Hegde",
            "Position": "Senior Python Backend Engineer",
            "Phone Number": "+91 97110 88234",
            "Email.id": "pooja.hegde92@outlook.com",
            "Total Experience": "5.2 Years",
            "Current CTC": "18 LPA",
            "Expected CTC": "24 LPA",
            "Notice Period": "15 Days (Serving)",
            "Candidate status (Time/ Date)": "Offer Letter Released (15 Nov)",
            "Google Calender": "",
            "Interview Feedback": "Selected by client VP. Offer rolled out at 26 LPA. Candidate expected to join next Monday.",
            "Remark": "Selected candidate. Offer negotiation done. Joining confirmed.",
            "Source Tracker": "Active Candidate Tracker",
            "Source Tab": "Azista Industries",
        },
        {
            "Date Added": "2026-11-05",
            "Candidate Name": "Vikramaditya Rao",
            "Position": "DevOps & Cloud Architect",
            "Phone Number": "+91 99002 33451",
            "Email.id": "vikram.rao.cloud@yahoo.com",
            "Total Experience": "8.5 Years",
            "Current CTC": "27 LPA",
            "Expected CTC": "36 LPA",
            "Notice Period": "45 Days",
            "Candidate status (Time/ Date)": "Client VC Round 2 Scheduled (19 Nov)",
            "Google Calender": "https://calendar.google.com/event?eid=pam-vikram-02",
            "Interview Feedback": "Interview stage: Screening ok. L1 panel gave 4.5/5 on Kubernetes and Terraform architecture.",
            "Remark": "Client impressed with multi-region AWS DR design.",
            "Source Tracker": "Active Candidate Tracker",
            "Source Tab": "Azista Industries",
        },
        {
            "Date Added": "2026-11-06",
            "Candidate Name": "Sneha Krishnan",
            "Position": "Frontend Lead (React / Next.js)",
            "Phone Number": "+91 98450 11982",
            "Email.id": "sneha.k.ui@gmail.com",
            "Total Experience": "7.0 Years",
            "Current CTC": "21 LPA",
            "Expected CTC": "26 LPA",
            "Notice Period": "60 Days (Negotiable)",
            "Candidate status (Time/ Date)": "Profile Shared with Hiring Manager",
            "Google Calender": "",
            "Interview Feedback": "Screening completed by recruiter team. Good portfolio on Figma & GitHub.",
            "Remark": "Awaiting hiring manager feedback for interview schedule.",
            "Source Tracker": "Active Candidate Tracker",
            "Source Tab": "Advait Technologies",
        },
        {
            "Date Added": "2026-11-08",
            "Candidate Name": "Arjun Singhania",
            "Position": "Frontend Lead (React / Next.js)",
            "Phone Number": "+91 91672 55410",
            "Email.id": "arjun.singhania@rediffmail.com",
            "Total Experience": "6.2 Years",
            "Current CTC": "19 LPA",
            "Expected CTC": "25 LPA",
            "Notice Period": "Immediate Joiner",
            "Candidate status (Time/ Date)": "Final Round Completed - Shortlisted",
            "Google Calender": "",
            "Interview Feedback": "Candidate shortlisted for final offer. Passed coding round with 100% score.",
            "Remark": "Shortlisted for offer. Client HR preparing compensation package.",
            "Source Tracker": "Active Candidate Tracker",
            "Source Tab": "Advait Technologies",
        },
        {
            "Date Added": "2026-11-09",
            "Candidate Name": "Meera Nambiar",
            "Position": "Product Manager - FinTech",
            "Phone Number": "+91 99881 22340",
            "Email.id": "meera.nambiar.pm@gmail.com",
            "Total Experience": "5.8 Years",
            "Current CTC": "24 LPA",
            "Expected CTC": "32 LPA",
            "Notice Period": "30 Days",
            "Candidate status (Time/ Date)": "L1 VC Interview with CTO (17 Nov, 4 PM)",
            "Google Calender": "https://calendar.google.com/event?eid=pam-meera-03",
            "Interview Feedback": "Interview stage: Screening ok. Experience in UPI and lending infrastructure.",
            "Remark": "Shared PRD samples with the panel.",
            "Source Tracker": "Active Candidate Tracker",
            "Source Tab": "Advait Technologies",
        },
        {
            "Date Added": "2026-11-10",
            "Candidate Name": "Kunal Deshmukh",
            "Position": "HR Business Partner (Talent & Culture)",
            "Phone Number": "+91 98221 44556",
            "Email.id": "kunal.deshmukh@hrpro.in",
            "Total Experience": "4.5 Years",
            "Current CTC": "14 LPA",
            "Expected CTC": "18 LPA",
            "Notice Period": "30 Days",
            "Candidate status (Time/ Date)": "Profile Shared with HR Director",
            "Google Calender": "",
            "Interview Feedback": "Screening done: MBA in HR, good communication and grievance handling experience.",
            "Remark": "Profile shared with client. Profile under review.",
            "Source Tracker": "Active Candidate Tracker",
            "Source Tab": "Nexa LifeSciences",
        },
    ]
    return pd.DataFrame(data)


def get_sample_pipeline_candidates() -> pd.DataFrame:
    """Returns realistic pipeline tracker candidates dataset (Sheet 3)."""
    data = [
        {
            "Date Added": "2026-11-12",
            "Candidate Name": "Ananya Mukherjee",
            "Position": "Senior Python Backend Engineer",
            "Phone Number": "+91 98301 23456",
            "Email id": "ananya.mukherjee@gmail.com",
            "Total Experience": "5.5 Years",
            "Current CTC": "19 LPA",
            "Expected CTC": "26 LPA",
            "Notice Period": "60 Days",
            "Next Follow-up Date": "2026-11-17",
            "Follow-up Time": "11:30 AM",
            "Remark": "Sourced via LinkedIn. Interested in remote work. Follow up for updated resume.",
            "Source Tracker": "Candidate Pipeline Tracker",
            "Source Tab": "Azista Industries",
        },
        {
            "Date Added": "2026-11-13",
            "Candidate Name": "Devendra Joshi",
            "Position": "DevOps & Cloud Architect",
            "Phone Number": "+91 97234 56789",
            "Email id": "dev.joshi.infra@gmail.com",
            "Total Experience": "9.0 Years",
            "Current CTC": "29 LPA",
            "Expected CTC": "38 LPA",
            "Notice Period": "45 Days",
            "Next Follow-up Date": "2026-11-18",
            "Follow-up Time": "03:00 PM",
            "Remark": "AWS Certified Solutions Architect. Discussing client project scope.",
            "Source Tracker": "Candidate Pipeline Tracker",
            "Source Tab": "Azista Industries",
        },
        {
            "Date Added": "2026-11-14",
            "Candidate Name": "Ritu Sharma",
            "Position": "Product Manager - FinTech",
            "Phone Number": "+91 98112 34567",
            "Email id": "ritu.sharma.pm@outlook.com",
            "Total Experience": "4.8 Years",
            "Current CTC": "22 LPA",
            "Expected CTC": "29 LPA",
            "Notice Period": "30 Days",
            "Next Follow-up Date": "2026-11-19",
            "Follow-up Time": "05:00 PM",
            "Remark": "Currently at Paytm. Keen to explore B2B neo-banking product role.",
            "Source Tracker": "Candidate Pipeline Tracker",
            "Source Tab": "Advait Technologies",
        },
        {
            "Date Added": "2026-11-15",
            "Candidate Name": "Aditya Saxena",
            "Position": "Frontend Lead (React / Next.js)",
            "Phone Number": "+91 99100 45678",
            "Email id": "aditya.saxena.web@gmail.com",
            "Total Experience": "6.0 Years",
            "Current CTC": "18.5 LPA",
            "Expected CTC": "24 LPA",
            "Notice Period": "Immediate Joiner",
            "Next Follow-up Date": "2026-11-17",
            "Follow-up Time": "10:00 AM",
            "Remark": "Immediate joiner available. Scheduled call to verify notice waiver.",
            "Source Tracker": "Candidate Pipeline Tracker",
            "Source Tab": "Advait Technologies",
        },
        {
            "Date Added": "2026-11-15",
            "Candidate Name": "Tanvi Gupta",
            "Position": "HR Business Partner (Talent & Culture)",
            "Phone Number": "+91 98765 43210",
            "Email id": "tanvi.gupta.hr@gmail.com",
            "Total Experience": "5.0 Years",
            "Current CTC": "13.5 LPA",
            "Expected CTC": "17 LPA",
            "Notice Period": "30 Days",
            "Next Follow-up Date": "2026-11-20",
            "Follow-up Time": "02:30 PM",
            "Remark": "Initial screening call scheduled to confirm location readiness for Pune.",
            "Source Tracker": "Candidate Pipeline Tracker",
            "Source Tab": "Nexa LifeSciences",
        },
    ]
    return pd.DataFrame(data)


def generate_sample_excel_with_dirty_rows(tracker_type: str) -> io.BytesIO:
    """
    Generates a realistic multi-tab Excel file with dirty rows (banner rows, instructions,
    secondary sub-tables) to test and showcase the automatic parsing functionality.
    """
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        if tracker_type == "open_positions":
            # Tab 1: Instruction Tab (Must be ignored)
            instr_df = pd.DataFrame([
                ["How to Use Open Position Tracker"],
                ["1. Enter each new position from client in the respective client tab."],
                ["2. Do not delete column headers."],
                ["3. Update next follow-up dates weekly."],
                ["PAMOHI Confidential Document - Template v2.4"]
            ])
            instr_df.to_excel(writer, sheet_name="How to Use", header=False, index=False)

            # Tab 2: Azista Industries Positions (Contains banner, 444, empty rows)
            azista_raw = [
                ["PAMOHI RECRUITMENT SOLUTIONS - CLIENT OPEN POSITIONS TRACKER", "", "", "", "", ""],
                ["CONFIDENTIAL - FOR INTERNAL RECRUITERS ONLY", "", "", "", "", ""],
                ["", "", "", "", "", ""],
                ["Enter each position below carefully", "", "", "", "", ""],
                ["Position ID", "Date Received", "Company Name", "Position Title", "Location", "JD Link",
                 "No. of Openings", "Budget", "Experience Required", "Priority", "Position Status",
                 "Last Follow-up Date", "Next Follow-up Date", "Remarks"],
                ["PAM-POS-101", "2026-10-15", "Azista Industries", "Senior Python Backend Engineer", "Bangalore / Hybrid",
                 "https://drive.google.com/jd/pam-pos-101", "3", "24 - 32 LPA", "5 - 8 Years", "High", "OPEN",
                 "2026-11-10", "2026-11-18", "Client urgently needs FastAPI + PostgreSQL + AWS."],
                ["PAM-POS-102", "2026-10-18", "Azista Industries", "DevOps & Cloud Architect", "Bangalore / Remote",
                 "https://drive.google.com/jd/pam-pos-102", "2", "30 - 40 LPA", "7 - 11 Years", "Critical", "OPEN",
                 "2026-11-12", "2026-11-19", "Kubernetes, Terraform, CI/CD pipeline automation."],
                ["444", "444", "444", "444", "444", "444", "444", "444", "444", "444", "444", "444", "444", "444"],
                ["Position ID", "Date Received", "Company Name", "Position Title", "Location", "JD Link",
                 "No. of Openings", "Budget", "Experience Required", "Priority", "Position Status",
                 "Last Follow-up Date", "Next Follow-up Date", "Remarks"],
                ["", "", "", "", "", "", "", "", "", "", "", "", "", ""],
            ]
            pd.DataFrame(azista_raw).to_excel(writer, sheet_name="Azista", header=False, index=False)

            # Tab 3: Advait Technologies Positions
            advait_raw = [
                ["PAMOHI CONSULTANCY CLIENT TRACKER", "", "", "", "", ""],
                ["", "", "", "", "", ""],
                ["Position ID", "Date Received", "Company Name", "Position Title", "Location", "JD Link",
                 "No. of Openings", "Budget", "Experience Required", "Priority", "Position Status",
                 "Last Follow-up Date", "Next Follow-up Date", "Remarks"],
                ["PAM-POS-103", "2026-10-22", "Advait Technologies", "Frontend Lead (React / Next.js)", "Hyderabad / Hybrid",
                 "https://drive.google.com/jd/pam-pos-103", "2", "22 - 28 LPA", "6 - 9 Years", "Medium", "IN PROGRESS",
                 "2026-11-08", "2026-11-17", "Strong UI/UX taste, micro-frontends."],
                ["PAM-POS-104", "2026-10-25", "Advait Technologies", "Product Manager - FinTech", "Mumbai / On-site",
                 "https://drive.google.com/jd/pam-pos-104", "1", "28 - 35 LPA", "4 - 7 Years", "High", "OPEN",
                 "2026-11-14", "2026-11-20", "B2B payment gateways and merchant onboarding."],
            ]
            pd.DataFrame(advait_raw).to_excel(writer, sheet_name="Advait", header=False, index=False)

        elif tracker_type == "active_candidates":
            # Multi-tab with Sub-table "Task Tracker" or "Reminder Interview" below main table
            raw_data = [
                ["PAMOHI ACTIVE CANDIDATE RECRUITMENT SHEET", "", "", "", ""],
                ["", "", "", "", ""],
                ["Date Added", "Candidate Name", "Position", "Phone Number", "Email.id", "Total Experience",
                 "Current CTC", "Expected CTC", "Notice Period", "Candidate status (Time/ Date)",
                 "Google Calender", "Interview Feedback", "Remark"],
                ["2026-10-28", "Rohit Verma", "Senior Python Backend Engineer", "+91 98230 45112",
                 "rohit.verma.tech@gmail.com", "6.5 Years", "20 LPA", "27 LPA", "30 Days",
                 "F2F Technical Round Cleared (14 Nov)", "https://calendar.google.com/event?eid=pam-rohit-01",
                 "Interview stage: Exceptional in system design. Manager round scheduled 18 Nov.", "High probability of offer."],
                ["2026-11-02", "Pooja Hegde", "Senior Python Backend Engineer", "+91 97110 88234",
                 "pooja.hegde92@outlook.com", "5.2 Years", "18 LPA", "24 LPA", "15 Days (Serving)",
                 "Offer Letter Released (15 Nov)", "",
                 "Selected by client VP. Offer rolled out at 26 LPA. Joining next week.", "Selected candidate. Offer confirmed."],
                ["2026-11-05", "Vikramaditya Rao", "DevOps & Cloud Architect", "+91 99002 33451",
                 "vikram.rao.cloud@yahoo.com", "8.5 Years", "27 LPA", "36 LPA", "45 Days",
                 "Client VC Round 2 Scheduled (19 Nov)", "https://calendar.google.com/event?eid=pam-vikram-02",
                 "Interview stage: Screening ok. L1 panel gave 4.5/5 on Kubernetes.", "Client impressed with AWS DR design."],
                ["2026-11-06", "Sneha Krishnan", "Frontend Lead (React / Next.js)", "+91 98450 11982",
                 "sneha.k.ui@gmail.com", "7.0 Years", "21 LPA", "26 LPA", "60 Days (Negotiable)",
                 "Profile Shared with Hiring Manager", "",
                 "Screening completed by PAMOHI team. Good portfolio on Figma & GitHub.", "Awaiting feedback."],
                ["", "", "", "", ""],
                # Secondary Sub-table below the main table (must stop parsing here!)
                ["Task Tracker & Reminder Interview", "", "", "", "", ""],
                ["Task ID", "Recruiter", "Pending Item", "Due Date", "Status"],
                ["TSK-01", "Dharmik", "Call Vikram for VC prep", "2026-11-18", "Pending"],
                ["TSK-02", "Dharmik", "Follow up with client for Pooja BG verification", "2026-11-19", "In Progress"]
            ]
            pd.DataFrame(raw_data).to_excel(writer, sheet_name="Active Candidates", header=False, index=False)

        elif tracker_type == "pipeline_candidates":
            raw_data = [
                ["PAMOHI CANDIDATE PIPELINE TRACKER", "", "", "", ""],
                ["Each company must add candidates to their respective roles", "", "", "", ""],
                ["How to Use: Keep track of warm candidates and upcoming follow-ups", "", "", "", ""],
                ["Add one row per prospective applicant", "", "", "", ""],
                ["", "", "", "", ""],
                ["Date Added", "Candidate Name", "Position", "Phone Number", "Email id", "Total Experience",
                 "Current CTC", "Expected CTC", "Notice Period", "Next Follow-up Date", "Follow-up Time", "Remark"],
                ["2026-11-12", "Ananya Mukherjee", "Senior Python Backend Engineer", "+91 98301 23456",
                 "ananya.mukherjee@gmail.com", "5.5 Years", "19 LPA", "26 LPA", "60 Days",
                 "2026-11-17", "11:30 AM", "Sourced via LinkedIn. Interested in remote work. Follow up for resume."],
                ["2026-11-13", "Devendra Joshi", "DevOps & Cloud Architect", "+91 97234 56789",
                 "dev.joshi.infra@gmail.com", "9.0 Years", "29 LPA", "38 LPA", "45 Days",
                 "2026-11-18", "03:00 PM", "AWS Certified Architect. Sourced via Naukri. Discussing project scope."],
                ["2026-11-14", "Ritu Sharma", "Product Manager - FinTech", "+91 98112 34567",
                 "ritu.sharma.pm@outlook.com", "4.8 Years", "22 LPA", "29 LPA", "30 Days",
                 "2026-11-19", "05:00 PM", "Currently at Paytm. Keen to explore B2B fintech role."],
                ["", "", "", "", ""],
                ["How to Use: Ensure all dates are YYYY-MM-DD", "", "", "", ""],
            ]
            pd.DataFrame(raw_data).to_excel(writer, sheet_name="Candidate Pipeline", header=False, index=False)

    output.seek(0)
    return output

