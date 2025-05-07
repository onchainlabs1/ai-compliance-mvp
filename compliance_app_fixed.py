"""
DevAgent-MCP: AI Compliance Analysis
=================================

Specialized interface for analyzing AI code compliance with
EU AI Act and ISO 42001 standards.
"""

import os
import json
import time
from pathlib import Path
import dotenv
import datetime

import streamlit as st
from tools.compliance_tools import ComplianceChecker, generate_compliance_report

# Load environment variables from .env file if it exists
if Path(".env").exists():
    dotenv.load_dotenv()

# Configure Streamlit page
st.set_page_config(
    page_title="AI Compliance Analyzer", 
    page_icon="🛡️",
    layout="centered"
)
st.title("🛡️ AI Compliance Analyzer")
st.write("This tool analyzes AI code for compliance with key regulatory frameworks:")
st.write("- **EU AI Act** - European Union's comprehensive AI regulation")
st.write("- **ISO 42001** - International standard for AI management systems")
st.write("Upload your code files or paste code for automated compliance assessment.")

# Initialize compliance checker
compliance_checker = ComplianceChecker()

# Define tabs for different input methods
tab1, tab2, tab3 = st.tabs(["Paste Code", "Upload Files", "GitHub PR"])

with tab1:
    st.header("Analyze Code Snippet")
    
    code_input = st.text_area(
        "Paste your AI code here:",
        height=300,
        placeholder="# Paste your AI code here...",
        help="Paste Python, JavaScript, or other code that implements AI functionality"
    )
    
    file_type = st.selectbox(
        "File Type", 
        options=["py", "js", "java", "cpp", "ts", "other"],
        index=0,
        help="Select the programming language of your code"
    )
    
    analyze_btn = st.button("Analyze for Compliance", type="primary", use_container_width=True)
    
    if analyze_btn and code_input:
        with st.spinner("Analyzing code for compliance issues..."):
            # Simulate longer processing for better UX
            time.sleep(1)
            
            # Analyze the code
            findings = compliance_checker.analyze_code(code_input, file_type)
            
            # Display results
            st.subheader("📊 Compliance Analysis Results")
            
            # Overall risk level with color coding
            risk_level = findings.get("overall_risk", "unknown")
            if risk_level == "high":
                st.error("⚠️ **Risk Level: HIGH**")
            elif risk_level == "medium":
                st.warning("⚠️ **Risk Level: MEDIUM**")
            else:
                st.success("✅ **Risk Level: LOW**")
            
            # Display summary
            st.text_area("Summary", findings.get("summary", ""), height=150)
            
            # Create tabs for detailed findings
            ai_act_tab, iso_tab, report_tab = st.tabs(["EU AI Act Issues", "ISO 42001 Issues", "Full Report"])
            
            with ai_act_tab:
                if not findings.get("ai_act"):
                    st.success("No EU AI Act compliance issues detected")
                else:
                    for i, issue in enumerate(findings.get("ai_act", [])):
                        with st.expander(f"{i+1}. {issue.get('description', 'Issue')}"):
                            st.write(f"**Type:** {issue.get('type', 'N/A')}")
                            st.write(f"**Risk Level:** {issue.get('risk_level', 'N/A')}")
                            st.write(f"**Recommendation:** {issue.get('recommendation', 'N/A')}")
                            
                            if "missing_elements" in issue:
                                st.write("**Missing Elements:**")
                                for elem in issue.get("missing_elements", []):
                                    st.write(f"- {elem}")
            
            with iso_tab:
                if not findings.get("iso_42001"):
                    st.success("No ISO 42001 compliance issues detected")
                else:
                    for i, issue in enumerate(findings.get("iso_42001", [])):
                        with st.expander(f"{i+1}. {issue.get('description', 'Issue')}"):
                            st.write(f"**Type:** {issue.get('type', 'N/A')}")
                            st.write(f"**Risk Level:** {issue.get('risk_level', 'N/A')}")
                            st.write(f"**Recommendation:** {issue.get('recommendation', 'N/A')}")
                            
                            if "missing_elements" in issue:
                                st.write("**Missing Elements:**")
                                for elem in issue.get("missing_elements", []):
                                    st.write(f"- {elem}")
            
            with report_tab:
                report_json = json.dumps(findings, indent=2)
                st.download_button(
                    "Download Full Report (JSON)",
                    report_json,
                    "compliance_report.json",
                    "application/json"
                )
                st.code(report_json, language="json")

# Sidebar for API config
with st.sidebar:
    st.header("🔑 API Configuration")
    
    # Get credentials from environment variables
    default_github = os.getenv("GITHUB_TOKEN", "")
    default_groq = os.getenv("GROQ_API_KEY", "")
    
    gh_token = st.text_input(
        "GitHub Token",
        value=default_github,
        type="password",
        help="GitHub personal token with 'repo' permissions"
    )
    
    groq_api_key = st.text_input(
        "GROQ API Key",
        value=default_groq,
        type="password",
        help="GROQ API key for advanced compliance analysis"
    )
    
    # Analysis depth options
    st.subheader("Analysis Options")
    
    analysis_depth = st.select_slider(
        "Analysis Depth",
        options=["Basic", "Standard", "Deep"],
        value="Standard",
        help="Controls how thoroughly the code is analyzed"
    )
    
    include_dependencies = st.checkbox(
        "Include Dependencies",
        value=False,
        help="Also analyze dependencies referenced in the code"
    )

# Footer information
st.markdown("---")
st.write("**AI Compliance Analyzer** is based on the latest EU AI Act and ISO 42001 guidelines.")  
st.write("This tool helps identify potential compliance issues but does not guarantee full regulatory compliance.")  
st.write("For critical AI systems, consider professional certification and legal review.")

if __name__ == "__main__":
    # Code that would be executed only when running this file directly
    pass 