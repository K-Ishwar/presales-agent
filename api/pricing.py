# api/pricing.py
# Rule-based pricing engine
# Calculates recommended tier and total price from requirements
# Pure Python — no AI, no external libraries
# This makes pricing auditable and predictable

from typing import List


# ── PRICING CONSTANTS ─────────────────────────────────────────────────────────
TIERS = {
    "Starter": {
        "price": 2000.0,
        "description": "Up to 1,000 users, 99.9% uptime, email support"
    },
    "Business": {
        "price": 8000.0,
        "description": "Up to 10,000 users, 99.95% uptime, priority support"
    },
    "Enterprise": {
        "price": 25000.0,
        "description": "Unlimited users, 99.99% uptime, dedicated engineer"
    }
}

ADDONS = {
    "training": {
        "name": "Training and Onboarding Package",
        "price": 3000.0,
        "keywords": ["training", "onboarding", "staff training", "employee training"]
    },
    "premium_sla": {
        "name": "Premium SLA Upgrade",
        "price": 2000.0,
        "keywords": ["premium sla", "1-hour response", "guaranteed response"]
    },
    "custom_connector": {
        "name": "Custom Connector Development",
        "price": 500.0,
        "keywords": ["custom connector", "custom integration", "bespoke integration"]
    },
    "account_manager": {
        "name": "Dedicated Account Manager",
        "price": 1500.0,
        "keywords": ["account manager", "dedicated manager", "relationship manager"]
    }
}


def calculate_price(requirements: List[str]) -> dict:
    """
    Calculate pricing based on extracted requirements.

    The logic:
    1. Convert all requirements to lowercase for matching
    2. Check for Enterprise-tier triggers (HIPAA, on-premise, 99.99%, unlimited)
    3. If not Enterprise, check for Business-tier triggers (SOC2, 10k+ users)
    4. If neither, recommend Starter
    5. Check for any add-ons that apply
    6. Sum everything up

    Parameters:
        requirements: List of requirement strings from RFP

    Returns:
        dict with tier, base_price, addons list, and total
    """

    # Join all requirements into one lowercase string for easy keyword search
    req_text = " ".join(requirements).lower()

    # ── DETERMINE TIER ────────────────────────────────────────────────────────

    # Enterprise triggers — any one of these means Enterprise tier
    enterprise_triggers = [
        "hipaa",                  # HIPAA compliance requires Enterprise
        "on-premise",             # On-premise deployment requires Enterprise
        "on premise",
        "unlimited users",
        "500,000",                # User counts requiring Enterprise scale
        "100,000",
        "50,000 users",
        "dedicated support",      # Dedicated engineer requires Enterprise
        "dedicated engineer",
        "99.99%",                 # 4 nines uptime requires Enterprise
        "custom sla",
        "data residency",
        "pci-dss",
        "iso 27001"
    ]

    # Business triggers — any one of these means Business tier minimum
    business_triggers = [
        "soc2",                   # SOC2 requires Business or above
        "soc 2",
        "10,000 users",
        "5,000 users",
        "gdpr",                   # GDPR requires Business or above
        "priority support",
        "24/7 support",
        "salesforce",             # Native Salesforce requires Business+
        "99.95%",
        "real-time streaming",
        "real time streaming"
    ]

    # Check from most expensive down
    if any(trigger in req_text for trigger in enterprise_triggers):
        tier = "Enterprise"
    elif any(trigger in req_text for trigger in business_triggers):
        tier = "Business"
    else:
        tier = "Starter"

    base_price = TIERS[tier]["price"]

    # ── DETERMINE ADD-ONS ─────────────────────────────────────────────────────
    applicable_addons = []

    for addon_key, addon_info in ADDONS.items():
        # Check if any keyword for this add-on appears in requirements
        if any(keyword in req_text for keyword in addon_info["keywords"]):
            applicable_addons.append({
                "name": addon_info["name"],
                "price": addon_info["price"]
            })

    # ── CALCULATE TOTAL ────────────────────────────────────────────────────────
    addon_total = sum(addon["price"] for addon in applicable_addons)
    total = base_price + addon_total

    return {
        "tier": tier,
        "base_price": base_price,
        "addons": applicable_addons,
        "total": total
    }


# Test — run with: python api/pricing.py
if __name__ == "__main__":

    test_cases = [
        {
            "name": "Simple client",
            "requirements": ["GDPR compliance", "REST API", "email support"],
            "expected_tier": "Business"
        },
        {
            "name": "Enterprise client",
            "requirements": [
                "HIPAA compliance", "99.99% uptime", "Salesforce integration",
                "dedicated support engineer", "training for 200 staff",
                "on-premise deployment"
            ],
            "expected_tier": "Enterprise"
        },
        {
            "name": "Starter client",
            "requirements": ["Basic data pipeline", "500 users", "standard support"],
            "expected_tier": "Starter"
        }
    ]

    for test in test_cases:
        print(f"\nTest: {test['name']}")
        result = calculate_price(test["requirements"])
        status = "✅" if result["tier"] == test["expected_tier"] else "❌"
        print(f"{status} Tier: {result['tier']} (expected {test['expected_tier']})")
        print(f"   Base: ${result['base_price']:,.0f}/month")
        for addon in result["addons"]:
            print(f"   + {addon['name']}: ${addon['price']:,.0f}/month")
        print(f"   Total: ${result['total']:,.0f}/month")