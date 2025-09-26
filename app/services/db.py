
from sqlmodel import SQLModel, Field, Session, create_engine, select
from uuid import uuid4, UUID
from datetime import datetime
from app.config import settings

# -----------------------------
# Booking table
# -----------------------------
class BookingModel(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    name: str
    email: str
    date: datetime
    time: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

# -----------------------------
# Document metadata table
# -----------------------------
class DocumentMetadata(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    document_id: str
    chunk_index: int
    text_snippet: str
    upload_date: datetime = Field(default_factory=datetime.utcnow)

# -----------------------------
# Repository
# -----------------------------
class BookingRepository:
    def __init__(self):
        # Connect to SQL database
        self.engine = create_engine(settings.DATABASE_DSN, echo=True)
        # Create all tables
        SQLModel.metadata.create_all(self.engine)

    # ---- Bookings ----
    async def create_booking(self, b):
        with Session(self.engine) as s:
            bm = BookingModel(
                name=b.name,
                email=b.email,
                date=b.date,
                time=b.time
            )
            s.add(bm)
            s.commit()
            s.refresh(bm)
            return bm

    async def list_bookings(self):
        with Session(self.engine) as s:
            return s.exec(select(BookingModel)).all()

    # ---- Document metadata ----
    async def save_document_metadata(self, document_id: str, metadata: dict):
        """
        Save document chunk metadata to SQL.
        metadata example: {"chunks": 3, "texts": ["text1","text2","text3"]}
        """
        texts = metadata.get("texts", [])
        with Session(self.engine) as s:
            for idx, txt in enumerate(texts):
                dm = DocumentMetadata(
                    document_id=document_id,
                    chunk_index=idx,
                    text_snippet=txt[:1000]  
                )
                s.add(dm)
            s.commit()
        return True
