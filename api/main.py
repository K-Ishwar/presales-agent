# api/main.py
# The FastAPI application entry point
# Connects all route files and configures middleware

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import rfp, proposal, email
from api.models import HealthResponse

# Create the FastAPI application instance
app = FastAPI(
    title="Pre-Sales Engineer Agent API",
    description="""
    AI-powered B2B pre-sales automation system.

    ## What This API Does
    1. **Upload RFP** — Upload a client's PDF, get structured analysis
    2. **Generate Proposal** — Convert analysis to a professional PDF
    3. **Draft Email** — Generate a personalized sales email

    ## How To Use
    1. POST /api/upload-rfp with a PDF file
    2. Use the returned analysis JSON in the next two calls
    3. POST /api/generate-proposal to get a downloadable PDF
    4. POST /api/draft-email to get a personalized email

    ## Built By
    Team: [Your Team Name] | Hackathon 2026
    """,
    version="1.0.0",
    docs_url="/docs",        # Interactive API docs
    redoc_url="/redoc"       # Alternative docs format
)

# ── CORS MIDDLEWARE ───────────────────────────────────────────────────────────
# CORS (Cross-Origin Resource Sharing) allows the React frontend
# running on localhost:3000 to make requests to this API on localhost:8000.
# Without this, browsers block cross-origin requests for security.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",    # React dev server
        "http://127.0.0.1:3000",   # Alternative localhost format
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# ── REGISTER ROUTES ───────────────────────────────────────────────────────────
# Each router handles a group of related endpoints
# prefix="/api" means all routes become /api/upload-rfp, /api/generate-proposal etc
app.include_router(
    rfp.router,
    prefix="/api",
    tags=["RFP Analysis"]           # Groups endpoints in /docs
)

app.include_router(
    proposal.router,
    prefix="/api",
    tags=["Proposal Generation"]
)

app.include_router(
    email.router,
    prefix="/api",
    tags=["Email Drafting"]
)


# ── HEALTH CHECK ──────────────────────────────────────────────────────────────
@app.get(
    "/health",
    response_model=HealthResponse,
    tags=["System"],
    summary="Check if the API is running"
)
def health_check():
    """
    Simple health check endpoint.
    Returns 200 OK if the server is running.
    Used by the frontend to verify backend connectivity.
    """
    return HealthResponse(
        status="ok",
        message="Pre-Sales Engineer Agent is running",
        version="1.0.0"
    )


# ── STARTUP EVENT ──────────────────────────────────────────────────────────────
@app.on_event("startup")
async def startup_event():
    """Runs when the server starts up."""
    print("\n" + "="*50)
    print("Pre-Sales Engineer Agent API")
    print("="*50)
    print("Status: Running")
    print("Docs:   http://localhost:8000/docs")
    print("Health: http://localhost:8000/health")
    print("="*50 + "\n")