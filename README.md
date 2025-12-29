# 🚀 Neo4j Langraph - Sistema de Conhecimento Pessoal

Sistema de conhecimento pessoal com **Neo4j**, **LocalAI**, **LangChain**, e **K3S**.

---

## 🏗️ ARQUITETURA

```
┌─────────────────────────────────────────────────────────┐
│  ARQUITETURA DO SISTEMA AI                       │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  Camada de Aplicação (LangChain)                 │
├─────────────────────────────────────────────────────────┤
│  • Python CLI (src/cli/knowledge_cli.py)          │
│  • Ingestion, Query, Relationship Management       │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│  Camada de Roteamento (LiteLLM)                │
├─────────────────────────────────────────────────────────┤
│  • Gemini Flash 2.5 (primário)                  │
│  • LocalAI (secundário)                          │
│  • Fallback automático                             │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│  Camada de Serviços (K3S)                      │
├─────────────────────────────────────────────────────────┤
│  • Neo4j (grafo) - Portas: 30474, 30687       │
│  • LocalAI (embeddings + LLM) - Porta: 30808     │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│  Camada de Infraestrutura                        │
├─────────────────────────────────────────────────────────┤
│  • K3S (Kubernetes local)                        │
│  • PVs manuais (/mnt/container-data/projects/)      │
│  • GPU (RTX 4070 - 8GB VRAM)                │
└─────────────────────────────────────────────────────────┘
```

---

## 🚀 GUIA DE INSTALAÇÃO

### **Pré-requisitos**

- [ ] **GitHub Pro** (para CI/CD ilimitado)
- [ ] **Ubuntu/Debian** (Pop!_OS recomendado)
- [ ] **GPU NVIDIA** (RTX 4070 ou similar)
- [ ] **Python 3.10+**
- [ ] **Docker** (opcional)

---

## 📋 INÍCIO RÁPIDO

### **1. Instalar K3S**

```bash
# Executar como root
sudo bash scripts/setup_k3s.sh
```

**O que faz:**
- ✅ Instala K3S (Kubernetes local)
- ✅ Configura kubectl
- ✅ Cria namespace `neo4j-langraph`
- ✅ Cria PVs manuais

---

### **2. Instalar GitHub Actions Self-Hosted Runner**

```bash
# Executar como usuário normal
bash scripts/setup_runner.sh
```

**O que faz:**
- ✅ Instala GitHub Actions Runner
- ✅ Configura como serviço systemd
- ✅ Registra no GitHub
- ✅ Pode executar workflows local

---

### **3. Configurar GitHub Secrets**

```bash
# Criar secrets no GitHub
bash scripts/setup_github_secrets.sh
```

**Secrets criados:**
- ✅ `KUBECONFIG` (config do K3S)
- ✅ `NEO4J_PASSWORD` (senha do Neo4j)
- ✅ `GOOGLE_API_KEY` (API key do Gemini)
- ✅ `LITELLM_MASTER_KEY` (master key do LiteLLM)

---

### **4. Fazer Push para GitHub**

```bash
# Inicializar repositório git (se necessário)
git init

# Adicionar arquivos
git add .
git commit -m "chore: initial commit"

# Adicionar remote (se necessário)
git remote add origin https://github.com/SEU_USUARIO/neo4j-langraph.git

# Push para GitHub
git push origin main
```

**O que acontece:**
- ✅ GitHub Actions executar `test.yml`
- ✅ GitHub Actions executar `deploy-dev.yml`
- ✅ Deploy automático no K3S local

---

## 📚 USO

### **Ingerir Documentos**

```bash
# Criar diretório de documentos
mkdir -p documents

# Adicionar documentos
echo "Django é um framework web em Python" > documents/django.txt
echo "FastAPI é moderno e rápido para APIs REST" > documents/fastapi.txt

# Ingerir no grafo
python3 -m src.cli.knowledge_cli ingest documents
```

---

### **Fazer Queries**

```bash
# Fazer query ao sistema de conhecimento
python3 -m src.cli.knowledge_cli query "frameworks web em Python"
```

