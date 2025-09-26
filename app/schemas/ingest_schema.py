from pydantic import BaseModel
from uuid import UUID

class IngestResponse(BaseModel):
    document_id: UUID
    chunks_indexed: int
    metadata: dict

class IngestRequest(BaseModel):
    strategy: str = "token"
