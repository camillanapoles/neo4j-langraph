# ESTRATEGIA_EMBEDDINGS.md - Estratégia Híbrida Otimizada

Este documento explica a **estratégia híbrida de embeddings** para máximo desempenho no seu caso de uso.

---

## 🎯 SEU CASO DE USO

```
┌─────────────────────────────────────────────────────────┐
│  CENÁRIO: 20.000 Documentos × 10KB                      │
└─────────────────────────────────────────────────────────┘

✅ Português brasileiro
✅ Engenharia de software, código, tecnologias
✅ Conhecimento geral (tudo tem)
✅ Multilíngua (50+ idiomas)
✅ RTX 4070 8GB VRAM
✅ LLM: Gemini Flash 2.5
```

---

## 🏆 ESTRATÉGIA HÍBRIDA: DOIS MODELOS PARA MÁXIMO DESEMPENHO

### Por que dois modelos?

```
Um modelo só não é perfeito para tudo:
  • Modelo para PT: MELHOR para português, mas não para código
  • Modelo para código: MELHOR para engenharia, mas não tanto para PT
  • Modelo geral: Bom em tudo, mas não excelente em nada

Solução: ESTRATÉGIA HÍBRIDA
  → Usar modelo CERTO para cada tipo de conteúdo!
```

---

## 📊 OS TRÊS MODELOS DA ESTRATÉGIA

### 1. **paraphrase-multilingual-mpnet-base-v2** 🥇 Para PT/Geral

```
╔══════════════════════════════════════════════════════╗
║  🥇 paraphrase-multilingual-mpnet-base-v2               ║
║  Sentence-Transformers (2023)                          ║
╠══════════════════════════════════════════════════════╣
║                                                        ║
║  🇧🇷 Português:        ⭐⭐⭐⭐⭐ MELHOR!            ║
║  📚 Geral:            ⭐⭐⭐⭐ Muito bom            ║
║  🌍 Multilíngua:      50+ idiomas                    ║
║  💻 Engenharia:       ⭐⭐⭐ Bom                    ║
║                                                        ║
║  📊 Tamanho:           1.5GB (Q4)                   ║
║  ⚡ Velocidade:        0.06s/embedding             ║
║  🎯 Dimensões:         768                          ║
║                                                        ║
║  ✅ Fortes:                                          ║
║     • MELHOR para português brasileiro           ║
║     • Excelente para conhecimento geral           ║
║     • Muito rápido (0.06s)                         ║
║     • Pequeno (1.5GB VRAM)                        ║
║     • 50+ idiomas                                 ║
║                                                        ║
║  ⚠️ Fracos:                                          ║
║     • Menos foco em código/engenharia              ║
║     • 50 idiomas (vs 100+)                        ║
║                                                        ║
╚══════════════════════════════════════════════════════╝
```

**Quando usar:**
- ✅ Documentos em português brasileiro
- ✅ Conhecimento pessoal geral
- ✅ Notas, artigos, tutoriais
- ✅ 80-90% dos seus documentos

---

### 2. **intfloat/e5-mistral-7b-instruct** 🥈 Para Engenharia/Código

```
╔══════════════════════════════════════════════════════╗
║  🥈 intfloat/e5-mistral-7b-instruct                   ║
║  Microsoft (2024)                                      ║
╠══════════════════════════════════════════════════════╣
║                                                        ║
║  💻 Engenharia:       ⭐⭐⭐⭐⭐ MELHOR!              ║
║  💻 Código:           ⭐⭐⭐⭐⭐ MELHOR!              ║
║  🔧 Tecnologias:      ⭐⭐⭐⭐⭐ MELHOR!              ║
║  🇧🇷 Português:        ⭐⭐⭐⭐ Muito bom            ║
║  🌍 Multilíngua:      100+ idiomas                   ║
║  📚 Geral:            ⭐⭐⭐⭐ Muito bom            ║
║                                                        ║
║  📊 Tamanho:           4.5GB (Q4)                   ║
║  ⚡ Velocidade:        0.12s/embedding             ║
║  🎯 Dimensões:         4096 (MÁXIMA PRECISÃO!)      ║
║                                                        ║
║  ✅ Fortes:                                          ║
║     • MELHOR para engenharia de software           ║
║     • MELHOR para código e tecnologias               ║
║     • Instrução-tuning (entende melhor contexto)     ║
║     • Dimensões gigantes (4096) = máxima precisão   ║
║     • 100+ idiomas                                 ║
║     • Excelente para português                       ║
║                                                        ║
║  ⚠️ Fracos:                                          ║
║     • VRAM maior (4.5GB vs 1.5GB)                   ║
║     • Um pouco mais lento (0.12s vs 0.06s)         ║
║     • Pode dar OOM na RTX 4070 (8GB)                ║
║                                                        ║
╚══════════════════════════════════════════════════════╝
```

