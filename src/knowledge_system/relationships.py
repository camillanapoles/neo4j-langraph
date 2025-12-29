"""Criação de relacionamentos semânticos no grafo"""

from typing import List, Dict, Any

from langchain_neo4j import Neo4jVector

from src.config import get_graph
from src.shared.embeddings import EmbeddingManager


class RelationshipManager:
    """Gerencia criação de relacionamentos semânticos entre itens"""

    def __init__(self):
        self.graph = get_graph()
        self.embedding_manager = EmbeddingManager()

    def create_vector_index(self, index_name: str = "itens_similares") -> None:
        """Cria índice vetorial para busca de similaridade"""
        self.graph.query(f"""
        CREATE VECTOR INDEX {index_name} IF NOT EXISTS
        FOR (i:Item)
        ON i.embedding
        OPTIONS {{indexConfig: {{
          `vector.dimensions`: 1536,
          `vector.similarity_function`: 'cosine'
        }}}}
        """)

    def create_semantic_relationships(self, threshold: float = 0.75,
                                      index_name: str = "itens_similares") -> int:
        """
        Cria relacionamentos RELACIONADO_A baseado em similaridade semântica

        Args:
            threshold: Limiar de similaridade (0-1)
            index_name: Nome do índice vetorial

        Returns:
            Número de relacionamentos criados
        """
        print(f"🔗 Descobrindo relacionamentos semânticos (threshold: {threshold})...")

        # Criar índice se não existe
        self.create_vector_index(index_name)

        # Configurar vector store
        vector_store = Neo4jVector.from_existing_index(
            embedding=self.embedding_manager.embedding_model,
            index_name=index_name,
            node_label="Item",
            embedding_node_property="embedding",
            text_node_property="contexto",
            graph=self.graph
        )

        # Buscar todos os itens
        items = self.graph.query("MATCH (i:Item) RETURN i.id as id, i.nome as nome, i.tipo as tipo")

        count = 0
        for item in items:
            # Buscar top 10 similares
            search_text = f"{item['nome']} {item.get('tipo', '')}"
            similares = vector_store.similarity_search_with_score(search_text, k=11)

            for doc, score in similares:
                if score > threshold and doc.metadata.get('id') != item['id']:
                    # Criar relacionamento
                    self.graph.query("""
                    MATCH (i1:Item {id: $id1})
                    MATCH (i2:Item {id: $id2})
                    MERGE (i1)-[r:RELACIONADO_A]-(i2)
                    SET r.score = $score,
                        r.descoberto_em = datetime()
                    """, {
                        "id1": item['id'],
                        "id2": doc.metadata.get('id'),
                        "score": float(score)
                    })
                    print(f"  🔗 {item['nome']} ↔ {doc.metadata.get('nome')} ({score:.3f})")
                    count += 1

        print(f"\n✅ {count} relacionamentos semânticos criados!")
        return count

    def detect_clusters(self, min_connections: int = 2) -> List[Dict[str, Any]]:
        """
        Detecta clusters de conhecimento fortemente conectado

        Args:
            min_connections: Número mínimo de conexões para formar cluster

        Returns:
            Lista de clusters detectados
        """
        print(f"🧩 Detectando clusters de conhecimento (mínimo {min_connections} conexões)...\n")

        clusters = self.graph.query(f"""
        MATCH (i1:Item)-[r:RELACIONADO_A]-(i2:Item)
        WHERE r.score > 0.8
        WITH i1, collect(DISTINCT i2) as relacionados
        WHERE size(relacionados) >= {min_connections}
        RETURN i1.nome as item_central,
               i1.tipo as tipo,
               i1.contexto as contexto,
               [r IN relacionados | r.nome + ' (' + r.tipo + ')'] as itens_relacionados
        LIMIT 20
        """)

        print(f"📦 Encontrados {len(clusters)} clusters potenciais:")
        for idx, cluster in enumerate(clusters, 1):
            print(f"\n  {idx}. {cluster['item_central']} ({cluster['tipo']})")
            print(f"     Contexto: {cluster['contexto'][:80]}...")
            print(f"     Conectado a {len(cluster['itens_relacionados'])} itens")

        return clusters

    def detect_evolutions(self) -> List[Dict[str, Any]]:
        """
        Detecta quando ideias/notas evoluíram para projetos

        Returns:
            Lista de evoluções detectadas
        """
        print("⏳ Rastreando evolução de conhecimento...\n")

        evolutions = self.graph.query("""
        MATCH (i1:Item)-[r:RELACIONADO_A]-(i2:Item)
        WHERE r.score > 0.85
          AND i1.tipo <> i2.tipo
          AND (
            (i1.tipo IN ['ideia', 'nota'] AND i2.tipo IN ['projeto', 'codigo'])
            OR
            (i1.tipo IN ['prompt'] AND i2.tipo IN ['projeto', 'codigo'])
          )
          AND i1.modificado < i2.modificado
        RETURN i1.nome as origem,
               i1.tipo as tipo_origem,
               i1.modificado as data_origem,
               i2.nome as destino,
               i2.tipo as tipo_destino,
               i2.modificado as data_destino,
               r.score as similaridade
        ORDER BY data_destino DESC
        """)

        count = 0
        for evo in evolutions:
            count += 1
            print(f"🌱 EVOLUÇÃO {count}:")
            print(f"   {evo['origem']} ({evo['tipo_origem']}) [{evo['data_origem'][:10]}]")
            print(f"   ↓")
            print(f"   {evo['destino']} ({evo['tipo_destino']}) [{evo['data_destino'][:10]}]")
            print(f"   Similaridade: {evo['similaridade']:.2f}\n")

            # Criar relacionamento de evolução
            self.graph.query("""
            MATCH (i1:Item {nome: $origem})
            MATCH (i2:Item {nome: $destino})
            MERGE (i1)-[e:EVOLUIU_PARA]->(i2)
            SET e.score = $score,
                e.detectado_em = datetime()
            """, {
                "origem": evo['origem'],
                "destino": evo['destino'],
                "score": float(evo['similaridade'])
            })

        print(f"✅ {count} evoluções detectadas e registradas!")
        return evolutions
