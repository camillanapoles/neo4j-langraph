#!/bin/bash
# Script para configurar modelos HuggingFace com GPU

set -e

echo "🤗 Configurando modelos HuggingFace com GPU..."
echo "=============================================="
echo ""

# Verificar se há GPU NVIDIA disponível
if command -v nvidia-smi &> /dev/null; then
    echo "🎮 GPU NVIDIA detectada!"
    nvidia-smi --query-gpu=name,memory.total --format=csv,noheader,nounits
    echo ""
else
    echo "⚠️ GPU NVIDIA não detectada, usando CPU"
    echo ""
fi

echo "📦 Instalando dependências de GPU..."
echo ""

# Instalar dependências GPU
uv pip install torch --index-url https://download.pytorch.org/whl/cu121
uv pip install transformers sentence-transformers accelerate

echo ""
echo "⬇️ Baixando modelos HuggingFace..."
echo ""

# Script Python para baixar modelos
cat > /tmp/download_models.py << 'EOF'
import os
from sentence_transformers import SentenceTransformer
import torch

print("Verificando disponibilidade de GPU...")
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Dispositivo: {device}")
if device == "cuda":
    print(f"GPU: {torch.cuda.get_device_name(0)}")
    print(f"Memória: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")
print()

print("⬇️ Baixando modelo de embeddings...")
model_name = os.getenv("HF_EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
print(f"Modelo: {model_name}")

model = SentenceTransformer(model_name)
print(f"✅ Modelo baixado e carregado em {device}!")
print(f"Dimensões de embeddings: {model.get_sentence_embedding_dimension()}")
EOF

# Executar download
HF_EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2 .venv/bin/python /tmp/download_models.py

echo ""
echo "✅ Configuração completa!"
echo ""
echo "📝 Próximos passos:"
echo "1. Copiar configuração GPU:"
echo "   cp .env.gpu .env"
echo ""
echo "2. Editar .env para usar EMBEDDING_BACKEND=huggingface"
echo ""
echo "3. Testar no sistema:"
echo "   .venv/bin/python test_system.py"
echo ""
