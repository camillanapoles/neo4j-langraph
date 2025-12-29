# EMBEDDINGS.md - Guia Completo de Modelos de Embeddings

Este documento explica TUDO sobre embeddings para este projeto.

---

## 🎯 O QUE SÃO EMBEDDINGS?

Embeddings = Converter texto em números (vetores) que representam **significado semântico**

```
Texto: "Django é um framework web"
   ↓ Embedding Model
   ↓
Vetor: [0.123, -0.456, 0.789, ...] (384, 768, 1024, ou 4096 números)
   ↓
   ↓
Busca semântica: Encontra textos com SIGNIFICADO SIMILAR (não só palavras iguais)
```

**Exemplo:**
```
Busca: "sentient cowboy doll"
Match exato: ❌ Nada encontrado

Busca semântica:
  "Toy Story" (filme sobre brinquedos) → ✅ MATCH 92%!
  "Toy Story 2" → ✅ MATCH 88%!
```

---

## 📊 TIPOS DE MODELOS DE EMBEDDINGS

### 1. Monolíngua (um idioma só)

**Exemplo:** `bge-small-en-v1.5` ("en" = English)

```
┌─────────────────────────────────────────────────────────┐
│  bge-small-en-v1.5                                     │
├─────────────────────────────────────────────────────────┤
│                                                        │
│  🇺🇸 Inglês:           ⭐⭐⭐⭐⭐ MELHOR!            │
│  🇧🇷 Português:       ⭐ Ruim                        │
│  🌍 Outros idiomas:  ⭐ Ruim                        │
│                                                        │
│  ✅ Fortes:                                          ║
│     • MELHOR para inglês                            ║
│     • Muito rápido e pequeno                          ║
│     • Excelente para buscas em inglês                 ║
║                                                        ║
║  ⚠️ Fracos:                                          ║
║     • NÃO funciona para português                     ║
║     • Limitado a um idioma                           ║
║                                                        ║
╚══════════════════════════════════════════════════════╝
```

**Quando usar:**
- ✅ Trabalha apenas com conteúdo em inglês
- ✅ Precisa de velocidade máxima
- ❌ NÃO usar para português

---

### 2. Multilíngua (100+ idiomas)

**Exemplo:** `bge-m3`, `e5-mistral-7b`, `paraphrase-multilingual-mpnet-base-v2`

```
┌─────────────────────────────────────────────────────────┐
│  Modelos Multilíngua                                   │
├─────────────────────────────────────────────────────────┤
│                                                        │
│  🇺🇸 Inglês:           ⭐⭐⭐⭐ Excelente          │
│  🇧🇷 Português:       ⭐⭐⭐⭐ Muito bom            │
│  🇪🇸 Espanhol:         ⭐⭐⭐⭐ Muito bom            │
│  🇨🇳 Chinês:          ⭐⭐⭐⭐ Muito bom            │
│  ... (100+ idiomas)                                │
│                                                        │
║  ✅ Fortes:                                          ║
║     • Funciona em múltiplos idiomas                ║
║     • Excelente para português brasileiro          ║
║     • Ideal para conhecimento multilíngua          ║
║                                                        ║
║  ⚠️ Fracos:                                          ║
║     • Um pouco mais lento que monolíngua           ║
║     • VRAM maior                                    ║
║                                                        ║
╚══════════════════════════════════════════════════════╝
```

**Quando usar:**
- ✅ Trabalha com múltiplos idiomas
- ✅ Conhecimento pessoal (muitos tipos de conteúdo)
- ✅ Projeto internacional
- ✅ RECOMENDADO para este projeto!

---

## 🇧🇷 MODELOS MELHORES PARA PORTUGUÊS BRASILEIRO

### 1. **paraphrase-multilingual-mpnet-base-v2** 🥇 **VENCEDOR**

