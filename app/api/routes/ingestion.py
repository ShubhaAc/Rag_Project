from fastapi import APIRouter, UploadFile, File, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.services.ingestion import ingest_document

router = APIRouter()


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    strategy: str = Query(default="recursive", enum=["recursive", "token"]),
    db: AsyncSession = Depends(get_db)
):
    result = await ingest_document(file, strategy, db)
    return result