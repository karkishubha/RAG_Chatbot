from pydantic import BaseModel, EmailStr
from datetime import datetime
from uuid import UUID

class BookingCreate(BaseModel):
    name: str
    email: EmailStr
    date: datetime
    time: str

class Booking(BookingCreate):
    id: UUID
