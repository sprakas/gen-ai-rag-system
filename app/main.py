from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.services.rag_service import RAGService
from app.services.vector_store import VectorStore
from app.ingestion.pipeline import load_all_docs
from app.ingestion.chunking import split_docs

rag: RAGService = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global rag
    # Create a single VectorStore, index documents into it, then pass to RAGService
    vs = VectorStore()
    docs = load_all_docs()
    if docs:
        chunks = split_docs(docs)
        texts = [doc.page_content for doc in chunks]
        metadatas = [doc.metadata for doc in chunks]
        vs.add_documents(texts, metadatas=metadatas)
        print(f"✅ Indexed {len(chunks)} chunks into vector store")
    else:
        print("⚠️  No documents found in data/pdfs or data/docs")
    rag = RAGService(vector_store=vs)
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/ask")
def ask(q: str):
    return {"answer": rag.generate(q)}