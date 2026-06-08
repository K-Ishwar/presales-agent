# api/routes/email.py
# POST /api/draft-email
# Takes RFP analysis, calls Claude to generate a personalized
# sales email, returns subject and body

from fastapi import APIRouter, HTTPException
from api.models import EmailRequest, EmailResponse
from google import genai
import os
import json
import time
from dotenv import load_dotenv

load_dotenv()
router = APIRouter()


@router.post(
    "/draft-email",
    response_model=EmailResponse,
    summary="Draft personalized sales email",
    description="""
    Takes the RFP analysis and generates a highly personalized
    sales email for the human sales rep to review and send.
    The email references specific client requirements and
    recommends the appropriate solution.
    """
)
async def draft_email(request: EmailRequest):
    """
    Generate a personalized sales email using Gemini AI.
    """

    print(f"\nDrafting email for: {request.analysis.client_name}")
    a = request.analysis  # shorthand for cleaner code below

    # ── BUILD THE PROMPT ──────────────────────────────────────────────────────
    met_count = len(a.can_meet)
    total_count = len(a.requirements_extracted)
    unmet_count = len(a.cannot_meet)

    # Format add-ons for the prompt
    addons_text = ""
    if a.addons:
        addon_lines = [f"  - {addon.name}: ${addon.price:,.0f}/month" for addon in a.addons]
        addons_text = "Recommended add-ons:\n" + "\n".join(addon_lines)

    # Format unmet requirements for honest mention
    unmet_text = ""
    if a.cannot_meet:
        unmet_text = f"Requirements we cannot currently meet: {', '.join(a.cannot_meet[:2])}"

    prompt = f"""You are a senior B2B sales representative at CloudMatrix,
an enterprise data pipeline company. You are writing a follow-up email
to a potential client who submitted an RFP.

CLIENT DETAILS:
- Company name: {a.client_name}
- Their key requirements: {', '.join(a.requirements_extracted[:4])}
- Requirements we can meet: {met_count} out of {total_count}
- Recommended plan: CloudMatrix Pro {a.recommended_tier}
- Total monthly investment: ${a.total_monthly_price:,.0f}
{addons_text}
{unmet_text}

YOUR TASK:
Write a professional, personalized sales email that:
1. Opens by referencing {a.client_name} specifically (not a generic greeting)
2. Demonstrates you read their RFP by mentioning 2-3 specific requirements
3. Clearly states we can meet {met_count} of their {total_count} requirements
4. Recommends the {a.recommended_tier} plan at ${a.total_monthly_price:,.0f}/month
5. If there are unmet requirements, acknowledges them honestly and briefly
6. Has a clear single call-to-action (schedule a 30-minute demo call)
7. Is signed by: {request.sales_rep_name}
8. Sounds human and conversational — NOT like a template or robot
9. Is 150-200 words (concise but complete)
10. Does not include any placeholder text like [Company Name] or [Date]

IMPORTANT:
- Use the actual company name {a.client_name} throughout
- Reference their actual requirements, not generic ones
- Be confident but not pushy
- Do not use bullet points in the email body

Respond ONLY with valid JSON in exactly this format.
No explanation before or after. No markdown. Start with {{:
{{
  "subject": "compelling subject line under 10 words",
  "body": "full email body with actual newlines as \\n"
}}"""

    # ── CALL GEMINI API ───────────────────────────────────────────────────────
    try:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY is not set in .env")

        client = genai.Client(api_key=api_key)

        # Retry up to 3 times on 503 (server overload) with backoff
        last_error = None
        for attempt in range(1, 4):
            try:
                response = client.models.generate_content(
                    model='gemini-3.1-flash-lite',
                    contents=prompt,
                    config=genai.types.GenerateContentConfig(
                        temperature=0.2,
                    ),
                )
                break  # success — exit retry loop
            except Exception as e:
                last_error = e
                if "503" in str(e) or "UNAVAILABLE" in str(e):
                    wait = attempt * 15  # 15s, 30s, 45s
                    print(f"Gemini overloaded (attempt {attempt}/3), retrying in {wait}s...")
                    time.sleep(wait)
                else:
                    raise  # non-503 error, re-raise immediately
        else:
            raise last_error or RuntimeError("All Gemini API retries exhausted")

        raw_response = response.text or ""
        print(f"Gemini responded ({len(raw_response)} chars)")

    except Exception as e:
        err_msg = str(e).lower()
        if "api key" in err_msg or "authentication" in err_msg or "invalid" in err_msg:
            raise HTTPException(
                status_code=500,
                detail="Invalid API key. Check your GEMINI_API_KEY in .env"
            )
        elif "quota" in err_msg or "rate limit" in err_msg:
            raise HTTPException(
                status_code=429,
                detail="AI service rate limit reached. Please wait a moment and try again."
            )
        raise HTTPException(
            status_code=500,
            detail=f"AI service error: {str(e)}"
        )

    # ── PARSE THE RESPONSE ────────────────────────────────────────────────────
    try:
        cleaned = raw_response.strip()
        if cleaned.startswith("```json"):
            cleaned = cleaned[7:]
        if cleaned.startswith("```"):
            cleaned = cleaned[3:]
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]
        cleaned = cleaned.strip()

        result = json.loads(cleaned)

        # Verify required keys exist
        if "subject" not in result or "body" not in result:
            raise ValueError("Response missing 'subject' or 'body' field")

        # Verify content is not empty
        if not result["subject"].strip() or not result["body"].strip():
            raise ValueError("Subject or body is empty")

    except (json.JSONDecodeError, ValueError) as e:
        print(f"Parse error: {e}")
        print(f"Raw response: {raw_response[:300]}")
        raise HTTPException(
            status_code=500,
            detail="Failed to parse AI response. Please try again."
        )

    print(f"Email drafted: '{result['subject']}'")

    return EmailResponse(
        subject=result["subject"],
        body=result["body"]
    )