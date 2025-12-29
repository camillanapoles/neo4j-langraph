#!/bin/bash
# Script para baixar modelos GGUF para LocalAI

set -e

MODELS_DIR="models"
mkdir -p "$MODELS_DIR"

echo "📦 Baixando modelos GGUF para LocalAI..."
echo "==============================================="
echo ""

# Lista de modelos para baixar
declare -A MODELS=(
    # LLMs (para Classificação e Geração)
    ["llama3.1-8b-instruct-q4_k_m.gguf"]="https://huggingface.co/QuantFactory/Llama-3.1-8B-Instruct-GGUF/resolve/main/Llama-3.1-8B-Instruct.Q4_K_M.gguf"

    # Embeddings (bge-m3 - MELHOR para português!)
    ["bge-m3-q4_k_m.gguf"]="https://huggingface.co/QuantFactory/bge-m3-GGUF/resolve/main/bge-m3.Q4_K_M.gguf"

    # LLM menor (mais rápido para classificação)
    ["phi-3-mini-4k-instruct-q4_k_m.gguf"]="https://huggingface.co/QuantFactory/Phi-3-mini-4k-Instruct-GGUF/resolve/main/Phi-3-mini-4k-Instruct.Q4_K_M.gguf"
)

echo "Modelos disponíveis:"
for model in "${!MODELS[@]}"; do
    echo "  • $model"
done
echo ""

for model_file in "${!MODELS[@]}"; do
    url="${MODELS[$model_file]}"
    model_path="$MODELS_DIR/$model_file"

    if [ -f "$model_path" ]; then
        echo "✅ $model_file já baixado"
        continue
    fi

    echo "⬇️ Baixando $model_file..."
    echo "   URL: $url"

    curl -L -o "$model_path" "$url"

    if [ $? -eq 0 ]; then
        size=$(du -h "$model_path" | cut -f1)
        echo "   ✅ Baixado com sucesso! ($size)"
    else
        echo "   ❌ Erro ao baixar $model_file"
        exit 1
    fi

    echo ""
done

echo "==============================================="
echo "✅ Todos os modelos baixados!"
echo ""
echo "📁 Diretório de modelos: $MODELS_DIR/"
echo ""

echo "📊 Tamanho dos modelos:"
du -h "$MODELS_DIR"/*
echo ""

echo "🚀 Próximos passos:"
echo "1. Copiar modelos para o PVC do LocalAI:"
echo "   kubectl cp $MODELS_DIR/ neo4j-langraph/localai-xxx-xxx:/models/"
echo ""
echo "2. Ou montar o diretório local no pod"
echo ""
