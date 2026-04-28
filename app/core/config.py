import os

class Settings:
    # Retrieval settings
    TOP_K = 3           # final number of chunks passed to LLM
    TOP_K_FETCH = 8     # candidates fetched before score filtering
    SCORE_THRESHOLD = 0.3  # minimum relevance score to keep a chunk
    MAX_CONTEXT_CHARS = 30000  # cap total context size for small LLMs

settings = Settings()