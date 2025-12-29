/# 🧠 SISTEMA UNIVERSAL DE ORGANIZAÇÃO DE CONHECIMENTO

---

## **O QUE VOCÊ REALMENTE PRECISA**

**É um CÉREBRO DIGITAL que auto-organiza TODO seu conhecimento.**

Um sistema que:
- ✅ Ingere QUALQUER COISA (notas, projetos, prompts, insights, anotações, PDFs, tweets salvos)
- ✅ Descobre automaticamente O QUE É cada coisa
- ✅ Encontra relações que você nem sabia que existiam
- ✅ Evolui com você (quanto mais você adiciona, mais inteligente fica)
- ✅ Responde "mostre tudo relacionado a X" independente de onde estava

---

## **📋 OBJETIVO REFORMULADO**

### **Copie Este Objetivo Genérico**:

```
OBJETIVO: Sistema de Gestão de Conhecimento Pessoal com Auto-Organização

PROBLEMA:
Conhecimento pessoal está fragmentado em centenas de arquivos sem estrutura:
- Notas soltas sobre assuntos diversos
- Projetos de software em diferentes estágios
- Prompts de IA que funcionaram
- Insights esparsos em arquivos de texto
- Anotações de reuniões, cursos, leituras
- Ideias não desenvolvidas
- Documentação técnica desatualizada

Não há como encontrar, correlacionar ou evoluir este conhecimento.

SOLUÇÃO:
Grafo de conhecimento universal que:
1. Ingere qualquer arquivo/pasta sem assumir estrutura prévia
2. Classifica automaticamente O QUE É cada item (projeto, nota, prompt, etc)
3. Extrai TÓPICOS, CONCEITOS, TECNOLOGIAS mencionadas
4. Cria relacionamentos semânticos automáticos
5. Detecta clusters emergentes de conhecimento relacionado
6. Rastreia evolução temporal (versões, ideias que viraram projetos)
7. Permite navegação conversacional total

ENTREGAS:
- Interface única: "mostre tudo sobre Machine Learning"
  → Retorna: projetos ML, notas de estudo, prompts úteis, insights
- Detecção de padrões: "você tem 5 notas sobre Django que podem virar projeto"
- Alertas: "há 3 versões conflitantes desta ideia"
- Sugestões: "este prompt é similar ao que você usou no projeto X"

SUCESSO:
- Zero esforço manual de organização
- Conhecimento sempre acessível em segundos
- Insights emergentes sobre padrões do seu próprio pensamento
- Decisões informadas sobre o que desenvolver/estudar
```

---

## **🏗️ ARQUITETURA UNIVERSAL**

### **Modelo de Grafo Genérico (Ontologia Emergente)**

```
(Item)  ← nó universal, tudo começa aqui
  ├─ tipo: descoberto automaticamente
  ├─ embedding: similaridade semântica
  ├─ conteudo: texto original
  └─ metadata: extraída automaticamente

(Item)-[:SOBRE]->(Topico)
(Item)-[:MENCIONA]->(Conceito)
(Item)-[:USA_TECNOLOGIA]->(Tecnologia)
(Item)-[:RELACIONADO_A {score, razao}]->(Item)
(Item)-[:EVOLUIU_PARA]->(Item)
(Item)-[:PARTE_DE]->(Colecao)
(Item)-[:CRIADO_EM]->(Data)
(Item)-[:TAG]->(Tag)
```

**NÃO há hierarquia fixa. Tudo é descoberto.**

---

## **⚙️ IMPLEMENTAÇÃO UNIVERSAL**

### **PASSO 1: Ingestão Agnóstica**

