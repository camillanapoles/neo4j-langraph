"""Script para testar configuração Gemini Flash 2.5 + Embeddings"""

from src.config import (
    get_llm,
    get_embeddings,
    configure_llm_gemini,
    configure_embeddings_code,
    configure_embeddings_general,
    configure_embeddings_multilingual,
)


def test_gemini_flash():
    """Testa Gemini Flash 2.5"""
    print("=" * 70)
    print("🧪 TESTE 1: Gemini Flash 2.5 (LLM)")
    print("=" * 70)
    print()

    # LLM Gemini
    llm = configure_llm_gemini(api_key="your-api-key")

    prompt = "Responda apenas: OK (Gemini Flash 2.5 funcionando!)"
    result = llm.invoke(prompt)

    print(f"🧠 Resposta: {result.content}")
    print()


def test_embeddings_general():
    """Testa embeddings para português/geral"""
    print("=" * 70)
    print("🧪 TESTE 2: Embeddings - Português / Geral")
    print("=" * 70)
    print()

    # Embeddings para geral
    emb = configure_embeddings_general()

    text = "Django é um framework web em Python"
    vector = emb.embed_query(text)

    print(f"📊 Texto: {text}")
    print(f"📊 Dimensões: {len(vector)}")
    print(f"📊 VRAM esperado: 1.5GB")
    print(f"✅ Embeddings gerados!")
    print()


def test_embeddings_code():
    """Testa embeddings para código"""
    print("=" * 70)
    print("🧪 TESTE 3: Embeddings - Engenharia / Código")
    print("=" * 70)
    print()

    # Embeddings para código
    emb = configure_embeddings_code()

    text = "def authenticate_user(username, password): return jwt.encode(...)"
    vector = emb.embed_query(text)

    print(f"📊 Texto: {text}")
    print(f"📊 Dimensões: {len(vector)}")
    print(f"📊 VRAM esperado: 4.5GB")
    print(f"✅ Embeddings gerados!")
    print()


def test_embeddings_multilingual():
    """Testa embeddings multilíngua"""
    print("=" * 70)
    print("🧪 TESTE 4: Embeddings - Multilíngua")
    print("=" * 70)
    print()

    # Embeddings multilíngua
    emb = configure_embeddings_multilingual()

    text = "Python is the best programming language"
    vector = emb.embed_query(text)

    print(f"📊 Texto: {text}")
    print(f"📊 Dimensões: {len(vector)}")
    print(f"📊 VRAM esperado: 2.5GB")
    print(f"✅ Embeddings gerados!")
    print()


def test_classification():
    """Testa classificação com Gemini Flash 2.5"""
    print("=" * 70)
    print("🧪 TESTE 5: Classificação - Engenharia + Português")
    print("=" * 70)
    print()

    llm = configure_llm_gemini(api_key="your-api-key")

    prompt = """
    Classifique este arquivo de engenharia de software em português.
    Retorne JSON:
    {{
      "tipo": "projeto | nota | tutorial | outro",
      "linguagem": "Python | JavaScript | outro",
      "stack": ["Django", "FastAPI", etc],
      "descricao": "breve descrição"
    }}

    Arquivo: arquitetura_sistema.md
    Conteúdo: O sistema usa microserviços com Django e RabbitMQ.
    É um projeto de e-commerce com arquitetura hexagonal.
    """

    print("📝 Classificando arquivo...")
    print()

    result = llm.invoke(prompt)

    print(f"💬 Classificação:")
    print(result.content)
    print()


def test_portuguese_quality():
    """Testa qualidade de português"""
    print("=" * 70)
    print("🧪 TESTE 6: Qualidade de Português")
    print("=" * 70)
    print()

    llm = configure_llm_gemini(api_key="your-api-key")

    prompt = """
    Explique o que é arquitetura hexagonal em engenharia de software.
    Responda em português brasileiro, de forma clara e didática.
    Máximo 3 parágrafos.
    """

    print("📝 Gerando explicação em português...")
    print()

    result = llm.invoke(prompt)

    print(f"💬 Explicação:")
    print(result.content)
    print()


def test_auto_embedding_selection():
    """Testa seleção automática de embeddings"""
    print("=" * 70)
    print("🧪 TESTE 7: Seleção Automática de Embeddings")
    print("=" * 70)
    print()

    # Auto-seleção para código
    print("1. Auto-seleção para CÓDIGO:")
    emb_code = get_embeddings(task="code")
    print(f"   ✅ Modelo para código configurado")
    print()

    # Auto-seleção para geral
    print("2. Auto-seleção para GERAL:")
    emb_general = get_embeddings(task="general")
    print(f"   ✅ Modelo para geral configurado")
    print()

    # Auto-seleção para multilíngua
    print("3. Auto-seleção para MULTILÍNGUA:")
    emb_multi = get_embeddings(task="multilingual")
    print(f"   ✅ Modelo para multilíngua configurado")
    print()


def main():
    """Executa todos os testes"""
    print("\n")
    print("╔════════════════════════════════════════════════════════════════╗")
    print("║  🚀 TESTE COMPLETO: Gemini Flash 2.5 + Embeddings Híbridos      ║")
    print("╚════════════════════════════════════════════════════════════════╝")
    print("\n")

    try:
        test_gemini_flash()
        test_embeddings_general()
        test_embeddings_code()
        test_embeddings_multilingual()
        test_classification()
        test_portuguese_quality()
        test_auto_embedding_selection()

        print("=" * 70)
        print("✅ TODOS OS TESTES PASSARAM!")
        print("=" * 70)
        print()
        print("🎉 Sua configuração está pronta:")
        print("   • LLM: Gemini Flash 2.5 (3x rápido, 10x barato)")
        print("   • Embeddings PT/Geral: paraphrase-multilingual (1.5GB VRAM)")
        print("   • Embeddings Código: e5-mistral-7b (4.5GB VRAM)")
        print("   • Embeddings Multilíngua: bge-m3 (2.5GB VRAM)")
        print()
        print("💡 Estratégia Híbrida:")
        print("   • configure_embeddings_code() → Para código")
        print("   • configure_embeddings_general() → Para PT/geral")
        print("   • configure_embeddings_multilingual() → Para multilíngua")
        print()
        return 0

    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        print("\nVerifique:")
        print("1. GOOGLE_API_KEY está configurada no .env")
        print("2. LocalAI está rodando: k9s -n neo4j-langraph")
        print("3. Modelos de embeddings estão disponíveis no LocalAI")
        print("4. .env está configurado corretamente")
        return 1


if __name__ == '__main__':
    exit(main())
