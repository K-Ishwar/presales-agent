from reportlab.pdfgen import canvas

def create_pdf(filename):
    c = canvas.Canvas(filename)
    c.drawString(100, 750, "Request for Proposal: Cloud Migration Services")
    c.drawString(100, 730, "Company: Test Corp")
    c.drawString(100, 710, "Requirements:")
    c.drawString(120, 690, "- 99.9% Uptime")
    c.drawString(120, 670, "- Automated backups")
    c.drawString(120, 650, "- 24/7 Support")
    c.save()
    print(f"Created {filename}")

if __name__ == "__main__":
    create_pdf("test_rfp_simple.pdf")
