#!/bin/bash
# Script de setup do GitHub Actions Self-Hosted Runner
# Melhores práticas de DevOps

set -e  # Parar em caso de erro

echo "🚀 SETUP DO GITHUB ACTIONS SELF-HOSTED RUNNER"
echo "==================================================="
echo ""

# ==========================================
# PRÉ-REQUISITOS
# ==========================================

echo "📋 VERIFICANDO PRÉ-REQUISITOS"
echo "-----------------------------------"

# Verificar se gh CLI está instalado
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

echo "✅ GitHub CLI está instalado"

# Verificar se está autenticado no GitHub
if ! gh auth status &> /dev/null; then
    echo "❌ Não está autenticado no GitHub!"
    echo ""
    echo "💡 Faça login:"
    echo "   gh auth login"
    echo ""
    echo "   Escolha:"
    echo "   1. GitHub.com"
    echo "   2. SSH"
    echo "   3. Login com web browser"
    exit 1
fi

echo "✅ Autenticado no GitHub"

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

echo "⚙️  CONFIGURAÇÕES DO RUNNER"
echo "-----------------------------------"

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

# Nome do runner
RUNNER_NAME="${1:-pop-os-runner}"
echo "📝 Nome do runner: $RUNNER_NAME"

# Labels do runner
RUNNER_LABELS="${2:-self-hosted,pop-os,k3s}"
echo "🏷️  Labels: $RUNNER_LABELS"
echo ""

# Diretório do runner
RUNNER_DIR="$HOME/actions-runner"
echo "📁 Diretório do runner: $RUNNER_DIR"
echo ""

# ==========================================
# CRIAR TOKEN DO RUNNER
# ==========================================

echo "🔑 CRIANDO TOKEN DO RUNNER"
echo "-----------------------------------"

echo "📦 Criando token de registro..."
RUNNER_TOKEN=$(gh api --method POST \
  -H "Accept: application/vnd.github+json" \
  "/repos/$REPO/actions/runners/registration-token" \
  -q .token)

if [ -z "$RUNNER_TOKEN" ]; then
    echo "❌ Erro ao criar token do runner!"
    exit 1
fi

echo "✅ Token criado: ${RUNNER_TOKEN:0:10}...${RUNNER_TOKEN: -10}"
echo ""

# ==========================================
# BAIXAR RUNNER
# ==========================================

echo "📥 BAIXANDO GITHUB ACTIONS RUNNER"
echo "-----------------------------------"

# Criar diretório do runner
mkdir -p "$RUNNER_DIR"
cd "$RUNNER_DIR"

# Obter versão mais recente do runner
LATEST_VERSION=$(gh api /repos/actions/runner/releases/latest -q .tag_name)
echo "📦 Versão mais recente: $LATEST_VERSION"

# Baixar runner
RUNNER_FILE="actions-runner-linux-x64-$(echo $LATEST_VERSION | sed 's/v//').tar.gz"
echo "📥 Baixando: $RUNNER_FILE"

if [ ! -f "$RUNNER_FILE" ]; then
    curl -o "$RUNNER_FILE" -L \
      "https://github.com/actions/runner/releases/download/$LATEST_VERSION/actions-runner-linux-x64-$(echo $LATEST_VERSION | sed 's/v//').tar.gz"
else
    echo "✅ Runner já baixado"
fi

