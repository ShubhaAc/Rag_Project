from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db.database import init_db
from app.core.config import get_settings
from app.api.routes.ingestion import router as ingestion_router
from app.api.routes.rag import router as rag_router

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(
    title="RAG API",
    description="Document Ingestion and Conversational RAG API",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(ingestion_router, prefix="/api/v1/ingest", tags=["Ingestion"])
app.include_router(rag_router, prefix="/api/v1/rag", tags=["RAG"])


@app.get("/health")
async def health_check():
    return {"status": "ok"}
  