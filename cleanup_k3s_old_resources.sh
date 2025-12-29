#!/bin/bash
# Script para limpar recursos antigos do K3S (mais de 20 dias)

set -e

echo "🧹 LIMPEZA DE RECURSOS ANTIGOS DO K3S"
echo "========================================"
echo ""

echo "🔍 Buscando namespaces com mais de 20 dias..."
echo ""

# Listar namespaces com idade
kubectl get namespaces 2>&1 | grep -v "NAME\|kube-\|default\|neo4j-langraph" | while read ns age; do
    if [ "$ns" != "NAMESPACE" ]; then
        echo "   - $ns (idade: $age)"
    fi
done

echo ""
echo "🔍 Buscando PVs soltos (sem claim)..."
echo ""

kubectl get pv --all-namespaces 2>&1 | grep "Released" | while read pv cap access reclaim policy age; do
    echo "   - $pv (solto, idade: $age)"
done

echo ""
echo "🗑️  Deletando namespaces antigos..."
echo ""

# Deletar claude-openspecs (28 dias)
kubectl delete namespace claude-openspecs --force --grace-period=0 2>&1 || echo "   ⚠️ claude-openspecs já deletado ou não existe"

# Deletar traefik (53 dias)
kubectl delete namespace traefik --force --grace-period=0 2>&1 || echo "   ⚠️ traefik já deletado ou não existe"

echo ""
echo "🗑️  Deletando PVs soltos (Released)..."
echo ""

kubectl get pv --all-namespaces 2>&1 | grep "Released" | while read pv cap access reclaim policy age; do
    echo "   - Deletando $pv..."
    kubectl delete pv "$pv" --force --grace-period=0 2>&1 || echo "     ⚠️ Erro ao deletar $pv"
done

echo ""
sleep 5
echo "📊 STATUS APÓS LIMPEZA:"
echo ""

kubectl get namespaces 2>&1 | grep -v "kube-" | head -10
echo ""
kubectl get pv --all-namespaces 2>&1 | grep -v "kube-" | head -10

echo ""
echo "✅ LIMPEZA CONCLUÍDA!"
echo ""
