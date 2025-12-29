#!/bin/bash
# Script de monitoramento contínuo com kubectl-ai
# Monitoramento automático de pods, deployments, serviços

set -e  # Parar em caso de erro

echo "📊 MONITORAMENTO CONTÍNUO COM KUBECTL-AI"
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

echo ""

# ==========================================
# CONFIGURAÇÕES
# ==========================================

echo "⚙️  CONFIGURAÇÕES"
echo "-----------------------------------"

# Namespace
NAMESPACE="neo4j-langraph"
echo "📁 Namespace: $NAMESPACE"

# Intervalo de monitoramento (segundos)
INTERVAL=60
echo "⏱️  Intervalo: $INTERVAL segundos"

echo ""

# ==========================================
# LOOP DE MONITORAMENTO
# ==========================================

echo "📊 INICIANDO MONITORAMENTO CONTÍNUO"
echo "======================================="
echo ""

trap "echo '🛑 Monitoramento interrompido'; exit 0" INT

while true; do
    # ==========================================
    # MONITORAMENTO DE PODS
    # ==========================================
    
    echo "📊 MONITORAMENTO DE PODS ($(date))"
    echo "-----------------------------------"
    
    kubectl-ai --quiet --skip-permissions "Verifique a saúde de todos os pods no namespace $NAMESPACE e reporte quaisquer problemas"
    
    echo ""
    
    # ==========================================
    # MONITORAMENTO DE DEPLOYMENTS
    # ==========================================
    
    echo "📊 MONITORAMENTO DE DEPLOYMENTS ($(date))"
    echo "-----------------------------------"
    
    kubectl-ai --quiet --skip-permissions "Verifique o status de todos os deployments no namespace $NAMESPACE e reporte quaisquer problemas"
    
    echo ""
    
    # ==========================================
    # MONITORAMENTO DE SERVIÇOS
    # ==========================================
    
    echo "📊 MONITORAMENTO DE SERVIÇOS ($(date))"
    echo "-----------------------------------"
    
    kubectl-ai --quiet --skip-permissions "Verifique o status de todos os serviços no namespace $NAMESPACE e reporte quaisquer problemas"
    
    echo ""
    
    # ==========================================
    # MONITORAMENTO DE PVCS
    # ==========================================
    
    echo "📊 MONITORAMENTO DE PVCS ($(date))"
    echo "-----------------------------------"
    
    kubectl-ai --quiet --skip-permissions "Verifique o status de todos os PVCs no namespace $NAMESPACE e reporte quaisquer problemas"
    
    echo ""
    
    # ==========================================
    # DIAGNÓSTICO DE PROBLEMAS
    # ==========================================
    
    echo "🔍 DIAGNÓSTICO DE PROBLEMAS ($(date))"
    echo "-----------------------------------"
    
    kubectl-ai --quiet --skip-permissions "Analise todos os recursos no namespace $NAMESPACE e identifique quaisquer problemas ou anomalias"
    
    echo ""
    
    # ==========================================
    # AGUARDAR INTERVALO
    # ==========================================
    
    echo "⏳ Aguardando $INTERVAL segundos antes do próximo ciclo..."
    echo "======================================="
    echo ""
    
    sleep $INTERVAL
done