```python
from pathlib import Path
from langchain_neo4j import Neo4jGraph
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
import hashlib
from datetime import datetime
import mimetypes

graph = Neo4jGraph(
    url="bolt://localhost:7687",
    username="neo4j",
    password="password"
)

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
embedding_model = OpenAIEmbeddings(model="text-embedding-ada-002")

# Prompt de classificação UNIVERSAL
prompt_classificacao = ChatPromptTemplate.from_messages([
    ("system", """Você é um classificador de conhecimento pessoal.
    
    Analise o conteúdo e retorne JSON:
    {{
      "tipo_primario": "projeto | nota | prompt | insight | anotacao | documentacao | ideia | tutorial | codigo | artigo | receita | outro",
      "subtipo": "descrição mais específica se aplicável",
      "topicos": ["Machine Learning", "Django", "Receitas", etc],
      "conceitos": ["conceitos técnicos ou abstratos mencionados"],
      "tecnologias": ["Python", "Docker", "PostgreSQL", etc se relevante],
      "tags": ["tags/palavras-chave úteis"],
      "status": "rascunho | em_andamento | completo | arquivado | abandonado",
      "maturidade": "ideia_inicial | exploracao | desenvolvimento | producao",
      "data_estimada": "tente inferir quando foi criado pelo conteúdo",
      "contexto": "breve descrição do que é e por que existe"
    }}
    
    Seja preciso. Use null se incerto.
    """),
    ("user", """Arquivo: {nome}
Caminho: {path}
Tamanho: {tamanho} bytes
Modificado: {modificado}

Conteúdo:
{conteudo}
""")
])

chain_classificacao = prompt_classificacao | llm

def ingerir_tudo(raiz: str):
    """
    Ingere TUDO de um diretório, sem assumir estrutura
    """
    raiz_path = Path(raiz)
    
    # Extensões de texto suportadas
    extensoes_texto = {
        '.md', '.txt', '.rst', '.py', '.js', '.json', '.yaml', '.yml',
        '.html', '.css', '.sql', '.sh', '.bash', '.env', '.conf',
        '.log', '.csv', '.xml', '.toml', '.ini'
    }
    
    print(f"🧠 Ingerindo conhecimento de: {raiz}")
    print("=" * 60)
    
    # Recursivo: encontrar TODOS os arquivos
    todos_arquivos = []
    for arquivo in raiz_path.rglob("*"):
        if arquivo.is_file() and arquivo.suffix.lower() in extensoes_texto:
            todos_arquivos.append(arquivo)
    
    print(f"📁 Encontrados {len(todos_arquivos)} arquivos para processar\n")
    
    for idx, arquivo in enumerate(todos_arquivos, 1):
        print(f"[{idx}/{len(todos_arquivos)}] Processando: {arquivo.name}")
        processar_item(arquivo)
    
    print(f"\n✅ {len(todos_arquivos)} itens ingeridos no grafo!")

def processar_item(arquivo: Path):
    """
    Processa um item individual (totalmente agnóstico)
    """
    try:
        conteudo = arquivo.read_text(encoding='utf-8', errors='ignore')
    except Exception as e:
        print(f"  ⚠️ Erro ao ler: {e}")
        return
    
    # Metadados do arquivo
    stat = arquivo.stat()
    hash_conteudo = hashlib.sha256(conteudo.encode()).hexdigest()
    modificado = datetime.fromtimestamp(stat.st_mtime)
    
    # Gerar embedding
    embedding = embedding_model.embed_query(conteudo[:8000])
    
    # Classificar com LLM
    print(f"  🔍 Classificando...")
    resultado = chain_classificacao.invoke({
        "nome": arquivo.name,
        "path": str(arquivo.relative_to(Path.cwd())),
        "tamanho": stat.st_size,
        "modificado": modificado.strftime("%Y-%m-%d"),
        "conteudo": conteudo[:6000]  # Primeiros 6k caracteres
    })
    
    # Parse do resultado
    import json
    try:
        classificacao = json.loads(resultado.content)
    except:
        print(f"  ⚠️ Erro ao parsear classificação, usando padrão")
        classificacao = {
            "tipo_primario": "outro",
            "topicos": [],
            "tags": []
        }
    
    print(f"  📌 Tipo: {classificacao.get('tipo_primario')} | Tópicos: {classificacao.get('topicos', [])[:3]}")
    
    # Criar nó universal (Item)
    graph.query("""
    MERGE (i:Item {id: $id})
    SET i.nome = $nome,
        i.path = $path,
        i.tipo = $tipo,
        i.subtipo = $subtipo,
        i.status = $status,
        i.maturidade = $maturidade,
        i.contexto = $contexto,
        i.conteudo = $conteudo,
        i.embedding = $embedding,
        i.hash = $hash,
        i.tamanho = $tamanho,
        i.modificado = $modificado,
        i.processado_em = datetime()
    """, {
        "id": hash_conteudo[:16],  # ID único baseado em conteúdo
        "nome": arquivo.name,
        "path": str(arquivo),
        "tipo": classificacao.get('tipo_primario', 'outro'),
        "subtipo": classificacao.get('subtipo'),
        "status": classificacao.get('status'),
        "maturidade": classificacao.get('maturidade'),
        "contexto": classificacao.get('contexto'),
        "conteudo": conteudo[:15000],
        "embedding": embedding,
        "hash": hash_conteudo,
        "tamanho": stat.st_size,
        "modificado": modificado.isoformat()
    })
    
    # Criar relacionamentos com Tópicos
    for topico in classificacao.get('topicos', []):
        if topico:
            graph.query("""
            MATCH (i:Item {id: $item_id})
            MERGE (t:Topico {nome: $topico})
            MERGE (i)-[:SOBRE]->(t)
            """, {"item_id": hash_conteudo[:16], "topico": topico})
    
    # Criar relacionamentos com Conceitos
    for conceito in classificacao.get('conceitos', []):
        if conceito:
            graph.query("""
            MATCH (i:Item {id: $item_id})
            MERGE (c:Conceito {nome: $conceito})
            MERGE (i)-[:MENCIONA]->(c)
            """, {"item_id": hash_conteudo[:16], "conceito": conceito})
    
    # Criar relacionamentos com Tecnologias
    for tech in classificacao.get('tecnologias', []):
        if tech:
            graph.query("""
            MATCH (i:Item {id: $item_id})
            MERGE (t:Tecnologia {nome: $tech})
            MERGE (i)-[:USA_TECNOLOGIA]->(t)
            """, {"item_id": hash_conteudo[:16], "tech": tech})
    
    # Criar Tags
    for tag in classificacao.get('tags', []):
        if tag:
            graph.query("""
            MATCH (i:Item {id: $item_id})
            MERGE (tg:Tag {nome: $tag})
            MERGE (i)-[:TAG]->(tg)
            """, {"item_id": hash_conteudo[:16], "tag": tag})
    
    print(f"  ✅ Item catalogado no grafo\n")

# EXECUTAR
ingerir_tudo("/caminho/para/seu/conhecimento")
# Pode executar múltiplas vezes em diretórios diferentes:
# ingerir_tudo("/notas")
# ingerir_tudo("/projetos")
# ingerir_tudo("/prompts")
```

