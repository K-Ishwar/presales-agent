# tests/test_rfp_route.py
# Run with: python tests/test_rfp_route.py
# (Backend must be running: python run.py)

import requests
import os

BASE_URL = "http://localhost:8000"


def test_health():
    """Basic server connectivity test."""
    r = requests.get(f"{BASE_URL}/health")
    assert r.status_code == 200, f"Expected 200, got {r.status_code}"
    data = r.json()
    assert data["status"] == "ok"
    print(f"[PASS] Health check: {data['message']}")


def test_upload_valid_pdf():
    """Test uploading a valid PDF."""
    pdf_path = "test_rfp_simple.pdf"

    if not os.path.exists(pdf_path):
        print(f"[WARN] {pdf_path} not found — run create_test_rfp.py first")
        return

    with open(pdf_path, "rb") as f:
        r = requests.post(
            f"{BASE_URL}/api/upload-rfp",
            files={"file": ("test_rfp.pdf", f, "application/pdf")}
        )

    assert r.status_code == 200, f"Expected 200, got {r.status_code}: {r.text}"
    data = r.json()

    # Verify all required fields exist
    required_fields = [
        "client_name", "requirements_extracted", "can_meet",
        "cannot_meet", "recommended_tier", "base_price",
        "addons", "total_monthly_price", "compatibility_score", "summary"
    ]
    for field in required_fields:
        assert field in data, f"Missing field: {field}"

    assert 0 <= data["compatibility_score"] <= 100
    assert data["total_monthly_price"] > 0

    print(f"[PASS] Upload RFP:")
    print(f"   Client: {data['client_name']}")
    print(f"   Tier: {data['recommended_tier']}")
    print(f"   Price: ${data['total_monthly_price']:,.0f}/month")
    print(f"   Score: {data['compatibility_score']}%")
    return data


def test_upload_wrong_file_type():
    """Test that non-PDF files are rejected."""
    r = requests.post(
        f"{BASE_URL}/api/upload-rfp",
        files={"file": ("image.jpg", b"fake image content", "image/jpeg")}
    )
    assert r.status_code == 400, f"Expected 400, got {r.status_code}"
    print(f"[PASS] Wrong file type correctly rejected: {r.json()['detail']}")


def test_upload_empty_file():
    """Test that empty files are rejected."""
    r = requests.post(
        f"{BASE_URL}/api/upload-rfp",
        files={"file": ("empty.pdf", b"", "application/pdf")}
    )
    assert r.status_code == 400, f"Expected 400, got {r.status_code}"
    print(f"[PASS] Empty file correctly rejected: {r.json()['detail']}")




def test_generate_proposal(analysis: dict):
    """Test PDF proposal generation."""
    r = requests.post(
        f"{BASE_URL}/api/generate-proposal",
        json={
            "analysis": analysis,
            "rfp_text": "Sample RFP text"
        }
    )
    assert r.status_code == 200, f"Expected 200, got {r.status_code}: {r.text}"
    assert r.headers["content-type"] == "application/pdf"
    assert len(r.content) > 100, "PDF should have actual content"

    # Save to verify it opens correctly
    with open("test_output_proposal.pdf", "wb") as f:
        f.write(r.content)

    print(f"[PASS] Generate proposal:")
    print(f"   PDF size: {len(r.content):,} bytes")
    print(f"   Saved to: test_output_proposal.pdf")
    print(f"   Open this file to verify it looks correct")

def test_draft_email(analysis: dict):
    """Test email drafting."""
    r = requests.post(
        f"{BASE_URL}/api/draft-email",
        json={
            "analysis": analysis,
            "sales_rep_name": "Alex Kumar"
        }
    )
    assert r.status_code == 200, f"Expected 200, got {r.status_code}: {r.text}"
    data = r.json()
    assert "subject" in data and len(data["subject"]) > 5
    assert "body" in data and len(data["body"]) > 50

    # Verify the email actually mentions the client name
    client_name = analysis["client_name"]
    assert client_name.split()[0].lower() in data["body"].lower(), \
        f"Email should mention client name '{client_name}'"

    print(f"[PASS] Draft email:")
    print(f"   Subject: {data['subject']}")
    print(f"   Body preview: {data['body'][:100]}...")
    return data

if __name__ == "__main__":
    print("Testing all endpoints...")
    print("(Make sure backend is running: python run.py)\n")

    try:
        test_health()
        analysis = test_upload_valid_pdf()
        test_upload_wrong_file_type()
        test_upload_empty_file()
        
        if analysis:
            test_generate_proposal(analysis)
            test_draft_email(analysis)
            
        print("\n[SUCCESS] All tests passed!")
    except requests.exceptions.ConnectionError:
        print("[FAIL] Cannot connect to backend.")
        print("   Start it first: python run.py")