# 📚 RAG Explained — Retrieval-Augmented Generation

## What is RAG?

**Retrieval-Augmented Generation (RAG)** is a technique that improves LLM answers by giving the model relevant facts from your own documents at query time — instead of relying solely on what the model learned during training.

> Think of it as: **open-book exam** vs closed-book exam.
> The LLM can look up your documents before answering.

---

## Why RAG?

| Problem with plain LLMs | How RAG solves it |
|---|---|
| Knowledge cut-off date | Your documents are always current |
| Hallucination (making things up) | LLM is grounded in real retrieved text |
| No access to private data | You index your own files locally |
| Expensive fine-tuning | No retraining needed — just add documents |

---

## The Core Idea

```
Your Documents  →  [Index]  →  Vector Store
                                    ↑
User Question  →  [Embed]  →  Search → Top Chunks
                                              ↓
                              LLM Prompt = Question + Chunks
                                              ↓
                                          Answer
```

---

## Step-by-Step Process

### Phase 1 — Indexing (done once at startup)

#### Step 1: Load Documents
Read all files from disk (`.txt`, `.md`, `.pdf`).

```
data/docs/meeting_notes.md     →  raw text
data/pdfs/product_manual.pdf   →  raw text (extracted)
```

#### Step 2: Chunk the Documents
Split long documents into smaller overlapping pieces so the embedding model can handle them and so each chunk stays focused on one idea.

```
Original (2000 chars):
"Chapter 1: Introduction. RAG stands for... [long text]"

After chunking (800 chars, 150 overlap):
Chunk 1: "Chapter 1: Introduction. RAG stands for Retrieval..."
Chunk 2: "...Retrieval-Augmented Generation. It was introduced..."
Chunk 3: "...introduced in 2020 by Facebook AI Research. The key..."
```

> Overlap ensures no idea is cut in half between chunks.

#### Step 3: Embed the Chunks
Convert each chunk into a **vector** (a list of numbers) that captures its meaning. Similar chunks get similar vectors.

```
"RAG uses vector search"       →  [0.12, 0.87, 0.03, ...]
"Retrieval-based AI methods"   →  [0.11, 0.84, 0.06, ...]  ← similar!
"The cat sat on the mat"       →  [0.93, 0.01, 0.74, ...]  ← very different
```

#### Step 4: Store in Vector Database
Save all chunk vectors + original text into Qdrant (in-memory).

```
Vector Store:
┌─────────────────────────────────────────────────┐
│ ID │ Vector           │ Text          │ Source   │
├────┼──────────────────┼───────────────┼──────────┤
│ 1  │ [0.12, 0.87, ...]│ "RAG uses..." │ notes.md │
│ 2  │ [0.45, 0.23, ...]│ "The model..." │ doc.pdf  │
│ 3  │ [0.91, 0.04, ...]│ "Action item..."│ notes.md│
└─────────────────────────────────────────────────┘
```

---

### Phase 2 — Querying (happens on every `/ask` request)

#### Step 5: Receive User Query
```
GET /ask?q=What is the action item from the last meeting?
```

#### Step 6: Multi-Query Expansion
The LLM generates alternative phrasings to improve recall — different users word questions differently.

```
Original:    "What is the action item from the last meeting?"
Variant 1:   "What tasks were assigned in the recent meeting?"
Variant 2:   "What are the follow-up actions from the meeting?"
```

All 3 queries are searched independently.

#### Step 7: Embed the Query
Convert the query (and each variant) into a vector using the same embedding model.

```
"What is the action item?" → [0.88, 0.05, 0.71, ...]
```

#### Step 8: Vector Search + Score Filtering
Find the closest chunks to the query vector using **cosine similarity**. Fetch 8 candidates, drop any below score `0.3`, re-rank by score, keep top 3.

