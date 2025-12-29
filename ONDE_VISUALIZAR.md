# ONDE_VISUALIZAR.md - Onde e como visualizar o sistema

Este documento explica TUDO sobre visualização e uso do sistema.

---

## 🎯 3 FORMAS DE INTERAGIR COM O SISTEMA

```
┌─────────────────────────────────────────────────────────┐
│  3 FORMAS DE USAR O SISTEMA                              │
└─────────────────────────────────────────────────────────┘

1. 📊 CLI (Linha de Comando)
   → Para operações principais
   → Ingestão, busca, queries, dashboard

2. 🌐 Neo4j Browser (Web)
   → Para visualizar o GRAFO
   → Ver nós, relacionamentos, dados

3. 🚀 k9s (Gerenciador)
   → Para ver CONTAINERS/PODS
   → Monitorar K3S, LocalAI, Neo4j
```

---

## 📊 1. CLI (Linha de Comando) - OPERAÇÕES PRINCIPAIS

### Sistema de Conhecimento Pessoal:

```bash
# Ingerir conhecimento
.venv/bin/python -m src.cli.knowledge_cli ingest /path/to/docs

# Criar relacionamentos
.venv/bin/python -m src.cli.knowledge_cli relationships

# Detectar clusters
.venv/bin/python -m src.cli.knowledge_cli clusters

# Fazer queries (busca conversacional)
.venv/bin/python -m src.cli.knowledge_cli query "Django"

# Ver dashboard completo
.venv/bin/python -m src.cli.knowledge_cli dashboard
```

### Sistema de Governança de Projetos:

```bash
# Indexar projeto
.venv/bin/python -m src.cli.project_cli index /path/to/project

# Calcular similaridades
.venv/bin/python -m src.cli.project_cli similarity

# Detectar mudanças
.venv/bin/python -m src.cli.project_cli detect-changes

# Gerar relatório
.venv/bin/python -m src.cli.project_cli report
```

---

## 🌐 2. Neo4j Browser (Web) - VISUALIZAR GRAFO

### Acessar Neo4j Browser:

```bash
# Depois do setup, acesse:
open http://localhost:30474
```

**Credenciais:**
- Usuário: `neo4j`
- Senha: `password`

### O que ver no Neo4j Browser:

```
┌─────────────────────────────────────────────────────────┐
│  NEO4J BROWSER (Web Interface)                          │
└─────────────────────────────────────────────────────────┘

1. Editor de Queries (Cypher)
   → Escrever queries para explorar o grafo

2. Visualização de Grafo
   → Ver nós e relacionamentos visualmente

3. Tabela de Resultados
   → Ver dados em formato tabular

4. Informações do Grafo
   → Estatísticas, número de nós, relacionamentos
```

### Exemplos de Queries para Visualizar:

```cypher
-- Ver todos os nós
MATCH (n) RETURN n LIMIT 50

-- Ver relacionamentos entre nós
MATCH (n1)-[r]->(n2) RETURN n1, r, n2 LIMIT 50

-- Ver itens de conhecimento
MATCH (i:Item) RETURN i LIMIT 50

-- Ver relacionamentos semânticos
MATCH (i:Item)-[r:RELACIONADO_A]->(i2:Item)
WHERE r.score > 0.8
RETURN i.nome, r.score, i2.nome

-- Ver clusters
MATCH (c:Cluster)-[:CONTÉM]->(i:Item)
RETURN c.nome, count(i) as itens
ORDER BY itens DESC
```

---

## 🚀 3. k9s (Gerenciador) - MONITORAR CONTAINERS/PODS

### Abrir k9s:

```bash
k9s -n neo4j-langraph
```

### O que ver no k9s:

```
┌─────────────────────────────────────────────────────────┐
│  k9s - Gerenciador de Pods K3S                         │
└─────────────────────────────────────────────────────────┘

Pods:
  • neo4j-xxx-xxx           - Grafo de conhecimento
  • localai-xxx-xxx         - Servidor de IA (llama.cpp)

Serviços:
  • neo4j                   - Grafo
  • localai                 - IA

Logs:
  • Ver logs de cada pod

Status:
  • Running, Pending, Error, etc
```

### Comandos úteis no k9s:

```
/     - Buscar recursos
:pod  - Filtrar por pods
:svc  - Filtrar por serviços
l     - Ver logs
s     - Executar shell
d     - Descrever recurso
ctrl+d - Remover recurso
```

---

## 🎮 ESTRUTURA DO SISTEMA (CONTAINERS)

### O projeto usa K3S (Kubernetes), NÃO Docker!

```
┌─────────────────────────────────────────────────────────┐
│  K3S CLUSTER (Kubernetes Leve)                         │
└─────────────────────────────────────────────────────────┘

Namespace: neo4j-langraph

┌─────────────────────────────────────────────────────────┐
│  CONTAINER: Neo4j                                       │
├─────────────────────────────────────────────────────────┤
│                                                        │
│  • Função: Banco de dados de grafos                    │
│  • Porta HTTP: 30474                                   │
│  • Porta BOLT: 30687                                   │
│  • VRAM: Não usa (CPU)                                 │
│  • Acesso: http://localhost:30474                        │
│                                                        │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  CONTAINER: LocalAI                                     │
├─────────────────────────────────────────────────────────┤
│                                                        │
│  • Função: Servidor de IA (llama.cpp)                  │
│  • Porta: 30808                                        │
│  • VRAM: 1.5GB (embeddings) + 4.5GB (código)          │
│  • Acesso: http://localhost:30808/docs                   │
│  • API: 100% OpenAI-compatible                        │
│                                                        │
└─────────────────────────────────────────────────────────┘
```

