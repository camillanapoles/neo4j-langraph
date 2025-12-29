"""Configuração com Gemini Flash 2.5 + Estratégia Híbrida de Embeddings"""

import os
from typing import Optional, Literal
from dotenv import load_dotenv
from langchain_neo4j import Neo4jGraph

load_dotenv()


class Neo4jConfig:
    """Configuração da conexão Neo4j"""

    @staticmethod
    def get_connection_url() -> str:
        return os.getenv("NEO4J_URI", "bolt://localhost:7687")

    @staticmethod
    def get_username() -> str:
        return os.getenv("NEO4J_USERNAME", "neo4j")

    @staticmethod
    def get_password() -> str:
        return os.getenv("NEO4J_PASSWORD", "password")

    @staticmethod
    def get_database() -> str:
        return os.getenv("NEO4J_DATABASE", "neo4j")


def get_graph() -> Neo4jGraph:
    """Retorna instância configurada do Neo4jGraph"""
    return Neo4jGraph(
        url=Neo4jConfig.get_connection_url(),
        username=Neo4jConfig.get_username(),
        password=Neo4jConfig.get_password(),
        database=Neo4jConfig.get_database(),
    )


def get_llm(
    provider: Literal["openai", "google", "localai"] = None,
    api_key: Optional[str] = None,
    model: Optional[str] = None,
    temperature: float = 0.0
) -> "BaseChatModel":
    """
    Retorna instância configurada do LLM

    Suporta:
    - Google Gemini Flash 2.5 (RECOMENDADO!)
    - OpenAI
    - LocalAI (llama.cpp)

    Args:
        provider: 'google', 'openai', 'localai'
        api_key: Chave de API
        model: Nome do modelo
        temperature: Temperatura

    Returns:
        Instância configurada do LLM
    """
    final_provider = provider or os.getenv("LLM_PROVIDER", "google")

    if final_provider == "google":
        # Gemini Flash 2.5 (RECOMENDADO!)
        from langchain_google_genai import ChatGoogleGenerativeAI

        final_api_key = api_key or os.getenv("GOOGLE_API_KEY")
        final_model = model or os.getenv("GOOGLE_MODEL", "gemini-2.0-flash-exp")

        print(f"🧠 LLM (Google): model={final_model}")

        return ChatGoogleGenerativeAI(
            model=final_model,
            temperature=temperature,
            api_key=final_api_key,
        )

    elif final_provider == "localai":
        # LocalAI (llama.cpp)
        from langchain_openai import ChatOpenAI

        final_base_url = os.getenv("LOCALAI_URL", "http://localhost:30808")
        final_api_key = api_key or os.getenv("LOCALAI_API_KEY", "dummy-key")
        final_model = model or os.getenv("LOCAL_LLM_MODEL", "llama3.1-8b-instruct")

        print(f"🧠 LLM (LocalAI): base_url={final_base_url}, model={final_model}")

        return ChatOpenAI(
            model=final_model,
            temperature=temperature,
            base_url=final_base_url,
            api_key=final_api_key,
        )

    else:  # openai
        from langchain_openai import ChatOpenAI

        final_api_key = api_key or os.getenv("OPENAI_API_KEY")
        final_model = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")

        print(f"🧠 LLM (OpenAI): model={final_model}")

        return ChatOpenAI(
            model=final_model,
            temperature=temperature,
            api_key=final_api_key,
        )


