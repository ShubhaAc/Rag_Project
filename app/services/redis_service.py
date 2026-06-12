import json
import httpx
from app.core.config import get_settings

settings = get_settings()

BASE_URL = settings.UPSTASH_REDIS_REST_URL
TOKEN = settings.UPSTASH_REDIS_REST_TOKEN
HEADERS = {"Authorization": f"Bearer {TOKEN}"}


async def get_chat_history(session_id: str) -> list[dict]:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/get/{session_id}", headers=HEADERS)
        data = response.json()
        result = data.get("result")
        if result:
            parsed = json.loads(result)
            if isinstance(parsed, list):
                return parsed
        return []


async def save_chat_history(session_id: str, history: list[dict]):
    async with httpx.AsyncClient() as client:
        await client.post(
            f"{BASE_URL}/set/{session_id}",
            headers=HEADERS,
            json={"value": json.dumps(history)}
        )


async def clear_chat_history(session_id: str):
    async with httpx.AsyncClient() as client:
        await client.get(f"{BASE_URL}/del/{session_id}", headers=HEADERS)
        