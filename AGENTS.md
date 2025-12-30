# 🤖 AGENTES - GUIA DE AUTOMAÇÃO

**Versão:** 1.0.0  
**Data:** 28/12/2024  
**Autor:** CNMFS

---

## 📋 ÍNDICE

1. [O que são Agentes?](#o-que-são-agentes)
2. [Procedimento de Branch](#procedimento-de-branch)
3. [Integração com GitHub Actions](#integração-com-github-actions)
4. [Melhores Práticas de Git](#melhores-práticas-de-git)
5. [Fluxo de Trabalho](#fluxo-de-trabalho)

---

## 🤖 O QUE SÃO AGENTES?

### **Definição**

Agentes são **sistemas de IA autônomos** que realizam tarefas específicas sem intervenção humana.

### **Tipos de Agentes**

| Tipo | Descrição | Exemplo |
|-------|-----------|----------|
| **Agente de Testes** | Executa testes automatizados | GitHub Actions |
| **Agente de Deploy** | Realiza deployments | kubectl-ai |
| **Agente de Monitoramento** | Monitora aplicações | Prometheus + Grafana |
| **Agente de Backup** | Realiza backups automáticos | CronJob |

---

## 🌳 PROCEDIMENTO DE BRANCH

### **🎯 OBJETIVO**

Evitar conflitos de branches e sessões distintas através de um **procedimento padrão de branch**.

### **📋 CHECKLIST ANTES DE QUALQUER ATIVIDADE**

- [ ] **Verificar branch atual**
- [ ] **Salvar mudanças locais**
- [ ] **Criar novo branch para a atividade**
- [ ] **Realizar mudanças**
- [ ] **Commit e push**
- [ ] **[Deletar ou não] branch após merge**

---

## 🔄 FLUXO DE BRANCH (PASSO A PASSO)

### **Passo 1: Verificar Branch Atual**<tool_call>bash
command</arg_key><arg_value>cat >> AGENTS.md << 'EOF'

```bash
# Verificar branch atual
git branch --show-current

# Saída esperada:
# main (ou dev, staging, etc.)
```

**Se você estiver no branch `main` (ou outro branch de produção):**
```bash
⚠️  NÃO faça mudanças diretamente no main!
💡 Crie um novo branch para a atividade (Passo 2)
```

---

### **Passo 2: Criar Novo Branch**

#### **2.1. Escolher Convenção de Nomenclatura**

Use **convenções de nomenclatura claras** para identificar o tipo de atividade:

| Tipo de Atividade | Prefixo | Exemplo |
|-------------------|----------|---------|
| **Feature** | `feature/` | `feature/add-neo4j-backup` |
| **Bugfix** | `bugfix/` | `bugfix/fix-neo4j-crash` |
| **Hotfix** | `hotfix/` | `hotfix/critical-security-fix` |
| **Refactor** | `refactor/` | `refactor/optimize-embeddings` |
| **Documentation** | `docs/` | `docs/update-readme` |
| **Test** | `test/` | `test/add-unit-tests` |
| **Deploy** | `deploy/` | `deploy/dev-to-staging` |
| **Chore** | `chore/` | `chore/update-dependencies` |

#### **2.2. Criar o Branch**

```bash
# Sintaxe:
git checkout -b <prefixo>/<descricao-curta>

# Exemplos:
git checkout -b feature/add-neo4j-backup
git checkout -b bugfix/fix-neo4j-crash
git checkout -b hotfix/critical-security-fix
git checkout -b refactor/optimize-embeddings
git checkout -b docs/update-readme
git checkout -b test/add-unit-tests
git checkout -b deploy/dev-to-staging
git checkout -b chore/update-dependencies
```

**Saída esperada:**
```
Switched to a new branch 'feature/add-neo4j-backup'
```

---

### **Passo 3: Verificar Mudanças Pendentes**

```bash
# Verificar mudanças não commitadas
git status

# Saída esperada:
# On branch feature/add-neo4j-backup
# nothing to commit, working tree clean
```

**Se houver mudanças pendentes:**
```bash
⚠️  Você tem mudanças não commitadas!

Opções:
1. Stash (salvar temporariamente)
   git stash

2. Commit (salvar permanentemente)
   git add .
   git commit -m "feat: descricao das mudancas"

3. Reset (descartar mudanças)
   git reset --hard HEAD
```

---

### **Passo 4: Realizar Mudanças**

```bash
# Realizar mudanças no código
echo "Nova funcionalidade" > novo_arquivo.txt

# Adicionar arquivos
git add .

# Verificar mudanças
git status
```

---

### **Passo 5: Commit**

```bash
# Sintaxe:
git commit -m "<tipo>: <descricao>"

# Tipos comuns:
# - feat: nova funcionalidade
# - fix: correção de bug
# - docs: mudança na documentação
# - style: mudança de estilo (formatação, pontuação)
# - refactor: mudança de código sem alterar comportamento
# - test: adicionar testes
# - chore: manutenção (atualização de dependências, etc.)

# Exemplos:
git commit -m "feat: adicionar backup automatizado do Neo4j"
git commit -m "fix: corrigir crash do Neo4j ao iniciar"
git commit -m "docs: atualizar README com instruções de deploy"
git commit -m "style: formatar código com black"
git commit -m "refactor: otimizar queries de embeddings"
git commit -m "test: adicionar testes unitários para ingestion"
git commit -m "chore: atualizar dependências Python"
```

---

### **Passo 6: Push para o Branch**

```bash
# Sintaxe:
git push -u origin <nome-do-branch>

# Exemplo:
git push -u origin feature/add-neo4j-backup
```

**Saída esperada:**
```
Branch 'feature/add-neo4j-backup' set up to track remote branch 'feature/add-neo4j-backup' from 'origin'.
```

---

### **Passo 7: Criar Pull Request**

#### **7.1. Via GitHub CLI (gh)**

```bash
# Criar Pull Request
gh pr create \
  --title "feat: Adicionar backup automatizado do Neo4j" \
  --body "## Descrição

Esta PR adiciona backup automatizado do Neo4j.

## Mudanças
- Adiciona CronJob para backup diário
- Adiciona script de verificação de integridade
- Adiciona limpeza de backups antigos (7 dias)

## Testes
- [ ] Testado localmente
- [ ] Testado em staging
- [ ] Testes unitários passando

## Checklist
- [ ] Código segue as melhores práticas
- [ ] Testes adicionados/atualizados
- [ ] Documentação atualizada
- [ ] Sem conflitos de merge
" \
  --base main \
  --head feature/add-neo4j-backup
```

#### **7.2. Via GitHub Web**

1. Acesse: https://github.com/SEU_USUARIO/neo4j-langraph/compare
2. Selecione:
   - Base: `main`
   - Compare: `feature/add-neo4j-backup`
3. Clique em **"Create pull request"**
4. Preencha:
   - **Title:** `feat: Adicionar backup automatizado do Neo4j`
   - **Description:** (veja template acima)
5. Clique em **"Create pull request"**

---

### **Passo 8: [DELETAR OU NÃO] Branch Após Merge**

#### **Opção A: Deletar Branch Após Merge (RECOMENDADO)**

**Quando deletar:**
- ✅ Branch de `feature`, `bugfix`, `hotfix`
- ✅ Merge foi concluído e aprovado
- ✅ Não há mais necessidade do branch

**Como deletar:**

```bash
# 1. Verificar se o branch foi merged no main
git checkout main
git pull origin main

# 2. Deletar branch local
git branch -d feature/add-neo4j-backup

# 3. Deletar branch remoto
git push origin --delete feature/add-neo4j-backup
```

**Saída esperada:**
```
Deleted branch feature/add-neo4j-backup (was abc123).
To github.com:usuario/neo4j-langraph.git
 - [deleted]         feature/add-neo4j-backup
```

---

#### **Opção B: Manter Branch Após Merge**

**Quando manter:**
- ✅ Branch de `dev`, `staging`, `prod`
- ✅ Branch de longa duração (ex: `feature/ai-agent`)
- ✅ Branch que continuará recebendo mudanças

**Como manter:**

```bash
# Apenas atualizar o branch após merge no main
git checkout main
git pull origin main

git checkout feature/add-neo4j-backup
git merge main
git push origin feature/add-neo4j-backup
```

---

## 🔗 INTEGRAÇÃO COM GITHUB ACTIONS

### **Triggers por Branch**

Os workflows do GitHub Actions são disparados por diferentes branches:

| Workflow | Trigger | Branch |
|----------|----------|--------|
| `test.yml` | Push, Pull Request | `main`, `dev`, `staging` |
| `deploy-dev.yml` | Push | `main`, `dev` |
| `deploy-staging.yml` | Push | `staging` |
| `deploy-prod.yml` | Manual | `prod` |
| `backup.yml` | Cron (diário às 2AM) | N/A (self-hosted runner) |

---

### **Exemplo de Workflow por Branch**

#### **1. Branch de Feature**

```bash
# Criar branch de feature
git checkout -b feature/add-neo4j-backup

# Fazer mudanças
echo "Backup functionality" > backup.sh
git add backup.sh

# Commit
git commit -m "feat: adicionar backup automatizado"

# Push
git push -u origin feature/add-neo4j-backup

# Criar Pull Request
gh pr create --base main --head feature/add-neo4j-backup \
  --title "feat: Adicionar backup automatizado" \
  --body "Esta PR adiciona backup automatizado."
```

**O que acontece:**
1. ✅ GitHub Actions executa `test.yml` (lint, unit, integration, e2e)
2. ✅ GitHub Actions executa `deploy-dev.yml` (self-hosted runner)
3. ✅ Pull Request é criado
4. ✅ Code review e aprovação
5. ✅ Merge no `main`
6. ✅ GitHub Actions executa `deploy-staging.yml` (se necessário)

---

#### **2. Branch de Bugfix**

```bash
# Criar branch de bugfix
git checkout -b bugfix/fix-neo4j-crash

# Fazer mudanças
echo "Fixed crash" > fix.py
git add fix.py

# Commit
git commit -m "fix: corrigir crash do Neo4j ao iniciar"

# Push
git push -u origin bugfix/fix-neo4j-crash

# Criar Pull Request
gh pr create --base main --head bugfix/fix-neo4j-crash \
  --title "fix: Corrigir crash do Neo4j ao iniciar" \
  --body "Esta PR corrige o crash do Neo4j."
```

**O que acontece:**
1. ✅ GitHub Actions executa `test.yml`
2. ✅ GitHub Actions executa `deploy-dev.yml`
3. ✅ Pull Request é criado
4. ✅ Code review e aprovação
5. ✅ Merge no `main`
6. ✅ Deploy automático para `staging`

---

#### **3. Branch de Hotfix**

```bash
# Criar branch de hotfix
git checkout -b hotfix/critical-security-fix

# Fazer mudanças
echo "Security fix" > security.py
git add security.py

# Commit
git commit -m "hotfix: corrigir vulnerabilidade crítica de segurança"

# Push
git push -u origin hotfix/critical-security-fix

# Criar Pull Request
gh pr create --base main --head hotfix/critical-security-fix \
  --title "hotfix: Corrigir vulnerabilidade crítica de segurança" \
  --body "Esta PR corrige uma vulnerabilidade crítica."
```

**O que acontece:**
1. ✅ GitHub Actions executa `test.yml`
2. ✅ GitHub Actions executa `deploy-dev.yml`
3. ✅ Pull Request é criado
4. ✅ Code review e aprovação (prioridade alta)
5. ✅ Merge no `main`
6. ✅ Deploy automático para `prod` (workflow manual)

---

## 🏆 MELHORES PRÁTICAS DE GIT

### **1. Convenções de Commit**

Use **conventional commits** para mensagens de commit claras:

```
<tipo>(<escopo>): <descrição curta>

[corpo opcional]

[rodapé opcional]
```

**Tipos:**
- `feat`: Nova funcionalidade
- `fix`: Correção de bug
- `docs`: Mudança na documentação
- `style`: Mudança de estilo (formatação, pontuação)
- `refactor`: Mudança de código sem alterar comportamento
- `test`: Adicionar ou atualizar testes
- `chore`: Manutenção (atualização de dependências, etc.)
- `perf`: Melhoria de performance
- `ci`: Mudança na CI/CD

**Exemplos:**
```bash
git commit -m "feat(backup): adicionar backup automatizado do Neo4j"
git commit -m "fix(neo4j): corrigir crash ao iniciar"
git commit -m "docs(readme): atualizar instruções de deploy"
git commit -m "style(formatting): formatar código com black"
git commit -m "refactor(embeddings): otimizar queries"
git commit -m "test(unit): adicionar testes unitários para ingestion"
git commit -m "chore(deps): atualizar dependências Python"
```

---

### **2. Branch Protection**

**Configure branch protection no GitHub:**

1. Acesse: https://github.com/SEU_USUARIO/neo4j-langraph/settings/branches
2. Clique em **"Add branch protection rule"**
3. Configure:
   - **Branch name pattern:** `main`
   - **Require status checks to pass before merging:** ✅
   - **Require branches to be up to date before merging:** ✅
   - **Require pull request reviews before merging:** ✅
   - **Dismiss stale PR approvals when new commits are pushed:** ✅
   - **Require review from CODEOWNERS:** ✅
   - **Limit who can push to matching branches:** ✅ (administradores)
   - **Do not allow bypassing the above settings:** ✅

---

### **3. Code Owners**

**Crie arquivo `.github/CODEOWNERS`:**

```markdown
# Code Owners

# Equipe de DevOps
* @devops-team

# Equipe de Backend
src/backend/* @backend-team

# Equipe de Frontend
src/frontend/* @frontend-team

# Equipe de DevOps (CI/CD)
.github/workflows/* @devops-team
scripts/setup_* @devops-team

# Equipe de Backend (K8S)
k8s/* @backend-team @devops-team

# Equipe de Backend (Neo4j)
k8s/neo4j/* @backend-team

# Equipe de Backend (LocalAI)
k8s/localai/* @backend-team
```

---

### **4. Pull Request Templates**

**Crie arquivo `.github/pull_request_template.md`:**

```markdown
## Descrição

Breve descrição das mudanças.

## Tipo de Mudança

- [ ] Bugfix
- [ ] Feature
- [ ] Breaking Change
- [ ] Documentation

## Mudanças

- Adicionado: ...
- Modificado: ...
- Removido: ...

## Testes

- [ ] Testes unitários
- [ ] Testes de integração
- [ ] Testes end-to-end
- [ ] Testados localmente

## Checklist

- [ ] Código segue as melhores práticas
- [ ] Testes adicionados/atualizados
- [ ] Documentação atualizada
- [ ] Sem conflitos de merge
- [ ] Pull request aprovado por code owners

## Screenshot (se aplicável)

[Screenshot da nova funcionalidade]

## Issue Relacionada

Fixes #ISSUE_NUMBER
```

---

## 🔄 FLUXO DE TRABALHO (GIT FLOW)

### **Estrutura de Branches**

```
main (produção)
  ↑
  ├── hotfix/* (correções urgentes para produção)
  │
  └── dev (desenvolvimento)
        ↑
        ├── staging (pre-produção)
        │
        ├── feature/* (novas funcionalidades)
        ├── bugfix/* (correções de bugs)
        ├── refactor/* (refatorações)
        ├── docs/* (documentação)
        └── test/* (testes)
```

---

### **Fluxo de Desenvolvimento**

#### **1. Iniciar Nova Feature**

```bash
# 1. Verificar branch atual
git branch --show-current  # Deve ser main

# 2. Atualizar main
git checkout main
git pull origin main

# 3. Criar branch de feature
git checkout -b feature/nova-funcionalidade

# 4. Fazer mudanças
# ...

# 5. Commit
git add .
git commit -m "feat: adicionar nova funcionalidade"

# 6. Push
git push -u origin feature/nova-funcionalidade

# 7. Criar Pull Request
gh pr create --base dev --head feature/nova-funcionalidade \
  --title "feat: Adicionar nova funcionalidade"
```

---

#### **2. Mergear para Staging**

```bash
# 1. Criar branch de release
git checkout -b release/staging-v1.0.0

# 2. Mergear features do dev
git merge dev

# 3. Push
git push -u origin release/staging-v1.0.0

# 4. Criar Pull Request para staging
gh pr create --base staging --head release/staging-v1.0.0 \
  --title "release: Staging v1.0.0"
```

---

#### **3. Mergear para Produção**

```bash
# 1. Criar branch de release
git checkout -b release/v1.0.0

# 2. Mergear staging
git merge staging

# 3. Tag do release
git tag -a v1.0.0 -m "Release v1.0.0"

# 4. Push
git push -u origin release/v1.0.0
git push origin v1.0.0

# 5. Criar Pull Request para main
gh pr create --base main --head release/v1.0.0 \
  --title "release: Production v1.0.0"

# 6. Deletar branch após merge
git checkout main
git pull origin main
git branch -d release/v1.0.0
git push origin --delete release/v1.0.0
```

---

### **Fluxo de Hotfix**

```bash
# 1. Verificar branch atual
git branch --show-current  # Deve ser main

# 2. Atualizar main
git checkout main
git pull origin main

# 3. Criar branch de hotfix
git checkout -b hotfix/critical-security-fix

# 4. Fazer mudanças
# ...

# 5. Commit
git add .
git commit -m "hotfix: corrigir vulnerabilidade crítica"

# 6. Push
git push -u origin hotfix/critical-security-fix

# 7. Criar Pull Request para main
gh pr create --base main --head hotfix/critical-security-fix \
  --title "hotfix: Corrigir vulnerabilidade crítica"

# 8. Merge para main
# (após code review e aprovação)

# 9. Mergear para dev (backport)
git checkout dev
git pull origin dev
git merge main
git push origin dev

# 10. Deletar branch
git checkout main
git branch -d hotfix/critical-security-fix
git push origin --delete hotfix/critical-security-fix
```

---

## 🎯 RESUMO DO PROCEDIMENTO DE BRANCH

### **CHECKLIST RÁPIDO**

| Passo | Ação | Comando |
|-------|-------|----------|
| 1 | Verificar branch atual | `git branch --show-current` |
| 2 | Atualizar main | `git checkout main && git pull origin main` |
| 3 | Criar novo branch | `git checkout -b <prefixo>/<descricao>` |
| 4 | Verificar mudanças pendentes | `git status` |
| 5 | Fazer mudanças | `git add .` |
| 6 | Commit | `git commit -m "<tipo>: <descricao>"` |
| 7 | Push | `git push -u origin <nome-do-branch>` |
| 8 | Criar Pull Request | `gh pr create --base main` |
| 9 | Aguardar code review | (via GitHub) |
| 10 | Mergear | (via GitHub) |
| 11 | Deletar branch | `git branch -d && git push origin --delete` |

---

## 📚 RECURSOS

- [GitHub Docs - Branch](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-and-deleting-branches-within-your-repository)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Git Flow](https://nvie.com/posts/a-successful-git-branching-model/)
- [GitHub Actions Docs](https://docs.github.com/en/actions)

---

**Autor:** CNMFS  
**Data:** 28/12/2024  
**Versão:** 1.0.0

---

**Status:** ✅ AGENTES.md COMPLETO! 🎉

---

## 🤖 KUBECTL-AI: ORQUESTRAÇÃO E MANUTENÇÃO DE KUBERNETES

### **🎯 OBJETIVO**

Usar **kubectl-ai** (agente de IA) para orquestrar e manter todos os recursos do Kubernetes automaticamente!

---

## 📚 KUBECTL-AI: GUIA DE ORQUESTRAÇÃO

### **📋 ÍNDICE**

1. [O que é kubectl-ai?](#o-que-é-kubectl-ai)
2. [Instalação e Configuração](#instalação-e-configuração)
3. [Comandos Básicos](#comandos-básicos)
4. [Orquestração de Recursos](#orquestração-de-recursos)
5. [Manutenção Automatizada](#manutenção-automatizada)
6. [Diagnóstico de Problemas](#diagnóstico-de-problemas)
7. [Integração com GitHub Actions](#integração-com-github-actions)
8. [Melhores Práticas](#melhores-práticas)
9. [Exemplos de Uso](#exemplos-de-uso)

---

## 🤖 O QUE É KUBECTL-AI?

### **Definição**

**kubectl-ai** é um agente de IA que **orquestra e mantém recursos do Kubernetes** usando LLMs (Large Language Models).

### **Funcionalidades**

| Funcionalidade | Descrição |
|---------------|-----------|
| **Orquestração** | Criar, atualizar, deletar recursos K8S |
| **Manutenção** | Monitorar saúde dos pods, deployments, serviços |
| **Diagnóstico** | Identificar e corrigir problemas automaticamente |
| **Automação** | Executar tarefas rotineiras (backup, limpeza) |
| **Integração** | Integrar com GitHub Actions, ArgoCD, etc. |

---

## 🔧 INSTALAÇÃO E CONFIGURAÇÃO

### **Passo 1: Verificar Instalação**

```bash
# Verificar se kubectl-ai está instalado
which kubectl-ai

# Saída esperada:
# /home/cnmfs/.local/bin/kubectl-ai

# Verificar versão
kubectl-ai version

# Saída esperada:
# version: dev
# commit: none
# date: unknown
```

---

### **Passo 2: Configurar LLM Provider**

**kubectl-ai suporta múltiplos LLM providers:**

| Provider | Modelo | Descrição |
|----------|---------|-----------|
| **zai** | glm-4.7 | Padrão (Zhipu AI) |
| **openai** | gpt-4, gpt-3.5-turbo | OpenAI |
| **anthropic** | claude-3-opus, claude-3-sonnet | Anthropic |
| **google** | gemini-2.0-flash, gemini-2.0-pro | Google |

**Configurar provider:**

```bash
# Usar Zhipu AI (padrão)
kubectl-ai --llm-provider zai --model glm-4.7

# Usar Google Gemini
kubectl-ai --llm-provider google --model gemini-2.0-flash

# Usar OpenAI
kubectl-ai --llm-provider openai --model gpt-4

# Usar Anthropic
kubectl-ai --llm-provider anthropic --model claude-3-opus
```

---

### **Passo 3: Configurar KUBECONFIG**

```bash
# Verificar se KUBECONFIG está configurado
export KUBECONFIG=/etc/rancher/k3s/k3s.yaml

# Verificar conexão com o cluster
kubectl cluster-info

# Saída esperada:
# Kubernetes control plane is running at https://192.168.68.104:6443
# CoreDNS is running at https://192.168.68.104:6443/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy
```

---

## 🎮 COMANDOS BÁSICOS

### **1. Modos de Interface**

**kubectl-ai suporta 3 tipos de interface:**

| Tipo | Descrição | Quando usar |
|-------|-----------|-------------|
| **Terminal** | CLI interativo (padrão) | Uso diário |
| **Web** | Interface web (localhost:8888) | Visualização |
| **TUI** | Interface de terminal | Avançado |

**Usar diferentes interfaces:**

```bash
# Terminal (padrão)
kubectl-ai

# Web UI
kubectl-ai --ui-type web --ui-listen-address 0.0.0.0:8888

# TUI
kubectl-ai --ui-type tui
```

---

### **2. Modos de Execução**

| Modo | Descrição | Quando usar |
|-------|-----------|-------------|
| **Interativo** (padrão) | Modo interativo com prompt | Uso diário |
| **Quiet** | Modo não-interativo | Scripts, CI/CD |
| **Session** | Sessão persistente | Long-running tasks |

**Usar diferentes modos:**

```bash
# Interativo (padrão)
kubectl-ai

# Quiet (não-interativo)
kubectl-ai --quiet "Liste todos os pods"

# Nova sessão
kubectl-ai --new-session

# Retomar sessão
kubectl-ai --resume-session latest

# Deletar sessão
kubectl-ai --delete-session SESSION_ID
```

---

### **3. Comandos de Gestão de Sessões**

```bash
# Listar todas as sessões
kubectl-ai --list-sessions

# Saída esperada:
# Session ID | Created | Last Used | Mode
#------------|---------|-----------|-----
# abc123     | 2m ago | 1m ago    | terminal
# def456     | 5m ago | 3m ago    | terminal

# Retomar última sessão
kubectl-ai --resume-session latest

# Deletar sessão específica
kubectl-ai --delete-session abc123

# Deletar todas as sessões
kubectl-ai --delete-session all
```

---

## 🚀 ORQUESTRAÇÃO DE RECURSOS

### **1. Criar Recursos**

#### **Criar Namespace**

```bash
kubectl-ai --quiet "Crie o namespace neo4j-langraph"

# Saída:
# ✅ Namespace neo4j-langraph criado
```

---

#### **Criar Deployment do Neo4j**

```bash
kubectl-ai --quiet --skip-permissions "Crie um deployment do Neo4j no namespace neo4j-langraph com as seguintes especificações:
- Imagem: docker.io/neo4j:4.4-community
- Réplicas: 1
- Portas: 7474 (http), 7687 (bolt)
- Recursos: request 512Mi memory, 250m cpu; limit 2Gi memory, 1000m cpu
- Volume: PVC neo4j-data-pvc montado em /data
- Secrets: NEO4J_AUTH do secret neo4j-credentials"

# Saída:
# ✅ Deployment neo4j criado
# ✅ Service neo4j criado
# ✅ PVC neo4j-data-pvc criado
```

---

#### **Criar Deployment do LocalAI**

```bash
kubectl-ai --quiet --skip-permissions "Crie um deployment do LocalAI no namespace neo4j-langraph com as seguintes especificações:
- Imagem: localai/localai:latest
- Réplicas: 1
- Portas: 8080 (http)
- Recursos: request 4Gi memory, 500m cpu; limit 8Gi memory, 2000m cpu
- Volume: PVC localai-models-pvc montado em /models
- GPU: nvidia.com/gpu: 1
- Environment: ENABLE_HTTP_HEADERS=true"

# Saída:
# ✅ Deployment localai criado
# ✅ Service localai criado
# ✅ PVC localai-models-pvc criado
```

---

### **2. Atualizar Recursos**

#### **Atualizar Imagem do Deployment**

```bash
kubectl-ai --quiet --skip-permissions "Atualize o deployment neo4j no namespace neo4j-langraph para usar a imagem docker.io/neo4j:5.23-community"

# Saída:
# ✅ Deployment neo4j atualizado
# ✅ Rollout iniciado
```

---

#### **Atualizar Réplicas do Deployment**

```bash
kubectl-ai --quiet --skip-permissions "Atualize o deployment neo4j no namespace neo4j-langraph para usar 3 réplicas"

# Saída:
# ✅ Deployment neo4j atualizado
# ✅ 3 réplicas configuradas
```

---

#### **Atualizar ConfigMaps**

```bash
kubectl-ai --quiet --skip-permissions "Atualize o configmap neo4j-config no namespace neo4j-langraph para adicionar a configuração NEO4J_dbms_memory_heap_max__size=1G"

# Saída:
# ✅ ConfigMap neo4j-config atualizado
```

---

### **3. Deletar Recursos**

#### **Deletar Pod**

```bash
kubectl-ai --quiet --skip-permissions "Dele o pod neo4j-xxx-xxx no namespace neo4j-langraph"

# Saída:
# ✅ Pod neo4j-xxx-xxx deletado
```

---

#### **Deletar Deployment**

```bash
kubectl-ai --quiet --skip-permissions "Dele o deployment neo4j no namespace neo4j-langraph"

# Saída:
# ✅ Deployment neo4j deletado
# ✅ Service neo4j deletado
```

---

## 🛠️ MANUTENÇÃO AUTOMATIZADA

### **1. Monitorar Saúde dos Pods**

```bash
kubectl-ai --quiet --skip-permissions "Verifique a saúde de todos os pods no namespace neo4j-langraph e reporte quaisquer problemas"

# Saída:
# 📊 Saúde dos Pods:
# 
# Pod: localai-8665bbdbc5-sxdsh
# Status: ✅ Running
# Restarts: 0
# Age: 33h
#
# Pod: neo4j-6ccc56d868-n56qw
# Status: ❌ CrashLoopBackOff
# Restarts: 4
# Age: 2m
#
# 🔍 Problema: Pod neo4j está em CrashLoopBackOff
# 💡 Ação: Ver logs para identificar o problema
```

---

### **2. Monitorar Deployments**

```bash
kubectl-ai --quiet --skip-permissions "Monitore os deployments no namespace neo4j-langraph e reporte o status"

# Saída:
# 📊 Status dos Deployments:
#
# Deployment: localai
# Replicas: 1/1
# Up-to-date: 1
# Available: 1
# Age: 3d2h
# Status: ✅ Ready
#
# Deployment: neo4j
# Replicas: 0/1
# Up-to-date: 1
# Available: 0
# Age: 5m
# Status: ❌ Not Ready
#
# 🔍 Problema: Deployment neo4j não está pronto
# 💡 Ação: Verificar rollout status
```

---

### **3. Limpar Recursos Antigos**

```bash
kubectl-ai --quiet --skip-permissions "Dele todos os pods no namespace neo4j-langraph que estão em status Error ou CrashLoopBackOff há mais de 1 hora"

# Saída:
# 🧹 Limpando pods antigos...
#
# Pod: neo4j-xxx-xxx
# Status: Error
# Age: 2h
# Ação: Deletando
# ✅ Pod deletado
```

---

### **4. Reiniciar Pods com Problemas**

```bash
kubectl-ai --quiet --skip-permissions "Reinicie todos os pods no namespace neo4j-langraph que estão em status CrashLoopBackOff"

# Saída:
# 🔄 Reiniciando pods com problemas...
#
# Pod: neo4j-xxx-xxx
# Status: CrashLoopBackOff
# Ação: Reiniciando
# ✅ Pod reiniciado
```

---

### **5. Escalar Deployments**

```bash
kubectl-ai --quiet --skip-permissions "Escale o deployment neo4j no namespace neo4j-langraph para 2 réplicas"

# Saída:
# 📈 Escalando deployment neo4j...
#
# Deployment: neo4j
# Réplicas atuais: 1
# Réplicas desejadas: 2
# Ação: Escalando
# ✅ Deployment escalado para 2 réplicas
```

---

## 🔍 DIAGNÓSTICO DE PROBLEMAS

### **1. Diagnóstico de Pod com CrashLoopBackOff**

```bash
kubectl-ai --quiet --skip-permissions "Analise os logs do pod neo4j-6ccc56d868-n56qw no namespace neo4j-langraph que está em CrashLoopBackOff e identifique o problema"

# Saída:
# 🔍 Diagnóstico do Pod: neo4j-6ccc56d868-n56qw
#
# Logs:
# su-exec: neo4j: Permission denied
#
# Problema: Permissão negada ao executar neo4j
# Causa: O PV neo4j-data-pv não tem as permissões corretas
#
# Soluções:
# 1. Corrigir permissões do PV:
#    kubectl patch deployment neo4j --type='json' -p='[{"op": "add", "path": "/spec/template/spec/securityContext", "value": {"fsGroup": 7474}}]'
#
# 2. Deletar pod e aguardar recriação:
#    kubectl delete pod neo4j-6ccc56d868-n56qw
#
# 3. Verificar permissões do diretório:
#    ls -la /mnt/container-data/projects/neo4j-langraph/neo4j/
```

---

### **2. Diagnóstico de Deployment com Rollout Falhado**

```bash
kubectl-ai --quiet --skip-permissions "Analise o deployment neo4j no namespace neo4j-langraph que não está ready e identifique o problema"

# Saída:
# 🔍 Diagnóstico do Deployment: neo4j
#
# Status: 0/1 replicas ready
# Rollout: Failed
#
# Problema: Rollout do deployment falhou
#
# Detalhes:
# - Pod neo4j-xxx-xxx está em CrashLoopBackOff
# - Restarts: 4
# - Last restart: 27s ago
#
# Causa: Permissões do PV não configuradas corretamente
#
# Solução:
# kubectl patch deployment neo4j --type='json' -p='[{"op": "add", "path": "/spec/template/spec/securityContext", "value": {"fsGroup": 7474}}]'
```

---

### **3. Diagnóstico de Service com Problemas**

```bash
kubectl-ai --quiet --skip-permissions "Analise o service neo4j no namespace neo4j-langraph e verifique se os endpoints estão corretos"

# Saída:
# 🔍 Diagnóstico do Service: neo4j
#
# Endpoints:
# - 7474: [10.42.1.172:7474]
# - 7687: [10.42.1.172:7687]
#
# Status: ✅ Endpoints configurados corretamente
#
# Verificação de conectividade:
# - Porta 7474 (http): ✅ Acessível
# - Porta 7687 (bolt): ✅ Acessível
#
# Recomendação: Nenhuma
```

---

### **4. Diagnóstico de PVC com Problemas**

```bash
kubectl-ai --quiet --skip-permissions "Analise o PVC neo4j-data-pvc no namespace neo4j-langraph e identifique o problema"

# Saída:
# 🔍 Diagnóstico do PVC: neo4j-data-pvc
#
# Status: Bound
# Capacity: 5Gi
# Access Modes: ReadWriteOnce
#
# Problema: Nenhum
#
# Detalhes:
# - PV: neo4j-data-pv
# - StorageClass: local-path
# - Mount: /mnt/container-data/projects/neo4j-langraph/neo4j
#
# Recomendação: Nenhuma
```

---

## 🔗 INTEGRAÇÃO COM GITHUB ACTIONS

### **1. Workflow de Testes com kubectl-ai**

```yaml
# .github/workflows/test-with-kubectl-ai.yml
name: Tests with kubectl-ai

on:
  push:
    branches: [main, dev]
  workflow_dispatch:

jobs:
  test:
    runs-on: ubuntu-latest
    container:
      image: bitnami/kubectl:latest
    
    steps:
      - name: Install kubectl-ai
        run: |
          curl -LO https://github.com/kubectl-ai/kubectl-ai/releases/download/v0.1.0/kubectl-ai-linux-amd64
          chmod +x kubectl-ai-linux-amd64
          mv kubectl-ai-linux-amd64 /usr/local/bin/kubectl-ai
      
      - name: Test kubectl-ai
        run: |
          kubectl-ai --quiet "Liste todos os namespaces"
      
      - name: Check pods in neo4j-langraph
        run: |
          kubectl-ai --quiet --skip-permissions "Verifique os pods no namespace neo4j-langraph"
```

---

### **2. Workflow de Deploy com kubectl-ai**

```yaml
# .github/workflows/deploy-with-kubectl-ai.yml
name: Deploy with kubectl-ai

on:
  push:
    branches: [main]
  workflow_dispatch:

jobs:
  deploy:
    runs-on: self-hosted
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Deploy with kubectl-ai
        run: |
          kubectl-ai --quiet --skip-permissions "Aplique os manifests K8S no namespace neo4j-langraph:
          - k8s/base/neo4j/deployment.yaml
          - k8s/base/neo4j/service.yaml
          - k8s/base/localai/deployment.yaml
          - k8s/base/localai/service.yaml
          Aguarde o rollout completar"
      
      - name: Verify deployments
        run: |
          kubectl-ai --quiet --skip-permissions "Verifique os deployments no namespace neo4j-langraph e reporte o status"
      
      - name: Health checks
        run: |
          kubectl-ai --quiet --skip-permissions "Execute health checks nos pods neo4j e localai no namespace neo4j-langraph"
```

---

### **3. Workflow de Backup com kubectl-ai**

```yaml
# .github/workflows/backup-with-kubectl-ai.yml
name: Backup with kubectl-ai

on:
  schedule:
    - cron: '0 2 * * *'  # 2AM UTC
  workflow_dispatch:

jobs:
  backup:
    runs-on: self-hosted
    
    steps:
      - name: Backup Neo4j with kubectl-ai
        run: |
          kubectl-ai --quiet --skip-permissions "Faça backup do Neo4j no namespace neo4j-langraph:
          - Execute: kubectl exec -n neo4j-langraph <pod> -- neo4j-admin backup --from=/data --to=/backup/neo4j_$(date +%Y%m%d_%H%M%S)
          - Verifique integridade do backup
          - Copie o backup para /mnt/container-data/backups/neo4j/
          - Dele backups antigos (mais de 7 dias)
          - Gere relatório de backup"
      
      - name: Backup LocalAI models with kubectl-ai
        run: |
          kubectl-ai --quiet --skip-permissions "Faça backup dos modelos LocalAI no namespace neo4j-langraph:
          - Liste os modelos em /models/
          - Copie os modelos para /mnt/container-data/backups/localai/
          - Verifique integridade dos modelos
          - Gere relatório de backup"
      
      - name: Upload backup report
        uses: actions/upload-artifact@v3
        with:
          name: backup-report-kubectl-ai
          path: backup-report.txt
```

---

## 🏆 MELHORES PRÁTICAS

### **1. Usar Modo Quiet para Scripts**

```bash
# ❌ NÃO (modo interativo não funciona em scripts)
kubectl-ai "Liste todos os pods"

# ✅ SIM (modo quiet funciona em scripts)
kubectl-ai --quiet "Liste todos os pods"
```

---

### **2. Usar --skip-permissions para Operações de Modificação**

```bash
# ❌ NÃO (pede confirmação)
kubectl-ai --quiet "Dele o pod neo4j-xxx"

# ✅ SIM (pula confirmações)
kubectl-ai --quiet --skip-permissions "Dele o pod neo4j-xxx"
```

---

### **3. Usar Prompts Claros e Específicos**

```bash
# ❌ NÃO (prompt vago)
kubectl-ai --quiet "Verifique o pod"

# ✅ SIM (prompt claro)
kubectl-ai --quiet "Verifique o pod neo4j-xxx-xxx no namespace neo4j-langraph e identifique o problema"
```

---

### **4. Usar Sessões para Long-Running Tasks**

```bash
# Criar nova sessão
kubectl-ai --new-session

# Executar múltiplas tarefas na mesma sessão
kubectl-ai --resume-session SESSION_ID "Crie um namespace"
kubectl-ai --resume-session SESSION_ID "Crie um deployment"
kubectl-ai --resume-session SESSION_ID "Verifique o status"

# Deletar sessão após terminar
kubectl-ai --delete-session SESSION_ID
```

---

### **5. Usar Web UI para Visualização**

```bash
# Iniciar Web UI
kubectl-ai --ui-type web --ui-listen-address 0.0.0.0:8888

# Acessar via browser:
# http://localhost:8888
```

---

### **6. Usar TUI para Avançados**

```bash
# Iniciar TUI
kubectl-ai --ui-type tui

# Navegação:
# - ↑/↓: Navegar pelos comandos
# - Enter: Executar comando
# - q: Sair
```

---

## 📚 EXEMPLOS DE USO

### **Exemplo 1: Setup Completo do K3S com kubectl-ai**

```bash
#!/bin/bash
# Script de setup do K3S com kubectl-ai

set -e

echo "🚀 Setup do K3S com kubectl-ai"

# 1. Criar namespace
kubectl-ai --quiet --skip-permissions "Crie o namespace neo4j-langraph"

# 2. Criar secrets
kubectl-ai --quiet --skip-permissions "Crie o secret neo4j-credentials no namespace neo4j-langraph com username=neo4j e password=password"

# 3. Criar PV neo4j-data-pv
kubectl-ai --quiet --skip-permissions "Crie um PersistentVolume neo4j-data-pv com:
- Capacity: 5Gi
- Access Modes: ReadWriteOnce
- Storage Class: local-path
- HostPath: /mnt/container-data/projects/neo4j-langraph/neo4j
- Reclaim Policy: Retain"

# 4. Criar PVC neo4j-data-pvc
kubectl-ai --quiet --skip-permissions "Crie um PersistentVolumeClaim neo4j-data-pvc no namespace neo4j-langraph com:
- Storage Request: 5Gi
- Access Mode: ReadWriteOnce
- Storage Class: local-path"

# 5. Criar deployment Neo4j
kubectl-ai --quiet --skip-permissions "Crie um deployment neo4j no namespace neo4j-langraph com:
- Imagem: docker.io/neo4j:4.4-community
- Réplicas: 1
- Portas: 7474, 7687
- Volume: PVC neo4j-data-pvc em /data
- Secrets: NEO4J_AUTH do secret neo4j-credentials"

# 6. Criar service Neo4j
kubectl-ai --quiet --skip-permissions "Crie um service neo4j no namespace neo4j-langraph com:
- Type: NodePort
- Ports: 7474:30474, 7687:30687
- Selector: app=neo4j"

# 7. Verificar status
kubectl-ai --quiet --skip-permissions "Verifique o status de todos os recursos no namespace neo4j-langraph"

echo "✅ Setup do K3S concluído!"
```

---

### **Exemplo 2: Backup Automatizado com kubectl-ai**

```bash
#!/bin/bash
# Script de backup automatizado com kubectl-ai

set -e

echo "📦 Backup automatizado com kubectl-ai"

# 1. Backup Neo4j
kubectl-ai --quiet --skip-permissions "Faça backup do Neo4j no namespace neo4j-langraph:
- Obtenha o pod neo4j mais recente
- Execute: kubectl exec -n neo4j-langraph <pod> -- neo4j-admin backup --from=/data --to=/backup/neo4j_$(date +%Y%m%d_%H%M%S)
- Verifique se o backup foi criado
- Verifique integridade (tamanho mínimo 10MB)
- Copie o backup para /mnt/container-data/backups/neo4j/"

# 2. Backup LocalAI
kubectl-ai --quiet --skip-permissions "Faça backup dos modelos LocalAI no namespace neo4j-langraph:
- Obtenha o pod localai mais recente
- Liste os modelos em /models/
- Copie os modelos para /mnt/container-data/backups/localai/
- Verifique integridade dos modelos"

# 3. Limpar backups antigos
kubectl-ai --quiet --skip-permissions "Dele todos os backups em /mnt/container-data/backups/neo4j/ que são mais antigos que 7 dias"

# 4. Gerar relatório
kubectl-ai --quiet --skip-permissions "Gere um relatório de backup com:
- Data e hora
- Número de backups
- Tamanho total
- Último backup
- Status de integridade"

echo "✅ Backup concluído!"
```

---

### **Exemplo 3: Diagnóstico e Recuperação Automática**

```bash
#!/bin/bash
# Script de diagnóstico e recuperação automática

set -e

echo "🔍 Diagnóstico e recuperação automática"

# 1. Verificar saúde dos pods
kubectl-ai --quiet --skip-permissions "Verifique a saúde de todos os pods no namespace neo4j-langraph e identifique quaisquer problemas"

# 2. Diagnóstico de pods com problemas
kubectl-ai --quiet --skip-permissions "Analise todos os pods no namespace neo4j-langraph que estão em status CrashLoopBackOff e identifique o problema"

# 3. Reiniciar pods com problemas
kubectl-ai --quiet --skip-permissions "Reinicie todos os pods no namespace neo4j-langraph que estão em status CrashLoopBackOff"

# 4. Aguardar rollout
kubectl-ai --quiet --skip-permissions "Aguarde o rollout dos deployments neo4j e localai no namespace neo4j-langraph completar"

# 5. Verificar saúde pós-recuperação
kubectl-ai --quiet --skip-permissions "Verifique a saúde de todos os pods no namespace neo4j-langraph novamente e confirme que todos estão rodando"

echo "✅ Diagnóstico e recuperação concluídos!"
```

---

### **Exemplo 4: Monitoramento Contínuo com kubectl-ai**

```bash
#!/bin/bash
# Script de monitoramento contínuo

set -e

echo "📊 Monitoramento contínuo"

while true; do
    # Verificar saúde dos pods
    kubectl-ai --quiet --skip-permissions "Verifique a saúde de todos os pods no namespace neo4j-langraph e reporte quaisquer problemas"
    
    # Verificar saúde dos deployments
    kubectl-ai --quiet --skip-permissions "Verifique o status dos deployments neo4j e localai no namespace neo4j-langraph"
    
    # Aguardar 60 segundos
    sleep 60
done
```

---

## 📊 RESUMO DE KUBECTL-AI

### **Comandos Principais**

| Comando | Descrição |
|----------|-----------|
| `kubectl-ai` | Modo interativo |
| `kubectl-ai --quiet` | Modo não-interativo |
| `kubectl-ai --skip-permissions` | Pular confirmações |
| `kubectl-ai --new-session` | Criar nova sessão |
| `kubectl-ai --resume-session` | Retomar sessão |
| `kubectl-ai --list-sessions` | Listar sessões |
| `kubectl-ai --delete-session` | Deletar sessão |
| `kubectl-ai --ui-type web` | Interface web |
| `kubectl-ai --ui-type tui` | Interface TUI |

---

### **Modos de Interface**

| Tipo | Comando | Quando usar |
|-------|----------|-------------|
| **Terminal** | `kubectl-ai` | Uso diário |
| **Web** | `kubectl-ai --ui-type web` | Visualização |
| **TUI** | `kubectl-ai --ui-type tui` | Avançado |

---

### **LLM Providers**

| Provider | Modelo | Comando |
|----------|---------|----------|
| **Zhipu AI** | glm-4.7 | `kubectl-ai --llm-provider zai` |
| **Google** | gemini-2.0-flash | `kubectl-ai --llm-provider google` |
| **OpenAI** | gpt-4 | `kubectl-ai --llm-provider openai` |
| **Anthropic** | claude-3-opus | `kubectl-ai --llm-provider anthropic` |

---

### **Fluxos de Trabalho**

| Tarefa | Comando kubectl-ai |
|-------|-------------------|
| **Criar recursos** | `kubectl-ai --quiet --skip-permissions "Crie..."` |
| **Atualizar recursos** | `kubectl-ai --quiet --skip-permissions "Atualize..."` |
| **Deletar recursos** | `kubectl-ai --quiet --skip-permissions "Dele..."` |
| **Monitorar saúde** | `kubectl-ai --quiet "Verifique..."` |
| **Diagnosticar problemas** | `kubectl-ai --quiet "Analise..."` |
| **Backup** | `kubectl-ai --quiet --skip-permissions "Faça backup..."` |
| **Recuperação** | `kubectl-ai --quiet --skip-permissions "Reinicie..."` |

---

**🎉 KUBECTL-AI: ORQUESTRAÇÃO E MANUTENÇÃO DE KUBERNETES COMPLETO!** 🚀

---

**Status:** ✅ AGENTS.md ATUALIZADO COM KUBECTL-AI! 🎉

**Autor:** CNMFS  
**Data:** 28/12/2024  
**Versão:** 1.1.0 (com kubectl-ai)