---

### **PASSO 2: Criar Relacionamentos Semânticos Automáticos**

```python
def criar_relacionamentos_semanticos(threshold=0.75):
    """
    Descobre relacionamentos entre itens por similaridade semântica
    """
    print("🔗 Descobrindo relacionamentos semânticos...")
    
    # Criar índice vetorial universal
    graph.query("""
    CREATE VECTOR INDEX itens_similares IF NOT EXISTS
    FOR (i:Item)
    ON i.embedding
    OPTIONS {indexConfig: {
      `vector.dimensions`: 1536,
      `vector.similarity_function`: 'cosine'
    }}
    """)
    
    from langchain_neo4j import Neo4jVector
    
    vector_store = Neo4jVector.from_existing_index(
        embedding=embedding_model,
        index_name="itens_similares",
        node_label="Item",
        embedding_node_property="embedding",
        text_node_property="contexto",
        graph=graph
    )
    
    # Para cada item, encontrar similares
    items = graph.query("MATCH (i:Item) RETURN i.id as id, i.nome as nome, i.tipo as tipo")
    
    for item in items:
        # Buscar top 10 similares
        similares = vector_store.similarity_search_with_score(
            item['nome'] + " " + str(item.get('tipo', '')),
            k=11  # 11 porque o próprio item será retornado
        )
        
        for doc, score in similares:
            if score > threshold and doc.metadata.get('id') != item['id']:
                # Criar relacionamento com score
                graph.query("""
                MATCH (i1:Item {id: $id1})
                MATCH (i2:Item {id: $id2})
                MERGE (i1)-[r:RELACIONADO_A]-(i2)
                SET r.score = $score,
                    r.descoberto_em = datetime()
                """, {
                    "id1": item['id'],
                    "id2": doc.metadata['id'],
                    "score": score
                })
                
                print(f"  🔗 {item['nome']} ↔ {doc.metadata.get('nome')} ({score:.3f})")
    
    print("✅ Relacionamentos semânticos criados!")

# EXECUTAR
criar_relacionamentos_semanticos(threshold=0.75)
```

---

### **PASSO 3: Detectar Padrões Emergentes**

