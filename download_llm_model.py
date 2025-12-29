#!/usr/bin/env python3
"""
Script para baixar modelo LLM no LocalAI
Modelo: Llama-3.2-3B-Instruct (Q4_K_M - quantização 4-bit, ~1.8GB)
"""

import os
import requests
import time

print("📥 BAIXANDO MODELO LLM NO LOCALAI")
print("=" * 60)
print()

# URL do modelo (GGUF quantizado)
model_url = "https://huggingface.co/MaziyarPanahi/Llama-3.2-3B-Instruct-GGUF/resolve/main/Llama-3.2-3B-Instruct.Q4_K_M.gguf"
model_name = "llama3.2:3b"
localai_url = "http://localhost:30808/v1"

print(f"🤖 Modelo: {model_name}")
print(f"📦 URL: {model_url}")
print(f"📊 Tamanho: ~1.8GB (Q4_K_M quantização)")
print()

# Verificar se LocalAI está rodando
print("🔌 Verificando LocalAI...")
try:
    response = requests.get(f"{localai_url}/models", timeout=5)
    if response.status_code == 200:
        print("  ✅ LocalAI rodando")
    else:
        print(f"  ❌ LocalAI erro: {response.status_code}")
        exit(1)
except Exception as e:
    print(f"  ❌ Erro ao conectar: {e}")
    print("  💡 Inicie o LocalAI:")
    print("     kubectl get pods -n neo4j-langraph")
    exit(1)

print()

# Baixar modelo no LocalAI
print("🚀 Baixando modelo no LocalAI...")
print("  ⏳ Isso pode levar alguns minutos...")
print()

try:
    response = requests.post(
        f"{localai_url}/models/{model_name}",
        json={"url": model_url},
        timeout=300  # 5 minutos
    )

    if response.status_code == 200:
        print("✅ Modelo baixado com sucesso!")
        print()
        print("📊 Modelo carregado:")
        print(f"  • Nome: {model_name}")
        print(f"  • Tipo: GGUF (quantizado)")
        print(f"  • Tamanho: ~1.8GB")
        print(f"  • VRAM: ~2GB")
        print()
    else:
        print(f"❌ Erro ao baixar: {response.status_code}")
        print(f"  Mensagem: {response.text}")
        exit(1)

except Exception as e:
    print(f"❌ Erro: {e}")
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
print("🎮 Modelo está pronto para ser usado via LiteLLM:")
print("  • Endpoint: http://localhost:30808/v1")
print("  • Model ID: localai/llama3.2:3b")
print()
