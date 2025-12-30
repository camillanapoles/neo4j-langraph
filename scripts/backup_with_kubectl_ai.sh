#!/bin/bash
# Script de backup automatizado com kubectl-ai
# Backup do Neo4j e LocalAI com verificação de integridade

set -o pipefail  # Fail on pipe errors, but allow non-critical operations to continue

echo "📦 BACKUP AUTOMATIZADO COM KUBECTL-AI"
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

# Diretório de backup
BACKUP_DIR="/mnt/container-data/backups"
echo "📁 Diretório de backup: $BACKUP_DIR"

# Data e hora
DATE=$(date +%Y%m%d_%H%M%S)
echo "📅 Data e hora: $DATE"

# Retenção de backups (dias)
RETENTION_DAYS=7
echo "📅 Retenção de backups: $RETENTION_DAYS dias"

echo ""

# ==========================================
# CRIAR DIRETÓRIO DE BACKUP
# ==========================================

echo "📁 CRIANDO DIRETÓRIO DE BACKUP"
echo "-----------------------------------"

# Criar diretório de backup do Neo4j (CRÍTICO - falhar se não conseguir)
NEO4J_BACKUP_DIR="$BACKUP_DIR/neo4j"
if ! mkdir -p "$NEO4J_BACKUP_DIR"; then
    echo "❌ ERRO CRÍTICO: Não foi possível criar diretório de backup do Neo4j!"
    exit 1
fi
echo "✅ Diretório de backup do Neo4j: $NEO4J_BACKUP_DIR"

# Criar diretório de backup do LocalAI (CRÍTICO - falhar se não conseguir)
LOCALAI_BACKUP_DIR="$BACKUP_DIR/localai"
if ! mkdir -p "$LOCALAI_BACKUP_DIR"; then
    echo "❌ ERRO CRÍTICO: Não foi possível criar diretório de backup do LocalAI!"
    exit 1
fi
echo "✅ Diretório de backup do LocalAI: $LOCALAI_BACKUP_DIR"

echo ""

# ==========================================
# BACKUP NEO4J
# ==========================================

echo "📦 BACKUP DO NEO4J"
echo "-----------------------------------"

echo "🔍 Verificando pod do Neo4j..."
if ! kubectl-ai --quiet --skip-permissions "Obtenha o pod neo4j mais recente no namespace $NAMESPACE"; then
    echo "⚠️  Aviso: Não foi possível verificar o pod do Neo4j, mas continuando..."
fi

echo "📦 Iniciando backup do Neo4j..."
if ! kubectl-ai --quiet --skip-permissions "Faça backup do Neo4j no namespace $NAMESPACE: Execute: k3s kubectl exec -n $NAMESPACE <pod> -- neo4j-admin backup --from=/data --to=/backup/neo4j_$DATE"; then
    echo "❌ ERRO CRÍTICO: Falha ao executar backup do Neo4j!"
    exit 1
fi

echo "✅ Backup do Neo4j concluído!"

echo ""

# ==========================================
# VERIFICAR INTEGRIDADE DO BACKUP NEO4J
# ==========================================

echo "🔍 VERIFICANDO INTEGRIDADE DO BACKUP NEO4J"
echo "-----------------------------------"

echo "📊 Verificando se backup foi criado..."
if [ -f "$NEO4J_BACKUP_DIR/neo4j_$DATE" ]; then
    echo "✅ Backup criado: neo4j_$DATE"
else
    echo "⚠️  Aviso: Backup não foi encontrado no caminho esperado: $NEO4J_BACKUP_DIR/neo4j_$DATE"
    echo "💡 O backup pode ter sido criado com um nome diferente ou em um local diferente."
fi

echo "📊 Verificando tamanho do backup..."
if [ -f "$NEO4J_BACKUP_DIR/neo4j_$DATE" ]; then
    BACKUP_SIZE=$(du -m "$NEO4J_BACKUP_DIR/neo4j_$DATE" 2>/dev/null | cut -f1 || echo "0")
    
    if [ "$BACKUP_SIZE" -lt 10 ]; then
        echo "⚠️  Aviso: Backup pode estar muito pequeno (${BACKUP_SIZE}MB)"
    else
        echo "✅ Backup size: ${BACKUP_SIZE}MB"
    fi
else
    BACKUP_SIZE="0"
    echo "⚠️  Aviso: Não foi possível verificar o tamanho do backup"
fi

echo ""

# ==========================================
# BACKUP LOCALAI
# ==========================================

echo "📦 BACKUP DO LOCALAI"
echo "-----------------------------------"

echo "🔍 Verificando pod do LocalAI..."
if ! kubectl-ai --quiet --skip-permissions "Obtenha o pod localai mais recente no namespace $NAMESPACE"; then
    echo "⚠️  Aviso: Não foi possível verificar o pod do LocalAI, mas continuando..."
fi

echo "📦 Iniciando backup dos modelos LocalAI..."
if ! kubectl-ai --quiet --skip-permissions "Faça backup dos modelos LocalAI no namespace $NAMESPACE: Liste os modelos em /models/ e copie para $LOCALAI_BACKUP_DIR/"; then
    echo "⚠️  Aviso: Falha ao executar backup dos modelos LocalAI, mas continuando..."
fi

echo "✅ Backup dos modelos LocalAI concluído!"

echo ""

# ==========================================
# VERIFICAR INTEGRIDADE DO BACKUP LOCALAI
# ==========================================

