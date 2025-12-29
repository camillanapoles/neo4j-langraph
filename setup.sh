#!/bin/bash
# Script de setup definitivo com LocalAI + llama.cpp

set -e

echo "🚀 Setup Definitivo - LocalAI + llama.cpp"
echo "=============================================="
echo ""

# Verificar K3S
if ! command -v k3s &> /dev/null; then
    echo "❌ K3S não encontrado. Instale com:"
    echo "   curl -sfL https://get.k3s.io | sh -"
    exit 1
fi

# Verificar Buildah
if ! command -v buildah &> /dev/null; then
    echo "❌ Buildah não encontrado."
    exit 1
fi

echo "✅ Pré-requisitos verificados!"
echo ""

# Criar namespace
echo "📦 Criando namespace..."
if ! command -v k3s &> /dev/null; then
    KUBECTL="kubectl"
else
    KUBECTL="k3s kubectl"
fi

$KUBECTL create namespace neo4j-langraph --dry-run=client -o yaml | $KUBECTL apply -f -

# Baixar modelos
echo ""
echo "📦 Baixando modelos GGUF..."
./download_models.sh

echo ""
echo "🚀 Deploy do Neo4j + LocalAI..."
echo ""

# Deploy Neo4j
echo "   • Neo4j..."
$KUBECTL apply -f k8s/neo4j/neo4j-deployment.yaml

# Deploy LocalAI
echo "   • LocalAI (com GPU)..."
$KUBECTL apply -f k8s/localai/localai-deployment.yaml

echo ""
echo "⏳ Aguardando pods ficarem prontos..."

# Aguardar Neo4j
echo "   • Aguardando Neo4j..."
$KUBECTL wait --for=condition=available -n neo4j-langraph deployment/neo4j --timeout=120s

# Aguardar LocalAI
echo "   • Aguardando LocalAI..."
$KUBECTL wait --for=condition=available -n neo4j-langraph deployment/localai --timeout=180s

echo ""
echo "✅ Deploy completo!"
echo ""

# Copiar configuração
echo "📝 Configurando ambiente..."
cp .env.localai .env

echo "✅ Configuração .env criada (usa LocalAI + llama.cpp)"
echo ""

# Obter portas
NEO4J_HTTP=$($KUBECTL get svc neo4j -n neo4j-langraph -o jsonpath='{.spec.ports[0].nodePort}')
NEO4J_BOLT=$($KUBECTL get svc neo4j -n neo4j-langraph -o jsonpath='{.spec.ports[1].nodePort}')
LOCALAI=$($KUBECTL get svc localai -n neo4j-langraph -o jsonpath='{.spec.ports[0].nodePort}')

echo "🔌 Serviços disponíveis:"
echo "   Neo4j HTTP:  http://localhost:$NEO4J_HTTP"
echo "   Neo4j BOLT:  bolt://localhost:$NEO4J_BOLT"
echo "   LocalAI API: http://localhost:$LOCALAI"
echo ""

echo "📊 Status dos pods:"
$KUBECTL get pods -n neo4j-langraph
echo ""

echo "💡 Próximos passos:"
echo "1. Monitorar com k9s:"
echo "   k9s -n neo4j-langraph"
echo ""
echo "2. Ver logs:"
echo "   ./logs.sh"
echo ""
echo "3. Testar sistema:"
echo "   .venv/bin/python test_system.py"
echo ""
echo "🎉 Setup completo! Seu sistema está rodando:"
echo "   • Neo4j (grafo de conhecimento)"
echo "   • LocalAI (llama.cpp super otimizado em C++)"
echo "   • Ambos acelerados pela sua RTX 4070!"
echo ""
