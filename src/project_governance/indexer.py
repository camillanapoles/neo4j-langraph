"""Indexação de projetos e documentação"""

import json
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime

from langchain_core.prompts import ChatPromptTemplate

from src.config import get_graph
from src.shared.embeddings import EmbeddingManager
from src.shared.llm import LLMConfig
from src.shared.utils import generate_hash, read_file_content


class ProjectIndexer:
    """Gerencia indexação de projetos e documentação"""

    def __init__(self):
        self.graph = get_graph()
        self.embedding_manager = EmbeddingManager()
        self.llm = LLMConfig.classification_llm()

    def index_project(self, project_path: str) -> int:
        """
        Indexa um diretório de projeto completo

        Args:
            project_path: Caminho do diretório do projeto

        Returns:
            Número de arquivos indexados
        """
        root = Path(project_path)
        if not root.exists():
            raise ValueError(f"Diretório não encontrado: {project_path}")

        project_name = root.name
        print(f"📁 Indexando projeto: {project_name}")

        # Criar nó do projeto
        self._create_project_node(project_name, str(root))

        # Indexar arquivos de documentação
        doc_extensions = ['.md', '.rst', '.README*', '.CHANGELOG*']
        doc_files = []

        for ext in doc_extensions:
            doc_files.extend(root.rglob(ext))

        for file_path in doc_files:
            if file_path.is_file():
                self._index_file(file_path, project_name)

        print(f"✅ Projeto {project_name} indexado com {len(doc_files)} arquivos")
        return len(doc_files)

    def _create_project_node(self, project_name: str, project_path: str):
        """Cria nó do projeto no grafo"""
        self.graph.query("""
        MERGE (p:Projeto {nome: $nome})
        ON CREATE SET p.data_criacao = datetime()
        SET p.path = $path
        """, {"nome": project_name, "path": project_path})

    def _index_file(self, file_path: Path, project_name: str):
        """
        Indexa um arquivo individual com extração de metadados

        Args:
            file_path: Caminho do arquivo
            project_name: Nome do projeto
        """
        content = read_file_content(file_path)
        if not content:
            return

        # Hash e metadados
        content_hash = generate_hash(content)
        last_modified = datetime.fromtimestamp(file_path.stat().st_mtime)

        # Gerar embedding
        embedding = self.embedding_manager.embed_text(content[:8000])

        # Extrair metadados com LLM
        metadata = self._extract_metadata(file_path, content)

        # Inserir arquivo no grafo
        self._create_file_node(
            file_path, project_name, content, embedding,
            content_hash, last_modified, metadata
        )

        # Adicionar relações do projeto
        self._create_project_relations(project_name, metadata)

        tema = metadata.get("tema")
        stacks = metadata.get("stacks", [])
        print(f"    ✅ {file_path.name} → Tema: {tema} | Stacks: {stacks}")

    def _extract_metadata(self, file_path: Path, content: str) -> Dict[str, Any]:
        """Extrai metadados do arquivo usando LLM"""
        prompt = ChatPromptTemplate.from_messages([
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

        chain = prompt | self.llm

        try:
            result = chain.invoke({
                "nome": file_path.name,
                "path": str(file_path),
                "conteudo": content[:4000]
            })
            return json.loads(result.content)
        except:
            return {
                "projeto_nome": file_path.parent.name,
                "tema": None,
                "stacks": [],
                "versao": None,
                "componentes": [],
                "status": None
            }

    def _create_file_node(self, file_path: Path, project_name: str,
                         content: str, embedding: list, content_hash: str,
                         last_modified: datetime, metadata: Dict[str, Any]):
        """Cria nó do arquivo no grafo"""
        self.graph.query("""
        MATCH (p:Projeto {nome: $projeto_nome})

        MERGE (a:Arquivo {path: $path})
        SET a.nome = $nome,
            a.conteudo = $conteudo,
            a.embedding = $embedding,
            a.hash_conteudo = $hash,
            a.ultima_modificacao = $modificacao,
            a.tamanho = $tamanho,
            a.status = 'atual'

        MERGE (p)-[:CONTEM]->(a)
        """, {
            "projeto_nome": project_name,
            "path": str(file_path),
            "nome": file_path.name,
            "conteudo": content[:10000],
            "embedding": embedding,
            "hash": content_hash,
            "modificacao": last_modified.isoformat(),
            "tamanho": len(content)
        })

    def _create_project_relations(self, project_name: str, metadata: Dict[str, Any]):
        """Cria relações do projeto com tema, stacks, etc"""
        # Tema
        if metadata.get("tema"):
            self.graph.query("""
            MATCH (p:Projeto {nome: $projeto_nome})
            MERGE (t:Tema {nome: $tema})
            MERGE (p)-[:TEM_TEMA]->(t)
            """, {"projeto_nome": project_name, "tema": metadata["tema"]})

        # Stacks
        for stack in metadata.get("stacks", []):
            self.graph.query("""
            MATCH (p:Projeto {nome: $projeto_nome})
            MERGE (s:Stack {nome: $stack})
            MERGE (p)-[:USA_STACK]->(s)
            """, {"projeto_nome": project_name, "stack": stack})

        # Versão
        if metadata.get("versao"):
            self.graph.query("""
            MATCH (p:Projeto {nome: $projeto_nome})
            MERGE (v:Versao {numero: $versao, projeto: $projeto_nome})
            SET v.data = datetime()
            MERGE (p)-[:TEM_VERSAO]->(v)
            """, {"projeto_nome": project_name, "versao": metadata["versao"]})
