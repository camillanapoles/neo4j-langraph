# ================================================================
# COMO CONFIGURAR GOOGLE API KEY
# ================================================================

## 1. Obter API Key do Google

1. Acesse: https://makersuite.google.com/app/apikey
2. Clique em "Create API Key"
3. Copie a chave (começa com `AIza...`)

## 2. Configurar no .env

Abra o arquivo .env e adicione sua chave:

```bash
# Edite o arquivo
vim .env

# Adicione sua chave após o sinal de =
GOOGLE_API_KEY=AIza...sua-chave-aqui
```

## 3. Testar a configuração

```bash
# Testar LLM
.venv/bin/python test_llm.py

# Testar embeddings (se configurado)
.venv/bin/python test_gemini_embeddings.py
```

## 4. Verificar se funcionou

Se tudo estiver OK, você verá:

```
✅ LLM funcionando!
📝 Resposta: Olá! Sou o Gemini...

🎉 SISTEMA AI COMPLETO TESTADO!
```

---

## 🚨 PROBLEMAS COMUNS

### Erro: "Missing Authorization header"

**Causa:** GOOGLE_API_KEY não configurada

**Solução:**
```bash
vim .env
# Adicione: GOOGLE_API_KEY=AIza...
```

### Erro: "API key not valid"

**Causa:** API key incorreta ou expirada

**Solução:**
1. Gerar nova chave em: https://makersuite.google.com/app/apikey
2. Atualizar no .env

### Erro: "Quota exceeded"

**Causa:** Limite de cota da API (free tier = 15 requests/min)

**Solução:**
1. Aguarde alguns minutos
2. Ou faça upgrade para plano pago

---

## 📊 CUSTOS DO GEMINI FLASH 2.5

| Operação | Preço | Uso típico | Custo mensal |
|----------|--------|------------|--------------|
| Input (texto) | $0.075/1M tokens | 100K tokens/dia | ~$0.23/mês |
| Output (texto) | $0.15/1M tokens | 50K tokens/dia | ~$0.23/mês |
| **TOTAL** | - | - | **~$0.46/mês** |

✅ **Muito mais barato que GPT-4!** (~$20/mês)

---

## 🎯 PRÓXIMOS PASSOS

1. ✅ Obter API Key do Google
2. ✅ Adicionar ao .env
3. ✅ Testar LLM
4. ✅ Ingerir documentos
5. ✅ Fazer queries

---

**Documentação:** https://ai.google.dev/gemini-api/docs
**Pricing:** https://ai.google.dev/pricing
**Console:** https://makersuite.google.com/