```python
def detectar_clusters():
    """
    Identifica clusters/grupos de conhecimento relacionado
    """
    print("🧩 Detectando clusters de conhecimento...\n")
    
    # Prompt para análise de clusters
    prompt_cluster = ChatPromptTemplate.from_messages([
        ("system", """Analise este grupo de itens relacionados e:
        1. Identifique o TEMA COMUM que os une
        2. Sugira um NOME para este cluster
        3. Identifique se há OPORTUNIDADE (ex: "várias notas sobre X podem virar projeto")
        
        Retorne JSON:
        {{
          "tema_comum": "descrição do que une estes itens",
          "nome_cluster": "nome sugestivo",
          "oportunidade": "sugestão acionável ou null"
        }}
        """),
        ("user", "Itens:\n{itens_desc}")
    ])
    
    chain_cluster = prompt_cluster | llm
    
    # Encontrar grupos fortemente conectados
    clusters_raw = graph.query("""
    MATCH (i1:Item)-[r:RELACIONADO_A]-(i2:Item)
    WHERE r.score > 0.8
    WITH i1, collect(DISTINCT i2) as relacionados
    WHERE size(relacionados) >= 2
    RETURN i1.nome as item_central,
           i1.tipo as tipo,
           i1.contexto as contexto,
           [r IN relacionados | r.nome + ' (' + r.tipo + ')'] as itens_relacionados
    LIMIT 20
    """)
    
    for cluster in clusters_raw:
        # Analisar com LLM
        itens_desc = f"Central: {cluster['item_central']} ({cluster['tipo']})\n"
        itens_desc += f"Contexto: {cluster['contexto']}\n\n"
        itens_desc += "Relacionados:\n" + "\n".join([f"- {i}" for i in cluster['itens_relacionados']])
        
        analise = chain_cluster.invoke({"itens_desc": itens_desc})
        
        try:
            import json
            resultado = json.loads(analise.content)
            
            print(f"📦 CLUSTER DETECTADO:")
            print(f"   Nome: {resultado['nome_cluster']}")
            print(f"   Tema: {resultado['tema_comum']}")
            if resultado.get('oportunidade'):
                print(f"   💡 OPORTUNIDADE: {resultado['oportunidade']}")
            print()
            
            # Criar nó de Cluster no grafo
            graph.query("""
            MERGE (c:Cluster {nome: $nome})
            SET c.tema = $tema,
                c.oportunidade = $oportunidade,
                c.detectado_em = datetime()
            WITH c
            MATCH (i:Item {nome: $item_central})
            MERGE (i)-[:PARTE_DE]->(c)
            """, {
                "nome": resultado['nome_cluster'],
                "tema": resultado['tema_comum'],
                "oportunidade": resultado.get('oportunidade'),
                "item_central": cluster['item_central']
            })
            
        except:
            continue

# EXECUTAR
detectar_clusters()
```

---

### **PASSO 4: Rastrear Evolução (Ideias → Projetos)**

```python
def detectar_evolucoes():
    """
    Identifica quando ideias/notas evoluíram para projetos
    """
    print("⏳ Rastreando evolução de conhecimento...\n")
    
    # Encontrar itens similares mas de tipos diferentes
    evolucoes = graph.query("""
    MATCH (i1:Item)-[r:RELACIONADO_A]-(i2:Item)
    WHERE r.score > 0.85
      AND i1.tipo <> i2.tipo
      AND (
        (i1.tipo IN ['ideia', 'nota'] AND i2.tipo IN ['projeto', 'codigo'])
        OR
        (i1.tipo IN ['prompt'] AND i2.tipo IN ['projeto', 'codigo'])
      )
      AND i1.modificado < i2.modificado
    RETURN i1.nome as origem,
           i1.tipo as tipo_origem,
           i1.modificado as data_origem,
           i2.nome as destino,
           i2.tipo as tipo_destino,
           i2.modificado as data_destino,
           r.score as similaridade
    ORDER BY data_destino DESC
    """)
    
    for evo in evolucoes:
        print(f"🌱 EVOLUÇÃO DETECTADA:")
        print(f"   {evo['origem']} ({evo['tipo_origem']}) [{evo['data_origem'][:10]}]")
        print(f"   ↓")
        print(f"   {evo['destino']} ({evo['tipo_destino']}) [{evo['data_destino'][:10]}]")
        print(f"   Similaridade: {evo['similaridade']:.2f}\n")
        
        # Criar relacionamento de evolução
        graph.query("""
        MATCH (i1:Item {nome: $origem})
        MATCH (i2:Item {nome: $destino})
        MERGE (i1)-[e:EVOLUIU_PARA]->(i2)
        SET e.score = $score,
            e.detectado_em = datetime()
        """, {
            "origem": evo['origem'],
            "destino": evo['destino'],
            "score": evo['similaridade']
        })

# EXECUTAR
detectar_evolucoes()
```

---

