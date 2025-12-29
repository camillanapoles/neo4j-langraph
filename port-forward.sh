#!/bin/bash
# Script para port-forward para desenvolvimento local

if ! command -v k3s &> /dev/null; then
    KUBECTL="kubectl"
else
    KUBECTL="k3s kubectl"
fi

echo "🔌 Configurando port-forward para Neo4j..."
echo ""
echo "Neo4j HTTP:  http://localhost:7474"
echo "Neo4j BOLT:  bolt://localhost:7687"
echo ""
echo "Pressione Ctrl+C para parar"
echo ""

$KUBECTL port-forward -n neo4j-langraph svc/neo4j 7474:7474 7687:7687
