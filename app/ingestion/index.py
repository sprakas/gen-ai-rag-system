from pathlib import Path
import sys

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.services.vector_store import VectorStore
from app.ingestion.pipeline import load_all_docs
from app.ingestion.chunking import split_docs

def run():
    vs = VectorStore()

    docs = load_all_docs()
    chunks = split_docs(docs)

    texts = [doc.page_content for doc in chunks]

    vs.add_documents(texts)

    print("✅ Data indexed in memory")

if __name__ == "__main__":
    run()