**Quando usar:**
- ✅ Documentos de código
- ✅ Documentação técnica de engenharia
- ✅ Documentos sobre tecnologias específicas
- ✅ READMEs, specs, arquitetura
- ✅ 10-20% dos seus documentos

---

### 3. **BAAI/bge-m3** 🥉 Para Multilíngua

```
╔══════════════════════════════════════════════════════╗
║  🥉 BAAI/bge-m3                                        ║
║  BAAI (2023)                                            ║
╠══════════════════════════════════════════════════════╣
║                                                        ║
║  🌍 Multilíngua:      100+ idiomas                   ║
║  🇧🇷 Português:        ⭐⭐⭐⭐ Muito bom            ║
║  💻 Engenharia:       ⭐⭐⭐⭐ Muito bom            ║
║  📚 Geral:            ⭐⭐⭐⭐ Muito bom            ║
║                                                        ║
║  📊 Tamanho:           2.5GB (Q4)                   ║
║  ⚡ Velocidade:        0.08s/embedding             ║
║  🎯 Dimensões:         1024                         ║
║                                                        ║
║  ✅ Fortes:                                          ║
║     • 100+ idiomas (mais que paraphrase)             ║
║     • Excelente equilíbrio geral                    ║
║     • Contexto longo (8192 tokens)                   ║
║     • Cabe bem na RTX 4070                           ║
║                                                        ║
║  ⚠️ Fracos:                                          ║
║     • Mais lento que paraphrase (0.08s vs 0.06s)    ║
║     • VRAM maior (2.5GB vs 1.5GB)                   ║
║     • Menos específico para PT que paraphrase         ║
║                                                        ║
╚══════════════════════════════════════════════════════╝
```

**Quando usar:**
- ✅ Documentos em múltiplos idiomas
- ✅ Documentos em inglês, espanhol, chinês, etc.
- ✅ Projetos internacionais
- ✅ <5% dos seus documentos

---

## 🎯 ESTRATÉGIA RECOMENDADA PARA SEU CASO

### **DISTRIBUIÇÃO DE DOCUMENTOS (20.000)**

```
┌─────────────────────────────────────────────────────────┐
│  DISTRIBUIÇÃO DE SEUS DOCUMENTOS                         │
└─────────────────────────────────────────────────────────┘

Português / Geral:        15.000 docs (75%)
Engenharia / Código:      4.000 docs (20%)
Multilíngua (outros):     1.000 docs (5%)
                          ───────
TOTAL:                   20.000 docs
```

### **MODELO PARA CADA GRUPO**

```
┌─────────────────────────────────────────────────────────┐
│  ESTRATÉGIA HÍBRIDA INTELIGENTE                         │
└─────────────────────────────────────────────────────────┘

🇧🇷 Português / Geral (15.000 docs):
   → paraphrase-multilingual-mpnet-base-v2
   → VRAM: 1.5GB
   → Velocidade: 0.06s
   → Precisão PT: MÁXIMA

💻 Engenharia / Código (4.000 docs):
   → e5-mistral-7b-instruct
   → VRAM: 4.5GB (carregar dinamicamente)
   → Velocidade: 0.12s
   → Precisão Código: MÁXIMA

🌍 Multilíngua (1.000 docs):
   → bge-m3
   → VRAM: 2.5GB (carregar dinamicamente)
   → Velocidade: 0.08s
   → Precisão Multilíngua: MÁXIMA
```

---

## 🚀 COMO USAR (CÓDIGO)

### Importar funções de conveniência:

```python
from src.config import (
    configure_embeddings_code,
    configure_embeddings_general,
    configure_embeddings_multilingual,
)
```

### Para código / engenharia:

```python
# Carregar modelo para código (4.5GB VRAM)
embeddings_code = configure_embeddings_code()

# Gerar embeddings
vector = embeddings_code.embed_query("def authenticate_user(...)")
```

### Para português / geral:

```python
# Carregar modelo para PT/geral (1.5GB VRAM)
embeddings_general = configure_embeddings_general()

# Gerar embeddings
vector = embeddings_general.embed_query("Django é um framework web")
```

### Para multilíngua:

```python
# Carregar modelo para multilíngua (2.5GB VRAM)
embeddings_multi = configure_embeddings_multilingual()

# Gerar embeddings
vector = embeddings_multi.embed_query("Python is the best language")
```

---

## 💻 AUTO-CLASSIFICAÇÃO (Seleção Dinâmica)

```python
from src.config import get_embeddings

# Auto-seleção baseada no tipo de conteúdo

# Se conteúdo for código
if content.is_code():
    embeddings = get_embeddings(task="code")

# Se conteúdo for em português
elif content.is_portuguese():
    embeddings = get_embeddings(task="general")

# Se conteúdo for multilíngua
else:
    embeddings = get_embeddings(task="multilingual")
```