def get_embeddings(
    provider: Literal["localai", "google", "openai", "huggingface"] = None,
    model: Optional[str] = None,
    task: Optional[str] = None
) -> "Embeddings":
    """
    Retorna instância configurada de embeddings

    ESTRATÉGIA HÍBRIDA INTELIGENTE:

    Para ENGENHARIA DE SOFTWARE/CÓDIGO:
        → intfloat/e5-mistral-7b-instruct (4.5GB, mais preciso)

    Para PORTUGUÊS/CONHECIMENTO GERAL:
        → paraphrase-multilingual-mpnet-base-v2 (1.5GB, mais rápido)

    Args:
        provider: 'localai', 'google', 'openai', 'huggingface'
        model: Nome do modelo de embeddings
        task: Tipo de tarefa ('code', 'general', 'multilingual')

    Returns:
        Instância configurada de embeddings
    """
    final_provider = provider or os.getenv("EMBEDDINGS_PROVIDER", "localai")

    # Estratégia automática de seleção de modelo
    if not model and task:
        if task == "code":
            # Engenharia de software / código
            model = "e5-mistral-7b-instruct"
            print(f"📊 Embeddings (Auto): Usando modelo para ENGENHARIA DE SOFTWARE")
        elif task == "multilingual":
            # Multilíngua (100+ idiomas)
            model = "bge-m3"
            print(f"📊 Embeddings (Auto): Usando modelo MULTILÍNGUA")
        else:  # general / pt
            # Português / conhecimento geral
            model = "paraphrase-multilingual-mpnet-base-v2"
            print(f"📊 Embeddings (Auto): Usando modelo para PORTUGUÊS/GERAL")

    if final_provider == "localai":
        from langchain_openai import OpenAIEmbeddings

        final_base_url = os.getenv("LOCALAI_URL", "http://localhost:30808")
        final_api_key = os.getenv("LOCALAI_API_KEY", "dummy-key")
        final_model = model or os.getenv("LOCAL_EMBEDDINGS_MODEL", "paraphrase-multilingual-mpnet-base-v2")

        print(f"📊 Embeddings (LocalAI): base_url={final_base_url}, model={final_model}")

        return OpenAIEmbeddings(
            model=final_model,
            base_url=final_base_url,
            api_key=final_api_key,
        )

    elif final_provider == "google":
        from langchain_google_genai import GoogleGenerativeAIEmbeddings

        final_api_key = api_key or os.getenv("GOOGLE_API_KEY")
        final_model = model or os.getenv("GOOGLE_EMBEDDINGS_MODEL", "models/text-embedding-004")

        print(f"📊 Embeddings (Google): model={final_model}")

        return GoogleGenerativeAIEmbeddings(
            model=final_model,
            api_key=final_api_key,
        )

    elif final_provider == "huggingface":
        from langchain_huggingface import HuggingFaceEmbeddings

        final_model = model or os.getenv("HF_EMBEDDINGS_MODEL", "sentence-transformers/paraphrase-multilingual-mpnet-base-v2")

        print(f"📊 Embeddings (HuggingFace): model={final_model}")

        return HuggingFaceEmbeddings(
            model_name=final_model,
            model_kwargs={"device": "cuda" if os.getenv("USE_GPU", "true").lower() == "true" else "cpu"},
        )

    else:  # openai
        from langchain_openai import OpenAIEmbeddings

        final_api_key = api_key or os.getenv("OPENAI_API_KEY")
        final_model = model or os.getenv("OPENAI_EMBEDDINGS_MODEL", "text-embedding-ada-002")

        print(f"📊 Embeddings (OpenAI): model={final_model}")

        return OpenAIEmbeddings(
            model=final_model,
            api_key=final_api_key,
        )


# Funções de conveniência para cada estratégia

def configure_llm_gemini(
    api_key: str,
    model: str = "gemini-2.0-flash-exp"
):
    """
    Configurar LLM com Gemini Flash 2.5 (RECOMENDADO!)

    Exemplo:
        llm = configure_llm_gemini(
            api_key="AIza...",
            model="gemini-2.0-flash-exp"
        )
    """
    return get_llm(provider="google", api_key=api_key, model=model)


def configure_embeddings_code():
    """
    Configurar embeddings para ENGENHARIA DE SOFTWARE / CÓDIGO

    Usa: intfloat/e5-mistral-7b-instruct
    VRAM: 4.5GB
    Precisão: MÁXIMA para código

    Exemplo:
        embeddings = configure_embeddings_code()
    """
    return get_embeddings(provider="localai", model="e5-mistral-7b-instruct", task="code")


def configure_embeddings_general():
    """
    Configurar embeddings para PORTUGUÊS / CONHECIMENTO GERAL

    Usa: paraphrase-multilingual-mpnet-base-v2
    VRAM: 1.5GB
    Precisão: MÁXIMA para português

    Exemplo:
        embeddings = configure_embeddings_general()
    """
    return get_embeddings(provider="localai", model="paraphrase-multilingual-mpnet-base-v2", task="general")


def configure_embeddings_multilingual():
    """
    Configurar embeddings MULTILÍNGUA (100+ idiomas)

    Usa: BAAI/bge-m3
    VRAM: 2.5GB
    Precisão: Muito boa em todos os idiomas

    Exemplo:
        embeddings = configure_embeddings_multilingual()
    """
    return get_embeddings(provider="localai", model="bge-m3", task="multilingual")
