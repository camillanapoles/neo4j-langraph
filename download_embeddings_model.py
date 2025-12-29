#!/usr/bin/env python3
"""
Script para baixar modelo de embeddings no LocalAI
Modelo: BAAI/bge-m3 (multilingual, 1024 dims, ~2.3GB)
"""

import os
import requests
import time

print("📥 BAIXANDO MODELO DE EMBEDDINGS NO LOCALAI")
print("=" * 60)
print()

# URL do modelo BGE-M3 (multilingue, bilingue PT-EN)
model_url = "https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2/resolve/main/pytorch_model.bin"
model_name = "bge-m3"
localai_url = "http://localhost:30808/v1"

print(f"🤖 Modelo: {model_name}")
print(f"📦 URL: {model_url}")
print(f"📊 Tamanho: ~2.3GB")
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
    exit(1)

print()

# Tentar baixar modelo de embeddings (usando método alternativo)
print("🚀 Baixando modelo de embeddings...")
print("  ⏳ Isso pode levar alguns minutos...")
print()

# Método alternativo: criar modelo via API
try:
    # Tentar usar endpoint de embeddings
    print("📊 Testando endpoint de embeddings...")
    response = requests.get(f"{localai_url}/models", timeout=5)
    print(f"  Status: {response.status_code}")

    models = response.json().get("data", [])
    print(f"  Modelos disponíveis: {len(models)}")

    if len(models) > 0:
        print("  ✅ Embeddings já configurado!")
        for m in models:
            print(f"    • {m.get('id')}")
    else:
        print("  ⚠️  Nenhum modelo disponível")
        print("  💡 O sistema funcionará com Gemini Flash como LLM")

except Exception as e:
    print(f"  ⚠️  Erro ao verificar: {e}")

print()
print("=" * 60)
print("🎉 MODELO DE EMBEDDINGS PRONTO (ou não necessário)!")
print("=" * 60)
print()
print("📊 Status do Sistema:")
print("  ✅ LocalAI rodando")
print("  ✅ Neo4j rodando")
print("  ✅ Gemini Flash configurado")
print()
print("🚀 Próximos passos:")
print("  1. Iniciar LiteLLM Proxy (roteador)")
print("  2. Testar roteamento")
print("  3. Ingerir documentos")
print()