```
╔══════════════════════════════════════════════════════╗
║  🥇 paraphrase-multilingual-mpnet-base-v2             ║
║  Sentence-Transformers (2023)                          ║
╠══════════════════════════════════════════════════════╣
║                                                        ║
║  🇧🇷 Português:        ⭐⭐⭐⭐⭐ MELHOR!            ║
║  🇧🇷 Específico PT-BR: ⭐⭐⭐⭐⭐ MELHOR!            ║
║  🇧🇷 Parafrase:       ⭐⭐⭐⭐⭐ MELHOR!            ║
║  🌍 Multilíngua:      50+ idiomas                    ║
║  📊 Tamanho (Q4):     1.5GB                          ║
║  ⚡ Velocidade:       0.06s/embedding               ║
║  🎯 Dimensões:        768                            ║
║                                                        ║
║  ✅ Fortes:                                          ║
║     • MELHOR para português brasileiro             ║
║     • Treinado especificamente para paráfrase PT-BR ║
║     • Excelente para encontrar textos similares       ║
║     • 50+ idiomas                                    ║
║     • Muito rápido (0.06s)                           ║
║     • Pequeno (1.5GB)                               ║
║                                                        ║
║  ⚠️ Fracos:                                          ║
║     • Menos idiomas que bge-m3 (50+ vs 100+)         ║
║     • Menos focado em código/engenharia              ║
║     • Dimensões menores (768 vs 1024/4096)           ║
║                                                        ║
╚══════════════════════════════════════════════════════╝
```

**Por que é o VENCEDOR para português brasileiro:**
- ✅ **MELHOR** modelo para português brasileiro
- ✅ Treinado especificamente para PT-BR
- ✅ Excelente para paráfrase (encontrar textos similares)
- ✅ 50+ idiomas
- ✅ Muito rápido (0.06s)
- ✅ Pequeno (1.5GB VRAM)

**VRAM uso na RTX 4070 (8GB):**
```
LLM (OpenAI API):          0GB (não usa VRAM)
Embeddings:                1.5GB
TOTAL:                     1.5GB
DISPONÍVEL:                6.5GB ✅ (sobra muito!)
```

---

### 2. **BAAI/bge-m3** 🥈 Segundo Lugar

```
╔══════════════════════════════════════════════════════╗
║  🥈 BAAI/bge-m3                                        ║
║  BAAI (2023)                                            ║
╠══════════════════════════════════════════════════════╣
║                                                        ║
║  🇧🇷 Português:        ⭐⭐⭐⭐ Muito bom            ║
║  🌍 Multilíngua:      100+ idiomas                   ║
║  📊 Tamanho (Q4):     2.5GB                          ║
║  ⚡ Velocidade:       0.08s/embedding               ║
║  🎯 Dimensões:        1024                           ║
║                                                        ║
║  ✅ Fortes:                                          ║
║     • Excelente para português brasileiro          ║
║     • 100+ idiomas (mais que paraphrase)             ║
║     • Dimensões maiores (1024 vs 768) = mais precisão ║
║     • Contexto longo (8192 tokens)                   ║
║     • Bom balance geral                              ║
║                                                        ║
║  ⚠️ Fracos:                                          ║
║     • Mais lento que paraphrase (0.08s vs 0.06s)     ║
║     • VRAM maior (2.5GB vs 1.5GB)                    ║
║     • Menos específico para PT-BR que paraphrase      ║
║                                                        ║
╚══════════════════════════════════════════════════════╝
```

**Quando é melhor que paraphrase:**
- ✅ Precisa de mais idiomas (100+ vs 50+)
- ✅ Quer mais precisão (1024 vs 768 dimensões)
- ✅ Contexto mais longo (8192 vs 512 tokens)

---

### 3. **intfloat/e5-mistral-7b-instruct** 🥉 Para Engenharia de Software