**O que faz:**
1. Converte query em embeddings (LocalAI com GPU)
2. Busca nós relacionados no Neo4j
3. Gera resposta com LLM (LiteLLM roteia para Gemini ou LocalAI)

---

### **Visualizar Grafo**

```bash
# Abrir Neo4j Browser
http://localhost:30474

# Usuário: neo4j
# Senha: password
```

**Comandos úteis:**
```cypher
// Ver todos os nós
MATCH (n) RETURN n;

// Ver nós de Documentos
MATCH (d:Document) RETURN d;

// Ver nós de Conceitos
MATCH (c:Concept) RETURN c;

// Ver relações
MATCH (a)-[r]->(b) RETURN a, r, b;

// Contar nós
MATCH (n) RETURN count(n);
```

---

## 📊 MONITORAMENTO

### **Verificar Status do K3S**

```bash
# Ver nós
kubectl get nodes

# Ver pods no namespace neo4j-langraph
kubectl get pods -n neo4j-langraph

# Ver serviços
kubectl get svc -n neo4j-langraph

# Ver logs de um pod
kubectl logs -f deployment/neo4j -n neo4j-langraph
```

---

### **Verificar Status dos Workflows GitHub Actions**

```bash
# Ver lista de runs
gh run list

# Ver run específico
gh run view RUN_ID

# Ver logs
gh run view RUN_ID --log

# Monitorar run em tempo real
gh run watch
```

---

## 🔧 DESENVOLVIMENTO

### **Estrutura de Diretórios**

```
neo4j-langraph/
├── .github/
│   └── workflows/          # Workflows GitHub Actions
│       ├── test.yml         # Testes automatizados
│       ├── deploy-dev.yml   # Deploy dev (Self-Hosted)
│       └── backup.yml      # Backup automatizado
│
├── k8s/                   # Manifestos K8S
│   ├── base/              # Manifestos base
│   ├── overlays/          # Kustomize overlays
│   └── scripts/          # Scripts K8S
│
├── scripts/               # Scripts de automação
│   ├── setup_runner.sh    # Setup self-hosted runner
│   ├── setup_k3s.sh      # Setup K3S
│   └── backup.sh         # Backup automatizado
│
├── src/                  # Código fonte
│   ├── cli/             # CLI
│   ├── knowledge_system/ # Sistema de conhecimento
│   └── shared/          # Utilitários compartilhados
│
├── tests/               # Testes
│   ├── unit/           # Testes unitários
│   ├── integration/    # Testes de integração
│   └── e2e/           # Testes end-to-end
│
├── docs/                # Documentação
├── .gitignore          # Ignorar arquivos sensíveis
├── requirements.txt     # Dependências Python
└── README.md           # Este arquivo
```

---

### **Executar Testes Localmente**

```bash
# Instalar dependências
pip install -r requirements.txt

# Executar testes unitários
pytest tests/unit/ -v

# Executar testes de integração
pytest tests/integration/ -v

# Executar todos os testes
pytest tests/ -v

# Executar com coverage
pytest tests/ --cov=src/ --cov-report=html
```

---

## 🔐 SEGURANÇA

### **Melhores Práticas de Segurança**

1. ✅ **Nunca versionar .env files**
   - Use `.gitignore` para ignorar `.env`, `.env.local`, etc.
   
2. ✅ **Usar GitHub Secrets**
   - Credenciais devem ser armazenadas como secrets
   - Use `gh secret set` para criar secrets

3. ✅ **Usar K8S Secrets**
   - Credenciais no K8S devem ser secrets
   - Use `kubectl create secret` para criar secrets

4. ✅ **Tokens de Acesso**
   - Use tokens temporários quando possível
   - Rote tokens regularmente

5. ✅ **Autenticação em 2 Fatores**
   - Ative 2FA no GitHub
   - Use autenticação forte

6. ✅ **Repositório Privado**
   - Mantenha o repositório privado
   - Limite acesso colaborativo

---

## 🔄 CI/CD

