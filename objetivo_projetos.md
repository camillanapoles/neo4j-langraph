# PROPOSTA PARA PROJETOS
---

✅ **Agrupar projetos por similaridade** (dominio ou publico-alvo + tipo-aplicacso)  
✅ **Detectar diferentes stacks** (ex: Django vs FastAPI)  
✅ **Ordenar cronologicamente** (criação → desenvolvimento → versões)  
✅ **Agrupar por tecnologia** (todos Django juntos, todos FastAPI juntos)  
✅ **Rastrear versões de documentação** (atual vs desatualizada)  
✅ **Detectar mudanças e inconsistências** (docs conflitantes)  

**Como?** Combinando **busca semântica** (similaridade) + **estrutura de grafo** (relações + versões) + **LLM** (extração automática de metadados).

---

## **📋 OBJETIVO DO SEU PROJETO**

### **Copie e Cole Este Objetivo**:

```
OBJETIVO: Sistema de Governança e Organização de Documentação de Projetos

PROBLEMA: 
Documentação de múltiplos projetos está dispersa, desorganizada e com versões 
conflitantes. Não há visibilidade de qual stack cada projeto usa, qual 
documentação está atualizada, e como projetos relacionados se conectam.

SOLUÇÃO:
Construir um grafo de conhecimento que indexa automaticamente documentação, 
extrai metadados (stack, versão, tema), detecta similaridades, agrupa por 
tecnologia, rastreia versões temporalmente e alerta sobre inconsistências.

ENTREGAS:
1. Indexação automática de todos os diretórios de projetos
2. Agrupamento por similaridade de tema (ex: todos projetos odontológicos)
3. Classificação por stack tecnológica (Django, FastAPI, React, etc)
4. Linha do tempo de versões de documentação
5. Detecção de documentação desatualizada ou conflitante
6. Interface conversacional para perguntar: 
   - "Quais projetos usam FastAPI?"
   - "Qual a documentação mais recente do projeto X?"
   - "Mostre projetos similares ao sistema odontológico"

SUCESSO:
- Zero tempo gasto procurando documentação
- Clareza sobre qual versão é a atual
- Decisões informadas sobre reutilização de código entre projetos similares
```

---

## **🏗️ ARQUITETURA ADAPTADA AO SEU CASO**

### **Modelo de Grafo Completo**:

```
(Projeto)-[:USA_STACK]->(Stack: "Django")
(Projeto)-[:TEM_TEMA]->(Tema: "Odontológico")
(Projeto)-[:TEM_VERSAO]->(Versao)-[:ANTERIOR_DE]->(Versao)
(Projeto)-[:CONTEM]->(Diretorio)-[:CONTEM]->(Arquivo)
(Arquivo)-[:VERSAO_DE]->(Arquivo)
(Projeto)-[:SIMILAR_A {score: 0.85}]->(Projeto)
(Arquivo)-[:DOCUMENTA {data_criacao, status}]->(Componente)
```

**Propriedades importantes**:
- **Projeto**: `nome`, `tema`, `data_criacao`, `embedding_descricao`
- **Stack**: `nome` (Django, FastAPI, React, PostgreSQL)
- **Versao**: `numero`, `data`, `changelog`, `status` (atual/obsoleta)
- **Arquivo**: `path`, `conteudo`, `embedding`, `hash_conteudo`, `ultima_modificacao`

---

## **⚙️ IMPLEMENTAÇÃO PASSO A PASSO**

### **PASSO 1: Indexação com Extração Automática de Metadados**

