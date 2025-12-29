# 🚀 Scripts de Automação com kubectl-ai

**Versão:** 1.0.0  
**Data:** 28/12/2024  
**Autor:** CNMFS

---

## 📋 ÍNDICE

1. [Descrição](#descrição)
2. [Scripts Disponíveis](#scripts-disponíveis)
3. [Como Usar](#como-usar)
4. [Dependências](#dependências)
5. [Exemplos de Uso](#exemplos-de-uso)

---

## 📝 DESCRIÇÃO

Este diretório contém **scripts de automação** que usam **kubectl-ai** para orquestrar e manter recursos do Kubernetes automaticamente!

---

## 📚 SCRIPTS DISPONÍVEIS

### **1. setup_k3s_with_kubectl_ai.sh**

**Descrição:** Script de setup do K3S com kubectl-ai

**O que faz:**
- ✅ Cria namespace `neo4j-langraph`
- ✅ Cria secrets (neo4j-credentials, google-api-key, litellm-master-key)
- ✅ Cria PVs (neo4j-data-pv, localai-models-pv)
- ✅ Cria PVCs (neo4j-data-pvc, localai-models-pvc)
- ✅ Cria deployments (neo4j, localai)
- ✅ Cria services (neo4j, localai)
- ✅ Aguarda rollout
- ✅ Executa health checks

**Como usar:**

```bash
bash scripts/setup_k3s_with_kubectl_ai.sh
```

**Saída esperada:**

```
🚀 SETUP DO K3S COM KUBECTL-AI
=======================================

📋 VERIFICANDO PRÉ-REQUISITOS
-----------------------------------
✅ kubectl-ai está instalado
✅ K3S está rodando

⚙️  CONFIGURAÇÕES
-----------------------------------
📁 Namespace: neo4j-langraph
📁 Diretório de dados: /mnt/container-data/projects

📦 CRIANDO NAMESPACE
-----------------------------------
✅ Namespace neo4j-langraph criado!

🔒 CRIANDO SECRETS
-----------------------------------
✅ Secret neo4j-credentials criado!
✅ Secret google-api-key criado!
✅ Secret litellm-master-key criado!

💾 CRIANDO PVS
-----------------------------------
✅ PV neo4j-data-pv criado!
✅ PV localai-models-pv criado!

💾 CRIANDO PVCS
-----------------------------------
✅ PVC neo4j-data-pvc criado!
✅ PVC localai-models-pvc criado!

🚀 CRIANDO DEPLOYMENT NEO4J
-----------------------------------
✅ Deployment neo4j criado!
✅ Service neo4j criado!

🚀 CRIANDO DEPLOYMENT LOCALAI
-----------------------------------
✅ Deployment localai criado!
✅ Service localai criado!

⏳ AGUARDANDO ROLLOUT
-----------------------------------
✅ Rollout do neo4j completado!
✅ Rollout do localai completado!

🔍 VERIFICANDO STATUS
-----------------------------------
📊 Verificando pods...
📊 Verificando deployments...
📊 Verificando serviços...

🧪 EXECUTANDO HEALTH CHECKS
-----------------------------------
✅ Health check do Neo4j concluído!
✅ Health check do LocalAI concluído!

=======================================
🎉 SETUP DO K3S CONCLUÍDO!
=======================================

📊 INFORMAÇÕES:
   Namespace: neo4j-langraph
   Data dir: /mnt/container-data/projects

📊 RECURSOS CRIADOS:
   • Namespace: neo4j-langraph
   • Secrets: neo4j-credentials, google-api-key, litellm-master-key
   • PVs: neo4j-data-pv, localai-models-pv
   • PVCs: neo4j-data-pvc, localai-models-pvc
   • Deployments: neo4j, localai
   • Services: neo4j, localai

📊 ACESSO:
   • Neo4j Browser: http://localhost:30474
   • LocalAI: http://localhost:30808
   • Neo4j Bolt: bolt://localhost:30687

📊 COMANDOS ÚTEIS:
   • Verificar pods:
     kubectl get pods -n neo4j-langraph

   • Verificar logs:
     kubectl logs -f deployment/neo4j -n neo4j-langraph

   • Verificar status:
     kubectl-ai --quiet "Liste todos os pods no namespace neo4j-langraph"

=======================================
```

---

### **2. backup_with_kubectl_ai.sh**

**Descrição:** Script de backup automatizado com kubectl-ai

**O que faz:**
- ✅ Backup do Neo4j
- ✅ Backup dos modelos LocalAI
- ✅ Verificação de integridade
- ✅ Limpeza de backups antigos (7 dias)
- ✅ Geração de relatório de backup

**Como usar:**

```bash
bash scripts/backup_with_kubectl_ai.sh
```

**Saída esperada:**

```
📦 BACKUP AUTOMATIZADO COM KUBECTL-AI
=======================================

📋 VERIFICANDO PRÉ-REQUISITOS
-----------------------------------
✅ kubectl-ai está instalado
✅ K3S está rodando

⚙️  CONFIGURAÇÕES
-----------------------------------
📁 Namespace: neo4j-langraph
📁 Diretório de backup: /mnt/container-data/backups
📅 Data e hora: 20241228_223000
📅 Retenção de backups: 7 dias

📁 CRIANDO DIRETÓRIO DE BACKUP
-----------------------------------
✅ Diretório de backup do Neo4j: /mnt/container-data/backups/neo4j
✅ Diretório de backup do LocalAI: /mnt/container-data/backups/localai

📦 BACKUP DO NEO4J
-----------------------------------
✅ Backup do Neo4j concluído!

🔍 VERIFICANDO INTEGRIDADE DO BACKUP NEO4J
-----------------------------------
✅ Backup size: 25MB

📦 BACKUP DO LOCALAI
-----------------------------------
✅ Backup dos modelos LocalAI concluído!

🔍 VERIFICANDO INTEGRIDADE DO BACKUP LOCALAI
-----------------------------------
✅ Modelos encontrados: 5
✅ Total size: 4.2GB

🧹 LIMPANDO BACKUPS ANTIGOS
-----------------------------------
✅ Clean up concluído!

📊 GERANDO RELATÓRIO DE BACKUP
-----------------------------------
✅ Relatório de backup gerado!

=======================================
🎉 BACKUP CONCLUÍDO!
=======================================

📊 INFORMAÇÕES:
   Date: Sat Dec 28 22:30:00 AM -03 2024
   Backup ID: 20241228_223000
   Namespace: neo4j-langraph

📊 BACKUPS:
   Neo4j: neo4j_20241228_223000 (25MB)
   LocalAI: 5 models (4.2GB)

📊 RETENTION:
   Neo4j: 7 dias (3 backups)
   LocalAI: 7 dias

=======================================
```

---

### **3. monitor_with_kubectl_ai.sh**

**Descrição:** Script de monitoramento contínuo com kubectl-ai

**O que faz:**
- ✅ Monitora saúde dos pods
- ✅ Monitora deployments
- ✅ Monitora serviços
- ✅ Monitora PVCs
- ✅ Diagnóstico de problemas

**Como usar:**

```bash
bash scripts/monitor_with_kubectl_ai.sh
```

**Saída esperada:**

```
📊 MONITORAMENTO CONTÍNUO COM KUBECTL-AI
=======================================

📋 VERIFICANDO PRÉ-REQUISITOS
-----------------------------------
✅ kubectl-ai está instalado
✅ K3S está rodando

⚙️  CONFIGURAÇÕES
-----------------------------------
📁 Namespace: neo4j-langraph
⏱️  Intervalo: 60 segundos

📊 INICIANDO MONITORAMENTO CONTÍNUO
=======================================

📊 MONITORAMENTO DE PODS (Sat Dec 28 22:31:00 AM -03 2024)
-----------------------------------
✅ Todos os pods estão rodando!

📊 MONITORAMENTO DE DEPLOYMENTS (Sat Dec 28 22:31:00 AM -03 2024)
-----------------------------------
✅ Todos os deployments estão ready!

📊 MONITORAMENTO DE SERVIÇOS (Sat Dec 28 22:31:00 AM -03 2024)
-----------------------------------
✅ Todos os serviços estão acessíveis!

📊 MONITORAMENTO DE PVCS (Sat Dec 28 22:31:00 AM -03 2024)
-----------------------------------
✅ Todos os PVCs estão bound!

🔍 DIAGNÓSTICO DE PROBLEMAS (Sat Dec 28 22:31:00 AM -03 2024)
-----------------------------------
✅ Nenhum problema encontrado!

⏳ Aguardando 60 segundos antes do próximo ciclo...
=======================================
```

---

### **4. diagnose_and_recover_with_kubectl_ai.sh**

**Descrição:** Script de diagnóstico e recuperação automática com kubectl-ai

**O que faz:**
- ✅ Diagnóstico de pods com problemas
- ✅ Diagnóstico de deployments com problemas
- ✅ Reinício de pods com CrashLoopBackOff
- ✅ Reinício de deployments com rollout falhado
- ✅ Deleção de pods antigos (>1 hora)
- ✅ Verificação pós-recuperação
- ✅ Health checks

**Como usar:**

```bash
bash scripts/diagnose_and_recover_with_kubectl_ai.sh
```

**Saída esperada:**

```
🔍 DIAGNÓSTICO E RECUPERAÇÃO AUTOMÁTICA COM KUBECTL-AI
====================================================

📋 VERIFICANDO PRÉ-REQUISITOS
-----------------------------------
✅ kubectl-ai está instalado
✅ K3S está rodando

⚙️  CONFIGURAÇÕES
-----------------------------------
📁 Namespace: neo4j-langraph
🔄 Auto-restart pods: true
🔄 Auto-restart deployments: true
🗑️  Auto-delete crashed pods: true

🔍 DIAGNÓSTICO INICIAL
-----------------------------------
📊 Verificando pods...
📊 Verificando deployments...
📊 Verificando serviços...

🔍 DIAGNÓSTICO DE PODS COM PROBLEMAS
-----------------------------------
🔍 Analisando pods com problemas...

🔄 RECUPERAÇÃO DE PODS
-----------------------------------
🔄 Reiniciando pods com problemas...
✅ Pods reiniciados!

🔄 RECUPERAÇÃO DE DEPLOYMENTS
-----------------------------------
🔄 Reiniciando deployments com problemas...
✅ Deployments reiniciados!

🧹 LIMPEZA DE PODS ANTIGOS
-----------------------------------
🧹 Deletando pods antigos...
✅ Pods antigos deletados!

⏳ AGUARDANDO ROLLOUT
-----------------------------------
⏳ Aguardando rollout do neo4j...
✅ Rollout do neo4j completado!
⏳ Aguardando rollout do localai...
✅ Rollout do localai completado!

🔍 VERIFICAÇÃO PÓS-RECUPERAÇÃO
-----------------------------------
📊 Verificando pods...
✅ Todos os pods estão rodando!
📊 Verificando deployments...
✅ Todos os deployments estão ready!

🧪 EXECUTANDO HEALTH CHECKS
-----------------------------------
✅ Health check do Neo4j concluído!
✅ Health check do LocalAI concluído!

====================================================
🎉 DIAGNÓSTICO E RECUPERAÇÃO CONCLUÍDOS!
====================================================
```

---

### **5. deploy_with_kubectl_ai.sh**

**Descrição:** Script de deploy com kubectl-ai

**O que faz:**
- ✅ Aplica manifests K8S
- ✅ Aguarda rollout
- ✅ Executa health checks
- ✅ Executa smoke tests
- ✅ Gera relatório de deploy

**Como usar:**

```bash
bash scripts/deploy_with_kubectl_ai.sh
```

**Saída esperada:**

```
🚀 DEPLOY COM KUBECTL-AI
=======================================

📋 VERIFICANDO PRÉ-REQUISITOS
-----------------------------------
✅ kubectl-ai está instalado
✅ K3S está rodando
✅ Diretório k8s/ encontrado

⚙️  CONFIGURAÇÕES
-----------------------------------
📁 Namespace: neo4j-langraph
📁 Diretório de manifests: k8s
⏭️  Skip permissions: true

📊 VERIFICANDO NAMESPACE
-----------------------------------
✅ Namespace neo4j-langraph existe

🚀 APLICANDO MANIFESTS K8S
-----------------------------------
📦 Aplicando manifests do diretório k8s...
✅ Manifests K8S aplicados!

⏳ AGUARDANDO ROLLOUT
-----------------------------------
⏳ Aguardando rollout do neo4j...
✅ Rollout do neo4j completado!
⏳ Aguardando rollout do localai...
✅ Rollout do localai completado!

🔍 VERIFICANDO STATUS
-----------------------------------
📊 Verificando pods...
📊 Verificando deployments...
📊 Verificando serviços...

🧪 EXECUTANDO HEALTH CHECKS
-----------------------------------
✅ Health check do Neo4j concluído!
✅ Health check do LocalAI concluído!

🧪 EXECUTANDO SMOKE TESTS
-----------------------------------
✅ Smoke test do Neo4j concluído!
✅ Smoke test do LocalAI concluído!

=======================================
🎉 DEPLOY CONCLUÍDO!
=======================================

📊 INFORMAÇÕES:
   Namespace: neo4j-langraph
   Manifest dir: k8s

📊 RECURSOS DEPLOYADOS:
   • Pods: 2
   • Deployments: 2
   • Services: 2

📊 ACESSO:
   • Neo4j Browser: http://localhost:30474
   • LocalAI: http://localhost:30808
   • Neo4j Bolt: bolt://localhost:30687

📊 HEALTH CHECKS:
   • Neo4j: ✅ Passed
   • LocalAI: ✅ Passed

📊 SMOKE TESTS:
   • Neo4j: ✅ Passed
   • LocalAI: ✅ Passed

=======================================
```

---

## 🚀 COMO USAR

### **Instalar kubectl-ai**

```bash
# Baixar e instalar kubectl-ai
curl -LO https://github.com/kubectl-ai/kubectl-ai/releases/download/v0.1.0/kubectl-ai-linux-amd64
chmod +x kubectl-ai-linux-amd64
sudo mv kubectl-ai-linux-amd64 /usr/local/bin/kubectl-ai
```

---

### **Instalar K3S**

```bash
# Instalar K3S
curl -sfL https://get.k3s.io | sh -

# Verificar status
sudo systemctl status k3s
```

---

### **Executar Scripts**

#### **Setup do K3S**

```bash
bash scripts/setup_k3s_with_kubectl_ai.sh
```

---

#### **Deploy**

```bash
bash scripts/deploy_with_kubectl_ai.sh
```

---

#### **Backup**

```bash
bash scripts/backup_with_kubectl_ai.sh
```

---

#### **Monitoramento**

```bash
# Executar em background
bash scripts/monitor_with_kubectl_ai.sh &

# Ver logs
tail -f /tmp/kubectl-ai-monitor.log
```

---

#### **Diagnóstico e Recuperação**

```bash
bash scripts/diagnose_and_recover_with_kubectl_ai.sh
```

---

## 📋 DEPENDÊNCIAS

| Dependência | Versão | Instalação |
|-------------|---------|-----------|
| **kubectl-ai** | v0.1.0+ | `curl -LO https://github.com/kubectl-ai/kubectl-ai/releases/download/v0.1.0/kubectl-ai-linux-amd64` |
| **K3S** | v1.28.0+ | `curl -sfL https://get.k3s.io | sh -` |
| **bash** | v4.0+ | Já instalado no Linux |
| **curl** | v7.68.0+ | `sudo apt install curl` |
| **kubectl** | v1.28.0+ | Já instalado com K3S |

---

## 📚 EXEMPLOS DE USO

### **Exemplo 1: Setup Inicial**

```bash
# 1. Instalar K3S
curl -sfL https://get.k3s.io | sh -

# 2. Instalar kubectl-ai
curl -LO https://github.com/kubectl-ai/kubectl-ai/releases/download/v0.1.0/kubectl-ai-linux-amd64
chmod +x kubectl-ai-linux-amd64
sudo mv kubectl-ai-linux-amd64 /usr/local/bin/kubectl-ai

# 3. Setup do K3S com kubectl-ai
bash scripts/setup_k3s_with_kubectl_ai.sh
```

---

### **Exemplo 2: Deploy Atualizado**

```bash
# 1. Fazer mudanças nos manifests
echo "Nova configuração" > k8s/neo4j/config.yaml

# 2. Deploy com kubectl-ai
bash scripts/deploy_with_kubectl_ai.sh
```

---

### **Exemplo 3: Backup Automatizado**

```bash
# 1. Criar CronJob para backup diário
crontab -e

# Adicionar:
# 0 2 * * * bash /home/cnmfs/Claude/Projects/neo4j_langraph/scripts/backup_with_kubectl_ai.sh >> /tmp/kubectl-ai-backup.log 2>&1

# 2. Ver logs
tail -f /tmp/kubectl-ai-backup.log
```

---

### **Exemplo 4: Monitoramento Contínuo**

```bash
# 1. Executar monitoramento em background
nohup bash scripts/monitor_with_kubectl_ai.sh > /tmp/kubectl-ai-monitor.log 2>&1 &

# 2. Ver logs
tail -f /tmp/kubectl-ai-monitor.log

# 3. Parar monitoramento
pkill -f monitor_with_kubectl_ai.sh
```

---

### **Exemplo 5: Diagnóstico e Recuperação**

```bash
# 1. Verificar se há problemas
kubectl get pods -n neo4j-langraph

# 2. Diagnóstico e recuperação
bash scripts/diagnose_and_recover_with_kubectl_ai.sh

# 3. Verificar se problemas foram resolvidos
kubectl get pods -n neo4j-langraph
```

---

## 📊 RESUMO

| Script | Descrição | Quando usar |
|--------|-----------|-------------|
| `setup_k3s_with_kubectl_ai.sh` | Setup inicial do K3S | Primeira vez |
| `deploy_with_kubectl_ai.sh` | Deploy de manifests | Deploy de mudanças |
| `backup_with_kubectl_ai.sh` | Backup automatizado | Backup diário |
| `monitor_with_kubectl_ai.sh` | Monitoramento contínuo | Monitoramento em produção |
| `diagnose_and_recover_with_kubectl_ai.sh` | Diagnóstico e recuperação | Diagnóstico de problemas |

---

**Autor:** CNMFS  
**Data:** 28/12/2024  
**Versão:** 1.0.0

---

**Status:** ✅ README DE SCRIPTS KUBECTL-AI COMPLETO! 🎉
