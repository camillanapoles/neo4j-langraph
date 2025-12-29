#!/usr/bin/env python
"""Script de exemplo rápido para testar o sistema"""

from src.config import get_graph, get_llm, get_embeddings
from src.knowledge_system import Ingestion, RelationshipManager, QueryLibrary
from src.project_governance import ProjectIndexer, SimilarityEngine, VersionManager


def test_connection():
    """Testa conexão com Neo4j"""
    print("🔌 Testando conexão com Neo4j...")
    graph = get_graph()
    result = graph.query("RETURN 1 as test")
    assert result[0]['test'] == 1
    print("✅ Conexão com Neo4j OK!\n")


def test_llm():
    """Testa LLM"""
    print("🤖 Testando LLM...")
    llm = get_llm()
    result = llm.invoke("Responda apenas: OK")
    assert "OK" in result.content
    print("✅ LLM OK!\n")


def test_embeddings():
    """Testa embeddings"""
    print("📊 Testando embeddings...")
    emb_model = get_embeddings()
    emb = emb_model.embed_query("teste")
    assert len(emb) == 1536
    print(f"✅ Embeddings OK (dimensões: {len(emb)})!\n")


def main():
    """Executa todos os testes"""
    print("=" * 60)
    print("🧪 TESTE RÁPIDO DO SISTEMA")
    print("=" * 60)
    print()

    try:
        test_connection()
        test_llm()
        test_embeddings()

        print("=" * 60)
        print("✅ TODOS OS TESTES PASSARAM!")
        print("=" * 60)
        print()
        print("O sistema está pronto para uso. Execute:")
        print("  docker-compose up -d           # Iniciar Neo4j")
        print("  neo4j-knowledge ingest ./data  # Ingerir conhecimento")
        print("  neo4j-knowledge dashboard      # Ver dashboard")
        print()
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        print("\nVerifique:")
        print("1. Neo4j está rodando (docker-compose ps)")
        print("2. OPENAI_API_KEY está configurada no .env")
        print("3. Dependências estão instaladas")
        return 1

    return 0


if __name__ == '__main__':
    exit(main())