# Extrair runner
echo "📦 Extraindo runner..."
if [ ! -d "runner" ]; then
    tar xzf "$RUNNER_FILE"
    mkdir -p runner
    mv * runner/ 2>/dev/null || true
    mv runner/* .
    rmdir runner 2>/dev/null || true
else
    echo "✅ Runner já extraído"
fi

echo "✅ Runner baixado e extraído"
echo ""

# ==========================================
# CONFIGURAR RUNNER
# ==========================================

echo "⚙️  CONFIGURANDO RUNNER"
echo "-----------------------------------"

echo "🔧 Configurando runner..."

./config.sh \
  --url "https://github.com/$REPO" \
  --token "$RUNNER_TOKEN" \
  --name "$RUNNER_NAME" \
  --labels "$RUNNER_LABELS" \
  --work "/tmp/_work" \
  --replace

echo "✅ Runner configurado"
echo ""

# ==========================================
# INSTALAR RUNNER COMO SERVIÇO
# ==========================================

echo "🔧 INSTALANDO RUNNER COMO SERVIÇO"
echo "-----------------------------------"

echo "📦 Instalando serviço..."
sudo ./svc.sh install

echo "✅ Serviço instalado"
echo ""

# ==========================================
# INICIAR RUNNER
# ==========================================

echo "🚀 INICIANDO RUNNER"
echo "-----------------------------------"

echo "📦 Iniciando serviço..."
sudo ./svc.sh start

echo "✅ Runner iniciado!"
echo ""

# ==========================================
# VERIFICAR RUNNER
# ==========================================

echo "🔍 VERIFICANDO RUNNER"
echo "-----------------------------------"

echo "📊 Verificando status do serviço..."
if sudo ./svc.sh status; then
    echo "✅ Runner está rodando"
else
    echo "❌ Runner não está rodando!"
    echo ""
    echo "💡 Ver logs:"
    echo "   sudo journalctl -u actions.runner.* -f"
    exit 1
fi

echo ""

echo "📊 Verificando runner no GitHub..."
sleep 5  # Aguardar o runner registrar no GitHub

RUNNERS=$(gh api /repos/$REPO/actions/runners -q '.runners[] | .name')
if echo "$RUNNERS" | grep -q "$RUNNER_NAME"; then
    echo "✅ Runner registrado no GitHub: $RUNNER_NAME"
else
    echo "⚠️  Runner ainda não registrado no GitHub"
    echo "💡 Aguarde alguns minutos e verifique:"
    echo "   gh api /repos/$REPO/actions/runners"
fi

echo ""

# ==========================================
# INFORMAÇÕES FINAIS
# ==========================================

echo "======================================================"
echo "🎉 GITHUB ACTIONS SELF-HOSTED RUNNER CONFIGURADO!"
echo "======================================================"
echo ""
echo "📊 INFORMAÇÕES:"
echo "   Repositório: $REPO"
echo "   Runner: $RUNNER_NAME"
echo "   Labels: $RUNNER_LABELS"
echo "   Diretório: $RUNNER_DIR"
echo ""
echo "📊 COMANDOS ÚTEIS:"
echo "   • Verificar status:"
echo "     sudo ./svc.sh status"
echo ""
echo "   • Reiniciar runner:"
echo "     sudo ./svc.sh restart"
echo ""
echo "   • Parar runner:"
echo "     sudo ./svc.sh stop"
echo ""
echo "   • Ver logs:"
echo "     sudo journalctl -u actions.runner.* -f"
echo ""
echo "   • Atualizar runner:"
echo "     cd $RUNNER_DIR"
echo "     curl -o actions-runner-linux-x64.tar.gz -L ..."
echo "     tar xzf actions-runner-linux-x64.tar.gz"
echo "     ./svc.sh stop"
echo "     ./bin/installdependencies.sh"
echo "     ./svc.sh start"
echo ""
echo "   • Remover runner:"
echo "     ./config.sh remove --token $TOKEN"
echo ""
echo "🚀 PRÓXIMO PASSO:"
echo "   git push origin main"
echo ""
echo "📝 O GitHub Actions vai:"
echo "   1. Executar testes (workflow: Tests)"
echo "   2. Deployar no dev (workflow: Deploy to Dev - Self-Hosted)"
echo "   3. Executar backup diário (workflow: Backup)"
echo ""
echo "🔍 Monitorar runner:"
echo "   gh api /repos/$REPO/actions/runners"
echo ""
echo "======================================================"
