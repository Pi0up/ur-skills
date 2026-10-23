"""Repository skeleton initializer for UR Knowledge Bases.
Implements Section 2.2 of socle-ur-spec v0.5.
"""

from __future__ import annotations

from pathlib import Path


def init_repository(repo_root: Path | str | None = None) -> list[Path]:
    """Create the mandatory folder structure for a UR knowledge base."""
    root = Path(repo_root) if repo_root else Path.cwd()

    directories = [
        root / "sources",
        root / "knowledge" / "projects",
        root / "knowledge" / "studies",
        root / "knowledge" / "insights",
        root / "knowledge" / "evidence",
        root / "knowledge" / "participants",
        root / "knowledge" / "methods",
        root / "knowledge" / "jobs",
        root / "knowledge" / "personas",
        root / "knowledge" / "journeys",
        root / "knowledge" / "recommendations",
        root / "knowledge" / "decisions",
        root / "knowledge" / "glossary",
        root / "guides",
        root / "templates" / "proto",
        root / "templates" / "atoms",
        root / "schema" / "rules",
        root / "indexes",
        root / "views" / "journeys",
        root / "scripts",
    ]

    created = []
    for d in directories:
        d.mkdir(parents=True, exist_ok=True)
        gitkeep = d / ".gitkeep"
        if not any(d.iterdir()):
            gitkeep.touch()
            created.append(gitkeep)

    return created
