# rag/test_search.py
# Run this to verify your vector store searches correctly
# python rag/test_search.py

import sys
from pathlib import Path

# Add project root to sys.path so we can import the rag package
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from rag.ingest import load_vector_store

def test_search(query: str, expected_keyword: str, k: int = 3):
    """Search and check if expected keyword appears in results."""
    print(f"\n{'='*60}")
    print(f"QUERY: '{query}'")
    print(f"{'='*60}")

    store = load_vector_store()
    results = store.similarity_search(query, k=k)

    found_keyword = False
    for i, doc in enumerate(results):
        print(f"\nResult {i+1} (from {doc.metadata.get('source', 'unknown')}):")
        print(f"  {doc.page_content[:200]}...")
        if expected_keyword.lower() in doc.page_content.lower():
            found_keyword = True

    if found_keyword:
        print(f"\n[PASS] — '{expected_keyword}' found in results")
    else:
        print(f"\n[FAIL] — '{expected_keyword}' NOT found in results")
        print(f"   Consider adding more content about this to company docs")

    return found_keyword


if __name__ == "__main__":
    print("Testing search quality...")

    # Test 1: Compliance queries
    test_search(
        query="Does your product support SOC2 compliance?",
        expected_keyword="SOC2"
    )

    # Test 2: Pricing queries
    test_search(
        query="How much does the Enterprise plan cost?",
        expected_keyword="25,000"
    )

    # Test 3: Scale queries
    test_search(
        query="How many users can the system support?",
        expected_keyword="500,000"
    )

    # Test 4: Integration queries
    test_search(
        query="Do you integrate with Salesforce?",
        expected_keyword="Salesforce"
    )

    # Test 5: HIPAA queries
    test_search(
        query="Is your product HIPAA compliant?",
        expected_keyword="HIPAA"
    )

    # Test 6: Something you CAN'T do
    test_search(
        query="Do you support blockchain integration?",
        expected_keyword="Blockchain"
    )