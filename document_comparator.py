"""
Document Comparator - Core Functionality
Compares SOP and Policy documents using Gemini API
"""

import os
from google import genai
from dotenv import load_dotenv


# from google.genai import types
import io

load_dotenv()


class DocumentComparator:
    """Compares SOP and Policy documents using Gemini Files API"""

    def __init__(self, api_key: str = None):
        """
        Initialize the DocumentComparator

        Args:
            api_key: Gemini API key. If None, reads from GEMINI_API_KEY env variable
        """
        if api_key:
            os.environ["GEMINI_API_KEY"] = api_key

        self.client = genai.Client(api_key=api_key or os.getenv("GEMINI_API_KEY"))
        self.model_name = "gemini-3-flash-preview"

    def upload_pdf(self, file_data: bytes, display_name: str) -> object:
        """
        Upload a PDF file to Gemini Files API

        Args:
            file_data: PDF file bytes
            display_name: Name for the uploaded file

        Returns:
            Uploaded file object
        """
        file_io = io.BytesIO(file_data)

        uploaded_file = self.client.files.upload(
            file=file_io,
            config=dict(mime_type="application/pdf", display_name=display_name),
        )

        return uploaded_file

    def compare_documents(self, sop_file, policy_file) -> str:
        """
        Compare SOP and Policy documents and generate a detailed report

        Args:
            sop_file: Uploaded SOP file object
            policy_file: Uploaded Policy file object

        Returns:
            Detailed comparison report as string
        """

        prompt = """You are a compliance auditor tasked with comparing a Policy document against a Standard Operating Procedure (SOP) document.

**Your Task:**
1. Analyze both documents thoroughly
2. Identify all key requirements, procedures, and guidelines in the SOP
3. Check if the Policy document adheres to each SOP requirement
4. Generate a comprehensive compliance report

**Report Structure:**

## Executive Summary
Provide a brief overview of compliance status (compliant, partially compliant, or non-compliant)

## Detailed Analysis

### 1. Adherence Assessment
For each major section/requirement in the SOP:
- **SOP Requirement:** [Describe the requirement]
- **Policy Implementation:** [How the policy addresses it]
- **Status:** ✅ Compliant / ⚠️ Partially Compliant / ❌ Non-Compliant
- **Gap Analysis:** [Describe any gaps or deviations]

### 2. Missing Elements
List any SOP requirements that are not addressed in the Policy

### 3. Conflicting Information
Identify any contradictions between the SOP and Policy

### 4. Additional Policy Elements
Note any elements in the Policy that go beyond SOP requirements

## Recommendations

### Priority 1 - Critical Issues
[Issues that must be addressed immediately]

### Priority 2 - Important Issues  
[Issues that should be addressed soon]

### Priority 3 - Suggestions for Improvement
[Nice-to-have improvements]

## Compliance Score
Provide an overall compliance percentage and rating

Please be thorough, specific, and cite exact sections/pages when possible."""

        response = self.client.models.generate_content(
            model=self.model_name, contents=[sop_file, policy_file, prompt]
        )

        return response.text

    def generate_report(self, sop_data: bytes, policy_data: bytes) -> str:
        """
        Main function to upload documents and generate comparison report

        Args:
            sop_data: SOP PDF file bytes
            policy_data: Policy PDF file bytes

        Returns:
            Comparison report as string
        """
        # Upload both documents
        sop_file = self.upload_pdf(sop_data, "SOP_Document")
        policy_file = self.upload_pdf(policy_data, "Policy_Document")

        # Generate comparison report
        report = self.compare_documents(sop_file, policy_file)

        return report


if __name__ == "__main__":
    # Example usage
    comparator = DocumentComparator()

    # Read sample PDFs (replace with actual file paths)
    with open("sop.pdf", "rb") as f:
        sop_data = f.read()

    with open("policy.pdf", "rb") as f:
        policy_data = f.read()

    # Generate report
    report = comparator.generate_report(sop_data, policy_data)
    print(report)
