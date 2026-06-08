# rag/ingest.py

# These are the libraries we need
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import os


def build_vector_store(
    docs_path: str = "company_docs",
    save_path: str = "vector_store"
):
    """
    This function:
    1. Loads all .txt files from company_docs/
    2. Splits them into 500-character chunks
    3. Converts each chunk to a vector (embedding)
    4. Saves all vectors to a FAISS index on disk

    You only need to run this once, or when you update company docs.
    """

    # ── STEP 1: LOAD DOCUMENTS ──────────────────────────────────────────────
    # DirectoryLoader scans the folder and loads every .txt file
    # loader_cls=TextLoader tells it to treat files as plain text
    print("Step 1: Loading company documents...")

    loader = DirectoryLoader(
        docs_path,
        glob="*.txt",        # only load .txt files
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"}
    )

    documents = loader.load()
    print(f"  Loaded {len(documents)} documents")

    # Each document has two parts:
    # - document.page_content → the actual text
    # - document.metadata     → info like the filename
    for doc in documents:
        print(f"  - {doc.metadata['source']} ({len(doc.page_content)} characters)")


    # ── STEP 2: SPLIT INTO CHUNKS ────────────────────────────────────────────
    # We split each document into smaller pieces for better search accuracy
    # chunk_size=500    → each piece is max 500 characters
    # chunk_overlap=50  → 50 characters are repeated between chunks
    #                     so context isn't lost at the boundary between chunks
    print("\nStep 2: Splitting documents into chunks...")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        length_function=len,       # measure length in characters
        separators=["\n\n", "\n", " ", ""]  # prefer splitting at paragraphs
    )

    chunks = splitter.split_documents(documents)
    print(f"  Created {len(chunks)} chunks")
    if not chunks:
        print("\n⚠️  No chunks created — make sure company_docs/ contains .txt files.")
        return None
    avg = sum(len(c.page_content) for c in chunks) // len(chunks)
    print(f"  Average chunk size: {avg} characters")


    # ── STEP 3: CREATE EMBEDDINGS ────────────────────────────────────────────
    # Embeddings convert text to vectors (lists of numbers)
    # Similar text → similar vectors → similar search results
    # We use HuggingFace's free model that runs locally (no API key needed)
    print("\nStep 3: Loading embedding model (downloads once, ~90MB)...")

    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2",
        # This model is:
        # - Free and open source
        # - Runs on your CPU (no GPU needed)
        # - Downloads automatically the first time
        # - Fast enough for development
    )
    print("  Embedding model ready")


    # ── STEP 4: BUILD AND SAVE FAISS INDEX ───────────────────────────────────
    # FAISS takes all chunks, embeds them, and builds a searchable index
    # This is the "database" that gets searched at query time
    print("\nStep 4: Building FAISS vector store...")
    print("  (This may take 1–2 minutes on first run)")

    vector_store = FAISS.from_documents(
        documents=chunks,
        embedding=embeddings
    )

    # Save to disk so we don't rebuild every time the server starts
    vector_store.save_local(save_path)
    print(f"  Vector store saved to '{save_path}/'")
    print(f"\n✅ Ingestion complete! {len(chunks)} chunks indexed and ready to search.")

    return vector_store


def load_vector_store(save_path: str = "vector_store") -> FAISS:
    """
    Load an already-built vector store from disk.
    Called every time a query is made — much faster than rebuilding.
    """
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    vector_store = FAISS.load_local(
        save_path,
        embeddings,
        allow_dangerous_deserialization=True
        # This flag is required by newer FAISS versions for security reasons
        # It's safe here because we built the index ourselves
    )
    return vector_store


# This block only runs when you execute: python rag/ingest.py
# It does NOT run when another file imports from this module
if __name__ == "__main__":
    build_vector_store()