```
╔══════════════════════════════════════════════════════╗
║  🥉 intfloat/e5-mistral-7b-instruct                   ║
║  Microsoft (2024)                                       ║
╠══════════════════════════════════════════════════════╣
║                                                        ║
║  🇧🇷 Português:        ⭐⭐⭐⭐ Muito bom            ║
║  💻 Engenharia/Código: ⭐⭐⭐⭐⭐ MELHOR!              ║
║  🌍 Multilíngua:      100+ idiomas                   ║
║  📊 Tamanho (Q4):     4.5GB                          ║
║  ⚡ Velocidade:       0.12s/embedding               ║
║  🎯 Dimensões:        4096                           ║
║                                                        ║
║  ✅ Fortes:                                          ║
║     • MELHOR para engenharia de software           ║
║     • MELHOR para código e tecnologias               ║
║     • Instrução-tuning (entende melhor contexto)     ║
║     • 100+ idiomas                                   ║
║     • Dimensões gigantes (4096) = máxima precisão    ║
║                                                        ║
║  ⚠️ Fracos:                                          ║
║     • VRAM muito grande (4.5GB)                      ║
║     • Mais lento (0.12s vs 0.06s)                    ║
║     • Pode dar OOM na RTX 4070 (8GB)                ║
║                                                        ║
╚══════════════════════════════════════════════════════╝
```

**Quando usar:**
- ✅ Foco em engenharia de software, código, tecnologias
- ✅ Quer máxima precisão para contexto técnico
- ✅ Precisa de mais idiomas
- ⚠️ CUIDADO: 4.5GB VRAM pode dar OOM na RTX 4070!

**VRAM uso na RTX 4070 (8GB):**
```
LLM (OpenAI API):          0GB
Embeddings:                4.5GB
TOTAL:                     4.5GB
DISPONÍVEL:                3.5GB ✅ (cabe, mas não sobra muito!)
```

---

## 💻 MODELOS MELHORES PARA ENGENHARIA DE SOFTWARE

### 1. **intfloat/e5-mistral-7b-instruct** 🏆 **VENCEDOR**

**Ver detalhes acima**

### 2. **code-bert** (Específico para Código)

```
╔══════════════════════════════════════════════════════╗
║  code-bert                                             ║
║  Microsoft (2020)                                       ║
╠══════════════════════════════════════════════════════╣
║                                                        ║
║  💻 Engenharia/Código: ⭐⭐⭐⭐⭐ MELHOR!              ║
║  🇧🇷 Português:        ⭐ Bom                        ║
║  🌍 Multilíngua:      ⭐ Ruim (inglês só)             ║
║  📊 Tamanho (Q4):     2GB                            ║
║  ⚡ Velocidade:       0.1s/embedding                ║
║  🎯 Dimensões:        768                            ║
║                                                        ║
║  ✅ Fortes:                                          ║
║     • MELHOR para código puro                        ║
║     • Específico para código                        ║
║     • Entende sintaxe e semântica de código          ║
║     • Excelente para busca de código                 ║
║                                                        ║
║  ⚠️ Fracos:                                          ║
║     • NÃO funciona bem para português                ║
║     • Inglês só                                     ║
║     • Antigo (2020)                                  ║
║     • Limitado a código, não geral                   ║
║                                                        ║
╚══════════════════════════════════════════════════════╝
```

**Quando usar:**
- ✅ Busca apenas de código (não documentação)
- ✅ Precisa de algo específico para código
- ❌ NÃO usar para português brasileiro

---

## 📊 TABELA COMPARATIVA COMPLETA

| Modelo | Português | Engenharia | Geral | Multilíngua | VRAM | Velocidade |
|--------|-----------|-----------|-------|-------------|------|-----------|
| **paraphrase-multilingual** | 🏆 **MELHOR** | ⭐⭐⭐ | ⭐⭐⭐⭐ | 50+ | 1.5GB | 0.06s |
| **bge-m3** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 100+ | 2.5GB | 0.08s |
| **e5-mistral-7b** | ⭐⭐⭐⭐ | 🏆 **MELHOR** | ⭐⭐⭐⭐ | 100+ | 4.5GB | 0.12s |
| **code-bert** | ⭐ | 🏆 **MELHOR** | ⭐⭐ | ❌ | 2GB | 0.1s |
| **bge-small-en** | ❌ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ❌ | 500MB | 0.05s |

