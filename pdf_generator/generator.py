import io
import os
from jinja2 import Environment, FileSystemLoader

# Try to import WeasyPrint dynamically. If GTK/GObject is missing (common on Windows),
# we catch the ImportError/OSError and fall back to ReportLab.
try:
    from weasyprint import HTML
    WEASYPRINT_AVAILABLE = True
except (ImportError, OSError) as e:
    print(f"Warning: WeasyPrint not available ({e}). Falling back to ReportLab for PDF generation.")
    WEASYPRINT_AVAILABLE = False


def _generate_pdf_reportlab(data: dict) -> bytes:
    """
    Fallback PDF generator using ReportLab.
    Creates a clean, professional PDF matching the template data.
    """
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib import colors

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=54,
        leftMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom styles
    h2_style = ParagraphStyle(
        'SectionHeading',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=colors.HexColor('#1f2937'),
        spaceBefore=15,
        spaceAfter=10,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'BodyTextCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10.5,
        leading=14,
        textColor=colors.HexColor('#374151'),
        spaceAfter=6
    )

    success_style = ParagraphStyle(
        'SuccessText',
        parent=body_style,
        textColor=colors.HexColor('#16a34a')
    )

    danger_style = ParagraphStyle(
        'DangerText',
        parent=body_style,
        textColor=colors.HexColor('#dc2626')
    )

    story = []

    # Header Banner
    banner_title = data.get("title", "CloudMatrix Proposal")
    banner_data = [[Paragraph(
        banner_title,
        ParagraphStyle('BannerText', fontName='Helvetica-Bold', fontSize=18, leading=22, textColor=colors.white)
    )]]
    banner_table = Table(banner_data, colWidths=[504])
    banner_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#1f2937')),
        ('TOPPADDING', (0, 0), (-1, -1), 15),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 15),
        ('LEFTPADDING', (0, 0), (-1, -1), 15),
        ('RIGHTPADDING', (0, 0), (-1, -1), 15),
    ]))
    story.append(banner_table)
    story.append(Spacer(1, 20))

    # Compatibility Score
    score = data.get("score", 0)
    score_color = '#16a34a' if score >= 80 else ('#d97706' if score >= 60 else '#dc2626')
    score_style = ParagraphStyle(
        'ScoreStyle',
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=colors.HexColor(score_color)
    )
    story.append(Paragraph(f"Compatibility Score: {score}%", score_style))
    story.append(Spacer(1, 10))

    # Executive Summary (if provided)
    if "summary" in data:
        story.append(Paragraph("Executive Summary", h2_style))
        story.append(Paragraph(data["summary"], body_style))

    # Strengths / Met Requirements
    story.append(Paragraph("Key Strengths & Met Requirements", h2_style))
    strengths_text = data.get("strengths", "")
    has_strengths = False
    for line in strengths_text.split('\n'):
        if line.strip():
            story.append(Paragraph(line, success_style))
            has_strengths = True
    if not has_strengths:
        story.append(Paragraph("None identified.", body_style))

    # Weaknesses / Unmet Requirements
    story.append(Paragraph("Gaps & Unmet Requirements", h2_style))
    weaknesses_text = data.get("weaknesses", "")
    has_weaknesses = False
    for line in weaknesses_text.split('\n'):
        if line.strip():
            story.append(Paragraph(line, danger_style))
            has_weaknesses = True
    if not has_weaknesses:
        story.append(Paragraph("None identified.", body_style))

    story.append(Spacer(1, 10))

    # Pricing Table
    story.append(Paragraph("Pricing & Investment Details", h2_style))

    table_data = [[
        Paragraph("<b>Item</b>", ParagraphStyle('TableHeader', fontName='Helvetica-Bold', fontSize=10, leading=13, textColor=colors.white)),
        Paragraph("<b>Cost</b>", ParagraphStyle('TableHeader', fontName='Helvetica-Bold', fontSize=10, leading=13, textColor=colors.white))
    ]]

    pricing_list = data.get("pricing", [])
    for item in pricing_list:
        name_val = item.get("name", "N/A")
        cost_val = item.get("cost", "N/A")
        is_total = (name_val == "Total Monthly" or "total" in name_val.lower())
        item_font = 'Helvetica-Bold' if is_total else 'Helvetica'

        table_data.append([
            Paragraph(f"{name_val}", ParagraphStyle('TableItem', fontName=item_font, fontSize=9.5, leading=12)),
            Paragraph(f"{cost_val}", ParagraphStyle('TableCost', fontName=item_font, fontSize=9.5, leading=12))
        ])

    pricing_table = Table(table_data, colWidths=[350, 154])
    t_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f2937')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#d1d5db')),
    ])

    for idx, item in enumerate(pricing_list):
        name_val = item.get("name", "N/A")
        is_total = (name_val == "Total Monthly" or "total" in name_val.lower())
        if is_total:
            t_style.add('BACKGROUND', (0, idx + 1), (-1, idx + 1), colors.HexColor('#f3f4f6'))

    pricing_table.setStyle(t_style)
    story.append(pricing_table)

    doc.build(story)
    return buffer.getvalue()


def generate_pdf(data, output_path):
    """
    Renders HTML using template and writes PDF to file.
    Falls back to ReportLab if WeasyPrint is unavailable.
    """
    if WEASYPRINT_AVAILABLE:
        try:
            env = Environment(loader=FileSystemLoader("pdf_generator/templates"))
            template = env.get_template("proposal.html")
            html = template.render(**data)
            HTML(string=html).write_pdf(output_path)
            return
        except Exception as err:
            print(f"WeasyPrint rendering failed ({err}). Falling back to ReportLab.")

    # Fallback to ReportLab and write to file
    pdf_bytes = _generate_pdf_reportlab(data)
    with open(output_path, "wb") as f:
        f.write(pdf_bytes)


def generate_proposal_pdf(analysis: dict, rfp_text: str = "") -> bytes:
    """
    Full implementation of generate_proposal_pdf for API integration.
    Maps analysis dict to template data structure, and generates PDF bytes.
    """
    # Map the RFP analysis dict structure to the template keys
    recommended_tier = analysis.get("recommended_tier", "Unknown")
    base_price = analysis.get("base_price", 0)
    total_monthly = analysis.get("total_monthly_price", 0)

    pricing_items = [
        {"name": f"Base Plan ({recommended_tier})", "cost": f"${base_price:,.2f}"}
    ]

    for addon in analysis.get("addons", []):
        pricing_items.append({
            "name": addon.get("name", "Add-on"),
            "cost": f"${addon.get('price', 0):,.2f}"
        })

    pricing_items.append({
        "name": "Total Monthly Price",
        "cost": f"${total_monthly:,.2f}"
    })

    strengths = "Met Requirements:\n" + "\n".join([f"• {req}" for req in analysis.get("can_meet", [])])
    weaknesses = "Unmet Requirements:\n" + "\n".join([f"• {req}" for req in analysis.get("cannot_meet", [])])

    data = {
        "title": f"CloudMatrix Proposal for {analysis.get('client_name', 'Client')}",
        "score": analysis.get("compatibility_score", 0),
        "strengths": strengths,
        "weaknesses": weaknesses,
        "pricing": pricing_items,
        "summary": analysis.get("summary", "")
    }

    if WEASYPRINT_AVAILABLE:
        try:
            env = Environment(loader=FileSystemLoader("pdf_generator/templates"))
            template = env.get_template("proposal.html")
            html = template.render(**data)
            return HTML(string=html).write_pdf()
        except Exception as err:
            print(f"WeasyPrint in-memory rendering failed ({err}). Falling back to ReportLab.")

    return _generate_pdf_reportlab(data)