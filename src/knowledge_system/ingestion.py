"""Ingestão de conhecimento para o grafo"""

import json
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime

from langchain_core.prompts import ChatPromptTemplate

from src.config import get_graph
from src.shared.embeddings import EmbeddingManager
from src.shared.llm import LLMConfig
from src.shared.utils import generate_hash, read_file_content, is_text_file


class Ingestion:
    """Gerencia ingestão de arquivos e conhecimento no grafo"""

    def __init__(self):
        self.graph = get_graph()
        self.embedding_manager = EmbeddingManager()
        self.llm = LLMConfig.classification_llm()

    def ingest_directory(self, root_path: str) -> int:
        """
        Ingere todos os arquivos de texto de um diretório

        Args:
            root_path: Caminho do diretório raiz

        Returns:
            Número de itens ingeridos
        """
        root = Path(root_path)
        if not root.exists():
            raise ValueError(f"Diretório não encontrado: {root_path}")

        print(f"🧠 Ingerindo conhecimento de: {root_path}")
        print("=" * 60)

        # Encontrar todos os arquivos de texto
        all_files = []
        for file_path in root.rglob("*"):
            if file_path.is_file() and is_text_file(file_path):
                all_files.append(file_path)

        print(f"📁 Encontrados {len(all_files)} arquivos para processar\n")

        count = 0
        for idx, file_path in enumerate(all_files, 1):
            print(f"[{idx}/{len(all_files)}] Processando: {file_path.name}")
            if self._process_item(file_path):
                count += 1

        print(f"\n✅ {count} itens ingeridos no grafo!")
        return count

    def _process_item(self, file_path: Path) -> bool:
        """
        Processa um item individual

        Args:
            file_path: Caminho do arquivo

        Returns:
            True se processado com sucesso
        """
        content = read_file_content(file_path)
        if not content:
            return False

        # Metadados do arquivo
        stat = file_path.stat()
        content_hash = generate_hash(content)
        modified = datetime.fromtimestamp(stat.st_mtime)

        # Gerar embedding
        embedding = self.embedding_manager.embed_text(content)

        # Classificar com LLM
        classification = self._classify_item(file_path, content)

        # Criar nó universal (Item)
        item_id = content_hash[:16]
        self.graph.query("""
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
            "id": item_id,
            "nome": file_path.name,
            "path": str(file_path),
            "tipo": classification.get('tipo_primario', 'outro'),
            "subtipo": classification.get('subtipo'),
            "status": classification.get('status'),
            "maturidade": classification.get('maturidade'),
            "contexto": classification.get('contexto'),
            "conteudo": content[:15000],
            "embedding": embedding,
            "hash": content_hash,
            "tamanho": stat.st_size,
            "modificado": modified.isoformat()
        })

        # Criar relacionamentos
        self._create_relationships(item_id, classification)

        tipo = classification.get('tipo_primario', 'outro')
        topicos = classification.get('topicos', [])[:3]
        print(f"  📌 Tipo: {tipo} | Tópicos: {topicos}")
        print(f"  ✅ Item catalogado no grafo\n")

        return True

    def _classify_item(self, file_path: Path, content: str) -> Dict[str, Any]:
        """
        Classifica um item usando LLM

        Args:
            file_path: Caminho do arquivo
            content: Conteúdo do arquivo

        Returns:
            Dicionário com classificação
        """
        stat = file_path.stat()
        modified = datetime.fromtimestamp(stat.st_mtime)

        prompt = ChatPromptTemplate.from_messages([
            ("system", """Você é um classificador de conhecimento pessoal.

            Analise o conteúdo e retorne JSON:
            {{
              "tipo_primario": "projeto | nota | prompt | insight | anotacao | documentacao | ideia | tutorial | codigo | artigo | receita | outro",
              "subtipo": "descrição mais específica se aplicável",
              "topicos": ["listar tópicos principais"],
              "conceitos": ["conceitos técnicos ou abstratos mencionados"],
              "tecnologias": ["tecnologias mencionadas se aplicável"],
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

        chain = prompt | self.llm

        try:
            result = chain.invoke({
                "nome": file_path.name,
                "path": str(file_path),
                "tamanho": stat.st_size,
                "modificado": modified.strftime("%Y-%m-%d"),
                "conteudo": content[:6000]
            })
            return json.loads(result.content)
        except Exception as e:
            print(f"  ⚠️ Erro ao parsear classificação: {e}, usando padrão")
            return {
                "tipo_primario": "outro",
                "topicos": [],
                "tags": []
            }

    def _create_relationships(self, item_id: str, classification: Dict[str, Any]):
        """Cria relacionamentos do item com tópicos, conceitos, tecnologias e tags"""
        # Tópicos
        for topico in classification.get('topicos', []):
            if topico:
                self.graph.query("""
                MATCH (i:Item {id: $item_id})
                MERGE (t:Topico {nome: $topico})
                MERGE (i)-[:SOBRE]->(t)
                """, {"item_id": item_id, "topico": topico})

        # Conceitos
        for conceito in classification.get('conceitos', []):
            if conceito:
                self.graph.query("""
                MATCH (i:Item {id: $item_id})
                MERGE (c:Conceito {nome: $conceito})
                MERGE (i)-[:MENCIONA]->(c)
                """, {"item_id": item_id, "conceito": conceito})

        # Tecnologias
        for tech in classification.get('tecnologias', []):
            if tech:
                self.graph.query("""
                MATCH (i:Item {id: $item_id})
                MERGE (t:Tecnologia {nome: $tech})
                MERGE (i)-[:USA_TECNOLOGIA]->(t)
                """, {"item_id": item_id, "tech": tech})

        # Tags
        for tag in classification.get('tags', []):
            if tag:
                self.graph.query("""
                MATCH (i:Item {id: $item_id})
                MERGE (tg:Tag {nome: $tag})
                MERGE (i)-[:TAG]->(tg)
                """, {"item_id": item_id, "tag": tag})
