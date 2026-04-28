from app.services.llm import LLMService
from app.services.vector_store import VectorStore
from app.services.guardrails import Guardrails
from app.core.config import settings

class RAGService:
    def __init__(self, vector_store: VectorStore = None):
        self.vector = vector_store or VectorStore()
        self.llm = LLMService()

    def _expand_queries(self, query: str) -> list[str]:
        """Generate alternative phrasings to improve retrieval recall."""
        prompt = f"""Generate 2 alternative search queries for the question below.
Return only the 2 queries, one per line, no numbering, no extra text.

Question: {query}

Alternative queries:"""
        try:
            result = self.llm.generate(prompt)
            variants = [q.strip() for q in result.strip().splitlines() if q.strip()]
            return [query] + variants[:2]
        except Exception:
            return [query]

    def _retrieve_and_merge(self, queries: list[str]) -> list:
        """Retrieve docs for all query variants, deduplicate by content."""
        seen = set()
        merged = []
        for q in queries:
            docs = self.vector.search(
                q,
                k=settings.TOP_K,
                fetch_k=settings.TOP_K_FETCH,
                score_threshold=settings.SCORE_THRESHOLD,
            )
            for doc in docs:
                if doc.page_content not in seen:
                    seen.add(doc.page_content)
                    merged.append(doc)
        return merged

    def _build_context(self, docs: list) -> str:
        """Build a source-attributed context string, capped at MAX_CONTEXT_CHARS."""
        parts = []
        total = 0
        for doc in docs:
            source = doc.metadata.get("source", "")
            if source:
                import os
                source = os.path.basename(source)
            header = f"[{source}]\n" if source else ""
            chunk = header + doc.page_content.strip()
            if total + len(chunk) > settings.MAX_CONTEXT_CHARS:
                # Add as much of the last chunk as fits
                remaining = settings.MAX_CONTEXT_CHARS - total
                if remaining > 100:
                    parts.append(chunk[:remaining])
                break
            parts.append(chunk)
            total += len(chunk)
        return "\n\n---\n\n".join(parts)

    def generate(self, query: str) -> str:
        # Guardrail 1: detect injection
        if Guardrails.detect_prompt_injection(query):
            return "Unsafe query detected."

        # Guardrail 2: sanitize
        query = Guardrails.sanitize_input(query).strip()

        # Expand query into multiple variants for better recall
        queries = self._expand_queries(query)

        # Retrieve and merge results from all variants
        docs = self._retrieve_and_merge(queries)

        if not docs:
            return "No relevant data found."

        context = self._build_context(docs)

        prompt = f"""You are a helpful assistant. Use only the context below to answer the question.

Rules:
- Write a clear, concise answer in your own words.
- Do NOT copy, quote, or reproduce the context text.
- Do NOT include speaker names, timestamps, or raw transcript text.
- If the answer cannot be determined from the context, say "I don't know".
- Do NOT make up information.

Context:
{context}

Question: {query}

Answer:"""

        response = self.llm.generate(prompt)

        # Guardrail 3: output validation
        return Guardrails.validate_output(response)

        response = self.llm.generate(prompt)

        # 🛡️ Guardrail 3: output validation
        return Guardrails.validate_output(response)