import uuid
from fastapi import UploadFile
from pypdf import PdfReader
from app.services.chunking import get_chunks
from app.services.embedding import embed_texts
from app.services.pinecone_service import upsert_vectors
from app.db.models import Document
from sqlalchemy.ext.asyncio import AsyncSession
import io


async def extract_text(file: UploadFile) -> str:
    contents = await file.read()
    if file.filename.endswith(".pdf"):
        reader = PdfReader(io.BytesIO(contents))
        return " ".join(page.extract_text() for page in reader.pages if page.extract_text())
    elif file.filename.endswith(".txt"):
        return contents.decode("utf-8")
    else:
        raise ValueError("Only .pdf and .txt files are supported")


async def ingest_document(file: UploadFile, strategy: str, db: AsyncSession) -> dict:
    text = await extract_text(file)
    chunks = get_chunks(text, strategy)
    embeddings = embed_texts(chunks)

    vectors = [
        {
            "id": str(uuid.uuid4()),
            "values": embeddings[i],
            "metadata": {"text": chunks[i], "filename": file.filename}
        }
        for i in range(len(chunks))
    ]

    upsert_vectors(vectors)

    doc = Document(
        filename=file.filename,
        chunk_count=len(chunks),
        chunking_strategy=strategy
    )
    db.add(doc)
    await db.commit()
    await db.refresh(doc)

    return {
        "filename": file.filename,
        "chunks": len(chunks),
        "strategy": strategy,
        "document_id": doc.id
    }