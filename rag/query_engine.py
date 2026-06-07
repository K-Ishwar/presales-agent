import os
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from rag.llm import call_llm   # 👈 NEW ADDITION

# Load environment variables
load_dotenv()

VECTOR_STORE_PATH = "vector_store"


# -----------------------------
# LOAD VECTOR STORE
# -----------------------------
def load_vector_store():
    if not os.path.exists(VECTOR_STORE_PATH):
        raise FileNotFoundError(
            "Vector store not found. Run ingest.py first!"
        )

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vector_store = FAISS.load_local(
        VECTOR_STORE_PATH,
        embeddings
    )

    return vector_store


# -----------------------------
# SEARCH FUNCTION
# -----------------------------
def search(query, vector_store, k=3):
    results = vector_store.similarity_search(query, k=k)
    return results


# -----------------------------
# MAIN RAG + LLM PIPELINE
# -----------------------------
def main():
    print("🔄 Loading vector store...")
    vector_store = load_vector_store()
    print("✅ Vector store loaded successfully!\n")

    print("💬 Ask your questions (type 'exit' to quit)\n")

    while True:
        query = input("You: ")

        if query.lower() == "exit":
            print("👋 Exiting...")
            break

        # Step 1: Retrieve relevant chunks
        docs = search(query, vector_store)

        context = "\n".join([doc.page_content for doc in docs])

        # Step 2: Build prompt for LLM
        prompt = f"""
You are a helpful AI sales assistant.

Use the context below to answer the user query.

CONTEXT:
{context}

QUESTION:
{query}

Give a clear, structured and professional answer.
"""

        # Step 3: Call HuggingFace LLM (from llm.py)
        result = call_llm(prompt)

        print("\n🤖 AI RESPONSE:\n")

        if "answer" in result:
            print(result["answer"])
        else:
            print(result)

        print("\n" + "=" * 50 + "\n")


if __name__ == "__main__":
    main()