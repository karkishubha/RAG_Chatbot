from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID

class ChatRequest(BaseModel):
    conversation_id: Optional[UUID] = None
    user_message: str
    k: int = 5

class ChatResponse(BaseModel):
    conversation_id: UUID
    assistant_message: str
    retrieved_docs: List[dict]