### **GitHub Actions Workflows**

#### **1. Testes (`.github/workflows/test.yml`)**

**O que faz:**
- ✅ Linting (flake8, mypy, black)
- ✅ Testes unitários (matrix Python 3.9, 3.10, 3.11)
- ✅ Testes de integração (com Neo4j container)
- ✅ Testes end-to-end (com Neo4j container)
- ✅ Security checks (bandit)
- ✅ Code coverage (codecov)

**Quando executa:**
- Push para branches `main`, `dev`, `staging`
- Pull requests para `main`, `dev`
- Manual (`workflow_dispatch`)

---

#### **2. Deploy Dev (`.github/workflows/deploy-dev.yml`)**

**O que faz:**
- ✅ Pre-flight checks (validação de manifests, verificação de secrets)
- ✅ Deploy no K3S local (self-hosted runner)
- ✅ Health checks (Neo4j, LocalAI)
- ✅ Verificação de deployments
- ✅ Relatório de deploy

**Quando executa:**
- Push para branches `main`, `dev`
- Manual (`workflow_dispatch`)

**Ambiente:**
- Dev (K3S local)
- Self-hosted runner (pop-os.local)

---

#### **3. Backup (`.github/workflows/backup.yml`)**

**O que faz:**
- ✅ Backup do Neo4j
- ✅ Backup dos modelos LocalAI
- ✅ Verificação de integridade
- ✅ Limpeza de backups antigos (7 dias)
- ✅ Relatório de backup

**Quando executa:**
- Diariamente às 2AM UTC (cron job)
- Manual (`workflow_dispatch`)

**Ambiente:**
- Local (self-hosted runner)

---

## 📊 ESTRUTURA DE DADOS

### **Neo4j Graph Schema**

```
┌─────────────────────────────────────────────────────────┐
│  NEO4J GRAPH SCHEMA                               │
└─────────────────────────────────────────────────────────┘

Nós:
  - Document
  - Concept
  - Entity
  - Attribute

Relações:
  - Document -> Concept :CONTAINS
  - Concept -> Concept :RELATED_TO
  - Entity -> Concept :MENTIONS
  - Concept -> Attribute :HAS

Índices:
  - Document.title
  - Concept.name
  - Entity.name
```

---

## 🎯 OBJETIVOS DO PROJETO

- ✅ **Sistema de conhecimento pessoal**
- ✅ **Busca semântica** (embeddings)
- ✅ **Grafo de conceitos** (Neo4j)
- ✅ **Respostas inteligentes** (LLM)
- ✅ **CI/CD automatizado** (GitHub Actions)
- ✅ **Alta disponibilidade** (K3S)
- ✅ **Segurança** (secrets, 2FA)
- ✅ **Monitoramento** (logs, métricas)

---

## 📖 RECURSOS

- [Neo4j Documentation](https://neo4j.com/docs/)
- [LangChain Documentation](https://python.langchain.com/)
- [LocalAI Documentation](https://localai.io/)
- [K3S Documentation](https://docs.k3s.io/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)

---

## 🤝 CONTRIBUIÇÃO

1. Fork o repositório
2. Crie uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'feat: Adiciona MinhaFeature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

---

## 📄 LICENÇA

Este projeto é licenciado sob a Licença MIT.

---

## 👤 AUTOR

**CNMFS**

---

## 📝 CHANGELOG

### **v1.0.0** (2024-12-28)
- ✅ Setup inicial do K3S
- ✅ Deploy de Neo4j e LocalAI
- ✅ Configuração do LiteLLM (roteador)
- ✅ GitHub Actions (CI/CD)
- ✅ Scripts de setup
- ✅ Documentação completa

---

**Status:** ✅ SISTEMA AI 90% PRONTO! 🚀

**Próximos Passos:**
1. Configurar ArgoCD (GitOps)
2. Configurar Prometheus + Grafana (monitoramento)
3. Configurar HPA + VPA (auto-scaling)
4. Implementar testes E2E
5. Configurar Sentry (error tracking)
