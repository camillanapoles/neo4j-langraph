"""Funções utilitárias compartilhadas"""

import hashlib
from pathlib import Path
from typing import Optional


def generate_hash(content: str) -> str:
    """Gera hash SHA-256 de um conteúdo"""
    return hashlib.sha256(content.encode('utf-8')).hexdigest()


def read_file_content(file_path: Path, encoding: str = 'utf-8',
                     max_length: Optional[int] = None) -> Optional[str]:
    """
    Lê conteúdo de arquivo com tratamento de erros

    Args:
        file_path: Caminho do arquivo
        encoding: Codificação (padrão: utf-8)
        max_length: Tamanho máximo em caracteres (opcional)

    Returns:
        Conteúdo do arquivo ou None em caso de erro
    """
    try:
        content = file_path.read_text(encoding=encoding, errors='ignore')
        if max_length and len(content) > max_length:
            return content[:max_length]
        return content
    except Exception as e:
        print(f"⚠️ Erro ao ler {file_path}: {e}")
        return None


def is_text_file(file_path: Path) -> bool:
    """Verifica se arquivo é baseado em texto"""
    text_extensions = {
        '.md', '.txt', '.rst', '.py', '.js', '.ts', '.json', '.yaml', '.yml',
        '.html', '.css', '.sql', '.sh', '.bash', '.env', '.conf',
        '.log', '.csv', '.xml', '.toml', '.ini', '.dockerfile', '.gitignore'
    }
    return file_path.suffix.lower() in text_extensions


def format_timestamp(dt) -> str:
    """Formata timestamp para string ISO"""
    if hasattr(dt, 'isoformat'):
        return dt.isoformat()
    return str(dt)
