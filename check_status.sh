#!/bin/bash
# Script de teste rápido para verificar tudo

set -e

echo "🧪 TESTE RÁPIDO DO SISTEMA"
echo "========================================"
echo ""

# 1. Verificar ambiente Python
echo "📦 1. Verificando ambiente Python..."
if [ -f ".venv/bin/python" ]; then
    echo "✅ Ambiente Python encontrado: .venv/"
    PYTHON=".venv/bin/python"
else
    echo "❌ Ambiente Python não encontrado!"
    echo "   Execute: uv venv"
    exit 1
fi
echo ""

# 2. Verificar dependências
echo "📚 2. Verificando dependências..."
if $PYTHON -c "import langchain" 2>/dev/null; then
    echo "✅ Dependências instaladas"
else
    echo "⚠️ Dependências podem não estar instaladas"
    echo "   Execute: uv pip install -e '.[dev]'"
fi
echo ""

# 3. Verificar K3S
echo "☸️  3. Verificando K3S..."
if command -v k3s &> /dev/null; then
    KUBECTL="k3s kubectl"
    echo "✅ K3S encontrado"
else
    KUBECTL="kubectl"
fi

if $KUBECTL get namespace neo4j-langraph &> /dev/null; then
    echo "✅ Namespace neo4j-langraph existe"
else
    echo "⚠️ Namespace neo4j-langraph não existe"
    echo "   Execute: ./setup.sh"
fi
echo ""

# 4. Verificar pods
echo "🐳 4. Verificando pods (K3S)..."
PODS=$($KUBECTL get pods -n neo4j-langraph --no-headers 2>/dev/null || echo "")
if [ -n "$PODS" ]; then
    echo "Pods encontrados:"
    echo "$PODS"
else
    echo "⚠️ Nenhum pod encontrado"
    echo "   Execute: ./setup.sh"
fi
echo ""

# 5. Verificar serviços
echo "🔌 5. Verificando serviços (K3S)..."
SERVICES=$($KUBECTL get svc -n neo4j-langraph --no-headers 2>/dev/null || echo "")
if [ -n "$SERVICES" ]; then
    echo "Serviços encontrados:"
    echo "$SERVICES"
else
    echo "⚠️ Nenhum serviço encontrado"
    echo "   Execute: ./setup.sh"
fi
echo ""

# 6. Verificar LocalAI (se rodando)
if echo "$PODS" | grep -q "localai"; then
    echo "🤖 6. LocalAI encontrado"

    # Verificar portas
    LOCALAI_PORT=$($KUBECTL get svc localai -n neo4j-langraph -o jsonpath='{.spec.ports[0].nodePort}' 2>/dev/null || echo "")

    if [ -n "$LOCALAI_PORT" ]; then
        echo "   🔌 LocalAI disponível em: http://localhost:$LOCALAI_PORT"
        echo "   📡 API Docs: http://localhost:$LOCALAI_PORT/docs"
    fi
fi
echo ""

# 7. Verificar Neo4j (se rodando)
if echo "$PODS" | grep -q "neo4j"; then
    echo "🗄️ 7. Neo4j encontrado"

    # Verificar portas
    NEO4J_HTTP=$($KUBECTL get svc neo4j -n neo4j-langraph -o jsonpath='{.spec.ports[0].nodePort}' 2>/dev/null || echo "")
    NEO4J_BOLT=$($KUBECTL get svc neo4j -n neo4j-langraph -o jsonpath='{.spec.ports[1].nodePort}' 2>/dev/null || echo "")

    if [ -n "$NEO4J_HTTP" ]; then
        echo "   🔌 Neo4j HTTP disponível em: http://localhost:$NEO4J_HTTP"
        echo "   🌐 Neo4j Browser: http://localhost:$NEO4J_HTTP"
        echo "   📊 Usuário: neo4j, Senha: password"
    fi

    if [ -n "$NEO4J_BOLT" ]; then
        echo "   🔌 Neo4j BOLT disponível em: bolt://localhost:$NEO4J_BOLT"
    fi
fi
echo ""

# 8. Verificar Google API Key
echo "🔑 8. Verificando Google API Key..."
if grep -q "your-google-api-key-here" .env 2>/dev/null; then
    echo "⚠️ Google API Key não configurada"
    echo "   Adicione no .env: GOOGLE_API_KEY=AIza..."
else
    echo "✅ Google API Key configurada"
fi
echo ""

# 9. Resumo e próximos passos
echo "========================================"
echo "📊 RESUMO"
echo "========================================"
echo ""

# Verificar se tudo está pronto para testar
READY=true

# Verificar pods rodando
if echo "$PODS" | grep -q "Running"; then
    echo "✅ Pods rodando"
else
    echo "❌ Pods não estão rodando"
    READY=false
fi

# Verificar API key
if ! grep -q "your-google-api-key-here" .env 2>/dev/null; then
    echo "✅ Google API Key configurada"
else
    echo "⚠️ Configure GOOGLE_API_KEY no .env"
    READY=false
fi

echo ""

if [ "$READY" = true ]; then
    echo "🎉 SISTEMA PRONTO PARA TESTAR!"
    echo ""
    echo "📋 PRÓXIMOS PASSOS:"
    echo ""
    echo "1. Testar configuração:"
    echo "   .venv/bin/python test_gemini_embeddings.py"
    echo ""
    echo "2. Ingerir documentos:"
    echo "   .venv/bin/python -m src.cli.knowledge_cli ingest /path/to/docs"
    echo ""
    echo "3. Fazer queries:"
    echo "   .venv/bin/python -m src.cli.knowledge_cli query 'Django'"
    echo ""
    echo "4. Ver grafo no Neo4j Browser:"
    echo "   Abra no navegador: http://localhost:30474"
    echo "   Usuário: neo4j, Senha: password"
    echo ""
    echo "5. Monitorar pods com k9s:"
    echo "   k9s -n neo4j-langraph"
    echo ""
else
    echo "⚠️ SISTEMA NÃO ESTÁ PRONTO"
    echo ""
    echo "📋 PRÓXIMOS PASSOS:"
    echo ""
    echo "1. Se pods não estão rodando:"
    echo "   ./setup.sh"
    echo ""
    echo "2. Se Google API Key não está configurada:"
    echo "   vim .env"
    echo "   Adicione: GOOGLE_API_KEY=AIza..."
    echo ""
fi

echo ""
echo "========================================"
