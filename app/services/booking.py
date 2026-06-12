import json
import re
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import Booking


def extract_booking_data(answer: str) -> dict | None:
    match = re.search(r'\{.*"action"\s*:\s*"book_interview".*\}', answer, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            return None
    return None


async def save_booking(data: dict, db: AsyncSession) -> Booking:
    booking = Booking(
        name=data["name"],
        email=data["email"],
        date=data["date"],
        time=data["time"]
    )
    db.add(booking)
    await db.commit()
    await db.refresh(booking)
    return booking