```
Results (scored):
┌──────────────────────────────────┬───────┐
│ Chunk                            │ Score │
├──────────────────────────────────┼───────┤
│ "Action item: review PR by Fri"  │ 0.91  │ ✅ kept
│ "Kapil will schedule follow-up"  │ 0.76  │ ✅ kept
│ "Next meeting is Tuesday"        │ 0.61  │ ✅ kept
│ "The cat sat on the mat"         │ 0.12  │ ❌ filtered out
└──────────────────────────────────┴───────┘
```

#### Step 9: Build Context
Combine the top chunks into a single context block, prefixed with their source file.

```
[meeting_notes.md]
Action item: review PR by Friday. Kapil will schedule follow-up.

---

[meeting_notes.md]
Next meeting is on Tuesday at 10am.
```

#### Step 10: Generate Answer
Send the context + original question to the LLM in a structured prompt.

```
Prompt:
  You are a helpful assistant. Use only the context below...

  Context:
  [meeting_notes.md]
  Action item: review PR by Friday...

  Question: What is the action item from the last meeting?

  Answer:
```

```
LLM Response:
  "The action item from the last meeting is to review the PR by Friday.
   Kapil will also schedule a follow-up."
```

#### Step 11: Output Validation
The guardrail checks the response before returning it — e.g. flags if the LLM said "I don't know" and returns a cleaner message.

---

## Full Example End-to-End

**Documents indexed:**
```
data/docs/meeting_2024_04.md  (contains notes from a team meeting)
data/pdfs/project_spec.pdf    (contains technical requirements)
```

**User asks:**
```
GET /ask?q=Who is responsible for the authentication module?
```

**Internally:**
1. Query expanded to 3 variants
2. Each variant searches the vector store
3. Chunks retrieved:
   - `"Vasyl will own the authentication module (OAuth2)"` — score 0.89
   - `"Auth module must support SSO and MFA"` — score 0.72
   - `"Vasyl to deliver auth module by Sprint 4"` — score 0.68
4. Context built from those 3 chunks
5. LLM answers: `"Vasyl is responsible for the authentication module, which must support OAuth2, SSO, and MFA, and is due by Sprint 4."`

---

## Key Concepts Glossary

| Term | Meaning |
|---|---|
| **Embedding** | Converting text to a vector of numbers that captures meaning |
| **Vector Store** | Database optimised for storing and searching vectors |
| **Cosine Similarity** | Measures how similar two vectors are (1 = identical, 0 = unrelated) |
| **Chunk** | A small piece of a document (e.g. 800 characters) |
| **Chunk Overlap** | Repeated characters between adjacent chunks to preserve context |
| **Top-K** | The K most relevant chunks retrieved |
| **Score Threshold** | Minimum similarity score a chunk must have to be used |
| **Multi-query Expansion** | Generating alternative phrasings to improve retrieval recall |
| **Grounding** | Constraining the LLM to answer only from provided context |
| **Hallucination** | When an LLM confidently states something false |

---

## RAG vs Fine-tuning vs Plain LLM

| | Plain LLM | Fine-tuned LLM | RAG |
|---|---|---|---|
| Uses your documents | ❌ | ✅ (baked in) | ✅ (retrieved live) |
| Stays up to date | ❌ | ❌ (needs retraining) | ✅ (just add files) |
| Cites sources | ❌ | ❌ | ✅ |
| Cost | Low | High | Low |
| Hallucination risk | High | Medium | Low |
| Best for | General Q&A | Domain style | Private doc Q&A |

---

## Common Failure Modes and Fixes

| Symptom | Likely Cause | Fix |
|---|---|---|
| "No relevant data found" | Score threshold too high or docs not indexed | Lower `SCORE_THRESHOLD`, check startup logs |
| Answer copies raw transcript | LLM too small to follow instructions | Use larger model, improve prompt |
| Answer is off-topic | Wrong chunks retrieved | Increase `TOP_K_FETCH`, check chunk size |
| Slow responses | Large docs, many chunks | Reduce `MAX_CONTEXT_CHARS` or chunk size |
| Same chunk repeated | Deduplication not working | Check `_retrieve_and_merge` in `rag_service.py` |
