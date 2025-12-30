#!/bin/bash
# Script de setup do K3S com kubectl-ai
# Orquestração automática de recursos K8S

set -e  # Parar em caso de erro

echo "🚀 SETUP DO K3S COM KUBECTL-AI"
echo "======================================="
echo ""

# ==========================================
# PRÉ-REQUISITOS
# ==========================================

echo "📋 VERIFICANDO PRÉ-REQUISITOS"
echo "-----------------------------------"

# Verificar se kubectl-ai está instalado
if ! command -v kubectl-ai &> /dev/null; then
    echo "❌ kubectl-ai não está instalado!"
    echo ""
    echo "💡 Instale kubectl-ai:"
    echo "   https://github.com/kubectl-ai/kubectl-ai"
    exit 1
fi

echo "✅ kubectl-ai está instalado"

# Verificar se K3S está rodando
if ! command -v k3s &> /dev/null || ! k3s kubectl cluster-info &> /dev/null; then
    echo "❌ K3S não está rodando!"
    echo ""
    echo "💡 Instale K3S:"
    echo "   curl -sfL https://get.k3s.io | sh -"
    exit 1
fi

echo "✅ K3S está rodando"

echo ""

# ==========================================
# CONFIGURAÇÕES
# ==========================================

echo "⚙️  CONFIGURAÇÕES"
echo "-----------------------------------"

# Namespace
NAMESPACE="neo4j-langraph"
echo "📁 Namespace: $NAMESPACE"

# Diretório de dados
DATA_DIR="/mnt/container-data/projects"
echo "📁 Diretório de dados: $DATA_DIR"

echo ""

# ==========================================
# CRIAR NAMESPACE
# ==========================================

echo "📦 CRIANDO NAMESPACE"
echo "-----------------------------------"

echo "🚀 Criando namespace: $NAMESPACE..."
kubectl-ai --quiet --skip-permissions "Crie o namespace $NAMESPACE"

echo "✅ Namespace $NAMESPACE criado!"

echo ""

# ==========================================
# CRIAR SECRETS
# ==========================================

echo "🔒 CRIANDO SECRETS"
echo "-----------------------------------"

echo "🔒 Criando secret neo4j-credentials..."
kubectl-ai --quiet --skip-permissions "Crie o secret neo4j-credentials no namespace $NAMESPACE com:
- username=neo4j
- password=password"

echo "✅ Secret neo4j-credentials criado!"

echo ""
echo "🔒 Criando secret google-api-key..."
kubectl-ai --quiet --skip-permissions "Crie o secret google-api-key no namespace $NAMESPACE com:
- api-key=AIzaSyClqjAVBkWnSVnv2Gj2xbUSCEPeeBG7bac"

echo "✅ Secret google-api-key criado!"

echo ""
echo "🔒 Criando secret litellm-master-key..."
kubectl-ai --quiet --skip-permissions "Crie o secret litellm-master-key no namespace $NAMESPACE com:
- master-key=sk-litellm-master-key"

echo "✅ Secret litellm-master-key criado!"

echo ""

# ==========================================
# CRIAR PVs
# ==========================================

echo "💾 CRIANDO PVS"
echo "-----------------------------------"

echo "💾 Criando PV neo4j-data-pv..."
kubectl-ai --quiet --skip-permissions "Crie um PersistentVolume neo4j-data-pv com:
- Capacity: 5Gi
- Access Modes: ReadWriteOnce
- Storage Class: local-path
- Host Path: $DATA_DIR/neo4j-langraph/neo4j
- Reclaim Policy: Retain"

echo "✅ PV neo4j-data-pv criado!"

echo ""
echo "💾 Criando PV localai-models-pv..."
kubectl-ai --quiet --skip-permissions "Crie um PersistentVolume localai-models-pv com:
- Capacity: 20Gi
- Access Modes: ReadWriteOnce
- Storage Class: local-path
- Host Path: $DATA_DIR/neo4j-langraph/models
- Reclaim Policy: Retain"

echo "✅ PV localai-models-pv criado!"

echo ""

# ==========================================
# CRIAR PVCs
# ==========================================

echo "💾 CRIANDO PVCS"
echo "-----------------------------------"

echo "💾 Criando PVC neo4j-data-pvc..."
kubectl-ai --quiet --skip-permissions "Crie um PersistentVolumeClaim neo4j-data-pvc no namespace $NAMESPACE com:
- Storage Request: 5Gi
- Access Mode: ReadWriteOnce
- Storage Class: local-path"

echo "✅ PVC neo4j-data-pvc criado!"

echo ""
echo "💾 Criando PVC localai-models-pvc..."
kubectl-ai --quiet --skip-permissions "Crie um PersistentVolumeClaim localai-models-pvc no namespace $NAMESPACE com:
- Storage Request: 20Gi
- Access Mode: ReadWriteOnce
- Storage Class: local-path"

echo "✅ PVC localai-models-pvc criado!"

echo ""

# ==========================================
# CRIAR DEPLOYMENT NEO4J
# ==========================================

echo "🚀 CRIANDO DEPLOYMENT NEO4J"
echo "-----------------------------------"

echo "🚀 Criando deployment neo4j..."
kubectl-ai --quiet --skip-permissions "Crie um deployment neo4j no namespace $NAMESPACE com:
- Imagem: docker.io/neo4j:4.4-community
- Réplicas: 1
- Portas: 7474 (http), 7687 (bolt)
- Recursos: request 512Mi memory, 250m cpu; limit 2Gi memory, 1000m cpu
- Volume: PVC neo4j-data-pvc montado em /data
- Secrets: NEO4J_AUTH do secret neo4j-credentials
- Environment Variables:
  - NEO4J_dbms_memory_heap_max__size: 512m
  - NEO4J_dbms_memory_pagecache_size: 512m"

