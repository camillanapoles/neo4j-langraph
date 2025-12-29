"""Configuração de LLMs para diferentes casos de uso"""

from typing import Optional
from langchain_openai import ChatOpenAI

from src.config import get_llm


class LLMConfig:
    """Configurações de LLM para diferentes propósitos"""

    @staticmethod
    def classification_llm() -> ChatOpenAI:
        """LLM otimizado para classificação (rápido, barato)"""
        return get_llm(model="gpt-4o-mini", temperature=0.0)

    @staticmethod
    def query_llm() -> ChatOpenAI:
        """LLM para geração de queries Cypher (precisão)"""
        return get_llm(model="gpt-4", temperature=0.0)

    @staticmethod
    def answer_llm() -> ChatOpenAI:
        """LLM para síntese de respostas (rápido)"""
        return get_llm(model="gpt-3.5-turbo", temperature=0.0)

    @staticmethod
    def analysis_llm() -> ChatOpenAI:
        """LLM para análise e clusterização (criativo)"""
        return get_llm(model="gpt-4", temperature=0.3)
