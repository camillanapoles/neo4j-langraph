# 🤖 LITELLM - Guia Completo

**Data:** 25/12/2024
**Projeto:** neo4j-langraph (Sistema de Conhecimento Pessoal)
**Stack:** K3S + Neo4j + LocalAI + LiteLLM + Gemini Flash 2.5

---

## 📚 ÍNDICE

1. [O que é LiteLLM?](#o-que-e-litellm)
2. [Arquitetura do Sistema](#arquitetura-do-sistema)
3. [Configuração](#configuração)
4. [Como Usar](#como-usar)
5. [Troubleshooting](#troubleshooting)

---

## 🤖 O QUE É LITELLM?

**LiteLLM** é um proxy de roteamento para múltiplos modelos LLM.

### ✅ Vantagens do LiteLLM:

1. **Roteamento Automático** - Escolhe o melhor modelo automaticamente
2. **Fallback Inteligente** - Se um modelo falhar, usa outro
3. **Load Balancing** - Distribui requests entre modelos
4. **Interface Unificada** - Todos os modelos usam formato OpenAI
5. **Custo Otimizado** - Roteia para modelo mais barato disponível

### 📊 Comparação: com e sem LiteLLM

| Aspecto | Sem LiteLLM | Com LiteLLM |
|---------|-------------|-------------|
| Roteamento | Manual | Automático ✅ |
| Fallback | Manual | Automático ✅ |
| Load Balancing | Não | Sim ✅ |
| Custo | Alto | Otimizado ✅ |
| Disponibilidade | 95% | 99%+ ✅ |

---

## 🏗️ ARQUITETURA DO SISTEMA

### Diagrama

```
┌─────────────────────────────────────────────────────────┐
│  LangChain App (Knowledge Graph)                     │
│     ↓                                                 │
│  LiteLLM Proxy (Roteador Inteligente)                │
│     ↓                                                 │
│  ┌──────────────┬──────────────┬──────────────┐     │
│  │ Gemini Flash│ LocalAI LLM │  OpenAI GPT4 │     │
│  │  (Primário) │ (Secundário)│  (Opcional)  │     │
│  └──────────────┴──────────────┴──────────────┘     │
│        ↓              ↓              ↓              │
│  Google API      Local GPU      OpenAI API            │
│  (Free Tier)     (Sem cota)     (Pago)               │
└─────────────────────────────────────────────────────────┘
```

### Fluxo de Roteamento

```
1. LangChain envia query para LiteLLM Proxy
   ↓
2. LiteLLM roteia para Gemini Flash (primário)
   ↓
3a. Se Gemini Flash funcionar (cota OK)
    → Retorna resposta
   ↓
3b. Se Gemini Flash falhar (cota 429)
    → Fallback para LocalAI (secundário)
    ↓
4. LocalAI processa (GPU local, sem cota)
    → Retorna resposta
```

---

## ⚙️ CONFIGURAÇÃO

### Arquivos de Configuração

#### 1. `.env.litellm` (Variáveis de Ambiente)

```bash
# Provider do LLM
LLM_PROVIDER=litellm

# Modelos configurados
LITELLM_PRIMARY_MODEL=gemini/gemini-2.0-flash-exp
LITELLM_SECONDARY_MODEL=localai/llama3.2:3b

# API Keys
GOOGLE_API_KEY=AIza...
LOCALAI_API_KEY=
OPENAI_API_KEY=

# LiteLLM Proxy
LITELLM_API_BASE=http://localhost:4000
LITELLM_FALLBACK_MODEL=localai/llama3.2:3b
LITELLM_ROUTING_STRATEGY=usage-based-routing
LITELLM_NUM_RETRIES=2
LITELLM_TIMEOUT=60

# LocalAI
LOCALAI_BASE_URL=http://localhost:30808/v1
LOCALAI_MODEL=llama3.2:3b
LOCALAI_TIMEOUT=60
```

#### 2. `litellm_config.yaml` (Configuração do Roteador)

```yaml
model_list:
  # Modelo Primário: Gemini Flash 2.5
  - model_name: gemini-flash
    litellm_params:
      model: gemini/gemini-2.0-flash-exp
      api_key: os.environ/GOOGLE_API_KEY
      max_tokens: 4096
      temperature: 0.7

  # Modelo Secundário: LocalAI (llama3.2:3b)
  - model_name: localai-llama
    litellm_params:
      model: localai/llama3.2:3b
      api_base: http://localhost:30808/v1
      api_key: os.environ/LOCALAI_API_KEY
      max_tokens: 2048
      temperature: 0.7

router_settings:
  model_group:
    primary-models:
      - gemini-flash
      - localai-llama

  routing_strategy: ["usage-based-routing"]
  fallback_model: localai-llama
  num_retries: 2
  timeout: 60
  set_fallbacks:
    - gemini-flash: localai-llama

general_settings:
  master_key: sk-litellm-master-key
  rpm_limit: 60
  max_batch_size: 10
  fallback_on_rate_limit: true

litellm_settings:
  drop_params: true
  validate_api_keys: false
  set_verbose: false
  debug: false
```

---

## 🚀 COMO USAR

### Passo 1: Baixar Modelo LLM (Secundário)

```bash
# Baixar modelo llama3.2:3b no LocalAI
python3 download_llm_model.py

# O modelo será salvo em:
# /mnt/container-data/projects/neo4j-langraph/models/
```

### Passo 2: Iniciar LiteLLM Proxy

```bash
# Iniciar o proxy na porta 4000
bash start_litellm.sh

# O proxy estará disponível em:
# http://localhost:4000
# Health: http://localhost:4000/health
# Models: http://localhost:4000/v1/models
```

### Passo 3: Testar Roteamento

```bash
# Testar o roteamento LiteLLM
python3 test_litellm.py

# O script irá:
# 1. Conectar ao LiteLLM Proxy
# 2. Enviar query para o grupo de modelos
# 3. LiteLLM roteia para Gemini Flash (primário)
# 4. Se Gemini falhar, roteia para LocalAI (secundário)
# 5. Retorna resposta
```

### Passo 4: Usar no LangChain

```python
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Conectar ao LiteLLM Proxy (usa formato OpenAI)
client = OpenAI(
    api_key="sk-litellm-master-key",
    base_url="http://localhost:4000/v1"
)

# Enviar query (LiteLLM roteia automaticamente)
response = client.chat.completions.create(
    model="gemini-flash",  # Modelo do grupo
    messages=[
        {"role": "user", "content": "Olá! Qual seu nome?"}
    ],
    temperature=0.7
)

print(response.choices[0].message.content)
```

---

## 🔧 TROUBLESHOOTING

### Problema 1: LiteLLM Proxy não inicia

**Sintoma:**
```
Error: Port 4000 already in use
```

**Solução:**
```bash
# Verificar o que está usando a porta 4000
lsof -i :4000

# Matar o processo
kill -9 [PID]

# Ou mudar a porta em litellm_config.yaml
```

---

### Problema 2: Erro 429 (Cota excedida)

**Sintoma:**
```
Error code: 429 - You exceeded your current quota
```

**Solução:**

LiteLLM deve rotear automaticamente para o modelo secundário. Verifique:

```bash
# Verificar se LocalAI está rodando
curl http://localhost:30808/v1/models

# Verificar se modelo LLM está baixado
python3 download_llm_model.py

# Verificar logs do LiteLLM
# (veja a saída do terminal onde rodou: bash start_litellm.sh)
```

---

### Problema 3: Modelo Secundário não funciona

**Sintoma:**
```
Error: Model 'localai/llama3.2:3b' not found
```

**Solução:**

Baixe o modelo LLM no LocalAI:

```bash
# Baixar modelo
python3 download_llm_model.py

# Verificar se modelo está disponível
curl http://localhost:30808/v1/models
```

---

### Problema 4: Timeout no LiteLLM

**Sintoma:**
```
Error: Timeout after 60 seconds
```

**Solução:**

Aumente o timeout:

```yaml
# No arquivo litellm_config.yaml
router_settings:
  timeout: 120  # Aumentar de 60 para 120 segundos
```

Ou no `.env.litellm`:

```bash
LITELLM_TIMEOUT=120
```

---

### Problema 5: Verbose logs

**Sintoma:**
```
Quer ver o que está acontecendo no roteamento
```

**Solução:**

Ative o modo verbose:

```yaml
# No arquivo litellm_config.yaml
litellm_settings:
  set_verbose: true
  debug: true
```

Ou inicie o proxy com flag verbose:

```bash
litellm --config litellm_config.yaml --port 4000 --verbose
```

---

## 📊 MÉTRICAS E MONITORAMENTE

### Verificar Status dos Modelos

```bash
# Listar modelos disponíveis no LiteLLM
curl http://localhost:4000/v1/models

# Verificar health do LiteLLM
curl http://localhost:4000/health
```

### Verificar Uso do Roteamento

Os logs do LiteLLM mostram:

```
[INFO] Routing to model: gemini/gemini-2.0-flash-exp
[INFO] Model returned: gemini-flash
[INFO] Request completed in 0.3s

[INFO] Routing to model: localai/llama3.2:3b
[INFO] Model returned: localai-llama
[INFO] Request completed in 0.5s
```

---

## 🎯 MELHORES PRÁTICAS

### 1. Use Nomes Descritivos

```yaml
# BOM
- model_name: gemini-flash-primary
- model_name: localai-llama-fallback

# RUIM
- model_name: model1
- model_name: model2
```

### 2. Configure Timeouts Apropriados

```yaml
# Gemini Flash: 60s (rápido)
# LocalAI: 120s (mais lento)
# OpenAI GPT4: 90s (balanceado)
```

### 3. Teste Fallbacks

```bash
# Testar se fallback funciona
# 1. Exceda cota do Gemini (faça many requests)
# 2. Verifique se roteia para LocalAI
# 3. Verifique logs do LiteLLM
```

### 4. Monitore Custos

```bash
# Gemini Flash: $0.075/1M tokens (input)
# LocalAI: $0 (gratuito)
# O LiteLLM roteará para o mais barato disponível
```

---

## 📚 REFERÊNCIAS

### Documentação Oficial

- **LiteLLM:** https://docs.litellm.ai/
- **Router:** https://docs.litellm.ai/docs/routing
- **Proxy:** https://docs.litellm.ai/docs/proxy
- **Python:** https://docs.litellm.ai/docs/providers

### Modelos Suportados

- **Google:** https://ai.google.dev/gemini-api/docs
- **LocalAI:** https://localai.io/
- **OpenAI:** https://platform.openai.com/docs

---

## ✅ CHECKLIST FINAL

### Configuração
- [x] Arquivo `.env.litellm` criado
- [x] Arquivo `litellm_config.yaml` criado
- [x] Google API Key configurada
- [x] LocalAI URL configurada

### Modelo LLM
- [ ] Modelo LLM baixado no LocalAI
- [ ] Modelo disponível na lista de modelos

### Proxy LiteLLM
- [ ] LiteLLM Proxy iniciado
- [ ] Proxy acessível em http://localhost:4000
- [ ] Health check OK

### Teste
- [ ] Roteamento testado
- [ ] Fallback testado
- [ ] LangChain integrado

---

## 🎉 CONCLUSÃO

### O que você aprendeu:

1. **✅ O que é LiteLLM** - Proxy de roteamento para múltiplos modelos
2. **✅ Arquitetura** - Roteamento automático com fallback
3. **✅ Configuração** - Arquivos `.env.litellm` e `litellm_config.yaml`
4. **✅ Como usar** - Scripts `start_litellm.sh` e `test_litellm.py`
5. **✅ Troubleshooting** - Problemas comuns e soluções

### Próximos Passos:

1. **Baixar modelo LLM**
   ```bash
   python3 download_llm_model.py
   ```

2. **Iniciar LiteLLM Proxy**
   ```bash
   bash start_litellm.sh
   ```

3. **Testar roteamento**
   ```bash
   python3 test_litellm.py
   ```

4. **Usar no LangChain**
   ```python
   from openai import OpenAI
   client = OpenAI(
       api_key="sk-litellm-master-key",
       base_url="http://localhost:4000/v1"
   )
   # ... usar LangChain ...
   ```

---

**Autor:** CNMFS
**Data:** 25/12/2024
**Versão:** 1.0.0
