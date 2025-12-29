#!/bin/bash

# Script de setup para ambiente virtual isolado com UV

set -e

echo "🔧 Configurando ambiente virtual isolado para neo4j-langraph..."

# Verificar se uv está instalado
if ! command -v uv &> /dev/null; then
    echo "❌ UV não encontrado. Instale com: pip install uv"
    exit 1
fi

# Criar ambiente virtual com uv
echo "📦 Criando ambiente virtual com uv..."
uv venv
echo "✅ Ambiente virtual criado em .venv/"

# Instalar o projeto em modo editável (development)
echo "📦 Instalando neo4j-langraph em modo editável..."
uv pip install -e ".[dev]"

# Criar arquivo .env se não existir
if [ ! -f .env ]; then
    echo "📄 Criando arquivo .env..."
    cp .env.example .env
    echo "⚠️  IMPORTANTE: Edite o arquivo .env com sua API Key da OpenAI"
    echo "   vim .env"
fi

echo ""
echo "✅ Setup completo!"
echo ""
echo "Para usar o ambiente:"
echo "  .venv/bin/python script.py"
echo ""
echo "Comandos disponíveis:"
echo "  neo4j-knowledge       - Sistema de conhecimento pessoal"
echo "    ├─ ingest <path>    - Ingerir conhecimento"
echo "    ├─ relationships    - Criar relacionamentos"
echo "    ├─ clusters         - Detectar clusters"
echo "    ├─ dashboard        - Visualizar dashboard"
echo "    └─ query <texto>    - Fazer perguntas"
echo ""
echo "  neo4j-governance       - Governança de projetos"
echo "    ├─ index <path>     - Indexar projeto"
echo "    ├─ similarity       - Calcular similaridades"
echo "    ├─ detect-changes   - Detectar mudanças"
echo "    ├─ report           - Relatório de governança"
echo "    └─ dashboard        - Dashboard de projetos"
echo ""
echo "Passos seguintes:"
echo "  1. Configure OPENAI_API_KEY no .env"
echo "  2. Inicie Neo4j: docker-compose up -d"
echo "  3. Teste: .venv/bin/python test_system.py"
echo ""
