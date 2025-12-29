@echo off
REM Script de setup para ambiente virtual isolado (Windows)

echo 🔧 Configurando ambiente virtual isolado para neo4j-langraph...

REM Criar ambiente virtual
python -m venv .venv

echo ✅ Ambiente virtual criado em .venv\

REM Ativar ambiente virtual
call .venv\Scripts\activate.bat

REM Atualizar pip
echo 📦 Atualizando pip...
python -m pip install --upgrade pip setuptools wheel

REM Instalar o projeto em modo editável
echo 📦 Instalando neo4j-langraph em modo editável...
pip install -e ".[dev]"

REM Criar arquivo .env se não existir
if not exist .env (
    echo 📄 Criando arquivo .env...
    copy .env.example .env
    echo ⚠️  IMPORTANTE: Edite o arquivo .env com sua API Key da OpenAI
)

echo.
echo ✅ Setup completo!
echo.
echo Para ativar o ambiente:
echo   .venv\Scripts\activate.bat
echo.
echo Para desativar:
echo   deactivate
echo.
echo Comandos disponíveis:
echo   neo4j-ingest           - Ingerir conhecimento pessoal
echo   neo4j-relationships    - Criar relacionamentos semânticos
echo   neo4j-clusters         - Detectar clusters de conhecimento
echo   neo4j-dashboard        - Visualizar dashboard
echo   neo4j-index-project    - Indexar projeto
echo   neo4j-similarity       - Calcular similaridades entre projetos
echo   neo4j-detect-changes   - Detectar mudanças na documentação
echo   neo4j-governance-report - Gerar relatório de governança
echo.
