"""Identifier allocator for UR knowledge repositories.
Format: PREFIX-YYYY-NNN (e.g. INS-2026-001)
Section 3 of socle-ur-spec v0.5.
"""

from __future__ import annotations

import datetime
import re
from pathlib import Path
from typing import Tuple

VALID_PREFIXES = {
    "PRJ", "STU", "INS", "EVD", "PAR", "MET",
    "JOB", "PER", "JRN", "REC", "DEC", "SRC", "GLO", "GDE"
}

ID_PATTERN = re.compile(r"^([A-Z]{3})-(\d{4})-(\d{3,})$")


def slugify(text: str) -> str:
    """Normalize text into a clean filename slug."""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_-]+", "-", text)
    return text.strip("-")


class IdAllocator:
    def __init__(self, repo_root: Path | str | None = None) -> None:
        if repo_root is None:
            self.repo_root = Path.cwd()
        else:
            self.repo_root = Path(repo_root)

    def scan_existing_ids(self) -> set[str]:
        """Scan all markdown files in repo to find existing atom IDs."""
        existing_ids = set()
        search_dirs = [
            self.repo_root / "knowledge",
            self.repo_root / "sources",
            self.repo_root / "guides",
        ]
        for base_dir in search_dirs:
            if not base_dir.exists():
                continue
            for file_path in base_dir.rglob("*.md"):
                # Check filename first
                parts = file_path.stem.split("-")
                if len(parts) >= 3:
                    candidate = f"{parts[0]}-{parts[1]}-{parts[2]}"
                    if ID_PATTERN.match(candidate):
                        existing_ids.add(candidate)

                # Also inspect frontmatter `id:`
                try:
                    content = file_path.read_text(encoding="utf-8")
                    for match in re.finditer(r"^id:\s*([A-Z]{3}-\d{4}-\d{3,})\b", content, re.MULTILINE):
                        existing_ids.add(match.group(1))
                except Exception:
                    pass

        return existing_ids

    def get_next_id(self, prefix: str, year: int | None = None) -> str:
        """Calculate next available sequential ID for given prefix and year."""
        prefix = prefix.upper().strip()
        if prefix not in VALID_PREFIXES:
            raise ValueError(f"Invalid prefix '{prefix}'. Must be one of {sorted(VALID_PREFIXES)}")

        if year is None:
            year = datetime.date.today().year

        existing_ids = self.scan_existing_ids()
        prefix_pattern = re.compile(rf"^{prefix}-{year}-(\d+)$")

        max_seq = 0
        for atom_id in existing_ids:
            m = prefix_pattern.match(atom_id)
            if m:
                seq = int(m.group(1))
                if seq > max_seq:
                    max_seq = seq

        next_seq = max_seq + 1
        return f"{prefix}-{year}-{next_seq:03d}"

    def allocate(self, prefix: str, title: str, year: int | None = None) -> Tuple[str, str]:
        """Allocate next ID and format canonical filename ID-slug.md."""
        atom_id = self.get_next_id(prefix, year)
        slug = slugify(title)
        filename = f"{atom_id}-{slug}.md" if slug else f"{atom_id}.md"
        return atom_id, filename