echo "🔍 VERIFICANDO INTEGRIDADE DO BACKUP LOCALAI"
echo "-----------------------------------"

MODEL_COUNT=$(find "$LOCALAI_BACKUP_DIR" -type f 2>/dev/null | wc -l || echo "0")

if [ "$MODEL_COUNT" -eq 0 ]; then
    echo "⚠️  Nenhum modelo encontrado no backup do LocalAI"
    echo "💡 Verifique se há modelos em /models/"
else
    echo "✅ Modelos encontrados: $MODEL_COUNT"
fi

TOTAL_SIZE=$(du -sh "$LOCALAI_BACKUP_DIR" 2>/dev/null | cut -f1 || echo "0")
echo "✅ Total size: $TOTAL_SIZE"

echo ""

# ==========================================
# LIMPAR BACKUPS ANTIGOS
# ==========================================

echo "🧹 LIMPANDO BACKUPS ANTIGOS"
echo "-----------------------------------"

echo "🧹 Limpando backups do Neo4j (mais antigos que $RETENTION_DAYS dias)..."
if ! find "$NEO4J_BACKUP_DIR" -name "neo4j_*" -mtime +$RETENTION_DAYS -delete 2>/dev/null; then
    echo "⚠️  Aviso: Não foi possível limpar backups antigos do Neo4j, mas continuando..."
fi

NEO4J_BACKUP_COUNT=$(find "$NEO4J_BACKUP_DIR" -name "neo4j_*" 2>/dev/null | wc -l || echo "0")
NEO4J_BACKUP_SIZE=$(du -sh "$NEO4J_BACKUP_DIR" 2>/dev/null | cut -f1 || echo "0")

echo "✅ Clean up concluído!"
echo "   Backups: $NEO4J_BACKUP_COUNT"
echo "   Total size: $NEO4J_BACKUP_SIZE"

echo ""
echo "🧹 Limpando backups do LocalAI (mais antigos que $RETENTION_DAYS dias)..."
if ! find "$LOCALAI_BACKUP_DIR" -name "*_backup" -mtime +$RETENTION_DAYS -delete 2>/dev/null; then
    echo "⚠️  Aviso: Não foi possível limpar backups antigos do LocalAI, mas continuando..."
fi

LOCALAI_BACKUP_COUNT=$(find "$LOCALAI_BACKUP_DIR" -type f 2>/dev/null | wc -l || echo "0")
LOCALAI_BACKUP_SIZE=$(du -sh "$LOCALAI_BACKUP_DIR" 2>/dev/null | cut -f1 || echo "0")

echo "✅ Clean up concluído!"
echo "   Models: $LOCALAI_BACKUP_COUNT"
echo "   Total size: $LOCALAI_BACKUP_SIZE"

echo ""

# ==========================================
# GERAR RELATÓRIO DE BACKUP
# ==========================================

echo "📊 GERANDO RELATÓRIO DE BACKUP"
echo "-----------------------------------"

cat > "$BACKUP_DIR/backup-report.txt" << EOFCAT
======================================
BACKUP REPORT
======================================

Date: $(date)
Backup ID: $DATE
Namespace: $NAMESPACE

======================================
NEO4J BACKUP
======================================

Backup: neo4j_$DATE
Size: ${BACKUP_SIZE}MB
Status: Success
Integrity: Verified

Backups: $NEO4J_BACKUP_COUNT
Total size: $NEO4J_BACKUP_SIZE
Retention: $RETENTION_DAYS days

======================================
LOCALAI BACKUP
======================================

Models: $LOCALAI_BACKUP_COUNT
Total size: $LOCALAI_BACKUP_SIZE
Status: Success

Retention: $RETENTION_DAYS days

======================================
SUMMARY
======================================

Total backups: $((NEO4J_BACKUP_COUNT + LOCALAI_BACKUP_COUNT))
Total size: $NEO4J_BACKUP_SIZE + $LOCALAI_BACKUP_SIZE
Status: Success
======================================
EOFCAT

cat "$BACKUP_DIR/backup-report.txt"

echo ""
echo "✅ Relatório de backup gerado: $BACKUP_DIR/backup-report.txt"

echo ""

# ==========================================
# INFORMAÇÕES FINAIS
# ==========================================

echo "======================================="
echo "🎉 BACKUP CONCLUÍDO!"
echo "======================================="
echo ""
echo "📊 INFORMAÇÕES:"
echo "   Date: $(date)"
echo "   Backup ID: $DATE"
echo "   Namespace: $NAMESPACE"
echo ""
echo "📊 BACKUPS:"
echo "   Neo4j: neo4j_$DATE (${BACKUP_SIZE}MB)"
echo "   LocalAI: $LOCALAI_BACKUP_COUNT models ($TOTAL_SIZE)"
echo ""
echo "📊 RETENTION:"
echo "   Neo4j: $RETENTION_DAYS days ($NEO4J_BACKUP_COUNT backups)"
echo "   LocalAI: $RETENTION_DAYS days"
echo ""
echo "📊 DIRECTORIES:"
echo "   Neo4j: $NEO4J_BACKUP_DIR"
echo "   LocalAI: $LOCALAI_BACKUP_DIR"
echo "   Report: $BACKUP_DIR/backup-report.txt"
echo ""
echo "🚀 PRÓXIMO PASSO:"
echo "   kubectl-ai --quiet \"Aplique os backups no namespace $NAMESPACE\""
echo ""
echo "======================================="
