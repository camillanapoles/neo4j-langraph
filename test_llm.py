#!/usr/bin/env python3
"""
Script de teste do LLM (Gemini Flash 2.5)
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

# Carregar variáveis de ambiente
load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key or api_key == "your-google-api-key-here":
    print("❌ ERRO: GOOGLE_API_KEY não configurada!")
    print("   Adicione ao .env:")
    print("   GOOGLE_API_KEY=AIza...")
    exit(1)

print("🧠 LLM: Testando Gemini Flash 2.5...")
print(f"🔑 API Key: {api_key[:10]}...{api_key[-10:]}")

try:
    # Criar cliente OpenAI (Google usa formato OpenAI)
    client = OpenAI(
        api_key=api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )
    
    # Fazer uma query simples
    response = client.chat.completions.create(
        model="gemini-2.0-flash-exp",
        messages=[
            {"role": "user", "content": "Olá! Qual é o seu nome? Responda em português."}
        ],
        temperature=0.7,
        max_tokens=100
    )
    
    print("✅ LLM funcionando!")
    print(f"📝 Resposta: {response.choices[0].message.content}")
    
except Exception as e:
    print(f"❌ Erro: {e}")
    exit(1)

print("\n🎉 SISTEMA AI COMPLETO TESTADO!")
