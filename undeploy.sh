#!/bin/bash
# Script para limpar recursos K3S

set -e

if ! command -v k3s &> /dev/null; then
    KUBECTL="kubectl"
else
    KUBECTL="k3s kubectl"
fi

echo "🧹 Limpando recursos do Neo4j Langraph..."
echo ""

echo "🗑️ Removendo namespace neo4j-langraph..."
$KUBECTL delete namespace neo4j-langraph --ignore-not-found=true

echo "🗑️ Removendo PVCs órfãos..."
$KUBECTL delete pvc -n neo4j-langraph --all --ignore-not-found=true

echo ""
echo "✅ Limpeza concluída!"
echo ""
echo "💡 Para ver recursos restantes:"
echo "   k9s"
echo ""
