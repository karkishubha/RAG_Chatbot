# app/routers/chat.py
from fastapi import APIRouter
from pydantic import BaseModel
from app.services.rag import ChatService

router = APIRouter()
chat_service = ChatService()

# Request model
class ChatRequest(BaseModel):
    conversation_id: str
    message: str
    k: int = 5  # optional parameter for future use

# POST endpoint
@router.post("/")
async def chat(request: ChatRequest):
    response_text, metadata = await chat_service.handle_message(
        request.conversation_id,
        request.message,
        request.k
    )
    return {"response": response_text, "metadata": metadata}