```python
from pathlib import Path
from langchain_neo4j import Neo4jGraph
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
import hashlib
from datetime import datetime

graph = Neo4jGraph(
    url="bolt://localhost:7687",
    username="neo4j",
    password="password"
)

llm = ChatOpenAI(model="gpt-4o-mini")
embedding_model = OpenAIEmbeddings(model="text-embedding-ada-002")

# Prompt para extração de metadados
prompt_extracao = ChatPromptTemplate.from_messages([
    ("system", """Analise este arquivo de documentação e extraia em JSON:
    {{
      "projeto_nome": "nome do projeto identificado",
      "tema": "área/domínio (ex: odontológico, e-commerce, financeiro)",
      "stacks": ["Django", "FastAPI", "React", etc],
      "versao": "número/identificador de versão se mencionado",
      "componentes": ["API", "Frontend", "Database", etc],
      "status": "em_desenvolvimento / producao / descontinuado"
    }}
    
    Se algo não estiver claro, use null.
    """),
    ("user", "Arquivo: {nome}\nCaminho: {path}\n\nConteúdo:\n{conteudo}")
])

chain_extracao = prompt_extracao | llm

def indexar_projeto(diretorio_raiz: str):
    """
    Indexa um diretório de projeto completo
    """
    raiz = Path(diretorio_raiz)
    projeto_nome = raiz.name
    
    print(f"📁 Indexando projeto: {projeto_nome}")
    
    # Criar nó do projeto
    graph.query("""
    MERGE (p:Projeto {nome: $nome})
    ON CREATE SET p.data_criacao = datetime()
    SET p.path = $path
    """, {"nome": projeto_nome, "path": str(raiz)})
    
    # Indexar todos os arquivos de documentação
    arquivos_docs = list(raiz.rglob("*.md")) + \
                    list(raiz.rglob("*.rst")) + \
                    list(raiz.rglob("README*")) + \
                    list(raiz.rglob("CHANGELOG*"))
    
    for arquivo in arquivos_docs:
        indexar_arquivo(arquivo, projeto_nome)
    
    print(f"✅ Projeto {projeto_nome} indexado com {len(arquivos_docs)} arquivos")

def indexar_arquivo(arquivo: Path, projeto_nome: str):
    """
    Indexa um arquivo individual com extração de metadados
    """
    try:
        conteudo = arquivo.read_text(encoding='utf-8')
    except:
        print(f"⚠️ Erro ao ler {arquivo}")
        return
    
    # Hash do conteúdo (para detectar mudanças)
    hash_conteudo = hashlib.sha256(conteudo.encode()).hexdigest()
    
    # Timestamp de modificação
    ultima_modificacao = datetime.fromtimestamp(arquivo.stat().st_mtime)
    
    # Gerar embedding
    embedding = embedding_model.embed_query(conteudo[:8000])  # Limitar tamanho
    
    # Extrair metadados com LLM
    print(f"  🔍 Analisando {arquivo.name}...")
    resultado = chain_extracao.invoke({
        "nome": arquivo.name,
        "path": str(arquivo),
        "conteudo": conteudo[:4000]  # Primeiros 4k chars
    })
    
    # Parse do JSON (com tratamento de erro)
    try:
        import json
        metadados = json.loads(resultado.content)
    except:
        metadados = {
            "projeto_nome": projeto_nome,
            "tema": None,
            "stacks": [],
            "versao": None,
            "componentes": [],
            "status": None
        }
    
    # Inserir arquivo no grafo
    graph.query("""
    MATCH (p:Projeto {nome: $projeto_nome})
    
    // Criar arquivo
    MERGE (a:Arquivo {path: $path})
    SET a.nome = $nome,
        a.conteudo = $conteudo,
        a.embedding = $embedding,
        a.hash_conteudo = $hash,
        a.ultima_modificacao = $modificacao,
        a.tamanho = $tamanho
    
    // Conectar ao projeto
    MERGE (p)-[:CONTEM]->(a)
    """, {
        "projeto_nome": projeto_nome,
        "path": str(arquivo),
        "nome": arquivo.name,
        "conteudo": conteudo[:10000],  # Limitar storage
        "embedding": embedding,
        "hash": hash_conteudo,
        "modificacao": ultima_modificacao.isoformat(),
        "tamanho": len(conteudo)
    })
    
    # Adicionar tema ao projeto
    if metadados.get("tema"):
        graph.query("""
        MATCH (p:Projeto {nome: $projeto_nome})
        MERGE (t:Tema {nome: $tema})
        MERGE (p)-[:TEM_TEMA]->(t)
        """, {"projeto_nome": projeto_nome, "tema": metadados["tema"]})
    
    # Adicionar stacks
    for stack in metadados.get("stacks", []):
        graph.query("""
        MATCH (p:Projeto {nome: $projeto_nome})
        MERGE (s:Stack {nome: $stack})
        MERGE (p)-[:USA_STACK]->(s)
        """, {"projeto_nome": projeto_nome, "stack": stack})
    
    # Adicionar versão se identificada
    if metadados.get("versao"):
        graph.query("""
        MATCH (p:Projeto {nome: $projeto_nome})
        MERGE (v:Versao {numero: $versao, projeto: $projeto_nome})
        SET v.data = datetime()
        MERGE (p)-[:TEM_VERSAO]->(v)
        """, {"projeto_nome": projeto_nome, "versao": metadados["versao"]})
    
    print(f"    ✅ {arquivo.name} → Tema: {metadados.get('tema')} | Stacks: {metadados.get('stacks')}")

# EXECUTAR INDEXAÇÃO
indexar_projeto("/caminho/para/projeto-odontologico")
indexar_projeto("/caminho/para/projeto-ecommerce")
indexar_projeto("/caminho/para/outro-projeto")
```

