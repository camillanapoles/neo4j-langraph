"""Similaridade entre projetos"""

from typing import List, Dict, Any

from langchain_neo4j import Neo4jVector

from src.config import get_graph
from src.shared.embeddings import EmbeddingManager


class SimilarityEngine:
    """Gerencia similaridade entre projetos"""

    def __init__(self):
        self.graph = get_graph()
        self.embedding_manager = EmbeddingManager()

    def calculate_project_embeddings(self) -> int:
        """
        Calcula embeddings de descrição para cada projeto

        Returns:
            Número de projetos processados
        """
        print("🧮 Calculando embeddings de descrição para projetos...")

        # Obter projetos e agregar conteúdo
        projects = self.graph.query("""
        MATCH (p:Projeto)-[:CONTEM]->(a:Arquivo)
        WITH p, collect(a.conteudo)[0..3] as conteudos
        RETURN p.nome as nome,
               reduce(s = '', c IN conteudos | s + ' ' + c) as descricao_agregada
        """)

        count = 0
        for project in projects:
            if project['descricao_agregada']:
                emb = self.embedding_manager.embed_text(project['descricao_agregada'])
                self.graph.query("""
                MATCH (p:Projeto {nome: $nome})
                SET p.embedding_descricao = $embedding
                """, {"nome": project['nome'], "embedding": emb})
                count += 1

        print(f"✅ Embeddings calculados para {count} projetos!")
        return count

    def create_vector_index(self, index_name: str = "projetos_similares") -> None:
        """Cria índice vetorial para projetos"""
        self.graph.query(f"""
        CREATE VECTOR INDEX {index_name} IF NOT EXISTS
        FOR (p:Projeto)
        ON p.embedding_descricao
        OPTIONS {{indexConfig: {{
          `vector.dimensions`: 1536,
          `vector.similarity_function`: 'cosine'
        }}}}
        """)

    def connect_similar_projects(self, threshold: float = 0.7,
                                index_name: str = "projetos_similares") -> int:
        """
        Cria relacionamentos SIMILAR_A entre projetos similares

        Args:
            threshold: Limiar de similaridade
            index_name: Nome do índice vetorial

        Returns:
            Número de conexões criadas
        """
        print(f"🔗 Conectando projetos similares (threshold: {threshold})...")

        # Criar índice
        self.create_vector_index(index_name)

        # Configurar vector store
        vector_store = Neo4jVector.from_existing_index(
            embedding=self.embedding_manager.embedding_model,
            index_name=index_name,
            node_label="Projeto",
            embedding_node_property="embedding_descricao",
            text_node_property="nome",
            graph=self.graph
        )

        # Buscar todos os projetos
        projects = self.graph.query("MATCH (p:Projeto) RETURN p.nome as nome")

        count = 0
        for project in projects:
            # Buscar top 5 similares
            similares = vector_store.similarity_search_with_score(
                project['nome'],
                k=6
            )

            for doc, score in similares:
                if score > threshold and doc.metadata.get('nome') != project['nome']:
                    self.graph.query("""
                    MATCH (p1:Projeto {nome: $projeto1})
                    MATCH (p2:Projeto {nome: $projeto2})
                    MERGE (p1)-[r:SIMILAR_A]-(p2)
                    SET r.score = $score
                    """, {
                        "projeto1": project['nome'],
                        "projeto2": doc.metadata['nome'],
                        "score": float(score)
                    })
                    print(f"  🔗 {project['nome']} ↔ {doc.metadata['nome']} ({score:.2f})")
                    count += 1

        print(f"\n✅ {count} conexões similares criadas!")
        return count

    def find_similar_to(self, project_name: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Encontra projetos similares a um projeto específico

        Args:
            project_name: Nome do projeto base
            limit: Número máximo de resultados

        Returns:
            Lista de projetos similares
        """
        results = self.graph.query("""
        MATCH (p1:Projeto {nome: $nome})-[r:SIMILAR_A]-(p2:Projeto)
        RETURN p2.nome as projeto_similar,
               r.score as similaridade,
               [(p2)-[:USA_STACK]->(s) | s.nome] as stacks
        ORDER BY r.score DESC
        LIMIT $limit
        """, {"nome": project_name, "limit": limit})

        return results

    def group_by_theme(self, theme: str) -> List[Dict[str, Any]]:
        """
        Agrupa projetos por tema

        Args:
            theme: Tema para buscar

        Returns:
            Lista de projetos do tema
        """
        results = self.graph.query("""
        MATCH (p:Projeto)-[:TEM_TEMA]->(t:Tema)
        WHERE toLower(t.nome) CONTAINS toLower($theme)
        RETURN p.nome, p.path
        """, {"theme": theme})

        return results

    def group_by_stack(self, stack: str) -> List[Dict[str, Any]]:
        """
        Agrupa projetos por tecnologia

        Args:
            stack: Nome da tecnologia

        Returns:
            Lista de projetos com a stack
        """
        results = self.graph.query("""
        MATCH (p:Projeto)-[:USA_STACK]->(s:Stack)
        WHERE toLower(s.nome) = toLower($stack)
        RETURN p.nome,
               [(p)-[:TEM_TEMA]->(t) | t.nome][0] as tema
        ORDER BY tema
        """, {"stack": stack})

        return results

    def get_dashboard_overview(self) -> Dict[str, Any]:
        """Retorna visão geral dos projetos e similaridades"""
        overview = {}

        # Total de projetos
        overview['total'] = self.graph.query("MATCH (p:Projeto) RETURN count(p) as total")[0]['total']

        # Projetos por stack
        overview['por_stack'] = self.graph.query("""
        MATCH (p:Projeto)-[:USA_STACK]->(s:Stack)
        RETURN s.nome as stack, count(p) as qtd
        ORDER BY qtd DESC
        """)

        # Projetos por tema
        overview['por_tema'] = self.graph.query("""
        MATCH (p:Projeto)-[:TEM_TEMA]->(t:Tema)
        RETURN t.nome as tema, count(p) as qtd
        ORDER BY qtd DESC
        """)

        # Conexões mais fortes
        overview['top_conexoes'] = self.graph.query("""
        MATCH (p1:Projeto)-[r:SIMILAR_A]-(p2:Projeto)
        RETURN p1.nome as projeto1, p2.nome as projeto2, r.score as score
        ORDER BY score DESC
        LIMIT 10
        """)

        return overview
