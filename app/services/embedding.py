from langchain_huggingface import HuggingFaceEmbeddings
from app.core.config import get_settings
from functools import lru_cache

settings = get_settings()


@lru_cache()
def get_embedding_model() -> HuggingFaceEmbeddings:
    return HuggingFaceEmbeddings(model_name=settings.EMBEDDING_MODEL)


def embed_texts(texts: list[str]) -> list[list[float]]:
    model = get_embedding_model()
    return model.embed_documents(texts)


def embed_query(text: str) -> list[float]:
    model = get_embedding_model()
    return model.embed_query(text)