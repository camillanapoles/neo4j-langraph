"""Interface conversacional para consultas ao grafo de conhecimento"""

from typing import Dict, Any, List, Optional

from langchain_neo4j import GraphCypherQAChain

from src.config import get_graph
from src.shared.llm import LLMConfig


class ConversationalInterface:
    """Interface para consultas conversacionais ao grafo de conhecimento"""

    def __init__(self, return_intermediate_steps: bool = True):
        self.graph = get_graph()
        self.chain = GraphCypherQAChain.from_llm(
            llm=LLMConfig.query_llm(),
            graph=self.graph,
            allow_dangerous_requests=True,
            return_intermediate_steps=return_intermediate_steps,
            verbose=False
        )

    def ask(self, query: str, show_cypher: bool = False) -> Dict[str, Any]:
        """
        Faz uma pergunta ao sistema

        Args:
            query: Pergunta em linguagem natural
            show_cypher: Se True, mostra a query Cypher gerada

        Returns:
            Dicionário com resultado e passos intermediários
        """
        result = self.chain.invoke({"query": query})

        if show_cypher and result.get('intermediate_steps'):
            print(f"🔍 Cypher: {result['intermediate_steps'][0]['query']}")

        return result

    def batch_ask(self, questions: List[str]) -> List[Dict[str, Any]]:
        """
        Faz múltiplas perguntas em lote

        Args:
            questions: Lista de perguntas

        Returns:
            Lista de resultados
        """
        results = []
        for question in questions:
            print(f"\n❓ {question}")
            print("=" * 60)
            result = self.ask(question)
            print(f"💬 {result['result']}")
            results.append(result)

        return results


