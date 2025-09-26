# app/services/vectorstore.py
from typing import List, Dict, Any
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
from app.config import settings

class VectorStoreClient:
    """
    Handles vector database operations using Qdrant.
    """
    COLLECTION_NAME = "documents"
    EMBEDDING_DIM = 4096  

    def __init__(self):
        
        self.client = QdrantClient(url=settings.QDRANT_URL, api_key=settings.EMBEDDING_API_KEY)
        self._ensure_collection()

    def _ensure_collection(self):
        """
        Creates (or recreates) the collection with the proper vector configuration.
        """
        self.client.recreate_collection(
            collection_name=self.COLLECTION_NAME,
            vectors_config=VectorParams(
                size=self.EMBEDDING_DIM,
                distance=Distance.COSINE
            )
        )

    async def upsert(self, records: List[Dict[str, Any]]):
        """
        Upsert vector records into Qdrant.
        Each record should have: {"id": str, "vector": List[float], "metadata": dict}
        """
        
        from asyncio import to_thread
        await to_thread(self._upsert_sync, records)

    def _upsert_sync(self, records: List[Dict[str, Any]]):
        points = [
            {
                "id": r["id"],
                "vector": r["vector"],
                "payload": r["metadata"]
            }
            for r in records
        ]
        self.client.upsert(collection_name=self.COLLECTION_NAME, points=points)

    async def query(self, vector: List[float], top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Query similar vectors from Qdrant.
        Returns top_k results.
        """
        from asyncio import to_thread
        return await to_thread(self._query_sync, vector, top_k)

    def _query_sync(self, vector: List[float], top_k: int = 5) -> List[Dict[str, Any]]:
        response = self.client.search(
            collection_name=self.COLLECTION_NAME,
            query_vector=vector,
            limit=top_k
        )
        
        return [{"id": r.id, "metadata": r.payload} for r in response]
