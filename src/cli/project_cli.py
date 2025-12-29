"""Módulo CLI para governança de projetos"""

import argparse
import sys

from src.project_governance import ProjectIndexer, SimilarityEngine, VersionManager


def index_project_command(args):
    """Comando para indexar projeto"""
    print(f"📁 Indexando projeto: {args.path}\n")
    indexer = ProjectIndexer()
    count = indexer.index_project(args.path)
    print(f"\n✅ Projeto indexado com {count} arquivos")


def similarity_command(args):
    """Comando para calcular similaridades"""
    print(f"🔗 Calculando similaridades entre projetos...\n")
    engine = SimilarityEngine()
    engine.calculate_project_embeddings()
    count = engine.connect_similar_projects(threshold=args.threshold)
    print(f"\n✅ {count} conexões similares criadas")


def detect_changes_command(args):
    """Comando para detectar mudanças"""
    print(f"🔍 Detectando mudanças na documentação...\n")
    manager = VersionManager()
    changes = manager.detect_changes()
    print(f"\n✅ {len(changes)} mudanças detectadas")


def report_command(args):
    """Comando para gerar relatório de governança"""
    print(f"📊 RELATÓRIO DE GOVERNANÇA DE DOCUMENTAÇÃO")
    print("=" * 60)

    manager = VersionManager()
    engine = SimilarityEngine()
    report = manager.get_governance_report()
    overview = engine.get_dashboard_overview()

    print(f"\n📁 Total de Projetos: {report['total_projetos']}")

    print(f"\n🛠️ DISTRIBUIÇÃO POR STACK:")
    for s in overview['por_stack']:
        print(f"   - {s['stack']}: {s['qtd']} projetos")

    print(f"\n🏷️ DISTRIBUIÇÃO POR TEMA:")
    for t in overview['por_tema']:
        print(f"   - {t['tema']}: {t['qtd']} projetos")

    if report['desatualizados']:
        print(f"\n⚠️ ALERTAS:")
        for d in report['desatualizados']:
            print(f"   ⚠️ {d['p.nome']}: {d['docs_antigas']} documentos desatualizados")

    if report['conflitos']:
        print(f"\n🔗 CONFLITOS DE DOCUMENTAÇÃO:")
        for c in report['conflitos']:
            print(f"   ⚠️ {c['projeto']}:")
            for arq in c['arquivos_conflitantes']:
                print(f"      - {arq}")

    if overview['top_conexoes']:
        print(f"\n🔗 CLUSTERS DE PROJETOS SIMILARES:")
        for c in overview['top_conexoes']:
            print(f"   🔗 {c['projeto1']} ↔ {c['projeto2']} ({c['score']:.2f})")

    print(f"\n📋 VERSÕES RECENTES:")
    for v in report['versoes_recentes']:
        print(f"   • {v['projeto']} - v{v['versao']} [{v['data'][:10]}]")

    print("\n" + "=" * 60)


def dashboard_command(args):
    """Comando para mostrar dashboard de projetos"""
    print(f"📊 DASHBOARD DE PROJETOS")
    print("=" * 70)

    engine = SimilarityEngine()
    overview = engine.get_dashboard_overview()

    print(f"\n📁 Total: {overview['total']} projetos")

    print(f"\n🛠️ STACKS MAIS UTILIZADAS:")
    for s in overview['por_stack']:
        print(f"   {s['stack']:25s}: {s['qtd']:2d} projetos")

    print(f"\n🏷️ TEMAS MAIS COMUNS:")
    for t in overview['por_tema']:
        print(f"   {t['tema']:30s}: {t['qtd']:2d} projetos")

    print(f"\n🔗 TOP CONEXÕES:")
    for c in overview['top_conexoes']:
        print(f"   {c['projeto1']:30s} ↔ {c['projeto2']:30s} ({c['score']:.2f})")

    print("\n" + "=" * 70)


def main():
    parser = argparse.ArgumentParser(
        description="CLI para Governança de Documentação de Projetos"
    )
    subparsers = parser.add_subparsers(dest='command', help='Comandos disponíveis')

    # Subcomando: index
    index_parser = subparsers.add_parser('index', help='Indexar um projeto')
    index_parser.add_argument('path', help='Caminho do diretório do projeto')

    # Subcomando: similarity
    sim_parser = subparsers.add_parser('similarity', help='Calcular similaridades entre projetos')
    sim_parser.add_argument('--threshold', type=float, default=0.7,
                           help='Limiar de similaridade (padrão: 0.7)')

    # Subcomando: detect-changes
    subparsers.add_parser('detect-changes', help='Detectar mudanças na documentação')

    # Subcomando: report
    subparsers.add_parser('report', help='Gerar relatório de governança')

    # Subcomando: dashboard
    subparsers.add_parser('dashboard', help='Mostrar dashboard de projetos')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    commands = {
        'index': index_project_command,
        'similarity': similarity_command,
        'detect-changes': detect_changes_command,
        'report': report_command,
        'dashboard': dashboard_command,
    }

    commands[args.command](args)


if __name__ == '__main__':
    main()
