# pdf_parser/__init__.py
# STUB — Member 3 will replace this with real pdfplumber implementation


def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    """
    STUB implementation of extract_text_from_pdf.
    Returns fake RFP text for backend development and testing.

    Real implementation: pdf_parser/parser.py (Member 3)

    Parameters:
        pdf_bytes: Raw bytes of the uploaded PDF file

    Returns:
        str: All text extracted from the PDF
    """
    print(f"[STUB] extract_text_from_pdf called with {len(pdf_bytes)} bytes")

    return """
    STUB RFP TEXT — Company: GlobalBank Corp
    Industry: Financial Services

    Requirements:
    1. 99.99% uptime SLA (mandatory)
    2. SOC2 Type II compliance (mandatory)
    3. Salesforce CRM integration
    4. Real-time event streaming for transactions
    5. Support for 50,000 concurrent users
    6. Dedicated support engineer required
    7. Staff training for 200 employees

    Budget: Flexible for the right enterprise solution.
    Decision Timeline: 30 days.

    This is stub text. Member 3's real implementation
    will extract actual text from the uploaded PDF.
    """