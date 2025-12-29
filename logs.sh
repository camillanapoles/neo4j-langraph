#!/bin/bash
# Script para logs do Neo4j

if ! command -v k3s &> /dev/null; then
    KUBECTL="kubectl"
else
    KUBECTL="k3s kubectl"
fi

echo "📋 Logs do Neo4j (Ctrl+C para sair)..."
echo ""

$KUBECTL logs -n neo4j-langraph -f deployment/neo4j --all-containers=true
