# api/routes/proposal.py
# POST /api/generate-proposal
# Takes RFP analysis data, generates a PDF proposal,
# returns it as a downloadable file

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from api.models import ProposalRequest
from pdf_generator import generate_proposal_pdf
import io

router = APIRouter()


@router.post(
    "/generate-proposal",
    summary="Generate PDF proposal",
    description="""
    Takes the RFP analysis and generates a professionally formatted
    PDF proposal document. Returns the PDF as a file download.
    """,
    response_description="PDF file download"
)
async def generate_proposal(request: ProposalRequest):
    """
    Generate a PDF proposal from RFP analysis data.

    The PDF contains:
    - Client name and date
    - Compatibility score
    - Requirements analysis with met/unmet breakdown
    - Pricing table with base plan and add-ons
    - Next steps section
    """

    print(f"\nGenerating proposal for: {request.analysis.client_name}")

    # ── GENERATE THE PDF ──────────────────────────────────────────────────────
    try:
        # Convert Pydantic model to dict for Member 3's function
        # .dict() converts nested Pydantic models to plain dicts too
        analysis_dict = request.analysis.dict()

        pdf_bytes = generate_proposal_pdf(
            analysis=analysis_dict,
            rfp_text=request.rfp_text
        )

    except Exception as e:
        print(f"PDF generation error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate PDF proposal: {str(e)}"
        )

    # Verify we got actual PDF bytes back
    if not pdf_bytes or len(pdf_bytes) < 100:
        raise HTTPException(
            status_code=500,
            detail="PDF generation produced empty output. Please try again."
        )

    print(f"PDF generated: {len(pdf_bytes):,} bytes")

    # ── RETURN AS FILE DOWNLOAD ───────────────────────────────────────────────
    # Create a safe filename from the client name
    # Replace spaces and special characters with underscores
    import re
    safe_name = re.sub(r'[^a-zA-Z0-9]', '_', request.analysis.client_name)
    safe_name = re.sub(r'_+', '_', safe_name).strip('_')
    filename = f"CloudMatrix_Proposal_{safe_name}.pdf"

    # StreamingResponse sends the bytes as a file download
    # The Content-Disposition header tells the browser to download it
    return StreamingResponse(
        io.BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename={filename}",
            "Content-Length": str(len(pdf_bytes))
        }
    )