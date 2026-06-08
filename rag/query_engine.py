# rag/query_engine.py

import os
import sys
from pathlib import Path
import json
from google import genai
from dotenv import load_dotenv

# Add project root to sys.path so we can import the rag package
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))
from rag.ingest import load_vector_store

load_dotenv()


def retrieve_relevant_context(query: str, k: int = 5) -> str:
    """
    Search the vector store for content relevant to the query.

    Parameters:
        query: The text to search for (usually the RFP text)
        k:     How many chunks to retrieve (5 is a good default)

    Returns:
        A single string with all retrieved chunks joined together,
        ready to be put into a prompt.
    """

    # Load the vector store from disk
    vector_store = load_vector_store()

    # Search for k most similar chunks
    # similarity_search returns Document objects sorted by relevance
    results = vector_store.similarity_search(query, k=k)

    # Join all chunks into one string with separators
    # This becomes the "context" section of our Claude prompt
    context_parts = []
    for i, doc in enumerate(results):
        source = doc.metadata.get("source", "unknown")
        context_parts.append(
            f"[Source: {source}]\n{doc.page_content}"
        )

    return "\n\n---\n\n".join(context_parts)


def analyze_rfp(rfp_text: str) -> dict:
    """
    Full RAG pipeline:
    1. Retrieve relevant company doc chunks for this RFP
    2. Build a prompt combining retrieved context + RFP text
    3. Call Gemini API
    4. Parse and return JSON response as Python dict
    """
    # ── STEP 1: RETRIEVE RELEVANT CONTEXT ────────────────────────────────────
    print("Retrieving relevant company documentation...")
    context = retrieve_relevant_context(rfp_text, k=6)

    # ── STEP 2: BUILD THE PROMPT ──────────────────────────────────────────────
    prompt = f"""You are a senior Pre-Sales Engineer at CloudMatrix, a B2B SaaS company.

A potential client has submitted a Request for Proposal (RFP). Your job is to:
1. Carefully read the entire RFP and extract every specific requirement
2. Cross-reference each requirement against the CloudMatrix documentation provided
3. Determine which requirements CloudMatrix CAN meet and which it CANNOT
4. Recommend the most appropriate pricing tier
5. Calculate the total monthly price including relevant add-ons
6. Give an honest compatibility score from 0 to 100

CLOUDMATRIX PRODUCT DOCUMENTATION:
{context}

CLIENT RFP DOCUMENT:
{rfp_text}

INSTRUCTIONS FOR YOUR RESPONSE:
- Extract ALL requirements from the RFP, even minor ones
- Be honest — if a requirement is not in the documentation, put it in cannot_meet
- Do not invent capabilities that are not in the documentation
- Base pricing recommendations ONLY on the pricing information provided
- The compatibility_score should reflect what percentage of requirements you can meet
- The summary should be 2-3 sentences explaining the fit and any important gaps

Respond ONLY with a valid JSON object. No explanation before or after.
No markdown code fences. Start your response with {{ and end with }}.

Use exactly this structure:
{{
  "client_name": "extract from RFP or use Unknown Client if not mentioned",
  "requirements_extracted": ["requirement 1", "requirement 2", "requirement 3"],
  "can_meet": ["requirement 1", "requirement 2"],
  "cannot_meet": ["requirement 3"],
  "recommended_tier": "Starter or Business or Enterprise",
  "base_price": 25000,
  "addons": [
    {{"name": "Training and Onboarding", "price": 3000}},
    {{"name": "Custom Connector", "price": 500}}
  ],
  "total_monthly_price": 28500,
  "compatibility_score": 85,
  "summary": "Two to three sentence summary of fit and any important gaps."
}}"""

    # ── STEP 3: CALL GEMINI API ───────────────────────────────────────────────
    print("Calling Gemini API for analysis...")

    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    # Retry up to 3 times on 503 (server overload) with backoff
    import time as _time
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
                _time.sleep(wait)
            else:
                raise  # non-503 error, re-raise immediately
    else:
        raise last_error or RuntimeError("All Gemini API retries exhausted")  # all retries exhausted

    raw_response = response.text or ""
    print(f"Gemini responded ({len(raw_response)} characters)")

    # ── STEP 4: PARSE THE RESPONSE ────────────────────────────────────────────
    result = parse_llm_response(raw_response)

    # ── STEP 5: CALCULATE PRICING VIA PRICING ENGINE ─────────────────────────
    # We use the rule-based pricing engine to ensure pricing is deterministic,
    # compliant with business rules, and never $0.
    try:
        from api.pricing import calculate_price
        reqs = result.get("requirements_extracted", [])
        pricing_result = calculate_price(reqs)
        
        result["recommended_tier"] = pricing_result["tier"]
        result["base_price"] = pricing_result["base_price"]
        result["addons"] = pricing_result["addons"]
        result["total_monthly_price"] = pricing_result["total"]
        print(f"Pricing calculated via engine: {pricing_result['tier']} - Total: ${pricing_result['total']:,.0f}")
    except Exception as pricing_err:
        print(f"Warning: Rule-based pricing calculation failed ({pricing_err}). Keeping LLM pricing.")

    return result


