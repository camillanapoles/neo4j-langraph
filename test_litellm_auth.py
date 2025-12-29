#!/usr/bin/env python3
"""
Script de teste do LiteLLM com API key correta
"""

import requests
import json

print("=" * 60)
print("🧪 LITELLM - TESTE COM API KEY")
print("=" * 60)
print()

# Master key configurada no litellm_config.yaml
master_key = "sk-litellm-master-key"

print("📊 Configuração:")
print(f"  • API Key: {master_key}")
print(f"  • URL: http://localhost:4000/v1")
print()

# 1. Verificar health (sem auth)
print("1️⃣  Verificando health (sem auth)...")
try:
    r = requests.get('http://localhost:4000/health', timeout=5)
    print(f"   Status: {r.status_code}")
    if r.status_code == 200:
        print("   ✅ LiteLLM rodando!")
except Exception as e:
    print(f"   ❌ Erro: {e}")
print()

# 2. Listar modelos (com auth)
print("2️⃣  Listando modelos (com auth)...")
headers = {
    "Authorization": f"Bearer {master_key}"
}
try:
    r = requests.get('http://localhost:4000/v1/models', headers=headers, timeout=5)
    print(f"   Status: {r.status_code}")
    if r.status_code == 200:
        models = r.json()
        print(f"   ✅ Modelos disponíveis: {len(models.get('data', []))}")
        for m in models.get('data', [])[:3]:
            print(f"      • {m.get('id')}")
    else:
        print(f"   ❌ Erro: {r.text[:100]}")
except Exception as e:
    print(f"   ❌ Erro: {e}")
print()

# 3. Testar chat completion (com auth)
print("3️⃣  Testando chat completion (com auth)...")
payload = {
    "model": "gemini-flash",
    "messages": [
        {"role": "user", "content": "Olá! Responda em 1 frase: Qual seu nome?"}
    ],
    "temperature": 0.7,
    "max_tokens": 50
}
headers = {
    "Authorization": f"Bearer {master_key}",
    "Content-Type": "application/json"
}
try:
    r = requests.post('http://localhost:4000/v1/chat/completions', headers=headers, json=payload, timeout=30)
    print(f"   Status: {r.status_code}")
    if r.status_code == 200:
        response = r.json()
        print("   ✅ Chat completion funcionando!")
        content = response['choices'][0]['message']['content']
        print(f"   📝 Resposta: {content[:100]}")
        model_used = response.get('model', 'unknown')
        print(f"   📊 Modelo usado: {model_used}")
    else:
        print(f"   ❌ Erro: {r.text[:200]}")
except Exception as e:
    print(f"   ❌ Erro: {e}")
print()

print("=" * 60)
print("🎉 TESTE DO LITELM CONCLUÍDO!")
print("=" * 60)
