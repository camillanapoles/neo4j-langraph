#!/bin/bash
# Script de diagnóstico e recuperação automática com kubectl-ai
# Diagnóstico de problemas e recuperação automática

set -e  # Parar em caso de erro

echo "🔍 DIAGNÓSTICO E RECUPERAÇÃO AUTOMÁTICA COM KUBECTL-AI"
echo "===================================================="
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

echo ""

# ==========================================
# CONFIGURAÇÕES
# ==========================================

echo "⚙️  CONFIGURAÇÕES"
echo "-----------------------------------"

# Namespace
NAMESPACE="neo4j-langraph"
echo "📁 Namespace: $NAMESPACE"

# Opções de recuperação
AUTO_RESTART_PODS=true
AUTO_RESTART_DEPLOYMENTS=true
AUTO_DELETE_CRASHED_PODS=true

echo "🔄 Auto-restart pods: $AUTO_RESTART_PODS"
echo "🔄 Auto-restart deployments: $AUTO_RESTART_DEPLOYMENTS"
echo "🗑️  Auto-delete crashed pods: $AUTO_DELETE_CRASHED_PODS"

echo ""

# ==========================================
# DIAGNÓSTICO INICIAL
# ==========================================

echo "🔍 DIAGNÓSTICO INICIAL"
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
# DIAGNÓSTICO DE PODS COM PROBLEMAS
# ==========================================

echo "🔍 DIAGNÓSTICO DE PODS COM PROBLEMAS"
echo "-----------------------------------"

echo "🔍 Analisando pods com problemas..."
kubectl-ai --quiet --skip-permissions "Analise todos os pods no namespace $NAMESPACE que estão em status Error, CrashLoopBackOff ou ImagePullBackOff e identifique o problema"

echo ""

# ==========================================
# RECUPERAÇÃO DE PODS
# ==========================================

echo "🔄 RECUPERAÇÃO DE PODS"
echo "-----------------------------------"

if [ "$AUTO_RESTART_PODS" = true ]; then
    echo "🔄 Reiniciando pods com problemas..."
    kubectl-ai --quiet --skip-permissions "Reinicie todos os pods no namespace $NAMESPACE que estão em status CrashLoopBackOff"
    echo "✅ Pods reiniciados!"
else
    echo "⏭️  Auto-restart de pods desabilitado"
fi

echo ""

# ==========================================
# RECUPERAÇÃO DE DEPLOYMENTS
# ==========================================

echo "🔄 RECUPERAÇÃO DE DEPLOYMENTS"
echo "-----------------------------------"

if [ "$AUTO_RESTART_DEPLOYMENTS" = true ]; then
    echo "🔄 Reiniciando deployments com problemas..."
    kubectl-ai --quiet --skip-permissions "Reinicie todos os deployments no namespace $NAMESPACE que estão em status de rollout falhado"
    echo "✅ Deployments reiniciados!"
else
    echo "⏭️  Auto-restart de deployments desabilitado"
fi

echo ""

# ==========================================
# LIMPEZA DE PODS ANTIGOS
# ==========================================

echo "🧹 LIMPEZA DE PODS ANTIGOS"
echo "-----------------------------------"

if [ "$AUTO_DELETE_CRASHED_PODS" = true ]; then
    echo "🧹 Deletando pods antigos..."
    kubectl-ai --quiet --skip-permissions "Dele todos os pods no namespace $NAMESPACE que estão em status Error ou CrashLoopBackOff há mais de 1 hora"
    echo "✅ Pods antigos deletados!"
else
    echo "⏭️  Auto-delete de pods desabilitado"
fi

echo ""

# ==========================================
# AGUARDAR ROLLOUT
# ==========================================

echo "⏳ AGUARDANDO ROLLOUT"
echo "-----------------------------------"

echo "⏳ Aguardando rollout do neo4j..."
kubectl-ai --quiet --skip-permissions "Aguarde o rollout do deployment neo4j no namespace $NAMESPACE completar"

echo ""
echo "⏳ Aguardando rollout do localai..."
kubectl-ai --quiet --skip-permissions "Aguarde o rollout do deployment localai no namespace $NAMESPACE completar"

echo ""

# ==========================================
# VERIFICAÇÃO PÓS-RECUPERAÇÃO
# ==========================================

echo "🔍 VERIFICAÇÃO PÓS-RECUPERAÇÃO"
echo "-----------------------------------"

echo "📊 Verificando pods..."
kubectl-ai --quiet --skip-permissions "Verifique a saúde de todos os pods no namespace $NAMESPACE e confirme que todos estão rodando"

echo ""
echo "📊 Verificando deployments..."
kubectl-ai --quiet --skip-permissions "Verifique o status de todos os deployments no namespace $NAMESPACE e confirme que todos estão ready"

echo ""

# ==========================================
# HEALTH CHECKS
# ==========================================

echo "🧪 EXECUTANDO HEALTH CHECKS"
echo "-----------------------------------"

echo "🧪 Verificando saúde do Neo4j..."
kubectl-ai --quiet --skip-permissions "Execute health checks no pod neo4j no namespace $NAMESPACE: Verifique se o pod está rodando e se o serviço neo4j está acessível"

echo ""
echo "🧪 Verificando saúde do LocalAI..."
kubectl-ai --quiet --skip-permissions "Execute health checks no pod localai no namespace $NAMESPACE: Verifique se o pod está rodando e se o serviço localai está acessível"

echo ""

# ==========================================
# RELATÓRIO FINAL
# ==========================================

echo "📊 RELATÓRIO FINAL"
echo "-----------------------------------"

echo "📊 Verificando status final de todos os recursos..."
kubectl-ai --quiet --skip-permissions "Verifique o status final de todos os recursos no namespace $NAMESPACE e gere um resumo"

echo ""

# ==========================================
# INFORMAÇÕES FINAIS
# ==========================================

echo "===================================================="
echo "🎉 DIAGNÓSTICO E RECUPERAÇÃO CONCLUÍDOS!"
echo "===================================================="
echo ""
echo "📊 INFORMAÇÕES:"
echo "   Namespace: $NAMESPACE"
echo "   Auto-restart pods: $AUTO_RESTART_PODS"
echo "   Auto-restart deployments: $AUTO_RESTART_DEPLOYMENTS"
echo "   Auto-delete crashed pods: $AUTO_DELETE_CRASHED_PODS"
echo ""
echo "📊 AÇÕES REALIZADAS:"
echo "   • Diagnóstico de pods com problemas"
echo "   • Diagnóstico de deployments com problemas"
echo "   • Reinício de pods com CrashLoopBackOff"
echo "   • Reinício de deployments com rollout falhado"
echo "   • Deleção de pods antigos (>1 hora)"
echo "   • Aguardar rollout dos deployments"
echo "   • Verificação pós-recuperação"
echo "   • Health checks (Neo4j, LocalAI)"
echo ""
echo "📊 COMANDOS ÚTEIS:"
echo "   • Verificar pods:"
echo "     kubectl get pods -n $NAMESPACE"
echo ""
echo "   • Verificar deployments:"
echo "     kubectl get deployments -n $NAMESPACE"
echo ""
echo "   • Verificar logs:"
echo "     kubectl logs -f deployment/neo4j -n $NAMESPACE"
echo ""
echo "   • Monitorar contínuo:"
echo "     bash scripts/monitor_with_kubectl_ai.sh"
echo ""
echo "🚀 PRÓXIMO PASSO:"
echo "   kubectl-ai --quiet \"Aplique os manifests K8S no namespace $NAMESPACE\""
echo ""
echo "===================================================="
