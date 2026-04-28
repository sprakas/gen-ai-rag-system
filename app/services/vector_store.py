from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from langchain_qdrant import QdrantVectorStore
from langchain_ollama import OllamaEmbeddings

class VectorStore:
    def __init__(self):
        # In-memory Qdrant
        self.client = QdrantClient(":memory:")

        self.embeddings = OllamaEmbeddings(model="nomic-embed-text")

        self.collection_name = "rag"

        # Create the collection if it doesn't exist
        # nomic-embed-text produces 768-dimensional embeddings
        self.client.create_collection(
            collection_name=self.collection_name,
            vectors_config=VectorParams(size=768, distance=Distance.COSINE),
        )

        self.vectorstore = QdrantVectorStore(
            client=self.client,
            collection_name=self.collection_name,
            embedding=self.embeddings,
        )

    def add_documents(self, texts, metadatas=None):
        self.vectorstore.add_texts(texts, metadatas=metadatas)

    def search(self, query: str, k: int = 3, fetch_k: int = 8, score_threshold: float = 0.3):
        # Fetch more candidates than needed, filter by relevance score, return top k
        results = self.vectorstore.similarity_search_with_relevance_scores(query, k=fetch_k)
        filtered = [(doc, score) for doc, score in results if score >= score_threshold]
        # Sort by score descending and return top k docs
        filtered.sort(key=lambda x: x[1], reverse=True)
        return [doc for doc, _ in filtered[:k]]