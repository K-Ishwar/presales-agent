# rag/__init__.py
# STUB — Member 1 will replace this with the real RAG implementation
# This stub exists so Member 2 can build and test the backend
# without waiting for the RAG module to be complete.
# The function signature and return structure MUST match exactly
# what Member 1's real implementation returns.


def analyze_rfp(rfp_text: str) -> dict:
    """
    STUB implementation of analyze_rfp.
    Returns hardcoded fake data for backend development and testing.

    Real implementation: rag/query_engine.py (Member 1)

    Parameters:
        rfp_text: Full text extracted from the client's RFP PDF

    Returns:
        dict with exactly these keys — Member 1's real function
        must return a dict with this exact same structure:
        - client_name          (str)
        - requirements_extracted  (list of str)
        - can_meet             (list of str)
        - cannot_meet          (list of str)
        - recommended_tier     (str: "Starter", "Business", or "Enterprise")
        - base_price           (float)
        - addons               (list of dicts, each with "name" and "price")
        - total_monthly_price  (float)
        - compatibility_score  (int, 0-100)
        - summary              (str)
    """
    print(f"[STUB] analyze_rfp called with {len(rfp_text)} characters of text")

    # Extract a fake client name from the first 200 characters
    # just to make stubs slightly dynamic during testing
    preview = rfp_text[:200].lower()
    if "bank" in preview:
        client = "GlobalBank Corp"
    elif "retail" in preview:
        client = "RetailX"
    elif "health" in preview or "medical" in preview:
        client = "MediCare Plus"
    else:
        client = "Test Client Inc"

    return {
        "client_name": client,
        "requirements_extracted": [
            "99.99% uptime SLA",
            "SOC2 Type II compliance",
            "Salesforce CRM integration",
            "Real-time event streaming",
            "50,000 concurrent users",
            "Dedicated support engineer"
        ],
        "can_meet": [
            "99.99% uptime SLA",
            "SOC2 Type II compliance",
            "Salesforce CRM integration",
            "Real-time event streaming",
            "50,000 concurrent users"
        ],
        "cannot_meet": [
            "Dedicated support engineer"
        ],
        "recommended_tier": "Enterprise",
        "base_price": 25000.0,
        "addons": [
            {"name": "Training and Onboarding", "price": 3000.0},
            {"name": "Premium SLA Upgrade", "price": 2000.0}
        ],
        "total_monthly_price": 30000.0,
        "compatibility_score": 83,
        "summary": (
            "STUB RESPONSE — CloudMatrix Enterprise is a strong fit. "
            "This is placeholder text that Member 1's real implementation "
            "will replace with an actual AI-generated analysis."
        )
    }