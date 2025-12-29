"""Módulo CLI para sistema de conhecimento pessoal"""

import argparse
import sys

from src.knowledge_system import Ingestion, RelationshipManager, QueryLibrary


def ingest_command(args):
    """Comando para ingerir conhecimento"""
    print(f"📥 Iniciando ingestão de: {args.path}\n")
    ingestion = Ingestion()
    count = ingestion.ingest_directory(args.path)
    print(f"\n✅ Processamento concluído: {count} itens ingeridos")


def relationships_command(args):
    """Comando para criar relacionamentos semânticos"""
    print(f"🔗 Criando relacionamentos semânticos...\n")
    manager = RelationshipManager()
    count = manager.create_semantic_relationships(threshold=args.threshold)
    print(f"\n✅ {count} relacionamentos criados")


def clusters_command(args):
    """Comando para detectar clusters"""
    print(f"🧩 Detectando clusters de conhecimento...\n")
    manager = RelationshipManager()

    clusters = manager.detect_clusters(min_connections=args.min_connections)
    evolutions = manager.detect_evolutions()

    print(f"\n✅ Análise concluída:")
    print(f"   - {len(clusters)} clusters detectados")
    print(f"   - {len(evolutions)} evoluções identificadas")


def dashboard_command(args):
    """Comando para mostrar dashboard"""
    print(f"📊 Dashboard de Conhecimento\n")
    print("=" * 70)

    queries = QueryLibrary()
    stats = queries.dashboard()

    print(f"\n📊 ESTASTÍSTICAS GERAIS:")
    print(f"   Total de itens: {stats['geral']['total_items']}")
    print(f"   Tipos diferentes: {stats['geral']['tipos_diferentes']}")
    print(f"   Volume: {stats['geral']['bytes_totais'] / 1024 / 1024:.2f} MB")

    print(f"\n📁 DISTRIBUIÇÃO POR TIPO:")
    for t in stats['tipos']:
        print(f"   {t['tipo']:20s}: {t['qtd']:4d} itens")

    print(f"\n🏷️ TÓPICOS MAIS FREQUENTES:")
    for t in stats['topicos']:
        print(f"   {t['topico']:30s}: {t['itens']:3d} itens")

    print(f"\n🛠️ TECNOLOGIAS:")
    for t in stats['tecnologias']:
        print(f"   {t['tech']:30s}: {t['itens']:3d} itens")

    print(f"\n📦 CLUSTERS DETECTADOS:")
    for c in stats['clusters']:
        print(f"   • {c['nome']}")
        print(f"     Tema: {c['tema']}")
        if c['oportunidade']:
            print(f"     💡 {c['oportunidade']}")

    print(f"\n🌱 EVOLUÇÕES RECENTES:")
    for e in stats['evolucoes']:
        print(f"   {e['de']} → {e['para']}")

    print(f"\n⚠️ ITENS DESCONECTADOS:")
    for o in stats['orfaos']:
        print(f"   • {o['nome']} ({o['tipo']})")

    print(f"\n⏰ ATIVIDADE RECENTE (últimos 7 dias):")
    for r in stats['recentes']:
        print(f"   • {r['nome']} ({r['tipo']}) - {r['quando'][:10]}")

    print("\n" + "=" * 70)


def query_command(args):
    """Comando para fazer uma pergunta"""
    print(f"❓ Pergunta: {args.query}\n")

    from src.knowledge_system import ConversationalInterface

    interface = ConversationalInterface()
    result = interface.ask(args.query, show_cypher=args.show_cypher)

    print(f"💬 {result['result']}\n")


def main():
    parser = argparse.ArgumentParser(
        description="CLI para Sistema de Conhecimento Pessoal"
    )
    subparsers = parser.add_subparsers(dest='command', help='Comandos disponíveis')

    # Subcomando: ingest
    ingest_parser = subparsers.add_parser('ingest', help='Ingerir conhecimento de um diretório')
    ingest_parser.add_argument('path', help='Caminho do diretório para ingerir')

    # Subcomando: relationships
    rel_parser = subparsers.add_parser('relationships', help='Criar relacionamentos semânticos')
    rel_parser.add_argument('--threshold', type=float, default=0.75,
                           help='Limiar de similaridade (padrão: 0.75)')

    # Subcomando: clusters
    cluster_parser = subparsers.add_parser('clusters', help='Detectar clusters de conhecimento')
    cluster_parser.add_argument('--min-connections', type=int, default=2,
                               help='Mínimo de conexões para cluster (padrão: 2)')

    # Subcomando: dashboard
    subparsers.add_parser('dashboard', help='Mostrar dashboard de conhecimento')

    # Subcomando: query
    query_parser = subparsers.add_parser('query', help='Fazer uma pergunta')
    query_parser.add_argument('query', help='Pergunta em linguagem natural')
    query_parser.add_argument('--show-cypher', action='store_true',
                            help='Mostrar query Cypher gerada')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    commands = {
        'ingest': ingest_command,
        'relationships': relationships_command,
        'clusters': clusters_command,
        'dashboard': dashboard_command,
        'query': query_command,
    }

    commands[args.command](args)


if __name__ == '__main__':
    main()
