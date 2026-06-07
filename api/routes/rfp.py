# api/routes/rfp.py
# POST /api/upload-rfp
# Accepts a PDF file upload, extracts text, runs RAG analysis,
# returns structured RFPAnalysis JSON

from fastapi import APIRouter, UploadFile, File, HTTPException
from api.models import RFPAnalysis
from pdf_parser import extract_text_from_pdf
from rag import analyze_rfp
import json

# APIRouter is like a mini FastAPI app for a group of related endpoints
# The prefix and tags are applied in main.py when this router is included
router = APIRouter()


@router.post(
    "/upload-rfp",
    response_model=RFPAnalysis,
    summary="Upload RFP and get analysis",
    description="""
    Upload a client's RFP PDF file.
    The system will:
    1. Extract all text from the PDF
    2. Search company documentation for relevant information
    3. Use Claude AI to analyse requirements and calculate pricing
    4. Return a structured analysis JSON
    """
)
async def upload_rfp(
    file: UploadFile = File(
        ...,
        description="The client's RFP document in PDF format"
    )
):
    """
    Main RFP upload and analysis endpoint.
    This is the entry point to the entire pre-sales pipeline.
    """

    # ── STEP 1: VALIDATE THE UPLOADED FILE ───────────────────────────────────
    print(f"\n{'='*50}")
    print(f"New RFP upload: {file.filename}")
    print(f"Content type: {file.content_type}")

    # Check file extension
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No filename provided. Please upload a PDF file."
        )

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type '{file.filename}'. Only PDF files are accepted."
        )

    # Check content type (browsers set this automatically)
    valid_content_types = ["application/pdf", "application/octet-stream"]
    if file.content_type and file.content_type not in valid_content_types:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid content type '{file.content_type}'. Please upload a PDF file."
        )


    # ── STEP 2: READ THE FILE BYTES ───────────────────────────────────────────
    try:
        contents = await file.read()
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to read uploaded file: {str(e)}"
        )

    # Check file is not empty
    if len(contents) == 0:
        raise HTTPException(
            status_code=400,
            detail="The uploaded file is empty. Please upload a valid PDF."
        )

    # Check file size (max 20MB)
    max_size = 20 * 1024 * 1024  # 20MB in bytes
    if len(contents) > max_size:
        size_mb = len(contents) / 1024 / 1024
        raise HTTPException(
            status_code=400,
            detail=f"File too large ({size_mb:.1f}MB). Maximum size is 20MB."
        )

    print(f"File size: {len(contents) / 1024:.1f}KB")


    # ── STEP 3: EXTRACT TEXT FROM PDF ────────────────────────────────────────
    print("Extracting text from PDF...")
    try:
        rfp_text = extract_text_from_pdf(contents)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to extract text from PDF: {str(e)}"
        )

    # Check we actually got text
    if not rfp_text or len(rfp_text.strip()) < 50:
        raise HTTPException(
            status_code=422,
            detail=(
                "Could not extract readable text from this PDF. "
                "The file may be a scanned image PDF. "
                "Please ensure the PDF contains selectable text."
            )
        )

    print(f"Extracted {len(rfp_text)} characters of text")
    # Print first 200 characters for debugging during development
    print(f"Preview: {rfp_text[:200].strip()}")


    # ── STEP 4: RUN RAG ANALYSIS ──────────────────────────────────────────────
    print("Running RAG analysis...")
    try:
        analysis_dict = analyze_rfp(rfp_text)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"AI analysis failed: {str(e)}"
        )

    # Verify the returned dict has the required structure
    required_keys = [
        "client_name", "requirements_extracted", "can_meet",
        "cannot_meet", "recommended_tier", "base_price",
        "addons", "total_monthly_price", "compatibility_score", "summary"
    ]
    missing_keys = [k for k in required_keys if k not in analysis_dict]
    if missing_keys:
        raise HTTPException(
            status_code=500,
            detail=f"AI analysis returned incomplete data. Missing fields: {missing_keys}"
        )


    # ── STEP 5: VALIDATE AND RETURN ───────────────────────────────────────────
    try:
        # Pydantic validates the dict against our model
        # If any field has wrong type or value, it raises ValidationError
        analysis = RFPAnalysis(**analysis_dict)
    except Exception as e:
        print(f"Pydantic validation error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Analysis data validation failed: {str(e)}"
        )

    print(f"Analysis complete:")
    print(f"  Client: {analysis.client_name}")
    print(f"  Tier: {analysis.recommended_tier}")
    print(f"  Price: ${analysis.total_monthly_price:,.0f}/month")
    print(f"  Score: {analysis.compatibility_score}%")
    print(f"{'='*50}\n")

    # FastAPI automatically converts the Pydantic model to JSON
    return analysis