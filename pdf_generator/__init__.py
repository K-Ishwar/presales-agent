# pdf_generator/__init__.py
# STUB — Member 3 will replace this with real WeasyPrint implementation


def generate_proposal_pdf(analysis: dict, rfp_text: str = "") -> bytes:
    """
    STUB implementation of generate_proposal_pdf.
    Returns a minimal valid PDF for backend development and testing.

    Real implementation: pdf_generator/generator.py (Member 3)

    Parameters:
        analysis: Dict from analyze_rfp()
        rfp_text: Original RFP text (optional)

    Returns:
        bytes: Raw PDF file bytes
    """
    print(f"[STUB] generate_proposal_pdf called for: {analysis.get('client_name', 'Unknown')}")

    # Return a real minimal PDF so the download actually works during testing
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import A4
    import io

    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 18)
    c.drawString(72, height - 80, "CloudMatrix — Solution Proposal")

    c.setFont("Helvetica-Bold", 13)
    c.drawString(72, height - 120, f"Client: {analysis.get('client_name', 'Unknown')}")

    c.setFont("Helvetica", 11)
    lines = [
        f"Recommended Plan: {analysis.get('recommended_tier', 'N/A')}",
        f"Monthly Investment: ${analysis.get('total_monthly_price', 0):,.0f}",
        f"Compatibility Score: {analysis.get('compatibility_score', 0)}%",
        "",
        "STUB PDF — Member 3's real implementation",
        "will replace this with a professionally designed proposal.",
    ]
    y = height - 160
    for line in lines:
        c.drawString(72, y, line)
        y -= 22

    c.save()
    return buffer.getvalue()