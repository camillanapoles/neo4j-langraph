"""Script para testar configuração LLM + Embeddings"""

from src.config import get_llm, get_embeddings, configure_llm, configure_embeddings


def test_default_config():
    """Testa configuração padrão do .env"""
    print("=" * 70)
    print("🧪 TESTE 1: Configuração Padrão (.env)")
    print("=" * 70)
    print()

    # LLM padrão
    print("🧠 Testando LLM (configuração padrão)...")
    llm = get_llm()
    result = llm.invoke("Responda apenas: OK")
    print(f"✅ LLM respondeu: {result.content}")
    print()

    # Embeddings padrão
    print("📊 Testando Embeddings (configuração padrão)...")
    emb = get_embeddings()
    vector = emb.embed_query("teste de embeddings")
    print(f"✅ Embeddings gerados: {len(vector)} dimensões")
    print()


def test_custom_config():
    """Testa configuração customizada (override endpoint, API key, modelo)"""
    print("=" * 70)
    print("🧪 TESTE 2: Configuração Customizada (Override)")
    print("=" * 70)
    print()

    # LLM customizado
    print("🧠 Testando LLM (configuração customizada)...")
    llm_custom = configure_llm(
        base_url="http://localhost:30808",
        api_key="dummy-key",
        model="llama3.1-8b-instruct"
    )
    result = llm_custom.invoke("Responda apenas: OK (config customizada)")
    print(f"✅ LLM respondeu: {result.content}")
    print()

    # Embeddings customizados
    print("📊 Testando Embeddings (configuração customizada)...")
    emb_custom = configure_embeddings(
        base_url="http://localhost:30808",
        api_key="dummy-key",
        model="bge-small-en-v1.5"
    )
    vector = emb_custom.embed_query("teste de embeddings customizados")
    print(f"✅ Embeddings gerados: {len(vector)} dimensões")
    print()


def test_engineering_task():
    """Testa tarefa real de engenharia em português"""
    print("=" * 70)
    print("🧪 TESTE 3: Tarefa Real (Engenharia + Português)")
    print("=" * 70)
    print()

    llm = get_llm()

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

    print("📝 Enviando prompt de classificação...")
    print()

    result = llm.invoke(prompt)
    print(f"💬 Resposta do LLM:")
    print(result.content)
    print()


def test_portuguese_quality():
    """Testa qualidade de português"""
    print("=" * 70)
    print("🧪 TESTE 4: Qualidade de Português")
    print("=" * 70)
    print()

    llm = get_llm()

    prompt = """
    Explique o que é arquitetura hexagonal em engenharia de software.
    Responda em português brasileiro, de forma clara e didática.
    Máximo 3 parágrafos.
    """

    print("📝 Enviando prompt em português...")
    print()

    result = llm.invoke(prompt)
    print(f"💬 Resposta do LLM:")
    print(result.content)
    print()


def main():
    """Executa todos os testes"""
    print("\n")
    print("╔════════════════════════════════════════════════════════════════╗")
    print("║  🚀 TESTE COMPLETO: LLM + Embeddings (Llama 3.1 8B)            ║")
    print("╚════════════════════════════════════════════════════════════════╝")
    print("\n")

    try:
        test_default_config()
        test_custom_config()
        test_engineering_task()
        test_portuguese_quality()

        print("=" * 70)
        print("✅ TODOS OS TESTES PASSARAM!")
        print("=" * 70)
        print()
        print("🎉 Sua configuração está pronta:")
        print("   • LLM: Llama 3.1 8B Instruct (engenharia + português)")
        print("   • Embeddings: bge-small-en-v1.5 (super rápido na GPU)")
        print("   • API: OpenAI-compatible (LocalAI)")
        print("   • GPU: RTX 4070 acelerando tudo")
        print()
        return 0

    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        print("\nVerifique:")
        print("1. LocalAI está rodando: k9s -n neo4j-langraph")
        print("2. Endpoint correto: http://localhost:30808")
        print("3. Modelo está disponível no LocalAI")
        print("4. .env está configurado corretamente")
        return 1


if __name__ == '__main__':
    exit(main())
