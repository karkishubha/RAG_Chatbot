from fastapi import FastAPI
from app.routers import ingestion, chat, booking

app = FastAPI(title="Palm Mind Backend")

app.include_router(ingestion.router, prefix="", tags=["Ingestion"])
app.include_router(chat.router, prefix="/chat", tags=["Chat"])
app.include_router(booking.router, prefix="/booking", tags=["Booking"])