---

### **PASSO 2: Criar Similaridades Automáticas**

```python
def calcular_similaridades():
    """
    Calcula similaridade entre projetos usando embeddings das descrições
    """
    print("🔗 Calculando similaridades entre projetos...")
    
    # Primeiro, criar embedding de descrição para cada projeto
    # (agregando conteúdo de seus arquivos)
    projetos = graph.query("""
    MATCH (p:Projeto)-[:CONTEM]->(a:Arquivo)
    WITH p, collect(a.conteudo)[0..3] as conteudos
    RETURN p.nome as nome, 
           reduce(s = '', c IN conteudos | s + ' ' + c) as descricao_agregada
    """)
    
    for projeto in projetos:
        if projeto['descricao_agregada']:
            emb = embedding_model.embed_query(projeto['descricao_agregada'])
            graph.query("""
            MATCH (p:Projeto {nome: $nome})
            SET p.embedding_descricao = $embedding
            """, {"nome": projeto['nome'], "embedding": emb})
    
    # Criar índice vetorial para projetos
    graph.query("""
    CREATE VECTOR INDEX projetos_similares IF NOT EXISTS
    FOR (p:Projeto)
    ON p.embedding_descricao
    OPTIONS {indexConfig: {
      `vector.dimensions`: 1536,
      `vector.similarity_function`: 'cosine'
    }}
    """)
    
    print("✅ Similaridades calculadas!")

def conectar_projetos_similares(threshold=0.7):
    """
    Cria relacionamentos SIMILAR_A entre projetos com score > threshold
    """
    projetos = graph.query("MATCH (p:Projeto) RETURN p.nome as nome")
    
    from langchain_neo4j import Neo4jVector
    
    vector_store = Neo4jVector.from_existing_index(
        embedding=embedding_model,
        index_name="projetos_similares",
        node_label="Projeto",
        embedding_node_property="embedding_descricao",
        text_node_property="nome",
        graph=graph
    )
    
    for projeto in projetos:
        # Buscar top 5 similares
        similares = vector_store.similarity_search_with_score(
            projeto['nome'], 
            k=6  # 6 porque ele mesmo será retornado
        )
        
        for doc, score in similares:
            if score > threshold and doc.metadata.get('nome') != projeto['nome']:
                graph.query("""
                MATCH (p1:Projeto {nome: $projeto1})
                MATCH (p2:Projeto {nome: $projeto2})
                MERGE (p1)-[r:SIMILAR_A]-(p2)
                SET r.score = $score
                """, {
                    "projeto1": projeto['nome'],
                    "projeto2": doc.metadata['nome'],
                    "score": score
                })
                print(f"  🔗 {projeto['nome']} ↔ {doc.metadata['nome']} (score: {score:.2f})")

# EXECUTAR
calcular_similaridades()
conectar_projetos_similares(threshold=0.7)
```

