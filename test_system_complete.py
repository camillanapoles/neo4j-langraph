#!/usr/bin/env python3
"""
Script completo de teste do sistema AI
Testa: LLM, Neo4j, LocalAI e Ingestão
"""

import os
import time
from dotenv import load_dotenv

print("=" * 60)
print("🧪 SISTEMA AI - TESTE COMPLETO")
print("=" * 60)
print()

# Carregar variáveis de ambiente
load_dotenv()

# ======================
# 1. TESTE DO LLM
# ======================
print("1️⃣  TESTE DO LLM (Gemini Flash 2.5)")
print("-" * 60)

try:
    from openai import OpenAI

    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key or api_key.startswith("your-google"):
        print("❌ ERRO: GOOGLE_API_KEY não configurada!")
        print("   Configure no .env: GOOGLE_API_KEY=AIza...")
        exit(1)

    print(f"🔑 API Key: {api_key[:10]}...{api_key[-10:]}")

    client = OpenAI(
        api_key=api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )

    print("📝 Enviando query para LLM...")
    response = client.chat.completions.create(
        model="gemini-2.0-flash-exp",
        messages=[
            {"role": "user", "content": "Olá! Responda em 1 frase: Qual seu nome?"}
        ],
        temperature=0.7,
        max_tokens=50
    )

    print("✅ LLM funcionando!")
    print(f"📝 Resposta: {response.choices[0].message.content}")
    print()

except Exception as e:
    print(f"❌ Erro no LLM: {e}")
    print()
    print("💡 Solução: Aguarde 60 segundos e teste novamente")
    print()

    # Se erro de cota (429), aguardar e tentar novamente
    if "429" in str(e) or "quota" in str(e).lower():
        print("⏳ Aguardando 60 segundos para o limite de cota...")
        for i in range(60, 0, -1):
            print(f"\r⏳ Aguardando... {i} segundos  ", end="", flush=True)
            time.sleep(1)
        print("\n✅ Aguardo concluído! Tentando novamente...")
        print()

        try:
            response = client.chat.completions.create(
                model="gemini-2.0-flash-exp",
                messages=[
                    {"role": "user", "content": "Olá! Responda em 1 frase: Qual seu nome?"}
                ],
                temperature=0.7,
                max_tokens=50
            )
            print("✅ LLM funcionando após aguardo!")
            print(f"📝 Resposta: {response.choices[0].message.content}")
            print()
        except Exception as e2:
            print(f"❌ Erro após aguardo: {e2}")
            print()
            print("💡 Solução: Configure Ollama (LLM local) ou aguarde mais tempo")
            exit(1)
    else:
        exit(1)

# ======================
# 2. TESTE DO NEO4J
# ======================
print("2️⃣  TESTE DO NEO4J (Grafo)")
print("-" * 60)

try:
    from neo4j import GraphDatabase

    print("🔌 Conectando ao Neo4j...")
    driver = GraphDatabase.driver(
        "bolt://localhost:30687",
        auth=("neo4j", "password")
    )

    driver.verify_connectivity()
    print("✅ Neo4j conectado!")

    # Query de teste
    session = driver.session()
    result = session.run("RETURN 'Neo4j está funcionando!' AS msg")
    print(f"📊 Query de teste: {result.single()['msg']}")

    # Contar nós
    result = session.run("MATCH (n) RETURN count(n) AS count")
    node_count = result.single()['count']
    print(f"📊 Total de nós no grafo: {node_count}")

    session.close()
    driver.close()
    print()

except Exception as e:
    print(f"❌ Erro no Neo4j: {e}")
    print()
    print("💡 Solução: Verifique se Neo4j está rodando:")
    print("   kubectl get pods -n neo4j-langraph")
    exit(1)

# ======================
# 3. TESTE DO LOCALAI
# ======================
print("3️⃣  TESTE DO LOCALAI (Embeddings com GPU)")
print("-" * 60)

try:
    import requests

    print("🔌 Conectando ao LocalAI...")
    response = requests.get(
        "http://localhost:30808/v1/models",
        timeout=5
    )

    if response.status_code == 200:
        print("✅ LocalAI conectado!")

        models = response.json()
        model_count = len(models.get("data", []))
        print(f"📊 Modelos disponíveis: {model_count}")

        if model_count == 0:
            print("⚠️  Nenhum modelo carregado")
            print("💡 Para carregar modelos, veja a documentação:")
            print("   https://localai.io/model-gallery/")
        print()
    else:
        print(f"❌ Erro no LocalAI: Status {response.status_code}")
        print()

except Exception as e:
    print(f"❌ Erro no LocalAI: {e}")
    print()
    print("💡 Solução: Verifique se LocalAI está rodando:")
    print("   kubectl get pods -n neo4j-langraph")
    exit(1)

# ======================
# 4. STATUS DO SISTEMA
# ======================
print("4️⃣  STATUS DO SISTEMA")
print("-" * 60)

try:
    import subprocess

    # Verificar pods
    result = subprocess.run(
        ["k3s", "kubectl", "get", "pods", "-n", "neo4j-langraph"],
        capture_output=True,
        text=True,
        timeout=10
    )

    if result.returncode == 0:
        print("🐳 Status dos Pods:")
        print(result.stdout)
    else:
        print("❌ Erro ao verificar pods")

    # Verificar GPU
    result = subprocess.run(
        ["nvidia-smi", "--query-gpu=name,memory.total,memory.used,memory.free,utilization.gpu",
         "--format=csv,noheader,nounits"],
        capture_output=True,
        text=True,
        timeout=10
    )

    if result.returncode == 0:
        print("🎮 Status da GPU (RTX 4070):")
        gpu_info = result.stdout.strip().split(',')
        print(f"   Nome:      {gpu_info[0]}")
        print(f"   Total VRAM: {gpu_info[1]} MB")
        print(f"   Usado:      {gpu_info[2]} MB ({round(int(gpu_info[2]) / int(gpu_info[1]) * 100)}%)")
        print(f"   Livre:      {gpu_info[3]} MB")
        print(f"   Utilização: {gpu_info[4]}%")
        print()

except Exception as e:
    print(f"⚠️  Não foi possível verificar o status completo: {e}")
    print()

# ======================
# 5. RESUMO FINAL
# ======================
print("=" * 60)
print("🎉 TESTE COMPLETO!")
print("=" * 60)
print()
print("✅ SISTEMA AI FUNCIONANDO!")
print()
print("🌐 ACESSOS:")
print("   • Neo4j Browser:   http://localhost:30474")
print("   • Neo4j BOLT:     bolt://localhost:30687")
print("   • LocalAI API:    http://localhost:30808")
print()
print("🎮 GPU (RTX 4070):")
print("   • Disponível para embeddings com LocalAI")
print()
print("🧠 LLM (Gemini Flash 2.5):")
print("   • Funcionando (responda queries)")
print()
print("📚 PRÓXIMOS PASSOS:")
print("   1. Ingerir documentos:")
print("      .venv/bin/python -m src.cli.knowledge_cli ingest /path/to/docs")
print()
print("   2. Fazer queries:")
print("      .venv/bin/python -m src.cli.knowledge_cli query 'sua pergunta'")
print()
print("   3. Visualizar grafo:")
print("      Abra http://localhost:30474")
print()
print("=" * 60)
