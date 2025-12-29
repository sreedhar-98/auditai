"""
Streamlit UI for SOP vs Policy Document Comparison
"""

import streamlit as st
import os
import sys
from dotenv import load_dotenv

# Add the parent directory to the Python path to allow imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from document_comparator import DocumentComparator

load_dotenv()

# Page configuration
st.set_page_config(page_title="Audit AI", page_icon="📄", layout="wide")

# Custom CSS
st.markdown(
    """
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stButton>button {
        background-color: #1f77b4;
        color: white;
        width: 100%;
        padding: 0.5rem;
        border-radius: 5px;
    }
    .upload-section {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Header
st.markdown(
    '<h1 class="main-header">📄 Audit AI</h1>',
    unsafe_allow_html=True,
)
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")

    # Get API key from environment variable
    api_key = os.getenv("GEMINI_API_KEY")

    if api_key:
        st.success("✅ API Key configured")
    else:
        st.error("❌ GEMINI_API_KEY not found in environment variables")

    st.markdown("---")
    st.markdown("### 📖 How to Use")
    st.markdown("""
    1. Upload your SOP document (PDF)
    2. Upload your Policy document (PDF)
    3. Click 'Generate Compliance Report'
    4. Review the detailed analysis
    """)

    st.markdown("---")
    st.markdown("### ℹ️ About")
    st.markdown("""
    This tool is used to compare policy documents against 
    Standard Operating Procedures (SOPs) and generate detailed compliance reports.
    """)

# Main content
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="upload-section">', unsafe_allow_html=True)
    st.subheader("📋 SOP Document")
    sop_file = st.file_uploader(
        "Upload SOP PDF",
        type=["pdf"],
        key="sop",
        help="Upload the Standard Operating Procedure document",
    )
    if sop_file:
        st.success(f"✅ Uploaded: {sop_file.name}")
        st.info(f"File size: {len(sop_file.getvalue()) / 1024:.2f} KB")
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown('<div class="upload-section">', unsafe_allow_html=True)
    st.subheader("📝 Policy Document")
    policy_file = st.file_uploader(
        "Upload Policy PDF",
        type=["pdf"],
        key="policy",
        help="Upload the Policy document to be checked against the SOP",
    )
    if policy_file:
        st.success(f"✅ Uploaded: {policy_file.name}")
        st.info(f"File size: {len(policy_file.getvalue()) / 1024:.2f} KB")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")

# Generate report button
if st.button("🔍 Generate Compliance Report", type="primary", use_container_width=True):
    # Validation
    if not api_key:
        st.error(
            "❌ GEMINI_API_KEY environment variable is not set. Please set it before running the app."
        )
    elif not sop_file:
        st.error("❌ Please upload an SOP document")
    elif not policy_file:
        st.error("❌ Please upload a Policy document")
    else:
        try:
            with st.spinner("🔄 Analyzing documents... This may take a minute..."):
                # Initialize comparator
                comparator = DocumentComparator(api_key=api_key)

                # Read file data
                sop_data = sop_file.getvalue()
                policy_data = policy_file.getvalue()

                # Generate report
                report = comparator.generate_report(sop_data, policy_data)

                # Display report
                st.markdown("---")
                st.markdown("## 📊 Compliance Report")
                st.markdown(report)

                # Download button
                st.download_button(
                    label="📥 Download Report",
                    data=report,
                    file_name="compliance_report.md",
                    mime="text/markdown",
                )

        except Exception as e:
            st.error(f"❌ Error generating report: {str(e)}")
            st.exception(e)

# Footer
# st.markdown("---")
# st.markdown(
#     "<p style='text-align: center; color: gray;'>Powered by Google Gemini API | "
#     "Built with Streamlit</p>",
#     unsafe_allow_html=True,
# )
