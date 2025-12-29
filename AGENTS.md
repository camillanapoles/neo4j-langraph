# AGENTS.md - Guia para Agentes no Projeto Neo4j Langraph

Este documento contém tudo o que um agente precisa saber para trabalhar efetivamente neste repositório.

## 📋 Visão Geral do Projeto

Este projeto implementa um **Sistema de Gerenciamento de Conhecimento com Grafo** usando Neo4j e LangChain. Ele consiste em dois subsistemas principais:

1. **Sistema de Conhecimento Pessoal** (`src/knowledge_system/`) - Organização automática de notas, projetos, prompts e insights pessoais
2. **Sistema de Governança de Projetos** (`src/project_governance/`) - Indexação e governança de documentação técnica de projetos

## 🚀 Configuração do Ambiente

### Ambiente Python Isolado

Este projeto usa **uv** como gerenciador de pacotes para ambientes Python isolados. O ambiente virtual já foi criado com:

```bash
.venv/bin/python
```

**Importante**: Sempre use o Python do ambiente virtual isolado para não misturar versões de pacotes entre projetos.

### Instalação de Dependências

As dependências já estão instaladas usando `uv`. Para reinstalar:

```bash
uv pip install -e ".[dev]"
```

### Variáveis de Ambiente

O arquivo `.env` deve conter:
- `OPENAI_API_KEY` - Chave da API da OpenAI (obrigatória)
- `NEO4J_URI` - URI do Neo4j (padrão: bolt://localhost:7687)
- `NEO4J_USERNAME` - Usuário Neo4j (padrão: neo4j)
- `NEO4J_PASSWORD` - Senha Neo4j (padrão: password)

**CRÍTICO**: A variável `OPENAI_API_KEY` deve ser configurada antes de qualquer operação que envolva LLMs.

## ☸️ Neo4j (K3S + Buildah)

### Deploy no K3S

```bash
./deploy.sh
```

### Verificar Status

```bash
# Via k9s (recomendado)
k9s -n neo4j-langraph

# Via kubectl/k3s kubectl
kubectl get pods -n neo4j-langraph
kubectl get svc -n neo4j-langraph
```

### Acessar Neo4j Browser

Abra: http://localhost:30474
- Usuário: `neo4j`
- Senha: `password`

### Port-Forward (Desenvolvimento)

```bash
./port-forward.sh
```

Neo4j estará disponível em http://localhost:7474

### Logs

```bash
./logs.sh
```

### Limpar Recursos

```bash
./undeploy.sh
```

## 🏗️ Estrutura do Código

### Diretórios Principais

```
k8s/
└── neo4j/
    └── neo4j-deployment.yaml  # Manifestos K3S para Neo4j
```

```
src/
├── config.py                 # Configurações e conexões (Neo4j, LLM, embeddings)
├── shared/                   # Utilitários compartilhados
│   ├── embeddings.py        # Gerenciador de embeddings (1536 dimensões)
│   ├── llm.py              # Configurações de LLM para diferentes casos
│   └── utils.py            # Funções utilitárias (hash, leitura de arquivos)
├── knowledge_system/        # Sistema de conhecimento pessoal
│   ├── ingestion.py        # Ingestão de arquivos e classificação automática
│   ├── relationships.py     # Relacionamentos semânticos e clusterização
│   └── queries.py          # Interface conversacional e queries predefinidas
├── project_governance/      # Governança de projetos
│   ├── indexer.py          # Indexação de projetos e extração de metadados
│   ├── similarity.py       # Similaridade entre projetos e agrupamento
│   └── versioning.py       # Versionamento e detecção de mudanças
└── cli/                     # Interfaces de linha de comando
    ├── knowledge_cli.py    # CLI para sistema de conhecimento
    └── project_cli.py     # CLI para governança de projetos
```

## 🔧 Comandos Essenciais

### Sistema de Conhecimento Pessoal

Todos os comandos usam: `neo4j-knowledge`

**Ingerir conhecimento:**
```bash
neo4j-knowledge ingest /caminho/do/conhecimento
```

**Criar relacionamentos semânticos:**
```bash
neo4j-knowledge relationships --threshold 0.75
```

**Detectar clusters:**
```bash
neo4j-knowledge clusters --min-connections 2
```

**Mostrar dashboard:**
```bash
neo4j-knowledge dashboard
```

**Fazer perguntas (interface conversacional):**
```bash
neo4j-knowledge query "Mostre tudo sobre Machine Learning"
neo4j-knowledge query "Quais notas podem virar projetos?" --show-cypher
```

### Sistema de Governança de Projetos

Todos os comandos usam: `neo4j-governance`

**Indexar projeto:**
```bash
neo4j-governance index /caminho/do/projeto
```

**Calcular similaridades entre projetos:**
```bash
neo4j-governance similarity --threshold 0.7
```

**Detectar mudanças na documentação:**
```bash
neo4j-governance detect-changes
```

**Gerar relatório de governança:**
```bash
neo4j-governance report
```

**Mostrar dashboard de projetos:**
```bash
neo4j-governance dashboard
```

## 🧩 Padrões e Convenções

### Uso de LLMs

O projeto usa **diferentes modelos LLM** para diferentes propósitos (veja `src/shared/llm.py`):

- **Classificação**: `gpt-4o-mini` (rápido, econômico, temperatura 0.0)
- **Geração de Queries Cypher**: `gpt-4` (precisão crítica, temperatura 0.0)
- **Síntese de Respostas**: `gpt-3.5-turbo` (rápido, temperatura 0.0)
- **Análise e Clusterização**: `gpt-4` (criativo, temperatura 0.3)

**Regra**: Use sempre os métodos de `LLMConfig` para obter LLMs, não instancie diretamente.

### Embeddings

- **Modelo**: `text-embedding-ada-002`
- **Dimensões**: 1536
- **Função de Similaridade**: Cosine

**Importante**: Todos os embeddings no grafo usam estas mesmas configurações para compatibilidade.

### Grafos e Conexões

Sempre use `get_graph()` de `src.config` para obter conexão com Neo4j. Nunca instancie `Neo4jGraph` diretamente.

```python
from src.config import get_graph

graph = get_graph()
result = graph.query("MATCH (n:Item) RETURN n")
```

### Consultas Cypher

As queries Cypher são geradas automaticamente pelo `GraphCypherQAChain`. Para queries manuais:

- Sempre use parâmetros para evitar injeção: `MATCH (n {id: $id})`
- Use `toLower()` para buscas case-insensitive: `WHERE toLower(n.nome) CONTAINS toLower($term)`
- Índices vetoriais usam opções específicas: `vector.dimensions: 1536`, `vector.similarity_function: 'cosine'`

## 📊 Modelo de Dados

### Sistema de Conhecimento

**Nós:**
- `Item` - Nó universal para qualquer conteúdo (arquivo, nota, projeto, etc)
- `Topico` - Tópicos mencionados nos itens
- `Conceito` - Conceitos técnicos ou abstratos
- `Tecnologia` - Tecnologias mencionadas
- `Tag` - Tags/palavras-chave
- `Cluster` - Grupos emergentes de itens relacionados

**Relacionamentos:**
- `Item-[:SOBRE]->Topico`
- `Item-[:MENCIONA]->Conceito`
- `Item-[:USA_TECNOLOGIA]->Tecnologia`
- `Item-[:TAG]->Tag`
- `Item-[:RELACIONADO_A {score}]->Item` (similaridade semântica)
- `Item-[:EVOLUIU_PARA]->Item` (evolução temporal)

### Sistema de Governança

**Nós:**
- `Projeto` - Projetos de software
- `Arquivo` - Arquivos de documentação
- `Stack` - Tecnologias usadas (Django, FastAPI, etc)
- `Tema` - Área/domínio (odontológico, e-commerce, etc)
- `Versao` - Versões de projeto

**Relacionamentos:**
- `Projeto-[:CONTEM]->Arquivo`
- `Projeto-[:USA_STACK]->Stack`
- `Projeto-[:TEM_TEMA]->Tema`
- `Projeto-[:TEM_VERSAO]->Versao`
- `Projeto-[:SIMILAR_A {score}]->Projeto` (similaridade entre projetos)
- `Arquivo-[:VERSAO_ANTERIOR]->Arquivo` (versionamento)

## ⚠️ Gotchas Importantes

### 1. Limiares de Similaridade

- **Conhecimento pessoal**: 0.75-0.85 padrão, ajuste conforme necessário
- **Similaridade de projetos**: 0.70-0.80 padrão
- **Evoluções**: > 0.85 (requer alta confiança)
- **Clusters**: > 0.8 para clusters fortes

### 2. Tamanho de Conteúdo

- **Embeddings**: Limitado a 8000 caracteres (padrão)
- **Armazenamento no grafo**: Limitado a 15000 caracteres (conhecimento) ou 10000 (projetos)
- **Envio para LLM**: Limitado a 4000-6000 caracteres para classificação

### 3. Versões de Arquivos

- Arquivos mudados são versionados automaticamente pelo hash SHA-256
- Arquivo mais recente tem `status: 'atual'`
- Arquivo anterior tem `status: 'obsoleta'`
- Use `VersionManager.detect_changes()` para atualizar

### 4. Índices Vetoriais

Deve criar índices vetoriais antes de usar similaridade:

```python
# Para conhecimento pessoal
graph.query("""
CREATE VECTOR INDEX itens_similares IF NOT EXISTS
FOR (i:Item) ON i.embedding
OPTIONS {indexConfig: {
  `vector.dimensions`: 1536,
  `vector.similarity_function`: 'cosine'
}}
""")

# Para projetos
graph.query("""
CREATE VECTOR INDEX projetos_similares IF NOT EXISTS
FOR (p:Projeto) ON p.embedding_descricao
OPTIONS {indexConfig: {
  `vector.dimensions`: 1536,
  `vector.similarity_function`: 'cosine'
}}
""")
```

### 5. Classificação de Tipos

Tipos primários suportados (do `Ingestion._classify_item`):
- `projeto`, `nota`, `prompt`, `insight`, `anotacao`
- `documentacao`, `ideia`, `tutorial`, `codigo`, `artigo`
- `receita`, `outro`

### 6. Ordem de Operações

Fluxo típico para conhecimento pessoal:
1. `ingest` - ingerir arquivos
2. `relationships` - criar relacionamentos semânticos
3. `clusters` - detectar clusters e evoluções
4. `query` - fazer perguntas

Fluxo típico para projetos:
1. `index` - indexar projeto(s)
2. `similarity` - calcular similaridades
3. `detect-changes` - atualizar versões
4. `report` - ver relatório de governança

## 🧪 Testes e Debugging

### Verificar Conexão Neo4j

Primeiro, garanta que Neo4j está rodando no K3S:

```bash
k9s -n neo4j-langraph
# Verifique que o pod neo4j está running
```

```python
from src.config import get_graph

graph = get_graph()
result = graph.query("RETURN 1 as test")
print(result)  # Deve retornar [{'test': 1}]
```

### Verificar LLM

```python
from src.shared.llm import LLMConfig

llm = LLMConfig.classification_llm()
result = llm.invoke("Olá, mundo!")
print(result.content)
```

### Verificar Embeddings

```python
from src.shared.embeddings import EmbeddingManager

em = EmbeddingManager()
emb = em.embed_text("Texto de exemplo")
print(f"Dimensões: {len(emb)}")  # Deve ser 1536
```

### Testar Scripts CLI

Primeiro, garanta que Neo4j está rodando no K3S:

```bash
./deploy.sh
k9s -n neo4j-langraph
```

```bash
# Testar conhecimento
neo4j-knowledge ingest ./test_data
neo4j-knowledge dashboard

# Testar governança
neo4j-governance index ./test_project
neo4j-governance report
```

## 📝 Documentação de Referência

- `knownledge.md` - Base técnica completa sobre Neo4j + LangChain (inglês)
- `objetivo_generalista.md` - Especificação do sistema de conhecimento pessoal
- `objetivo_projetos.md` - Especificação do sistema de governança
- `README.md` - Documentação geral do projeto

## 🔍 Queries Úteis para Debug

### Verificar todos os itens no grafo
```cypher
MATCH (i:Item) RETURN i.nome, i.tipo, i.path LIMIT 20
```

### Verificar relacionamentos
```cypher
MATCH (i1:Item)-[r:RELACIONADO_A]->(i2:Item)
RETURN i1.nome, r.score, i2.nome
ORDER BY r.score DESC
LIMIT 10
```

### Verificar tópicos mais populares
```cypher
MATCH (t:Topico)<-[:SOBRE]-(i:Item)
RETURN t.nome, count(i) as itens
ORDER BY itens DESC
LIMIT 10
```

### Verificar versões de arquivos
```cypher
MATCH (a1:Arquivo)-[:VERSAO_ANTERIOR]->(a2:Arquivo)
RETURN a1.nome, a1.status, a2.nome, a2.status
```

## 🎯 Boas Práticas

1. **Sempre use o ambiente virtual isolado** (`.venv/bin/python`)
2. **Configure `OPENAI_API_KEY`** antes de qualquer operação com LLM
3. **Deploy Neo4j no K3S** antes de executar qualquer comando: `./deploy.sh`
4. **Use k9s para monitoramento**: `k9s -n neo4j-langraph`
5. **Use os CLI scripts** em vez de executar módulos Python diretamente
6. **Verifique o dashboard** após qualquer operação major de ingestão/indexação
7. **Limiares de similaridade**: comece com 0.75 e ajuste conforme resultados
8. **Versionamento**: execute `detect-changes` periodicamente para manter grafo atualizado
9. **Backup**: os dados do Neo4j persistem em PVC, faça backups regulares do namespace

## 🚨 Erros Comuns

### "OPENAI_API_KEY not found"
**Solução**: Configure a variável no arquivo `.env`

### "Connection refused" ao conectar ao Neo4j
**Solução**: Verifique status com k9s ou kubectl:
```bash
k9s -n neo4j-langraph
# ou
kubectl get pods -n neo4j-langraph
```

### Pod Neo4j não inicia (CrashLoopBackOff)
**Solução**: Verifique logs e eventos:
```bash
./logs.sh
# ou
kubectl logs -n neo4j-langraph deployment/neo4j
kubectl describe pod -n neo4j-langraph -l app=neo4j
```

### PVC não cria ou não conecta
**Solução**: Verifique se storageClass `local-path` está disponível no K3S:
```bash
kubectl get storageclass
```

### Embedding dimensions mismatch
**Solução**: Garanta que todos os índices vetoriais usam `vector.dimensions: 1536`

### Queries retornam vazio
**Solução**: Verifique se há dados no grafo: `MATCH (n) RETURN count(n)`

### Python modules not found
**Solução**: Reinstale dependências: `uv pip install -e ".[dev]"`

---

Este documento é mantido atualizado. Se encontrar algo que deva ser adicionado, atualize-o.
