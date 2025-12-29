#!/bin/bash
# Script para iniciar o proxy LiteLLM
# Roteia entre Gemini Flash 2.5 (primário) e LocalAI (secundário)

echo "🤖 INICIANDO LITELLM PROXY..."
echo "========================================"
echo ""

# Carregar variáveis de ambiente
source .env.litellm

echo "📊 Configuração:"
echo "  • Modelo Primário:  gemini/gemini-2.0-flash-exp"
echo "  • Modelo Secundário: localai/llama3.2:3b"
echo "  • Estratégia: usage-based-routing"
echo "  • Fallback: localai/llama3.2:3b"
echo ""

# Verificar se LocalAI está rodando
echo "🔌 Verificando LocalAI..."
if curl -s http://localhost:30808/v1/models > /dev/null; then
    echo "  ✅ LocalAI rodando (http://localhost:30808)"
else
    echo "  ❌ LocalAI não está rodando!"
    echo "  💡 Inicie o LocalAI:"
    echo "     kubectl get pods -n neo4j-langraph"
    exit 1
fi

echo ""

# Iniciar LiteLLM Proxy
echo "🚀 Iniciando LiteLLM Proxy na porta 4000..."
echo "  URL: http://localhost:4000"
echo "  Health: http://localhost:4000/health"
echo "  Models: http://localhost:4000/v1/models"
echo ""

# Iniciar em background (para não bloquear o terminal)
litellm --config litellm_config.yaml --port 4000 --host 0.0.0.0