echo "✅ Deployment neo4j criado!"

echo ""
echo "🚀 Criando service neo4j..."
kubectl-ai --quiet --skip-permissions "Crie um service neo4j no namespace $NAMESPACE com:
- Type: NodePort
- Selector: app=neo4j
- Ports: 7474:30474, 7687:30687"

echo "✅ Service neo4j criado!"

echo ""

# ==========================================
# CRIAR DEPLOYMENT LOCALAI
# ==========================================

echo "🚀 CRIANDO DEPLOYMENT LOCALAI"
echo "-----------------------------------"

echo "🚀 Criando deployment localai..."
kubectl-ai --quiet --skip-permissions "Crie um deployment localai no namespace $NAMESPACE com:
- Imagem: localai/localai:latest
- Réplicas: 1
- Portas: 8080 (http)
- Recursos: request 4Gi memory, 500m cpu; limit 8Gi memory, 2000m cpu
- Volume: PVC localai-models-pvc montado em /models
- GPU: nvidia.com/gpu: 1
- Environment Variables:
  - ENABLE_HTTP_HEADERS: true"

echo "✅ Deployment localai criado!"

echo ""
echo "🚀 Criando service localai..."
kubectl-ai --quiet --skip-permissions "Crie um service localai no namespace $NAMESPACE com:
- Type: NodePort
- Selector: app=localai
- Ports: 8080:30808"

echo "✅ Service localai criado!"

echo ""

# ==========================================
# AGUARDAR ROLLOUT
# ==========================================

echo "⏳ AGUARDANDO ROLLOUT"
echo "-----------------------------------"

echo "⏳ Aguardando rollout do neo4j..."
kubectl-ai --quiet --skip-permissions "Aguarde o rollout do deployment neo4j no namespace $NAMESPACE completar"

echo "✅ Rollout do neo4j completado!"

echo ""
echo "⏳ Aguardando rollout do localai..."
kubectl-ai --quiet --skip-permissions "Aguarde o rollout do deployment localai no namespace $NAMESPACE completar"

echo "✅ Rollout do localai completado!"

echo ""

# ==========================================
# VERIFICAR STATUS
# ==========================================

echo "🔍 VERIFICANDO STATUS"
echo "-----------------------------------"

echo "📊 Verificando pods..."
kubectl-ai --quiet --skip-permissions "Liste todos os pods no namespace $NAMESPACE e reporte o status"

echo ""
echo "📊 Verificando deployments..."
kubectl-ai --quiet --skip-permissions "Liste todos os deployments no namespace $NAMESPACE e reporte o status"

echo ""
echo "📊 Verificando serviços..."
kubectl-ai --quiet --skip-permissions "Liste todos os serviços no namespace $NAMESPACE e reporte o status"

echo ""

# ==========================================
# HEALTH CHECKS
# ==========================================

echo "🧪 EXECUTANDO HEALTH CHECKS"
echo "-----------------------------------"

echo "🧪 Verificando saúde do Neo4j..."
kubectl-ai --quiet --skip-permissions "Execute health checks no pod neo4j no namespace $NAMESPACE:
- Verifique se o pod está rodando
- Verifique se o serviço neo4j está acessível
- Execute: cypher-shell -u neo4j -p password \"RETURN 1 AS num\""

echo "✅ Health check do Neo4j concluído!"

echo ""
echo "🧪 Verificando saúde do LocalAI..."
kubectl-ai --quiet --skip-permissions "Execute health checks no pod localai no namespace $NAMESPACE:
- Verifique se o pod está rodando
- Verifique se o serviço localai está acessível
- Execute: curl -f http://localhost:8080/health"

echo "✅ Health check do LocalAI concluído!"

echo ""

# ==========================================
# INFORMAÇÕES FINAIS
# ==========================================

echo "======================================="
echo "🎉 SETUP DO K3S CONCLUÍDO!"
echo "======================================="
echo ""
echo "📊 INFORMAÇÕES:"
echo "   Namespace: $NAMESPACE"
echo "   Data dir: $DATA_DIR"
echo ""
echo "📊 RECURSOS CRIADOS:"
echo "   • Namespace: $NAMESPACE"
echo "   • Secrets: neo4j-credentials, google-api-key, litellm-master-key"
echo "   • PVs: neo4j-data-pv, localai-models-pv"
echo "   • PVCs: neo4j-data-pvc, localai-models-pvc"
echo "   • Deployments: neo4j, localai"
echo "   • Services: neo4j, localai"
echo ""
echo "📊 ACESSO:"
echo "   • Neo4j Browser: http://localhost:30474"
echo "   • LocalAI: http://localhost:30808"
echo "   • Neo4j Bolt: bolt://localhost:30687"
echo ""
echo "📊 COMANDOS ÚTEIS:"
echo "   • Verificar pods:"
echo "     kubectl get pods -n $NAMESPACE"
echo ""
echo "   • Verificar logs:"
echo "     kubectl logs -f deployment/neo4j -n $NAMESPACE"
echo ""
echo "   • Verificar status:"
echo "     kubectl-ai --quiet \"Liste todos os pods no namespace $NAMESPACE\""
echo ""
echo "🚀 PRÓXIMO PASSO:"
echo "   kubectl-ai --quiet \"Aplique os manifests K8S no namespace $NAMESPACE\""
echo ""
echo "======================================="
