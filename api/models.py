# api/models.py
# Data models for the Pre-Sales Engineer Agent API
# These Pydantic models do three things:
# 1. Validate incoming request data (wrong types = automatic 422 error)
# 2. Validate outgoing response data
# 3. Generate documentation in FastAPI's /docs page automatically

from pydantic import BaseModel, Field
from typing import List, Optional


# ── BUILDING BLOCK MODELS ────────────────────────────────────────────────────
# These are small models used inside larger ones

class Addon(BaseModel):
    """
    Represents a single pricing add-on.
    Example: {"name": "Training Package", "price": 3000.0}
    """
    name: str = Field(
        description="Name of the add-on service",
        example="Training and Onboarding"
    )
    price: float = Field(
        description="Monthly cost of this add-on in USD",
        example=3000.0
    )


# ── MAIN ANALYSIS MODEL ──────────────────────────────────────────────────────
# This is the most important model — it's the output of the entire RAG pipeline
# and the input to both the PDF generator and email drafter

class RFPAnalysis(BaseModel):
    """
    The complete structured analysis of a client's RFP.
    Produced by Member 1's RAG pipeline.
    Used by Member 3's PDF generator and the email drafter.
    """

    client_name: str = Field(
        description="Name of the client company extracted from the RFP",
        example="GlobalBank Corp"
    )

    requirements_extracted: List[str] = Field(
        description="All requirements found in the RFP",
        example=["99.99% uptime", "SOC2 compliance", "Salesforce integration"]
    )

    can_meet: List[str] = Field(
        description="Requirements that CloudMatrix can fully meet",
        example=["99.99% uptime", "SOC2 compliance"]
    )

    cannot_meet: List[str] = Field(
        description="Requirements that CloudMatrix cannot currently meet",
        example=["Blockchain integration"]
    )

    recommended_tier: str = Field(
        description="Recommended pricing tier: Starter, Business, or Enterprise",
        example="Enterprise"
    )

    base_price: float = Field(
        description="Monthly base price for the recommended tier in USD",
        example=25000.0
    )

    addons: List[Addon] = Field(
        default=[],
        description="List of recommended add-ons with their prices",
    )

    total_monthly_price: float = Field(
        description="Total monthly price including base and all add-ons",
        example=28000.0
    )

    compatibility_score: int = Field(
        description="Percentage of requirements CloudMatrix can meet (0-100)",
        example=87,
        ge=0,   # must be >= 0
        le=100  # must be <= 100
    )

    summary: str = Field(
        description="2-3 sentence summary of fit and any important gaps",
        example="CloudMatrix Pro is an excellent fit for GlobalBank Corp..."
    )


# ── REQUEST MODELS ───────────────────────────────────────────────────────────
# These define what the API endpoints ACCEPT as input

class ProposalRequest(BaseModel):
    """
    Request body for POST /api/generate-proposal
    Contains the full analysis + original RFP text
    """
    analysis: RFPAnalysis = Field(
        description="The complete RFP analysis from the upload step"
    )
    rfp_text: str = Field(
        default="",
        description="Original RFP text (used for context in PDF generation)"
    )


class EmailRequest(BaseModel):
    """
    Request body for POST /api/draft-email
    """
    analysis: RFPAnalysis = Field(
        description="The complete RFP analysis from the upload step"
    )
    sales_rep_name: Optional[str] = Field(
        default="the CloudMatrix Sales Team",
        description="Name to sign the email with",
        example="Alex Kumar"
    )


# ── RESPONSE MODELS ──────────────────────────────────────────────────────────
# These define what the API endpoints RETURN

class EmailResponse(BaseModel):
    """
    Response body from POST /api/draft-email
    """
    subject: str = Field(
        description="Email subject line",
        example="CloudMatrix Enterprise — Proposal for GlobalBank Corp"
    )
    body: str = Field(
        description="Full email body text with \\n for line breaks",
        example="Dear GlobalBank Corp team,\n\nThank you for..."
    )


class HealthResponse(BaseModel):
    """Response from GET /health"""
    status: str
    message: str
    version: str