---

### **PASSO 3: Rastrear Versões e Mudanças**

```python
def detectar_mudancas_documentacao():
    """
    Detecta quando arquivos mudaram comparando hash do conteúdo
    """
    print("🔍 Detectando mudanças na documentação...")
    
    arquivos = graph.query("""
    MATCH (a:Arquivo)
    RETURN a.path as path, a.hash_conteudo as hash_antigo
    """)
    
    for arq in arquivos:
        arquivo = Path(arq['path'])
        if not arquivo.exists():
            print(f"  ⚠️ Arquivo removido: {arquivo}")
            continue
        
        # Recalcular hash
        conteudo_atual = arquivo.read_text(encoding='utf-8')
        hash_atual = hashlib.sha256(conteudo_atual.encode()).hexdigest()
        
        if hash_atual != arq['hash_antigo']:
            print(f"  🔄 MUDANÇA DETECTADA: {arquivo.name}")
            
            # Criar nova versão
            timestamp = datetime.now().isoformat()
            graph.query("""
            MATCH (a_antigo:Arquivo {path: $path})
            
            // Criar nova versão do arquivo
            CREATE (a_novo:Arquivo {
                path: $path,
                nome: $nome,
                conteudo: $conteudo,
                hash_conteudo: $hash_novo,
                versao: $timestamp,
                status: 'atual'
            })
            
            // Marcar antiga como obsoleta
            SET a_antigo.status = 'obsoleta',
                a_antigo.versao = $timestamp_old
            
            // Criar relacionamento de versionamento
            CREATE (a_novo)-[:VERSAO_ANTERIOR]->(a_antigo)
            
            // Copiar relacionamentos do projeto
            WITH a_antigo, a_novo
            MATCH (p:Projeto)-[r:CONTEM]->(a_antigo)
            CREATE (p)-[:CONTEM]->(a_novo)
            """, {
                "path": str(arquivo),
                "nome": arquivo.name,
                "conteudo": conteudo_atual[:10000],
                "hash_novo": hash_atual,
                "timestamp": timestamp,
                "timestamp_old": arq.get('versao', 'unknown')
            })

# EXECUTAR PERIODICAMENTE (ex: via cron job)
detectar_mudancas_documentacao()
```

---

## **🔍 QUERIES PARA SEUS PROBLEMAS ESPECÍFICOS**

### **1. Agrupar Projetos por Tema**

```cypher
// Todos projetos odontológicos
MATCH (p:Projeto)-[:TEM_TEMA]->(t:Tema {nome: "Odontológico"})
RETURN p.nome, p.path
```

### **2. Agrupar por Stack**

```cypher
// Todos projetos Django
MATCH (p:Projeto)-[:USA_STACK]->(s:Stack {nome: "Django"})
RETURN p.nome, 
       [(p)-[:TEM_TEMA]->(t) | t.nome][0] as tema
ORDER BY tema
```

### **3. Projetos Similares**

```cypher
// Projetos similares ao "sistema-odontologico"
MATCH (p1:Projeto {nome: "sistema-odontologico"})-[r:SIMILAR_A]-(p2:Projeto)
RETURN p2.nome as projeto_similar, 
       r.score as similaridade,
       [(p2)-[:USA_STACK]->(s) | s.nome] as stacks
ORDER BY r.score DESC
```

### **4. Documentação Desatualizada**

```cypher
// Arquivos com versões mais novas disponíveis
MATCH (a_atual:Arquivo {status: 'atual'})-[:VERSAO_ANTERIOR]->(a_antiga:Arquivo)
RETURN a_atual.nome,
       a_atual.versao as versao_atual,
       a_antiga.versao as versao_antiga,
       a_atual.path
ORDER BY a_atual.versao DESC
```

### **5. Projetos com Documentação Conflitante**

