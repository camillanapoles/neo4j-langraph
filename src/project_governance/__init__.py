"""Módulo de governança de projetos"""

from src.project_governance.indexer import ProjectIndexer
from src.project_governance.similarity import SimilarityEngine
from src.project_governance.versioning import VersionManager

__all__ = [
    "ProjectIndexer",
    "SimilarityEngine",
    "VersionManager",
]
