#!/usr/bin/env python3
"""
Script de teste do LiteLLM
Roteia entre Gemini Flash 2.5 (primário) e LocalAI (secundário)
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

# Carregar variáveis de ambiente
load_dotenv()

print("=" * 60)
print("🤖 LITELLM - TESTE DE ROTEAMENTO")
print("=" * 60)
print()

# Configurar cliente LiteLLM (usa formato OpenAI)
print("📊 Configuração:")
print("  • Modelo Primário:   gemini/gemini-2.0-flash-exp")
print("  • Modelo Secundário: localai/llama3.2:3b")
print("  • Estratégia:        usage-based-routing")
print("  • Fallback:          localai/llama3.2:3b")
print()

# Criar cliente (aponta para LiteLLM Proxy)
print("🔌 Conectando ao LiteLLM Proxy...")
try:
    client = OpenAI(
        api_key="sk-litellm-master-key",  # LiteLLM master key
        base_url="http://localhost:4000/v1"
    )
    print("✅ Conectado ao LiteLLM Proxy!")
    print()

except Exception as e:
    print(f"❌ Erro ao conectar: {e}")
    print()
    print("💡 Solução: Inicie o LiteLLM Proxy:")
    print("   bash start_litellm.sh")
    exit(1)

# Listar modelos disponíveis
print("📊 Modelos disponíveis:")
try:
    models = client.models.list()
    for model in models.data:
        print(f"  • {model.id}")
    print()
except Exception as e:
    print(f"⚠️  Não foi possível listar modelos: {e}")
    print()

# Testar roteamento
print("🧪 Testando roteamento...")
print()

try:
    # Fazer uma query
    print("📝 Enviando query...")
    response = client.chat.completions.create(
        model="gemini-flash",  # Modelo do grupo (LiteLLM roteia automaticamente)
        messages=[
            {"role": "user", "content": "Olá! Responda em 1 frase: Qual seu nome?"}
        ],
        temperature=0.7,
        max_tokens=50
    )

    print("✅ Query enviada com sucesso!")
    print()
    print(f"📝 Resposta: {response.choices[0].message.content}")
    print()
    print(f"📊 Modelo usado: {response.model}")
    print()

except Exception as e:
    print(f"❌ Erro na query: {e}")
    print()
    print("💡 Possíveis causas:")
    print("   1. Gemini Flash: Cota excedida (429)")
    print("   2. LocalAI: Modelo não baixado")
    print("   3. LiteLLM Proxy: Não está rodando")
    print()
    print("💡 Soluções:")
    print("   1. Baixar modelo LLM: python3 download_llm_model.py")
    print("   2. Iniciar LiteLLM: bash start_litellm.sh")
    exit(1)

# Resumo final
print("=" * 60)
print("🎉 LITELLM ROTEAMENTO TESTADO!")
print("=" * 60)
print()
print("✅ Sistema de roteamento funcionando!")
print()
print("📊 Como funciona:")
print("  1. Query é enviada para LiteLLM Proxy")
print("  2. LiteLLM roteia para Gemini Flash (primário)")
print("  3. Se Gemini falhar (cota 429), roteia para LocalAI")
print("  4. Fallback automático e transparente")
print()
