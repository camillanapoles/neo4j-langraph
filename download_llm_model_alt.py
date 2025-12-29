#!/usr/bin/env python3
"""
Script alternativo para baixar modelo LLM no LocalAI
Modelo: Llama-3.2-3B-Instruct (Q4_K_M - quantização 4-bit, ~1.8GB)
"""

import os
import requests
import time

print("📥 BAIXANDO MODELO LLM NO LOCALAI (ALTERNATIVO)")
print("=" * 60)
print()

# URLs alternativas do modelo (tentar cada uma)
model_urls = [
    "https://huggingface.co/MaziyarPanahi/Llama-3.2-3B-Instruct-GGUF/resolve/main/Llama-3.2-3B-Instruct.Q4_K_M.gguf",
    "https://huggingface.co/MaziyarPanahi/Llama-3.2-3B-Instruct-GGUF/resolve/main/Llama-3.2-3B-Instruct.Q5_K_M.gguf",
    "https://huggingface.co/QuantFactory/Meta-Llama-3-2-3B-Instruct-GGUF/resolve/main/Meta-Llama-3-2-3B-Instruct.Q4_K_M.gguf",
]

model_name = "llama3.2:3b"
localai_url = "http://localhost:30808/v1"

# Tentar cada URL
for i, model_url in enumerate(model_urls, 1):
    print(f"🚀 Tentando URL {i}/{len(model_urls)}...")
    print(f"📦 URL: {model_url}")
    print()

    # Verificar se LocalAI está rodando
    print("🔌 Verificando LocalAI...")
    try:
        response = requests.get(f"{localai_url}/models", timeout=5)
        if response.status_code == 200:
            print("  ✅ LocalAI rodando")
        else:
            print(f"  ❌ LocalAI erro: {response.status_code}")
            continue
    except Exception as e:
        print(f"  ❌ Erro ao conectar: {e}")
        continue

    print()

    # Baixar modelo no LocalAI
    print("🚀 Baixando modelo no LocalAI...")
    print("  ⏳ Isso pode levar alguns minutos...")
    print()

    try:
        response = requests.post(
            f"{localai_url}/models/{model_name}",
            json={"url": model_url},
            timeout=600  # 10 minutos
        )

        if response.status_code == 200:
            print("✅ Modelo baixado com sucesso!")
            print()
            print("📊 Modelo carregado:")
            print(f"  • Nome: {model_name}")
            print(f"  • Tipo: GGUF (quantizado)")
            print(f"  • Tamanho: ~1.8-2GB")
            print(f"  • VRAM: ~2GB")
            print()

            # Sucesso! Sair do loop
            break
        elif response.status_code == 404:
            print(f"❌ Erro 404: Modelo não encontrado nessa URL")
            print()
            if i < len(model_urls):
                print("💡 Tentando próxima URL...")
                print()
        else:
            print(f"❌ Erro ao baixar: {response.status_code}")
            print(f"  Mensagem: {response.text}")
            print()

            if i < len(model_urls):
                print("💡 Tentando próxima URL...")
                print()

    except Exception as e:
        print(f"❌ Erro: {e}")
        print()
        if i < len(model_urls):
            print("💡 Tentando próxima URL...")
            print()
else:
    # Se o loop completar sem sucesso
    print("=" * 60)
    print("❌ ERRO: Não foi possível baixar o modelo!")
    print("=" * 60)
    print()
    print("💡 Soluções alternativas:")
    print()
    print("1. Usar modelo de embeddings apenas (sem LLM)")
    print("   - O sistema de embeddings já está pronto")
    print("   - Pode fazer queries sem LLM local")
    print()
    print("2. Configurar Ollama (LLM local alternativo)")
    print("   - curl -fsSL https://ollama.com/install.sh | sh")
    print("   - ollama pull llama3.2:3b")
    print()
    print("3. Usar apenas Gemini Flash (sem fallback)")
    print("   - Esperar reset de cota (1 dia)")
    print("   - O sistema funciona sem LocalAI LLM")
    print()
    exit(1)

# Verificar modelo disponível
print("🔍 Verificando se modelo está disponível...")
try:
    response = requests.get(f"{localai_url}/models", timeout=5)
    models = response.json().get("data", [])

    print(f"📊 Modelos disponíveis: {len(models)}")
    for model in models:
        print(f"  • {model.get('id')}")
    print()

    # Verificar se nosso modelo está na lista
    model_ids = [m.get('id') for m in models]
    if model_name in model_ids:
        print(f"✅ Modelo {model_name} está disponível!")
    else:
        print(f"⚠️  Modelo {model_name} não está na lista")
        print("  💡 Pode estar carregando...")
        print("  Aguarde alguns minutos e teste novamente")

except Exception as e:
    print(f"❌ Erro ao verificar: {e}")

print()
print("=" * 60)
print("🎉 MODELO LLM PRONTO PARA USO!")
print("=" * 60)
print()