```cypher
// Projetos que têm múltiplas versões de docs sem uma marcada como atual
MATCH (p:Projeto)-[:CONTEM]->(a:Arquivo)
WHERE a.nome CONTAINS 'README'
WITH p, collect(a) as arquivos
WHERE size(arquivos) > 1
  AND none(a IN arquivos WHERE a.status = 'atual')
RETURN p.nome as projeto,
       [arq IN arquivos | arq.nome + ' (' + arq.ultima_modificacao + ')'] as arquivos_conflitantes
```

### **6. Ordem de Execução (Cronológica)**

```cypher
// Linha do tempo de desenvolvimento do projeto
MATCH (p:Projeto {nome: "meu-projeto"})-[:TEM_VERSAO]->(v:Versao)
RETURN v.numero as versao, 
       v.data as data,
       v.changelog as mudancas
ORDER BY v.data ASC
```

### **7. Dashboard Completo**

```cypher
// Visão geral de todos os projetos
MATCH (p:Projeto)
OPTIONAL MATCH (p)-[:USA_STACK]->(s:Stack)
OPTIONAL MATCH (p)-[:TEM_TEMA]->(t:Tema)
OPTIONAL MATCH (p)-[:SIMILAR_A]-(similar:Projeto)
RETURN p.nome as projeto,
       collect(DISTINCT s.nome) as stacks,
       collect(DISTINCT t.nome) as temas,
       count(DISTINCT similar) as projetos_similares,
       p.data_criacao as criado_em
ORDER BY p.data_criacao DESC
```

---

## **💬 INTERFACE CONVERSACIONAL**

```python
from langchain_neo4j import GraphCypherQAChain

chain = GraphCypherQAChain.from_llm(
    llm=ChatOpenAI(model="gpt-4"),
    graph=graph,
    allow_dangerous_requests=True,
    return_intermediate_steps=True,
    verbose=True
)

# Agora você pode perguntar:
perguntas = [
    "Quais projetos usam Django?",
    "Mostre projetos similares ao sistema odontológico",
    "Qual a documentação mais recente do projeto X?",
    "Liste todos os projetos de e-commerce",
    "Quais arquivos do projeto Y mudaram recentemente?",
    "Mostre stacks usadas em projetos odontológicos",
    "Quais projetos não têm documentação atualizada?"
]

for pergunta in perguntas:
    print(f"\n❓ {pergunta}")
    resultado = chain.invoke({"query": pergunta})
    print(f"💬 {resultado['result']}\n")
```

---

## **🎯 FLUXO DE TRABALHO DIÁRIO**

### **Cenário Real**: Você quer trabalhar no projeto odontológico

**1. Pergunta conversacional**:
```python
chain.invoke({"query": "Mostre a documentação atual do sistema odontológico e projetos similares"})
```

**Resposta**:
```
📋 Sistema Odontológico (Django + PostgreSQL)
   - README.md (v2.3 - 2024-12-20) ✅ ATUAL
   - API_DOCS.md (v2.3 - 2024-12-20) ✅ ATUAL
   
🔗 Projetos Similares:
   - sistema-clinica-medica (similaridade: 0.87)
   - gestao-consultorio (similaridade: 0.82)
   
⚠️ ATENÇÃO: Existe docs/OLD_README.md (v1.5) que pode estar obsoleta
```

**2. Verificar mudanças recentes**:
```python
chain.invoke({"query": "O que mudou no sistema odontológico nos últimos 7 dias?"})
```

**3. Ver stack completa**:
```python
chain.invoke({"query": "Quais tecnologias o sistema odontológico usa?"})
```

---

## **📊 RELATÓRIOS AUTOMÁTICOS**

