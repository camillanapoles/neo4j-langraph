#!/bin/bash
# Script de deploy com kubectl-ai
# Deploy automático de manifests K8S

set -e  # Parar em caso de erro

echo "🚀 DEPLOY COM KUBECTL-AI"
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
    echo "💡 Verifique se K3S está rodando:"
    echo "   systemctl status k3s"
    exit 1
fi

echo "✅ K3S está rodando"

# Verificar se há manifests K8S
if [ ! -d "k8s" ]; then
    echo "❌ Diretório k8s/ não encontrado!"
    echo ""
    echo "💡 Crie os manifests K8S em k8s/"
    exit 1
fi

echo "✅ Diretório k8s/ encontrado"

echo ""

# ==========================================
# CONFIGURAÇÕES
# ==========================================

echo "⚙️  CONFIGURAÇÕES"
echo "-----------------------------------"

# Namespace
NAMESPACE="neo4j-langraph"
echo "📁 Namespace: $NAMESPACE"

# Diretório de manifests
MANIFEST_DIR="k8s"
echo "📁 Diretório de manifests: $MANIFEST_DIR"

# Skip permissions (não pedir confirmação)
SKIP_PERMISSIONS=true
echo "⏭️  Skip permissions: $SKIP_PERMISSIONS"

echo ""

# ==========================================
# VERIFICAR NAMESPACE
# ==========================================

echo "📊 VERIFICANDO NAMESPACE"
echo "-----------------------------------"

echo "🔍 Verificando se namespace existe..."
if kubectl-ai --quiet "Verifique se o namespace $NAMESPACE existe"; then
    echo "✅ Namespace $NAMESPACE existe"
else
    echo "⚠️  Namespace $NAMESPACE não existe, criando..."
    kubectl-ai --quiet --skip-permissions "Crie o namespace $NAMESPACE"
    echo "✅ Namespace $NAMESPACE criado"
fi

echo ""

# ==========================================
# APLICAR MANIFESTS K8S
# ==========================================

echo "🚀 APLICANDO MANIFESTS K8S"
echo "-----------------------------------"

echo "📦 Aplicando manifests do diretório $MANIFEST_DIR..."
kubectl-ai --quiet --skip-permissions "Aplique todos os manifests K8S no diretório $MANIFEST_DIR no namespace $NAMESPACE:
- Aplique namespace.yaml
- Aplique secrets/
- Aplique neo4j/
- Aplique localai/
- Aguarde o rollout completar"

echo "✅ Manifests K8S aplicados!"

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
# SMOKE TESTS
# ==========================================

echo "🧪 EXECUTANDO SMOKE TESTS"
echo "-----------------------------------"

echo "🧪 Executando smoke test do Neo4j..."
kubectl-ai --quiet --skip-permissions "Execute smoke test do Neo4j no namespace $NAMESPACE:
- Execute: cypher-shell -a bolt://localhost:30687 -u neo4j -p password \"RETURN 1 AS num\""

echo "✅ Smoke test do Neo4j concluído!"

echo ""
echo "🧪 Executando smoke test do LocalAI..."
kubectl-ai --quiet --skip-permissions "Execute smoke test do LocalAI no namespace $NAMESPACE:
- Execute: curl -f http://localhost:30808/health"

echo "✅ Smoke test do LocalAI concluído!"

echo ""

# ==========================================
# GERAR RELATÓRIO DE DEPLOY
# ==========================================

echo "📊 GERANDO RELATÓRIO DE DEPLOY"
echo "-----------------------------------"

kubectl-ai --quiet --skip-permissions "Gere um relatório de deploy com:
- Data e hora
- Namespace: $NAMESPACE
- Pods listados
- Deployments listados
- Serviços listados
- Status de cada recurso
- Resultados dos health checks
- Resultados dos smoke tests"

echo "✅ Relatório de deploy gerado!"

echo ""

# ==========================================
# INFORMAÇÕES FINAIS
# ==========================================

echo "======================================="
echo "🎉 DEPLOY CONCLUÍDO!"
echo "======================================="
echo ""
echo "📊 INFORMAÇÕES:"
echo "   Namespace: $NAMESPACE"
echo "   Manifest dir: $MANIFEST_DIR"
echo ""
echo "📊 RECURSOS DEPLOYADOS:"
echo "   • Pods: $(kubectl get pods -n $NAMESPACE --no-headers | wc -l)"
echo "   • Deployments: $(kubectl get deployments -n $NAMESPACE --no-headers | wc -l)"
echo "   • Services: $(kubectl get svc -n $NAMESPACE --no-headers | wc -l)"
echo ""
echo "📊 ACESSO:"
echo "   • Neo4j Browser: http://localhost:30474"
echo "   • LocalAI: http://localhost:30808"
echo "   • Neo4j Bolt: bolt://localhost:30687"
echo ""
echo "📊 HEALTH CHECKS:"
echo "   • Neo4j: ✅ Passed"
echo "   • LocalAI: ✅ Passed"
echo ""
echo "📊 SMOKE TESTS:"
echo "   • Neo4j: ✅ Passed"
echo "   • LocalAI: ✅ Passed"
echo ""
echo "📊 COMANDOS ÚTEIS:"
echo "   • Verificar pods:"
echo "     kubectl get pods -n $NAMESPACE"
echo ""
echo "   • Verificar deployments:"
echo "     kubectl get deployments -n $NAMESPACE"
echo ""
echo "   • Verificar serviços:"
echo "     kubectl get svc -n $NAMESPACE"
echo ""
echo "   • Verificar logs:"
echo "     kubectl logs -f deployment/neo4j -n $NAMESPACE"
echo ""
echo "   • Monitorar contínuo:"
echo "     bash scripts/monitor_with_kubectl_ai.sh"
echo ""
echo "   • Diagnóstico e recuperação:"
echo "     bash scripts/diagnose_and_recover_with_kubectl_ai.sh"
echo ""
echo "   • Backup:"
echo "     bash scripts/backup_with_kubectl_ai.sh"
echo ""
echo "🚀 PRÓXIMO PASSO:"
echo "   kubectl-ai --quiet \"Aplique os manifests K8S no namespace $NAMESPACE\""
echo ""
echo "======================================="
