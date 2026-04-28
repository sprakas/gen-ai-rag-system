# 🛠️ Developer Onboarding Guide

Everything you need to get the RAG system running locally from scratch.

---

## Prerequisites

| Tool | Version | Purpose |
|---|---|---|
| Python | 3.10+ | Runtime |
| pip | latest | Package manager |
| [Ollama](https://ollama.com) | latest | Local LLM + embeddings |
| Git | any | Clone the repo |

---

## 1. Clone the Repository

```bash
git clone <repo-url>
cd gen-ai-rag-system
```

---

## 2. Create a Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate        # macOS / Linux
.venv\Scripts\activate           # Windows
```

---

## 3. Install Python Dependencies

```bash
pip install -r requirements.txt
pip install pypdf langchain-ollama langchain-qdrant "unstructured[md]"
```

> If you add new packages, update `requirements.txt`:
> ```bash
> pip freeze > requirements.txt
> ```

---

## 4. Install and Start Ollama

### Install
Download from [https://ollama.com](https://ollama.com) and install for your OS.

### Verify Ollama is running
```bash
ollama list
```

If you get a connection error, start the Ollama service first:
```bash
ollama serve
```

### Pull Required Models

```bash
# LLM for generating answers
ollama pull llama3.2:1b

# Embedding model for vector search
ollama pull nomic-embed-text
```

Verify both are available:
```bash
ollama list
# Should show:
# llama3.2:1b
# nomic-embed-text
```

---

## 5. Add Your Documents

Place files in the `data/` folder. Nested subfolders are supported.

```
app/data/
├── docs/             ← .txt and .md files go here
│   ├── notes.md
│   └── team/
│       └── meeting_april.txt
└── pdfs/             ← PDF files go here
    ├── manual.pdf
    └── reports/
        └── q1.pdf
```

Supported formats: `.txt`, `.md`, `.markdown`, `.pdf`

---

## 6. Run the API

Documents are **automatically indexed at startup** — no separate step needed.

```bash
uvicorn app.main:app --reload
```

Expected startup output:
```
INFO:     Started server process [XXXXX]
INFO:     Waiting for application startup.
✅ Indexed 142 chunks into vector store
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000
```

> If you see `⚠️ No documents found`, check that files exist in `app/data/docs/` or `app/data/pdfs/`.

---

## 7. Test the API

```bash
curl "http://localhost:8000/ask?q=What are the action items from the meeting?"
```

Expected response:
```json
{
  "answer": "The action items from the meeting include..."
}
```

Or open in your browser:
```
http://localhost:8000/ask?q=your+question+here
```

FastAPI interactive docs (auto-generated):
```
http://localhost:8000/docs
```

---

## Project Structure

```
gen-ai-rag-system/
│
├── app/
│   ├── main.py                  # FastAPI app entry point + lifespan indexing
│   ├── core/
│   │   └── config.py            # Tunable retrieval settings
│   ├── services/
│   │   ├── rag_service.py       # Core RAG logic (expansion, retrieval, generation)
│   │   ├── vector_store.py      # Qdrant in-memory wrapper
│   │   ├── llm.py               # Ollama LLM wrapper
│   │   └── guardrails.py        # Prompt injection + output validation
│   ├── ingestion/
│   │   ├── index.py             # Standalone script to index docs manually
│   │   ├── pipeline.py          # Recursive file loader (.txt, .md, .pdf)
│   │   └── chunking.py          # Text splitter config
│   └── data/
│       ├── docs/                # Text/Markdown source files
│       └── pdfs/                # PDF source files
│
├── requirements.txt
├── Readme.md
├── RAG_EXPLAINED.md             # Conceptual guide to RAG
└── DEVELOPER_ONBOARDING.md      # This file
```

---

## Configuration

All retrieval parameters are in `app/core/config.py`:

| Setting | Default | What to change it for |
|---|---|---|
| `TOP_K` | `3` | More chunks = more context but slower/noisier |
| `TOP_K_FETCH` | `8` | Higher = better recall before filtering |
| `SCORE_THRESHOLD` | `0.3` | Raise if getting irrelevant answers; lower if getting "No relevant data found" |
| `MAX_CONTEXT_CHARS` | `30000` | Lower this if the LLM ignores the end of long contexts |

---

## Common Issues

### `No relevant data found` for all questions
- Documents may not be indexed. Check startup logs for `✅ Indexed N chunks`.
- Lower `SCORE_THRESHOLD` in `config.py` (try `0.1`).
- Verify Ollama is running: `ollama list`.

### `model "nomic-embed-text" not found`
```bash
ollama pull nomic-embed-text
```

### `ModuleNotFoundError`
```bash
pip install pypdf langchain-ollama langchain-qdrant "unstructured[md]"
```

### SSL errors during startup (NLTK)
This was caused by `UnstructuredMarkdownLoader` — already fixed. Markdown files now use `TextLoader` instead.

### Answer echoes raw transcript text
The LLM (`llama3.2:1b`) is too small to reliably follow instructions. This is a known limitation of 1b models. The prompt is tuned to minimise this but cannot fully prevent it.

### `collection "rag" not found`
Qdrant in-memory collections are created at startup. If you see this mid-run it means `VectorStore.__init__` didn't complete — check the startup traceback.

---

## Running the Standalone Indexer (optional)

You can index documents without starting the API:

```bash
python app/ingestion/index.py
```

> Note: this creates a separate in-memory instance and **does not share** data with the running API. It's useful for testing the ingestion pipeline in isolation.

---

## Development Tips

- **Adding a new file type**: edit `app/ingestion/pipeline.py` and add the extension to `TEXT_EXTENSIONS` or add a new loader branch.
- **Changing the LLM**: edit `app/services/llm.py` and update the `model=` value to any model available via `ollama list`.
- **Tuning retrieval quality**: adjust `SCORE_THRESHOLD` and `TOP_K_FETCH` in `app/core/config.py` — no code changes needed.
- **Inspecting retrieved chunks**: add a `print(docs)` in `rag_service._retrieve_and_merge()` before the context is built.
