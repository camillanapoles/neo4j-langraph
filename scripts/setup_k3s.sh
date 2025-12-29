#!/bin/bash
# Script de setup do K3S (Kubernetes local)
# Melhores práticas de DevOps

set -e  # Parar em caso de erro

echo "🚀 SETUP DO K3S (KUBERNETES LOCAL)"
echo "======================================="
echo ""

# ==========================================
# PRÉ-REQUISITOS
# ==========================================

echo "📋 VERIFICANDO PRÉ-REQUISITOS"
echo "-----------------------------------"

# Verificar se está rodando como root
if [ "$EUID" -ne 0 ]; then
    echo "❌ Este script deve ser executado como root (sudo)!"
    echo ""
    echo "💡 Execute:"
    echo "   sudo $0"
    exit 1
fi

# Verificar se é Linux
if [ "$(uname)" != "Linux" ]; then
    echo "❌ Este script é suportado apenas em Linux!"
    echo ""
    echo "💡 Para macOS, use:"
    echo "   brew install k3s"
    echo ""
    echo "   Para Windows, use:"
    echo "   winget install Rancher.k3s"
    exit 1
fi

echo "✅ Sistema operacional: Linux"

# Verificar se K3S já está instalado
if command -v k3s &> /dev/null; then
    K3S_VERSION=$(k3s --version)
    echo "✅ K3S já está instalado: $K3S_VERSION"
    echo ""
    read -p "Deseja reinstalar K3S? [y/N] " REINSTALL
    if [[ ! $REINSTALL =~ ^[Yy]$ ]]; then
        echo "❌ Abortando..."
        exit 0
    fi
    echo ""
    echo "🔄 Reinstalando K3S..."
    systemctl stop k3s 2>/dev/null || true
    systemctl disable k3s 2>/dev/null || true
    rm -rf /etc/rancher/k3s
    rm -f /usr/local/bin/k3s
    rm -f /usr/local/bin/kubectl
fi

echo ""

# ==========================================
# CONFIGURAÇÕES
# ==========================================

echo "⚙️  CONFIGURAÇÕES DO K3S"
echo "-----------------------------------"

# Diretório de dados
K3S_DATA_DIR="/mnt/container-data/projects/k3s"
echo "📁 Diretório de dados: $K3S_DATA_DIR"

# Porta do API server
K3S_API_PORT="6443"
echo "📡 Porta do API server: $K3S_API_PORT"

# Criação de PVs
PV_DIR="/mnt/container-data/projects"
echo "📁 Diretório de PVs: $PV_DIR"

echo ""

# ==========================================
# INSTALAR K3S
# ==========================================

echo "📦 INSTALANDO K3S"
echo "-----------------------------------"

# Criar diretórios necessários
mkdir -p "$K3S_DATA_DIR"
mkdir -p "$PV_DIR"
chown -R cnmfs:cnmfs "$K3S_DATA_DIR"
chown -R cnmfs:cnmfs "$PV_DIR"

echo "✅ Diretórios criados"

# Instalar K3S
echo "📦 Baixando e instalando K3S..."
curl -sfL https://get.k3s.io | sh -

# Configurar K3S
echo "🔧 Configurando K3S..."
cat > /etc/systemd/system/k3s.service << EOFK3S
[Unit]
Description=Lightweight Kubernetes
Documentation=https://k3s.io
After=network-online.target
Wants=network-online.target

[Service]
Type=notify
EnvironmentFile=-/etc/default/%i
EnvironmentFile=-/etc/sysconfig/%i
ExecStart=/usr/local/bin/k3s \
    server \
    --data-dir=$K3S_DATA_DIR \
    --write-kubeconfig-mode=644 \
    --disable traefik \
    --disable local-storage \
    --disable-cloud-controller \
    --disable metrics-server \
    --kubelet-arg=config=/dev/null \
    --kubelet-arg=max-pods=110 \
    --bind-address=0.0.0.0 \
    --https-listen-port=$K3S_API_PORT \
    --node-name=pop-os.local

KillMode=process
Delegate=yes
LimitNOFILE=1048576
LimitNPROC=infinity
LimitCORE=infinity
TasksMax=infinity
TimeoutStartSec=0
Restart=always
RestartSec=5s

[Install]
WantedBy=multi-user.target
EOFK3S

# Recarregar systemd
systemctl daemon-reload

# Habilitar K3S
systemctl enable k3s

# Iniciar K3S
systemctl start k3s

echo "✅ K3S instalado e iniciado"

# Aguardar K3S iniciar
echo "⏳ Aguardando K3S iniciar..."
for i in {1..30}; do
    if systemctl is-active --quiet k3s; then
        echo "✅ K3S está rodando"
        break
    fi
    echo "   Aguardando... ($i/30)"
    sleep 2
done

if ! systemctl is-active --quiet k3s; then
    echo "❌ K3S não iniciou corretamente!"
    echo ""
    echo "💡 Ver logs:"
    echo "   journalctl -u k3s -n 50"
    exit 1
fi

echo ""

# ==========================================
# INSTALAR KUBECTL
# ==========================================

echo "📦 INSTALANDO KUBECTL"
echo "-----------------------------------"

# K3S já instala o kubectl
# Mas vamos criar um link simbólico para facilitar
ln -sf /usr/local/bin/k3s /usr/local/bin/kubectl

echo "✅ kubectl instalado"

