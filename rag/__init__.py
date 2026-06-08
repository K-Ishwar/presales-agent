# rag/__init__.py
# This file makes the rag/ folder a Python module
# and exposes the functions that other team members import

from .query_engine import analyze_rfp, retrieve_relevant_context
from .ingest import build_vector_store, load_vector_store

# Other team members use:
# from rag import analyze_rfp