## **🔍 QUERIES UNIVERSAIS**

### **1. "Mostre tudo sobre Machine Learning"**

```cypher
MATCH (i:Item)-[:SOBRE|MENCIONA|TAG]-(n)
WHERE n.nome CONTAINS 'Machine Learning' 
   OR n.nome CONTAINS 'ML'
RETURN i.nome as item,
       i.tipo as tipo,
       i.contexto as descricao,
       labels(n)[0] as encontrado_via
ORDER BY i.modificado DESC
```

### **2. "Quais notas podem virar projetos?"**

```cypher
// Notas com múltiplos relacionamentos (indica profundidade)
MATCH (n:Item {tipo: 'nota'})-[r:RELACIONADO_A]-(outros)
WITH n, count(r) as conexoes
WHERE conexoes >= 3
RETURN n.nome as nota,
       n.contexto as sobre,
       conexoes as items_relacionados
ORDER BY conexoes DESC
```

### **3. "Há versões conflitantes sobre o mesmo assunto?"**

```cypher
// Items muito similares mas modificados em datas diferentes
MATCH (i1:Item)-[r:RELACIONADO_A]-(i2:Item)
WHERE r.score > 0.9
  AND i1.id <> i2.id
  AND abs(duration.between(
        datetime(i1.modificado), 
        datetime(i2.modificado)
      ).days) > 30
RETURN i1.nome as versao_antiga,
       i1.modificado as data_antiga,
       i2.nome as versao_nova,
       i2.modificado as data_nova,
       r.score as similaridade
ORDER BY data_nova DESC
```

### **4. "Prompts que usei em projetos"**

```cypher
MATCH (p:Item {tipo: 'prompt'})-[r:RELACIONADO_A]-(proj:Item {tipo: 'projeto'})
RETURN p.nome as prompt,
       proj.nome as projeto,
       r.score as relevancia
ORDER BY relevancia DESC
```

### **5. "Mapa completo de um tópico"**

```cypher
// Exemplo: tudo sobre Django
MATCH caminho = (i:Item)-[:SOBRE|MENCIONA*1..2]-(t:Topico {nome: 'Django'})
RETURN caminho
LIMIT 50
```

### **6. "Clusters de oportunidade"**

```cypher
MATCH (c:Cluster)
WHERE c.oportunidade IS NOT NULL
RETURN c.nome as cluster,
       c.tema as sobre,
       c.oportunidade as acao_sugerida,
       c.detectado_em as quando
ORDER BY c.detectado_em DESC
```

### **7. "Linha do tempo do meu conhecimento"**

```cypher
MATCH (i:Item)
RETURN i.tipo as tipo,
       count(i) as quantidade,
       min(datetime(i.modificado)) as primeiro,
       max(datetime(i.modificado)) as ultimo
ORDER BY quantidade DESC
```

---

## **💬 INTERFACE CONVERSACIONAL UNIVERSAL**

```python
from langchain_neo4j import GraphCypherQAChain
from langchain_openai import ChatOpenAI

# Criar chain com contexto enriquecido
chain = GraphCypherQAChain.from_llm(
    llm=ChatOpenAI(model="gpt-4", temperature=0),
    graph=graph,
    allow_dangerous_requests=True,
    return_intermediate_steps=True,
    verbose=True
)

# Agora você pode fazer QUALQUER pergunta
perguntas = [
    "Mostre tudo que tenho sobre Machine Learning",
    "Quais prompts de IA funcionaram bem?",
    "Tenho alguma nota sobre Django que pode virar projeto?",
    "Liste projetos relacionados a e-commerce",
    "Mostre insights sobre produtividade",
    "Qual a última vez que escrevi sobre Python?",
    "Há documentação desatualizada sobre autenticação?",
    "Quais tecnologias eu mais uso?",
    "Mostre clusters de conhecimento sobre saúde",
    "Qual nota evoluiu para o projeto X?"
]

def perguntar(query: str):
    """Interface única para todo conhecimento"""
    print(f"\n❓ {query}")
    print("=" * 60)
    
    resultado = chain.invoke({"query": query})
    
    print(f"\n💬 {resultado['result']}")
    
    if resultado.get('intermediate_steps'):
        print(f"\n🔍 Cypher gerado:")
        print(resultado['intermediate_steps'][0]['query'])
    
    print("\n" + "=" * 60)
    
    return resultado

# Uso
for pergunta in perguntas:
    perguntar(pergunta)
```

---

## **📊 DASHBOARD UNIVERSAL**