# Verificar kubectl
echo "📊 Verificando kubectl..."
KUBECTL_VERSION=$(kubectl version --client --short 2>/dev/null | grep Client | awk '{print $3}')
echo "✅ kubectl versão: $KUBECTL_VERSION"

# Criar diretório .kube para o usuário
mkdir -p /home/cnmfs/.kube
cp /etc/rancher/k3s/k3s.yaml /home/cnmfs/.kube/config
chown -R cnmfs:cnmfs /home/cnmfs/.kube
chmod 600 /home/cnmfs/.kube/config

echo "✅ KUBECONFIG configurado para usuário cnmfs"

echo ""

# ==========================================
# CONFIGURAR HELM (OPCIONAL)
# ==========================================

echo "📦 INSTALANDO HELM (OPCIONAL)"
echo "-----------------------------------"

if ! command -v helm &> /dev/null; then
    echo "📦 Baixando e instalando Helm..."
    curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
    chmod +x get_helm.sh
    ./get_helm.sh
    rm get_helm.sh
    
    HELM_VERSION=$(helm version --short 2>/dev/null)
    echo "✅ Helm instalado: $HELM_VERSION"
else
    HELM_VERSION=$(helm version --short 2>/dev/null)
    echo "✅ Helm já está instalado: $HELM_VERSION"
fi

echo ""

# ==========================================
# CRIAR NAMESPACE
# ==========================================

echo "📦 CRIANDO NAMESPACE neo4j-langraph"
echo "-----------------------------------"

kubectl create namespace neo4j-langraph --dry-run=client -o yaml | kubectl apply -f -

echo "✅ Namespace neo4j-langraph criado"

echo ""

# ==========================================
# CRIAR PVs MANUAIS
# ==========================================

echo "📦 CRIANDO PVs MANUAIS"
echo "-----------------------------------"

# PV para Neo4j
cat > /tmp/neo4j-pv.yaml << 'EOFPV'
apiVersion: v1
kind: PersistentVolume
metadata:
  name: neo4j-pv
spec:
  capacity:
    storage: 10Gi
  accessModes:
    - ReadWriteOnce
  persistentVolumeReclaimPolicy: Retain
  storageClassName: manual
  hostPath:
    path: /mnt/container-data/projects/neo4j-langraph/neo4j
EOFPV

kubectl apply -f /tmp/neo4j-pv.yaml
echo "✅ PV neo4j-pv criado"

# PV para LocalAI
cat > /tmp/localai-pv.yaml << 'EOFPV'
apiVersion: v1
kind: PersistentVolume
metadata:
  name: localai-pv
spec:
  capacity:
    storage: 50Gi
  accessModes:
    - ReadWriteOnce
  persistentVolumeReclaimPolicy: Retain
  storageClassName: manual
  hostPath:
    path: /mnt/container-data/projects/neo4j-langraph/models
EOFPV

kubectl apply -f /tmp/localai-pv.yaml
echo "✅ PV localai-pv criado"

echo ""

# ==========================================
# VERIFICAR K3S
# ==========================================

echo "🔍 VERIFICANDO K3S"
echo "-----------------------------------"

# Verificar nós
echo "📊 Nós:"
kubectl get nodes

# Verificar pods
echo ""
echo "📊 Pods:"
kubectl get pods --all-namespaces

# Verificar serviços
echo ""
echo "📊 Serviços:"
kubectl get svc --all-namespaces

# Verificar PVs
echo ""
echo "📊 Persistent Volumes:"
kubectl get pv

echo ""

# ==========================================
# INFORMAÇÕES FINAIS
# ==========================================

echo "======================================"
echo "🎉 K3S CONFIGURADO COM SUCESSO!"
echo "======================================"
echo ""
echo "📊 INFORMAÇÕES:"
echo "   K3S versão: $(k3s --version | cut -d' ' -f2)"
echo "   kubectl versão: $(kubectl version --client --short 2>/dev/null | grep Client | awk '{print $3}')"
echo "   Helm versão: $(helm version --short 2>/dev/null || echo 'N/A')"
echo "   Data dir: $K3S_DATA_DIR"
echo "   PV dir: $PV_DIR"
echo ""
echo "📊 COMANDOS ÚTEIS:"
echo "   • Verificar status:"
echo "     systemctl status k3s"
echo ""
echo "   • Verificar logs:"
echo "     journalctl -u k3s -f"
echo ""
echo "   • Listar nós:"
echo "     kubectl get nodes"
echo ""
echo "   • Listar pods:"
echo "     kubectl get pods --all-namespaces"
echo ""
echo "   • Listar serviços:"
echo "     kubectl get svc --all-namespaces"
echo ""
echo "   • Verificar cluster info:"
echo "     kubectl cluster-info"
echo ""
echo "   • Verificar kubeconfig:"
echo "     cat /etc/rancher/k3s/k3s.yaml"
echo ""
echo "🚀 PRÓXIMO PASSO:"
echo "   1. Instalar GitHub Actions Self-Hosted Runner:"
echo "      bash scripts/setup_runner.sh"
echo ""
echo "   2. Deployar aplicações:"
echo "      kubectl apply -f k8s/base/"
echo ""
echo "   3. Acessar aplicações:"
echo "      kubectl port-forward svc/neo4j 7474:7474"
echo "      http://localhost:7474"
echo ""
echo "======================================"