```python
def gerar_relatorio_governanca():
    """
    Relatório executivo de saúde da documentação
    """
    print("=" * 60)
    print("📊 RELATÓRIO DE GOVERNANÇA DE DOCUMENTAÇÃO")
    print("=" * 60)
    
    # Total de projetos
    total = graph.query("MATCH (p:Projeto) RETURN count(p) as total")[0]['total']
    print(f"\n📁 Total de Projetos: {total}")
    
    # Projetos por stack
    print("\n🛠️ DISTRIBUIÇÃO POR STACK:")
    stacks = graph.query("""
    MATCH (p:Projeto)-[:USA_STACK]->(s:Stack)
    RETURN s.nome as stack, count(p) as qtd
    ORDER BY qtd DESC
    """)
    for s in stacks:
        print(f"   - {s['stack']}: {s['qtd']} projetos")
    
    # Projetos por tema
    print("\n🏷️ DISTRIBUIÇÃO POR TEMA:")
    temas = graph.query("""
    MATCH (p:Projeto)-[:TEM_TEMA]->(t:Tema)
    RETURN t.nome as tema, count(p) as qtd
    ORDER BY qtd DESC
    """)
    for t in temas:
        print(f"   - {t['tema']}: {t['qtd']} projetos")
    
    # Documentação desatualizada
    print("\n⚠️ ALERTAS:")
    desatualizados = graph.query("""
    MATCH (p:Projeto)-[:CONTEM]->(a:Arquivo)
    WHERE a.status = 'obsoleta'
    RETURN p.nome, count(a) as docs_antigas
    """)
    for d in desatualizados:
        print(f"   ⚠️ {d['p.nome']}: {d['docs_antigas']} documentos desatualizados")
    
    # Clusters de similaridade
    print("\n🔗 CLUSTERS DE PROJETOS SIMILARES:")
    clusters = graph.query("""
    MATCH (p1:Projeto)-[r:SIMILAR_A]-(p2:Projeto)
    WHERE r.score > 0.8
    RETURN p1.nome as projeto1, p2.nome as projeto2, r.score as score
    ORDER BY score DESC
    LIMIT 10
    """)
    for c in clusters:
        print(f"   🔗 {c['projeto1']} ↔ {c['projeto2']} ({c['score']:.2f})")
    
    print("\n" + "=" * 60)

# EXECUTAR
gerar_relatorio_governanca()
```

---

## **✅ CHECKLIST DE IMPLEMENTAÇÃO**

### **Semana 1: Setup**
- [ ] Neo4j rodando
- [ ] Script de indexação funcionando
- [ ] Primeiro projeto indexado com sucesso
- [ ] Metadados extraídos corretamente (tema, stack, versão)

### **Semana 2: Enriquecimento**
- [ ] Similaridades calculadas
- [ ] Relacionamentos SIMILAR_A criados
- [ ] Detecção de mudanças implementada
- [ ] Versionamento de arquivos funcionando

### **Semana 3: Queries**
- [ ] Todas as 7 queries principais testadas
- [ ] Interface conversacional respondendo corretamente
- [ ] Dashboard visual no Neo4j Browser

### **Semana 4: Automação**
- [ ] Cron job para reindexação diária
- [ ] Alertas automáticos de documentação desatualizada
- [ ] Relatório de governança semanal

---

## **🚀 COMECE AGORA (30 minutos)**

**Script completo de início rápido**:

```bash
# 1. Subir Neo4j
docker-compose up -d

# 2. Instalar dependências
pip install langchain-neo4j langchain-openai

# 3. Criar arquivo indexador.py (código acima)
# 4. Executar primeira indexação
python indexador.py --projeto /caminho/do/seu/projeto

# 5. Abrir Neo4j Browser
# http://localhost:7474

# 6. Executar query de teste
# MATCH (p:Projeto)-[:USA_STACK]->(s) RETURN p, s
```

---

## **💡 RESULTADO FINAL**

Você terá:

✅ **Visibilidade total** de todos os projetos  
✅ **Organização automática** por tema e stack  
✅ **Rastreamento de versões** com linha do tempo  
✅ **Detecção de similaridades** para reutilização de código  
✅ **Alertas de desatualização** automáticos  
✅ **Interface conversacional** para qualquer pergunta  

**Tempo de setup**: 4-6 horas  
**Benefício imediato**: Você nunca mais vai se confundir com documentação antiga

---

