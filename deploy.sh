#!/bin/bash
# Script para deploy com Buildah + K3S

set -e

echo "🚀 Neo4j Langraph - Buildah + K3S Setup"
echo "=========================================="
echo ""

# Verificar K3S
if ! command -v k3s &> /dev/null; then
    echo "❌ K3S não encontrado. Instale com:"
    echo "   curl -sfL https://get.k3s.io | sh -"
    exit 1
fi

# Verificar Buildah
if ! command -v buildah &> /dev/null; then
    echo "❌ Buildah não encontrado. Instale com:"
    echo "   sudo apt-get install buildah  # Debian/Ubuntu"
    echo "   ou: sudo dnf install buildah  # Fedora/RHEL"
    exit 1
fi

# Verificar kubectl
if ! command -v kubectl &> /dev/null; then
    echo "⚠️ kubectl não encontrado. Usando k3s kubectl..."
    KUBECTL="k3s kubectl"
else
    KUBECTL="kubectl"
fi

# Verificar k9s (opcional)
if command -v k9s &> /dev/null; then
    echo "✅ k9s encontrado"
    K9S_AVAILABLE=true
else
    echo "⚠️ k9s não encontrado. Instale para melhor gestão:"
    echo "   https://k9scli.io/"
    K9S_AVAILABLE=false
fi

echo ""
echo "📦 Criando namespace..."
$KUBECTL create namespace neo4j-langraph --dry-run=client -o yaml | $KUBECTL apply -f -

echo ""
echo "🚀 Deploy do Neo4j..."
$KUBECTL apply -f k8s/neo4j/neo4j-deployment.yaml

echo ""
echo "⏳ Aguardando Neo4j ficar pronto..."
$KUBECTL wait --for=condition=available -n neo4j-langraph deployment/neo4j --timeout=120s

echo ""
echo "✅ Deploy completo!"
echo ""
echo "📊 Status:"
$KUBECTL get pods -n neo4j-langraph
echo ""

# Obter NodePort
HTTP_PORT=$($KUBECTL get svc neo4j -n neo4j-langraph -o jsonpath='{.spec.ports[0].nodePort}')
BOLT_PORT=$($KUBECTL get svc neo4j -n neo4j-langraph -o jsonpath='{.spec.ports[1].nodePort}')

echo "🔌 Neo4j disponível em:"
echo "   HTTP:  http://localhost:$HTTP_PORT"
echo "   BOLT:  bolt://localhost:$BOLT_PORT"
echo ""
echo "   Credenciais:"
echo "   Usuário: neo4j"
echo "   Senha:   password"
echo ""

if [ "$K9S_AVAILABLE" = true ]; then
    echo "💡 Para monitorar com k9s:"
    echo "   k9s -n neo4j-langraph"
    echo ""
fi

echo "🧪 Testar conexão:"
echo "   .venv/bin/python test_system.py"
echo ""
