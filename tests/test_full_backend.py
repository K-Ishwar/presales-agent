# tests/test_full_backend.py
# Complete end-to-end backend test
# Run with: python tests/test_full_backend.py
# (Backend must be running: python run.py)

import requests
import json
import os
import sys

BASE_URL = "http://localhost:8000"
PASSED = []
FAILED = []


def run_test(name: str, test_fn):
    """Run a single test and track results."""
    try:
        result = test_fn()
        PASSED.append(name)
        return result
    except AssertionError as e:
        FAILED.append((name, str(e)))
        print(f"❌ FAILED — {name}: {e}")
        return None
    except Exception as e:
        FAILED.append((name, str(e)))
        print(f"❌ ERROR  — {name}: {type(e).__name__}: {e}")
        return None


def test_01_health():
    r = requests.get(f"{BASE_URL}/health", timeout=5)
    assert r.status_code == 200, f"Status {r.status_code}"
    data = r.json()
    assert data["status"] == "ok"
    print(f"✅ Health check OK — version {data.get('version', 'unknown')}")
    return data


def test_02_upload_valid_pdf():
    if not os.path.exists("test_rfp_simple.pdf"):
        print("   ⚠️  Skipped — test_rfp_simple.pdf not found")
        print("   Run: python create_test_rfp.py")
        return None

    with open("test_rfp_simple.pdf", "rb") as f:
        r = requests.post(
            f"{BASE_URL}/api/upload-rfp",
            files={"file": ("test.pdf", f, "application/pdf")},
            timeout=60
        )

    assert r.status_code == 200, f"Status {r.status_code}: {r.text[:200]}"
    data = r.json()

    required = ["client_name", "requirements_extracted", "can_meet",
                "cannot_meet", "recommended_tier", "base_price",
                "addons", "total_monthly_price", "compatibility_score", "summary"]
    for field in required:
        assert field in data, f"Missing field: {field}"

    assert isinstance(data["compatibility_score"], int)
    assert 0 <= data["compatibility_score"] <= 100
    assert data["total_monthly_price"] > 0
    assert len(data["client_name"]) > 0

    print(f"✅ Upload RFP — {data['client_name']} | {data['recommended_tier']} | ${data['total_monthly_price']:,.0f}/mo | {data['compatibility_score']}%")
    return data


def test_03_upload_wrong_type():
    r = requests.post(
        f"{BASE_URL}/api/upload-rfp",
        files={"file": ("photo.jpg", b"fake", "image/jpeg")},
        timeout=10
    )
    assert r.status_code == 400, f"Expected 400, got {r.status_code}"
    print(f"✅ Wrong file type rejected — {r.json()['detail'][:50]}")


def test_04_upload_empty_file():
    r = requests.post(
        f"{BASE_URL}/api/upload-rfp",
        files={"file": ("empty.pdf", b"", "application/pdf")},
        timeout=10
    )
    assert r.status_code == 400, f"Expected 400, got {r.status_code}"
    print(f"✅ Empty file rejected — {r.json()['detail'][:50]}")


def test_05_generate_proposal(analysis: dict):
    if not analysis:
        print("   ⚠️  Skipped — no analysis data")
        return None

    r = requests.post(
        f"{BASE_URL}/api/generate-proposal",
        json={"analysis": analysis, "rfp_text": "test rfp text"},
        timeout=30
    )
    assert r.status_code == 200, f"Status {r.status_code}: {r.text[:200]}"
    assert "application/pdf" in r.headers.get("content-type", "")
    assert len(r.content) > 500, "PDF too small"

    with open("test_output_proposal.pdf", "wb") as f:
        f.write(r.content)

    print(f"✅ Generate proposal — {len(r.content):,} bytes — saved test_output_proposal.pdf")
    return r.content


def test_06_draft_email(analysis: dict):
    if not analysis:
        print("   ⚠️  Skipped — no analysis data")
        return None

    r = requests.post(
        f"{BASE_URL}/api/draft-email",
        json={"analysis": analysis, "sales_rep_name": "Test Rep"},
        timeout=30
    )
    assert r.status_code == 200, f"Status {r.status_code}: {r.text[:200]}"
    data = r.json()
    assert "subject" in data and len(data["subject"]) > 3
    assert "body" in data and len(data["body"]) > 50

    # Should mention the client name somewhere
    client = analysis.get("client_name", "")
    first_word = client.split()[0].lower() if client else ""
    if first_word:
        assert first_word in data["body"].lower(), \
            f"Email should mention client '{client}'"

    print(f"✅ Draft email — Subject: {data['subject'][:60]}")
    return data


def test_07_generate_proposal_bad_data():
    """Test with missing required fields."""
    r = requests.post(
        f"{BASE_URL}/api/generate-proposal",
        json={"analysis": {"client_name": "Test"}, "rfp_text": ""},
        timeout=10
    )
    assert r.status_code == 422, f"Expected 422, got {r.status_code}"
    print(f"✅ Bad proposal data rejected with 422 validation error")


def print_summary():
    total = len(PASSED) + len(FAILED)
    print(f"\n{'='*50}")
    print(f"TEST RESULTS: {len(PASSED)}/{total} passed")
    print(f"{'='*50}")

    if PASSED:
        print(f"\nPassed ({len(PASSED)}):")
        for name in PASSED:
            print(f"  ✅ {name}")

    if FAILED:
        print(f"\nFailed ({len(FAILED)}):")
        for name, error in FAILED:
            print(f"  ❌ {name}: {error}")

    if not FAILED:
        print("\n🎉 All tests passed! Backend is ready for integration.")
    else:
        print(f"\n⚠️  Fix {len(FAILED)} failing test(s) before integration week.")

    print(f"{'='*50}\n")


if __name__ == "__main__":
    print("Pre-Sales Agent — Full Backend Test Suite")
    print("Make sure the backend is running: python run.py\n")

    # Check connectivity first
    try:
        requests.get(f"{BASE_URL}/health", timeout=3)
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend at localhost:8000")
        print("   Start it first: python run.py")
        sys.exit(1)

    # Run all tests in order
    run_test("01 Health check", test_01_health)
    analysis = run_test("02 Upload valid PDF", test_02_upload_valid_pdf)
    run_test("03 Upload wrong file type", test_03_upload_wrong_type)
    run_test("04 Upload empty file", test_04_upload_empty_file)
    run_test("05 Generate proposal PDF", lambda: test_05_generate_proposal(analysis))
    run_test("06 Draft sales email", lambda: test_06_draft_email(analysis))
    run_test("07 Bad proposal data rejected", test_07_generate_proposal_bad_data)

    print_summary()