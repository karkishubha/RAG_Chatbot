from fastapi import APIRouter, HTTPException
from app.schemas.booking_schema import BookingCreate, Booking
from app.services.db import BookingRepository
router = APIRouter()
repo = BookingRepository()

@router.post("/", response_model=Booking)
async def create_booking(b: BookingCreate):
    booking = await repo.create_booking(b)
    return booking

@router.get("/", response_model=list[Booking])
async def list_bookings():
    return await repo.list_bookings()
