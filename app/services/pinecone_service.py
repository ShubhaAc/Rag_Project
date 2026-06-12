from pinecone import Pinecone
from app.core.config import get_settings
from functools import lru_cache
import logging

settings = get_settings()


@lru_cache()
def get_pinecone_index():
    pc = Pinecone(api_key=settings.PINECONE_API_KEY)
    return pc.Index(settings.PINECONE_INDEX_NAME)

logger = logging.getLogger(__name__)

def upsert_vectors(vectors: list[dict]):
    index = get_pinecone_index()
    response = index.upsert(vectors=vectors)
    logger.info(f"Pinecone upsert response: {response}")
    print(f"Pinecone upsert response: {response}")


def query_vectors(embedding: list[float], top_k: int = 10) -> list[dict]:
    index = get_pinecone_index()
    results = index.query(vector=embedding, top_k=top_k, include_metadata=True)
    return results["matches"]