---

## 📊 DESEMPENHO COM ESTRATÉGIA HÍBRIDA

### Tempo para 20.000 documentos:

```
┌─────────────────────────────────────────────────────────┐
│  TEMPO DE PROCESSAMENTO (1ª vez)                        │
└─────────────────────────────────────────────────────────┘

Classificação (Gemini Flash 2.5):
  20.000 docs × 0.1s = 2.000s ÷ 60 = 33 minutos

Embeddings (Estratégia Híbrida):
  15.000 docs (PT/geral) × 0.06s = 900s = 15 minutos
  4.000 docs (código) × 0.12s = 480s = 8 minutos
  1.000 docs (multilíngua) × 0.08s = 80s = 1.3 minutos
                            ─────
  Total embedings:          ~24.3 minutos

Inserção Neo4j:
  ~30 minutos
                        ─────
TOTAL:                  ~1.3 horas
```

### Custo mensal:

```
LLM (Gemini Flash 2.5):
  10M tokens × $0.015/1M = $0.15

Embeddings (LocalAI):
  $0.00 (grátis na GPU)

TOTAL:                  $0.15/mês
```

### VRAM uso:

```
┌─────────────────────────────────────────────────────────┐
│  VRAM NA RTX 4070 (8GB)                                │
└─────────────────────────────────────────────────────────┘

LLM (Gemini Flash):       0GB (API Google)

Embeddings:
  - Modelo PT/geral:      1.5GB (sempre carregado)
  - Modelo código:        4.5GB (carregar sob demanda)
  - Modelo multilíngua:    2.5GB (carregar sob demanda)
  - Batch temporário:      0.5GB

TOTAL MÁXIMO:            9.0GB
DISPONÍVEL:              8GB

⚠️ CUIDADO: Pode dar OOM se carregar código + multilíngua juntos!

SOLUÇÃO: Carregar UM modelo de cada vez (não todos simultaneamente)
```

---

## 🎯 RECOMENDAÇÃO FINAL

### **USE ESTRATÉGIA HÍBRIDA!** 🏆

**Por quê?**

1. ✅ **MÁXIMA PRECISÃO** em cada categoria
   - PT/geral: paraphrase-multilingual (MELHOR!)
   - Código: e5-mistral-7b (MELHOR!)
   - Multilíngua: bge-m3 (MELHOR!)

2. ✅ **MELHOR EQUILÍBRIO** qualidade/velocidade
   - PT/geral: 0.06s (super rápido!)
   - Código: 0.12s (aceitável para máxima precisão)
   - Multilíngua: 0.08s (rápido!)

3. ✅ **VRAM EFICIENTE** (carregar sob demanda)
   - PT/geral: 1.5GB (sempre carregado)
   - Código: 4.5GB (carregar apenas quando necessário)
   - Multilíngua: 2.5GB (carregar apenas quando necessário)

4. ✅ **FLEXÍVEL** para qualquer tipo de conteúdo
   - Seu conhecimento muda, adapta-se!

---

## 💡 IMPLEMENTAÇÃO PRÁTICA

### Passo 1: Classificar documentos (Gemini Flash 2.5)

```python
# Classifica: "tipo": "pt-geral | codigo | multilíngua"
llm = configure_llm_gemini(api_key="...")

for doc in documents:
    tipo = llm.classify(doc.content)
    doc.tipo = tipo  # Salvar tipo
```

### Passo 2: Gerar embeddings (modelo certo para cada tipo)

```python
# Gerar embeddings com modelo apropriado
for doc in documents:
    if doc.tipo == "codigo":
        emb = configure_embeddings_code()
    elif doc.tipo == "multilíngua":
        emb = configure_embeddings_multilingual()
    else:  # pt-geral
        emb = configure_embeddings_general()

    doc.embedding = emb.embed_query(doc.content)
```

### Passo 3: Inserir no Neo4j

```python
# Inserir com metadata do modelo usado
graph.query("""
  CREATE (i:Item {
    nome: $nome,
    tipo: $tipo,
    embedding_model: $embedding_model,
    embedding: $embedding
  })
""", params={...})
```

---

## 📝 RESUMO EM 1 FRASE

> **ESTRATÉGIA HÍBRIDA:**
> 
> - 80% PT/geral → `paraphrase-multilingual` (1.5GB, 0.06s)
> - 20% código/engenharia → `e5-mistral-7b` (4.5GB, 0.12s)
> - <5% multilíngua → `bge-m3` (2.5GB, 0.08s)
> 
> **= MÁXIMA PRECISÃO + MELHOR DESEMPENHO!**

---

Ainda tem dúvida? Posso implementar o código completo de auto-classificação!
