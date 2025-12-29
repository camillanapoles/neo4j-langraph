#!/bin/bash
# Script para configurar GitHub Secrets

echo "🔒 CONFIGURAR GITHUB SECRETS"
echo "================================="
echo ""
echo "Este script vai ajudar você a configurar os secrets no GitHub."
echo ""
echo "📋 PRÉ-REQUISITOS:"
echo "  1. Ter o GitHub CLI (gh) instalado"
echo "  2. Estar autenticado no GitHub"
echo "  3. Ter permissão de administrador no repositório"
echo ""

# Verificar se gh está instalado
if ! command -v gh &> /dev/null; then
    echo "❌ GitHub CLI (gh) não está instalado!"
    echo ""
    echo "💡 Instale com:"
    echo "   # Ubuntu/Debian"
    echo "   sudo apt install gh"
    echo ""
    echo "   # macOS"
    echo "   brew install gh"
    echo ""
    echo "   # Ver documentação:"
    echo "   https://cli.github.com/manual/installation"
    exit 1
fi

# Verificar se está autenticado
if ! gh auth status &> /dev/null; then
    echo "❌ Não está autenticado no GitHub!"
    echo ""
    echo "💡 Faça login:"
    echo "   gh auth login"
    exit 1
fi

# Obter repositório atual
REPO=$(git remote get-url origin 2>/dev/null | grep -oE 'github\.com[:/][^/]+/[^.]+' | sed 's/github.com[://]//g')

if [ -z "$REPO" ]; then
    echo "❌ Não foi possível identificar o repositório!"
    echo ""
    echo "💡 Use:"
    echo "   git remote add origin https://github.com/usuario/repo.git"
    exit 1
fi

echo "📊 Repositório: $REPO"
echo ""

# Criar KUBECONFIG secret
echo "🔧 1. Criando KUBECONFIG secret..."
echo "   Lendo KUBECONFIG..."
KUBECONFIG_B64=$(cat /etc/rancher/k3s/k3s.yaml | base64 -w 0)
echo "   ✅ KUBECONFIG codificado em base64!"
echo ""

echo "🔧 2. Adicionando secrets ao GitHub..."
echo ""

# KUBECONFIG
echo "   • KUBECONFIG..."
gh secret set KUBECONFIG -b "$KUBECONFIG_B64" -R "$REPO" || {
    echo "   ❌ Erro ao adicionar KUBECONFIG"
    exit 1
}
echo "   ✅ KUBECONFIG adicionado!"

# Neo4j Password
echo ""
echo "   • NEO4J_PASSWORD..."
read -sp "   Digite a senha do Neo4j (ou pressione Enter para usar 'password'): " NEO4J_PASSWORD
NEO4J_PASSWORD=${NEO4J_PASSWORD:-password}
gh secret set NEO4J_PASSWORD -b "$NEO4J_PASSWORD" -R "$REPO"
echo "   ✅ NEO4J_PASSWORD adicionado!"

# Google API Key
echo ""
echo "   • GOOGLE_API_KEY..."
read -sp "   Digite a Google API Key: " GOOGLE_API_KEY
gh secret set GOOGLE_API_KEY -b "$GOOGLE_API_KEY" -R "$REPO"
echo "   ✅ GOOGLE_API_KEY adicionado!"

# LiteLLM Master Key
echo ""
echo "   • LITELLM_MASTER_KEY..."
LITELLM_KEY=$(k3s kubectl get secret litellm-master-key -n neo4j-langraph -o jsonpath='{.data.master-key}' | base64 -d)
gh secret set LITELLM_MASTER_KEY -b "$LITELLM_KEY" -R "$REPO"
echo "   ✅ LITELLM_MASTER_KEY adicionado!"

echo ""
echo "================================="
echo "✅ GITHUB SECRETS CONFIGURADOS!"
echo "================================="
echo ""
echo "📊 Secrets adicionados:"
echo "   • KUBECONFIG"
echo "   • NEO4J_PASSWORD"
echo "   • GOOGLE_API_KEY"
echo "   • LITELLM_MASTER_KEY"
echo ""
echo "🚀 Próximo passo:"
echo "   git push origin main"
echo ""
echo "📝 O GitHub Actions vai:"
echo "   1. Executar testes (workflow: Tests)"
echo "   2. Deployar no K3S (workflow: Deploy to K3S)"
echo ""
echo "🔍 Monitorar actions:"
echo "   gh run list -R $REPO"
echo "   ou:"
echo "   gh run watch -R $REPO"
echo ""
