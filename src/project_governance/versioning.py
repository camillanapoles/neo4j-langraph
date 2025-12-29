"""Versionamento e detecção de mudanças em documentação"""

import json
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime

from src.config import get_graph
from src.shared.utils import generate_hash, read_file_content


class VersionManager:
    """Gerencia versionamento de documentação e detecção de mudanças"""

    def __init__(self):
        self.graph = get_graph()

    def detect_changes(self) -> List[Dict[str, Any]]:
        """
        Detecta mudanças na documentação comparando hashes

        Returns:
            Lista de mudanças detectadas
        """
        print("🔍 Detectando mudanças na documentação...")

        # Buscar todos os arquivos
        files = self.graph.query("""
        MATCH (a:Arquivo)
        RETURN a.path as path, a.hash_conteudo as hash_antigo
        """)

        changes = []
        for file_info in files:
            file_path = Path(file_info['path'])

            if not file_path.exists():
                print(f"  ⚠️ Arquivo removido: {file_path}")
                continue

            # Recalcular hash
            current_content = read_file_content(file_path)
            if not current_content:
                continue

            current_hash = generate_hash(current_content)

            if current_hash != file_info['hash_antigo']:
                print(f"  🔄 MUDANÇA DETECTADA: {file_path.name}")

                # Criar nova versão
                self._create_new_version(
                    file_path, file_info['path'],
                    current_content, current_hash, file_info.get('versao', 'unknown')
                )

                changes.append({
                    'path': str(file_path),
                    'nome': file_path.name,
                    'hash_antigo': file_info['hash_antigo'],
                    'hash_novo': current_hash
                })

        print(f"\n✅ {len(changes)} mudanças detectadas!")
        return changes

    def _create_new_version(self, file_path: Path, old_path: str,
                          new_content: str, new_hash: str, old_version: str):
        """Cria nova versão do arquivo"""
        timestamp = datetime.now().isoformat()

        self.graph.query("""
        MATCH (a_antigo:Arquivo {path: $path})

        CREATE (a_novo:Arquivo {
            path: $path,
            nome: $nome,
            conteudo: $conteudo,
            hash_conteudo: $hash_novo,
            versao: $timestamp,
            status: 'atual'
        })

        SET a_antigo.status = 'obsoleta',
            a_antigo.versao = $timestamp_old

        CREATE (a_novo)-[:VERSAO_ANTERIOR]->(a_antigo)

        WITH a_antigo, a_novo
        MATCH (p:Projeto)-[r:CONTEM]->(a_antigo)
        CREATE (p)-[:CONTEM]->(a_novo)
        """, {
            "path": str(file_path),
            "nome": file_path.name,
            "conteudo": new_content[:10000],
            "hash_novo": new_hash,
            "timestamp": timestamp,
            "timestamp_old": old_version
        })

    def find_outdated_docs(self) -> List[Dict[str, Any]]:
        """
        Encontra documentação desatualizada

        Returns:
            Lista de arquivos desatualizados
        """
        results = self.graph.query("""
        MATCH (a_atual:Arquivo {status: 'atual'})-[:VERSAO_ANTERIOR]->(a_antiga:Arquivo)
        RETURN a_atual.nome,
               a_atual.versao as versao_atual,
               a_antiga.versao as versao_antiga,
               a_atual.path
        ORDER BY a_atual.versao DESC
        """)

        return results

    def find_conflicting_docs(self) -> List[Dict[str, Any]]:
        """
        Encontra projetos com documentação conflitante

        Returns:
            Lista de conflitos
        """
        results = self.graph.query("""
        MATCH (p:Projeto)-[:CONTEM]->(a:Arquivo)
        WHERE a.nome CONTAINS 'README'
        WITH p, collect(a) as arquivos
        WHERE size(arquivos) > 1
          AND none(a IN arquivos WHERE a.status = 'atual')
        RETURN p.nome as projeto,
               [arq IN arquivos | arq.nome + ' (' + arq.ultima_modificacao + ')'] as arquivos_conflitantes
        """)

        return results

    def get_version_timeline(self, project_name: str) -> List[Dict[str, Any]]:
        """
        Retorna linha do tempo de versões de um projeto

        Args:
            project_name: Nome do projeto

        Returns:
            Timeline de versões
        """
        results = self.graph.query("""
        MATCH (p:Projeto {nome: $nome})-[:TEM_VERSAO]->(v:Versao)
        RETURN v.numero as versao,
               v.data as data
        ORDER BY v.data ASC
        """, {"nome": project_name})

        return results

    def get_latest_docs(self, project_name: str) -> List[Dict[str, Any]]:
        """
        Retorna documentação mais recente de um projeto

        Args:
            project_name: Nome do projeto

        Returns:
            Lista de arquivos atuais
        """
        results = self.graph.query("""
        MATCH (p:Projeto {nome: $nome})-[:CONTEM]->(a:Arquivo)
        WHERE a.status = 'atual'
        RETURN a.nome, a.versao, a.path
        ORDER BY a.ultima_modificacao DESC
        """, {"nome": project_name})

        return results

    def get_governance_report(self) -> Dict[str, Any]:
        """Retorna relatório completo de governança"""
        report = {}

        # Total de projetos
        report['total_projetos'] = self.graph.query("MATCH (p:Projeto) RETURN count(p) as total")[0]['total']

        # Documentação desatualizada por projeto
        report['desatualizados'] = self.graph.query("""
        MATCH (p:Projeto)-[:CONTEM]->(a:Arquivo)
        WHERE a.status = 'obsoleta'
        RETURN p.nome, count(a) as docs_antigas
        ORDER BY docs_antigas DESC
        """)

        # Conflitos detectados
        report['conflitos'] = self.find_conflicting_docs()

        # Versões recentes
        report['versoes_recentes'] = self.graph.query("""
        MATCH (p:Projeto)-[:TEM_VERSAO]->(v:Versao)
        RETURN p.nome as projeto, v.numero as versao, v.data as data
        ORDER BY v.data DESC
        LIMIT 10
        """)

        # Arquivos sem versão atual
        report['sem_versao_atual'] = self.graph.query("""
        MATCH (p:Projeto)-[:CONTEM]->(a:Arquivo)
        WHERE NOT (a)-[:VERSAO_ANTERIOR]-()
          AND a.status = 'atual'
        RETURN p.nome as projeto, a.nome as arquivo
        LIMIT 20
        """)

        return report