---

## 📋 COMO TESTAR AGORA?

### Passo 1: Verificar Status

```bash
./check_status.sh
```

Isso vai mostrar:
- ✅ Se K3S está rodando
- ✅ Se pods estão rodando
- ✅ Se serviços estão disponíveis
- ✅ Se Google API Key está configurada
- ✅ URLs para acessar cada serviço

---

### Passo 2: Se Tudo OK, Testar

```bash
# 1. Testar configuração (LLM + Embeddings)
.venv/bin/python test_gemini_embeddings.py

# 2. Ingerir alguns documentos de teste
mkdir -p test_data
echo "Django é um framework web em Python" > test_data/django.txt
echo "FastAPI é moderno e rápido" > test_data/fastapi.txt

.venv/bin/python -m src.cli.knowledge_cli ingest test_data

# 3. Fazer uma query
.venv/bin/python -m src.cli.knowledge_cli query "frameworks web"

# 4. Ver dashboard
.venv/bin/python -m src.cli.knowledge_cli dashboard
```

---

### Passo 3: Visualizar Grafo (Neo4j Browser)

```bash
# Abrir no navegador
open http://localhost:30474
```

Ou acesse: http://localhost:30474

Credenciais:
- Usuário: `neo4j`
- Senha: `password`

Query para ver tudo:
```cypher
MATCH (n) RETURN n LIMIT 100
```

---

### Passo 4: Monitorar Pods (k9s)

```bash
# Abrir k9s
k9s -n neo4j-langraph
```

Ver:
- Status dos pods (Running, Error, etc.)
- Logs de cada pod
- Uso de recursos
- Portas e serviços

---

## 🔌 ENDPOINTS DISPONÍVEIS

### Após `./setup.sh`:

```bash
┌─────────────────────────────────────────────────────────┐
│  ENDPOINTS DISPONÍVEIS                                    │
└─────────────────────────────────────────────────────────┘

Neo4j HTTP (Grafo):
  → http://localhost:30474
  → Usuário: neo4j, Senha: password

Neo4j BOLT (Grafo API):
  → bolt://localhost:30687

LocalAI (IA API):
  → http://localhost:30808
  → API Docs: http://localhost:30808/docs
  → Modelos: http://localhost:30808/v1/models
```

---

## 📊 VISUALIZAÇÃO DO GRAFO

### No Neo4j Browser, você verá:

```
┌─────────────────────────────────────────────────────────┐
│  VISUALIZAÇÃO DO GRAFO                                   │
└─────────────────────────────────────────────────────────┘

🔵 NÓS (Itens de Conhecimento):
  • Item (nota, projeto, tutorial, etc.)
  • Tópico (tema principal)
  • Tecnologia (Django, FastAPI, etc.)
  • Cluster (grupo de itens relacionados)

➖ RELACIONAMENTOS:
  • SOBRE (item é sobre um tópico)
  • MENCIONA (item menciona uma tecnologia)
  • TAG (item tem tag)
  • RELACIONADO_A (semântico, com score)
  • VERSÃO_ANTERIOR (evolução)

📊 ESTATÍSTICAS:
  • Total de nós
  • Total de relacionamentos
  • Clusters detectados
  • Tópicos mais comuns
  • Tecnologias usadas
```

---

## 💡 EXEMPLO PRÁTICO COMPLETO

### 1. Ingerir Documentos

```bash
# Criar dados de teste
mkdir -p test_data

cat > test_data/django_rest.txt << 'EOF'
Django REST Framework é poderoso.
Permite criar APIs REST rapidamente.
EOF

cat > test_data/fastapi_async.txt << 'EOF'
FastAPI é moderno e assíncrono.
Muito rápido para desenvolvimento.
EOF

# Ingerir
.venv/bin/python -m src.cli.knowledge_cli ingest test_data
```

### 2. Criar Relacionamentos

```bash
.venv/bin/python -m src.cli.knowledge_cli relationships --threshold 0.7
```

### 3. Ver no Neo4j Browser

```bash
# Abrir
open http://localhost:30474

# Query
MATCH (n) RETURN n

# Ou relacionamentos
MATCH (n1)-[r]->(n2) RETURN n1, r, n2
```

### 4. Fazer Query via CLI

```bash
.venv/bin/python -m src.cli.knowledge_cli query "APIs modernas"
```

---

## 📝 RESUMO

| Método | O que faz | Como acessar |
|--------|-----------|-------------|
| **CLI** | Operações principais | Terminal |
| **Neo4j Browser** | Visualizar grafo | http://localhost:30474 |
| **k9s** | Monitorar pods | `k9s -n neo4j-langraph` |

---

**Pronto para testar!** 🚀

Execute `./check_status.sh` para ver o status atual!
