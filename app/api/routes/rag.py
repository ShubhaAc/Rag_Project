from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.services.rag import get_rag_response
from app.services.booking import extract_booking_data, save_booking

router = APIRouter()


class ChatRequest(BaseModel):
    session_id: str
    question: str


@router.post("/chat")
async def chat(request: ChatRequest, db: AsyncSession = Depends(get_db)):
    result = await get_rag_response(request.session_id, request.question)

    booking_data = extract_booking_data(result["answer"])
    if booking_data:
        booking = await save_booking(booking_data, db)
        result["answer"] = (
            f"Interview booked successfully for {booking.name}! "
            f"A confirmation will be sent to {booking.email}. "
            f"Scheduled on {booking.date} at {booking.time}."
        )
        result["booking"] = {
            "id": booking.id,
            "name": booking.name,
            "email": booking.email,
            "date": booking.date,
            "time": booking.time
        }

    return result