def parse_llm_response(raw: str) -> dict:
    """
    Safely parse LLM text response into a Python dict.
    Handles edge cases like markdown code fences.
    """
    cleaned = raw.strip()
    if cleaned.startswith("```json"):
        cleaned = cleaned[7:]
    elif cleaned.startswith("```"):
        cleaned = cleaned[3:]
    if cleaned.endswith("```"):
        cleaned = cleaned[:-3]
    cleaned = cleaned.strip()

    try:
        result = json.loads(cleaned)
        
        required_keys = [
            "client_name", "requirements_extracted", "can_meet",
            "cannot_meet", "recommended_tier", "base_price",
            "addons", "total_monthly_price", "compatibility_score", "summary"
        ]
        missing = [k for k in required_keys if k not in result]
        if missing:
            print(f"Warning: Missing keys in response: {missing}")
            for key in missing:
                if key in ["requirements_extracted", "can_meet", "cannot_meet", "addons"]:
                    result[key] = []
                elif key in ["base_price", "total_monthly_price"]:
                    result[key] = 0
                elif key == "compatibility_score":
                    result[key] = 50
                else:
                    result[key] = "Unknown"
        return result
    except json.JSONDecodeError as e:
        print(f"JSON parse failed: {e}")
        print(f"Raw response was:\n{raw[:500]}")
        return {
            "client_name": "Unknown Client",
            "requirements_extracted": ["Could not parse requirements from RFP"],
            "can_meet": [],
            "cannot_meet": ["Analysis failed — please retry"],
            "recommended_tier": "Business",
            "base_price": 8000,
            "addons": [],
            "total_monthly_price": 8000,
            "compatibility_score": 0,
            "summary": "The AI analysis could not be completed. Please try uploading the RFP again."
        }


if __name__ == "__main__":
    # ── TEST 1: Simple RFP ──
    print("\n" + "="*60)
    print("TEST 1: Simple RFP")
    print("="*60)
    simple_rfp = """
    Company: RetailX
    We are a small e-commerce company with around 500 users.
    We need a data pipeline solution with basic GDPR compliance.
    We need REST API access and email support.
    Our budget is around $5,000 per month.
    """
    result1 = analyze_rfp(simple_rfp)
    print(json.dumps(result1, indent=2))

    import time
    print("\n[WAITING] 5 seconds to avoid API rate limits...")
    time.sleep(5)

    # ── TEST 2: Complex RFP ──────────
    print("\n" + "="*60)
    print("TEST 2: Complex Enterprise RFP")
    print("="*60)
    complex_rfp = """
    Company: GlobalBank Corp
    Industry: Financial Services

    We require a data pipeline solution for 50,000 concurrent users.
    Our requirements:
    1. SOC2 Type II compliance is mandatory
    2. HIPAA compliance required for certain data types
    3. 99.99% uptime SLA is non-negotiable
    4. Native Salesforce CRM integration required
    5. Real-time event streaming for transaction processing
    6. API response time must be under 200ms at p99
    7. Dedicated support engineer required
    8. Staff training and onboarding for 200 employees
    9. On-premise deployment option required
    Decision Timeline: 30 days. Budget is flexible for the right solution.
    """
    result2 = analyze_rfp(complex_rfp)
    print(json.dumps(result2, indent=2))

    print("\n[WAITING] 5 seconds to avoid API rate limits...")
    time.sleep(5)

    # ── TEST 3: Edge case RFP ─────────
    print("\n" + "="*60)
    print("TEST 3: Edge Case RFP with Impossible Requirements")
    print("="*60)
    edge_rfp = """
    Company: CryptoVentures Inc
    We need a platform for 200 users.
    Requirements:
    1. Blockchain audit trail for all transactions
    2. Quantum encryption for data security
    3. SOC2 compliance
    4. Basic REST API access
    5. Email support acceptable
    """
    result3 = analyze_rfp(edge_rfp)
    print(json.dumps(result3, indent=2))

    print("\n" + "="*60)
    print("[PASS] All 3 tests complete")
    print("="*60)