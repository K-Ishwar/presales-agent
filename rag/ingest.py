import os
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

# Path to docs
DOCS_PATH = "company_docs"

# Path to save vector DB
VECTOR_STORE_PATH = "vector_store"


def load_documents():
    documents = []

    for file in os.listdir(DOCS_PATH):
        if file.endswith(".txt"):
            file_path = os.path.join(DOCS_PATH, file)
            loader = TextLoader(file_path, encoding="utf-8")
            documents.extend(loader.load())

    return documents


def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )
    return splitter.split_documents(documents)


def build_vector_store():
    print("Loading documents...")
    documents = load_documents()
    print(f"Loaded {len(documents)} documents")

    print("Splitting documents...")
    chunks = split_documents(documents)
    print(f"Created {len(chunks)} chunks")

    print("Creating embeddings model...")
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    print("Building FAISS vector store...")
    vector_store = FAISS.from_documents(
    chunks,
    embeddings
)

    print("Saving vector store...")
    vector_store.save_local(VECTOR_STORE_PATH)

    print(f"Vector store saved to '{VECTOR_STORE_PATH}'")


def load_vector_store():
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    return FAISS.load_local(
    VECTOR_STORE_PATH,
    embeddings,
    allow_dangerous_deserialization=True,
    embedding_function=embeddings.embed_query
)



if __name__ == "__main__":
    build_vector_store()