class QueryLibrary:
    """Biblioteca de queries predefinidas para o sistema de conhecimento"""

    def __init__(self):
        self.graph = get_graph()

    def show_all_about_topic(self, topic: str) -> List[Dict[str, Any]]:
        """Mostra todos os itens sobre um tópico específico"""
        results = self.graph.query("""
        MATCH (i:Item)-[:SOBRE|MENCIONA|TAG]-(n)
        WHERE toLower(n.nome) CONTAINS toLower($topic)
        RETURN i.nome as item,
               i.tipo as tipo,
               i.contexto as descricao,
               labels(n)[0] as encontrado_via
        ORDER BY i.modificado DESC
        """, {"topic": topic})

        return results

    def find_notes_for_projects(self) -> List[Dict[str, Any]]:
        """Encontra notas que podem virar projetos"""
        results = self.graph.query("""
        MATCH (n:Item {tipo: 'nota'})-[r:RELACIONADO_A]-(outros)
        WITH n, count(r) as conexoes
        WHERE conexoes >= 3
        RETURN n.nome as nota,
               n.contexto as sobre,
               conexoes as itens_relacionados
        ORDER BY conexoes DESC
        """)

        return results

    def find_conflicting_versions(self, days_threshold: int = 30) -> List[Dict[str, Any]]:
        """Encontra versões conflitantes do mesmo assunto"""
        results = self.graph.query("""
        MATCH (i1:Item)-[r:RELACIONADO_A]-(i2:Item)
        WHERE r.score > 0.9
          AND i1.id <> i2.id
          AND abs(duration.between(
                datetime(i1.modificado),
                datetime(i2.modificado)
              ).days) > $days
        RETURN i1.nome as versao_antiga,
               i1.modificado as data_antiga,
               i2.nome as versao_nova,
               i2.modificado as data_nova,
               r.score as similaridade
        ORDER BY data_nova DESC
        """, {"days": days_threshold})

        return results

    def prompts_in_projects(self) -> List[Dict[str, Any]]:
        """Encontra prompts usados em projetos"""
        results = self.graph.query("""
        MATCH (p:Item {tipo: 'prompt'})-[r:RELACIONADO_A]-(proj:Item {tipo: 'projeto'})
        RETURN p.nome as prompt,
               proj.nome as projeto,
               r.score as relevancia
        ORDER BY relevancia DESC
        """)

        return results

    def topic_map(self, topic: str, max_depth: int = 2) -> List[Dict[str, Any]]:
        """Mapa completo de um tópico"""
        results = self.graph.query(f"""
        MATCH caminho = (i:Item)-[:SOBRE|MENCIONA*1..{max_depth}]-(t:Topico)
        WHERE toLower(t.nome) CONTAINS toLower($topic)
        RETURN [n IN nodes(caminho) | n.nome] as caminho_nomes
        LIMIT 50
        """, {"topic": topic})

        return results

    def opportunity_clusters(self) -> List[Dict[str, Any]]:
        """Clusters com oportunidades de desenvolvimento"""
        results = self.graph.query("""
        MATCH (c:Cluster)
        WHERE c.oportunidade IS NOT NULL
        RETURN c.nome as cluster,
               c.tema as sobre,
               c.oportunidade as acao_sugerida,
               c.detectado_em as quando
        ORDER BY c.detectado_em DESC
        """)

        return results

    def knowledge_timeline(self) -> List[Dict[str, Any]]:
        """Linha do tempo do conhecimento"""
        results = self.graph.query("""
        MATCH (i:Item)
        RETURN i.tipo as tipo,
               count(i) as quantidade,
               min(datetime(i.modificado)) as primeiro,
               max(datetime(i.modificado)) as ultimo
        ORDER BY quantidade DESC
        """)

        return results

    def dashboard(self) -> Dict[str, Any]:
        """Dashboard completo do conhecimento"""
        stats = {}

        # Estatísticas gerais
        general = self.graph.query("""
        MATCH (i:Item)
        RETURN count(i) as total_items,
               count(DISTINCT i.tipo) as tipos_diferentes,
               sum(i.tamanho) as bytes_totais
        """)[0]
        stats['geral'] = general

        # Distribuição por tipo
        stats['tipos'] = self.graph.query("""
        MATCH (i:Item)
        RETURN i.tipo as tipo, count(*) as qtd
        ORDER BY qtd DESC
        """)

        # Tópicos mais frequentes
        stats['topicos'] = self.graph.query("""
        MATCH (t:Topico)<-[:SOBRE]-(i:Item)
        RETURN t.nome as topico, count(i) as itens
        ORDER BY itens DESC
        LIMIT 10
        """)

        # Tecnologias utilizadas
        stats['tecnologias'] = self.graph.query("""
        MATCH (t:Tecnologia)<-[:USA_TECNOLOGIA]-(i:Item)
        RETURN t.nome as tech, count(i) as itens
        ORDER BY itens DESC
        LIMIT 10
        """)

        # Clusters detectados
        stats['clusters'] = self.graph.query("""
        MATCH (c:Cluster)
        RETURN c.nome as nome, c.tema as tema, c.oportunidade as oportunidade
        ORDER BY c.detectado_em DESC
        LIMIT 5
        """)

        # Evoluções detectadas
        stats['evolucoes'] = self.graph.query("""
        MATCH (i1:Item)-[e:EVOLUIU_PARA]->(i2:Item)
        RETURN i1.nome as de, i2.nome as para
        ORDER BY e.detectado_em DESC
        LIMIT 5
        """)

        # Itens órfãos
        stats['orfaos'] = self.graph.query("""
        MATCH (i:Item)
        WHERE NOT (i)-[:RELACIONADO_A]-()
          AND NOT (i)-[:SOBRE]-()
          AND NOT (i)-[:MENCIONA]-()
        RETURN i.nome as nome, i.tipo as tipo
        LIMIT 10
        """)

        # Atividade recente
        stats['recentes'] = self.graph.query("""
        MATCH (i:Item)
        WHERE datetime(i.modificado) > datetime() - duration('P7D')
        RETURN i.nome as nome, i.tipo as tipo, i.modificado as quando
        ORDER BY i.modificado DESC
        LIMIT 10
        """)

        return stats