```python
def dashboard_conhecimento():
    """
    Visão geral completa do seu conhecimento
    """
    print("\n" + "=" * 70)
    print("🧠 DASHBOARD DO SEU CONHECIMENTO")
    print("=" * 70)
    
    # Estatísticas gerais
    stats = graph.query("""
    MATCH (i:Item)
    RETURN count(i) as total_items,
           count(DISTINCT i.tipo) as tipos_diferentes,
           sum(i.tamanho) as bytes_totais
    """)[0]
    
    print(f"\n📊 ESTATÍSTICAS GERAIS:")
    print(f"   Total de itens: {stats['total_items']}")
    print(f"   Tipos diferentes: {stats['tipos_diferentes']}")
    print(f"   Volume: {stats['bytes_totais'] / 1024 / 1024:.2f} MB")
    
    # Distribuição por tipo
    print(f"\n📁 DISTRIBUIÇÃO POR TIPO:")
    tipos = graph.query("""
    MATCH (i:Item)
    RETURN i.tipo as tipo, count(*) as qtd
    ORDER BY qtd DESC
    """)
    for t in tipos:
        print(f"   {t['tipo']:20s}: {t['qtd']:4d} itens")
    
    # Tópicos mais recorrentes
    print(f"\n🏷️ TÓPICOS MAIS FREQUENTES:")
    topicos = graph.query("""
    MATCH (t:Topico)<-[:SOBRE]-(i:Item)
    RETURN t.nome as topico, count(i) as itens
    ORDER BY itens DESC
    LIMIT 10
    """)
    for t in topicos:
        print(f"   {t['topico']:30s}: {t['itens']:3d} itens")
    
    # Tecnologias utilizadas
    print(f"\n🛠️ TECNOLOGIAS:")
    techs = graph.query("""
    MATCH (t:Tecnologia)<-[:USA_TECNOLOGIA]-(i:Item)
    RETURN t.nome as tech, count(i) as itens
    ORDER BY itens DESC
    LIMIT 10
    """)
    for t in techs:
        print(f"   {t['tech']:30s}: {t['itens']:3d} itens")
    
    # Clusters detectados
    print(f"\n📦 CLUSTERS DETECTADOS:")
    clusters = graph.query("""
    MATCH (c:Cluster)
    RETURN c.nome as nome, c.tema as tema, c.oportunidade as oportunidade
    ORDER BY c.detectado_em DESC
    LIMIT 5
    """)
    for c in clusters:
        print(f"   • {c['nome']}")
        print(f"     Tema: {c['tema']}")
        if c['oportunidade']:
            print(f"     💡 {c['oportunidade']}")
    
    # Evoluções detectadas
    print(f"\n🌱 EVOLUÇÕES RECENTES:")
    evolucoes = graph.query("""
    MATCH (i1:Item)-[e:EVOLUIU_PARA]->(i2:Item)
    RETURN i1.nome as de, i2.nome as para
    ORDER BY e.detectado_em DESC
    LIMIT 5
    """)
    for e in evolucoes:
        print(f"   {e['de']} → {e['para']}")
    
    # Itens órfãos (sem relacionamentos)
    print(f"\n⚠️ ITENS DESCONECTADOS:")
    orfaos = graph.query("""
    MATCH (i:Item)
    WHERE NOT (i)-[:RELACIONADO_A]-()
      AND NOT (i)-[:SOBRE]-()
      AND NOT (i)-[:MENCIONA]-()
    RETURN i.nome as nome, i.tipo as tipo
    LIMIT 10
    """)
    for o in orfaos:
        print(f"   • {o['nome']} ({o['tipo']})")
    
    # Atividade recente
    print(f"\n⏰ ATIVIDADE RECENTE (últimos 7 dias):")
    recentes = graph.query("""
    MATCH (i:Item)
    WHERE datetime(i.modificado) > datetime() - duration('P7D')
    RETURN i.nome as nome, i.tipo as tipo, i.modificado as quando
    ORDER BY i.modificado DESC
    LIMIT 10
    """)
    for r in recentes:
        print(f"   • {r['nome']} ({r['tipo']}) - {r['quando'][:10]}")
    
    print("\n" + "=" * 70)

# EXECUTAR
dashboard_conhecimento()
```

---

## **🎯 WORKFLOWS PRÁTICOS**

### **Workflow 1: Manhã de Trabalho**

```python
# "O que devo trabalhar hoje?"
perguntar("Mostre clusters com oportunidades de desenvolvimento")

