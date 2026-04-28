# 🧠 Local RAG System (Docs + PDF Q&A)

A fully **local Retrieval-Augmented Generation (RAG)** system that answers questions from your documents and PDFs using:

* 🧠 Local LLM via Ollama
* 🗄️ In-memory vector database using Qdrant
* ⚡ FastAPI for serving queries

> No external APIs. No cloud dependencies. Fully offline.

---

## 🚀 Features

* 📄 Supports TXT, MD, and PDF ingestion (including nested subfolders)
* ✂️ Automatic document chunking with overlap
* 🔍 Semantic search using embeddings with relevance-score filtering
* 🤖 Local LLM inference via Ollama (`llama3.2:1b`)
* 🧩 Multi-query expansion for improved retrieval recall
* 📎 Source attribution in retrieved context
* 🛡️ Guardrails for prompt injection, sanitization, and output validation
* ⚡ FastAPI-based API with lifespan-based auto-indexing on startup

---

## 🧱 Architecture

```text
Docs/PDFs → Chunk (800 chars, 150 overlap)
          → Embed (nomic-embed-text via Ollama)
          → Qdrant (in-memory vector store)

User Query → Multi-query Expansion (LLM)
           → Retrieve top-8 candidates per variant
           → Score filter (≥ 0.3) + re-rank + top-3
           → Deduplicate + trim context (30k chars max)
           → LLM (llama3.2:1b via Ollama)
           → Output validation
           → Answer
```

---

## 📁 Project Structure

```bash
gen-ai-rag-system/
│
├── app/
│   ├── main.py                  # FastAPI app + lifespan indexing
│   ├── core/
│   │   └── config.py            # Retrieval settings
│   ├── services/
│   │   ├── rag_service.py       # Query expansion, retrieval, generation
│   │   ├── vector_store.py      # Qdrant wrapper with score filtering
│   │   ├── llm.py               # Ollama LLM wrapper
│   │   └── guardrails.py        # Injection detection + sanitization
│   ├── ingestion/
│   │   ├── index.py             # Standalone indexing entry point
│   │   ├── pipeline.py          # Recursive doc/PDF loader
│   │   └── chunking.py          # RecursiveCharacterTextSplitter
│   └── data/
│       ├── docs/                # .txt / .md files (nested folders supported)
│       └── pdfs/                # PDF files (nested folders supported)
│
├── requirements.txt
├── Readme.md
├── RAG_EXPLAINED.md             # Conceptual guide to RAG
└── DEVELOPER_ONBOARDING.md      # Setup and installation guide
```

---

## 🛡️ Guardrails

* **Prompt injection detection** — blocks queries containing known attack patterns
* **Query sanitization** — strips suspicious substrings before retrieval
* **Output validation** — post-processes LLM response before returning

---

## 🔍 Retrieval Pipeline

1. **Multi-query expansion** — the LLM generates 2 alternative phrasings of the query
2. **Over-fetch** — `TOP_K_FETCH=8` candidates are retrieved per query variant
3. **Score filter** — chunks below `SCORE_THRESHOLD=0.3` are dropped
4. **Re-rank** — remaining chunks are sorted by relevance score (highest first)
5. **Deduplicate** — identical chunks from different query variants are merged
6. **Context trimming** — total context is capped at `MAX_CONTEXT_CHARS`
7. **Source attribution** — each chunk is prefixed with its source filename

---

## ⚠️ Limitations

* 🗄️ In-memory Qdrant — data is lost on restart (re-indexed automatically)
* 🧠 Quality depends on the local LLM size (`llama3.2:1b` is fast but limited)
* 📡 Requires Ollama to be running locally

---

## 🔄 Future Improvements

* Persist Qdrant to disk or use Docker-based Qdrant
* Add hybrid search (BM25 keyword + vector)
* Add streaming responses (`/ask/stream`)
* Add evaluation metrics (faithfulness, relevance)
* Upgrade to a larger local LLM for better instruction following

---

## 💡 When to Use This

* You want **fully offline AI** with no cloud dependency
* You need **data privacy** (documents never leave your machine)
* You are **learning RAG architecture** from scratch

---

## 📖 Further Reading

* [RAG_EXPLAINED.md](RAG_EXPLAINED.md) — conceptual deep-dive into how RAG works with examples
* [DEVELOPER_ONBOARDING.md](DEVELOPER_ONBOARDING.md) — setup, installation, and troubleshooting guide

---

## 📄 License

MIT License