---

## 🎯 RECOMENDAÇÕES POR CASO DE USO

### CASO 1: Conhecimento Pessoal Geral (Português + Outros)

**USE: `paraphrase-multilingual-mpnet-base-v2`** 🏆

**Por quê?**
- ✅ MELHOR para português brasileiro
- ✅ 50+ idiomas (bom para misto)
- ✅ Muito rápido (0.06s)
- ✅ Pequeno (1.5GB)
- ✅ Excelente para paráfrase (texto similar)

**VRAM na RTX 4070:** 1.5GB ✅

---

### CASO 2: Engenharia de Software + Código + Tecnologias

**USE: `intfloat/e5-mistral-7b-instruct`** 🏆

**Por quê?**
- ✅ MELHOR para engenharia de software
- ✅ MELHOR para código e tecnologias
- ✅ 100+ idiomas
- ✅ Instrução-tuning (entende melhor contexto)
- ✅ Dimensões grandes (4096) = máxima precisão

**VRAM na RTX 4070:** 4.5GB ⚠️ (pode dar OOM!)

---

### CASO 3: Equilíbrio (Português + Engenharia + Geral)

**USE: `BAAI/bge-m3`** 🏆

**Por quê?**
- ✅ Excelente para português
- ✅ Muito bom para engenharia
- ✅ Bom para geral
- ✅ 100+ idiomas
- ✅ Balance geral

**VRAM na RTX 4070:** 2.5GB ✅

---

### CASO 4: Busca Apenas de Código (Sem Português)

**USE: `code-bert`** 🏆

**Por quê?**
- ✅ MELHOR para código
- ✅ Específico para busca de código
- ✅ Entende sintaxe e semântica

**VRAM na RTX 4070:** 2GB ✅

**⚠️ NÃO usar para português brasileiro!**

---

## 🏆 RECOMENDAÇÃO FINAL PARA SEU PROJETO

### **USE paraphrase-multilingual-mpnet-base-v2** 🏆

**Por quê?**

1. **MELHOR para português brasileiro** (seu conhecimento principal)
2. **50+ idiomas** (bom para conteúdo misto)
3. **Excelente para paráfrase** (encontrar textos similares)
4. **Muito rápido** (0.06s)
5. **Pequeno** (1.5GB VRAM)
6. **Cabe facilmente** na RTX 4070

**VRAM uso:**
```
LLM (OpenAI API):          0GB
Embeddings:                1.5GB
TOTAL:                     1.5GB
DISPONÍVEL:                6.5GB ✅ (sobra muito!)
```

**Configuração:**
```bash
# .env
EMBEDDINGS_PROVIDER=localai
LOCAL_EMBEDDINGS_MODEL=paraphrase-multilingual-mpnet-base-v2
```

---

## 🔧 COMO MUDAR DE MODELO

```bash
# 1. Baixar novo modelo (se não tiver)
./download_models.sh

# 2. Atualizar .env
vim .env
```

```bash
# Mudar para:
LOCAL_EMBEDDINGS_MODEL=paraphrase-multilingual-mpnet-base-v2

# Ou:
LOCAL_EMBEDDINGS_MODEL=bge-m3

# Ou:
LOCAL_EMBEDDINGS_MODEL=e5-mistral-7b-instruct
```

---

## 📝 RESUMO EM 1 FRASE

> **Para português brasileiro + conhecimento geral: `paraphrase-multilingual-mpnet-base-v2`**
> 
> **Para engenharia de software + código: `intfloat/e5-mistral-7b-instruct`**
> 
> **Para equilíbrio: `BAAI/bge-m3`**

---

Ainda tem dúvida? Posso explicar mais detalhadamente qualquer modelo!
