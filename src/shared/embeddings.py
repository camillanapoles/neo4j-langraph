"""Gerenciador de embeddings compartilhado"""

from typing import List, Optional
from langchain_openai import OpenAIEmbeddings

from src.config import get_embeddings


class EmbeddingManager:
    """Gerencia criação e operações com embeddings"""

    def __init__(self, embedding_model: Optional[OpenAIEmbeddings] = None):
        self.embedding_model = embedding_model or get_embeddings()

    def embed_text(self, text: str, max_length: int = 8000) -> List[float]:
        """Gera embedding para um texto"""
        text_truncated = text[:max_length] if len(text) > max_length else text
        return self.embedding_model.embed_query(text_truncated)

    def embed_texts(self, texts: List[str], max_length: int = 8000) -> List[List[float]]:
        """Gera embeddings para múltiplos textos"""
        texts_truncated = [t[:max_length] if len(t) > max_length else t for t in texts]
        return self.embedding_model.embed_documents(texts_truncated)
