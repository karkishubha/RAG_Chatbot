from typing import List, Tuple
from app.services.embedding import EmbeddingClient
from app.services.vectorstore import VectorStoreClient
from app.services.chunking import chunk_by_tokens, chunk_by_sentences
from app.services.files import extract_text_from_pdf_or_txt, save_upload_file
from app.services.db import BookingRepository
from app.services.redis_memory import RedisChatMemory
from pathlib import Path
from uuid import uuid4

embedding_client = EmbeddingClient()
vector_client = VectorStoreClient()
booking_repo = BookingRepository()
redis_memory = RedisChatMemory()


async def process_document(document_id: str, file_path: str, strategy: str = "token") -> bool:
    """
    Extract text, chunk, embed, and upsert to vector DB.
    """
    try:
        print(f"DEBUG: Processing document {document_id} -> {file_path}")
        text = extract_text_from_pdf_or_txt(file_path)
        print(f"DEBUG: Extracted text length: {len(text)}")

        chunks = chunk_by_tokens(text) if strategy == "token" else chunk_by_sentences(text)
        print(f"DEBUG: Number of chunks: {len(chunks)}")

        texts = [c.text for c in chunks]
        embeddings = await embedding_client.embed_texts(texts)

        records = []
        for idx, (chunk, emb) in enumerate(zip(chunks, embeddings)):
            if emb is None:
                print(f"WARNING: Skipping invalid embedding tuple for chunk {idx}")
                continue
            point_id = str(uuid4())
            meta = {"document_id": document_id, "chunk_index": idx, "text": chunk.text[:1000]}
            records.append({"id": point_id, "vector": emb, "metadata": meta})

        await vector_client.upsert(records)
        await booking_repo.save_document_metadata(document_id, {"chunks": len(chunks)})

        print(f"DEBUG: process_document completed for {document_id}")
        return True
    except Exception as e:
        print(f"ERROR in process_document: {e}")
        raise


def build_prompt(memory_context: List[dict], retrieved_texts: List[str], user_message: str) -> str:
    parts = []
    if memory_context:
        parts.append(
            "Conversation memory:\n"
            + "\n".join([f'{m["role"]}: {m["text"]}' for m in memory_context])
        )
    if retrieved_texts:
        parts.append("Relevant documents:\n" + "\n\n".join(retrieved_texts))
    parts.append(f"User: {user_message}\nAssistant:")
    return "\n\n".join(parts)


class ChatService:
    """ Handles chat using RAG. """

    def __init__(self):
        self.emb = embedding_client
        self.vs = vector_client
        self.redis = redis_memory

    async def handle_message(self, conversation_id: str, message: str, k: int = 5) -> Tuple[str, List[dict]]:
        memory_context = await self.redis.get_context(conversation_id)
        q_emb_list = await self.emb.embed_texts([message])

        if not q_emb_list or not isinstance(q_emb_list[0], list):
            raise ValueError(f"Invalid embedding for message: {q_emb_list}")

        q_vector = q_emb_list[0]
        results = await self.vs.query(q_vector, top_k=k)
        retrieved_texts = [r.get("metadata", {}).get("text", "") for r in results]

        prompt = build_prompt(memory_context, retrieved_texts, message)
        assistant = await self.emb.generate_text(prompt)

        await self.redis.append_message(conversation_id, {"role": "user", "text": message})
        await self.redis.append_message(conversation_id, {"role": "assistant", "text": assistant})

        return assistant, [r.get("metadata") for r in results]
