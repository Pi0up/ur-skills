"""Mechanical verbatim checker for Evidence atoms.
Verifies that quoted text appears verbatim at the locator in the source.
Section 17 rule 24 & Section 20.3 of socle-ur-spec v0.5.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import NamedTuple


class VerbatimCheckResult(NamedTuple):
    is_valid: bool
    evidence_id: str
    source_id: str
    locator: str
    message: str
    matched_snippet: str | None = None


def normalize_whitespace(text: str) -> str:
    """Normalize internal spacing for resilient verbatim comparison."""
    return re.sub(r"\s+", " ", text).strip()


class VerbatimChecker:
    def __init__(self, repo_root: Path | str | None = None) -> None:
        if repo_root is None:
            self.repo_root = Path.cwd()
        else:
            self.repo_root = Path(repo_root)

    def find_source_file(self, source_id: str) -> Path | None:
        """Find source markdown file in /sources/."""
        sources_dir = self.repo_root / "sources"
        if not sources_dir.exists():
            return None
        for p in sources_dir.glob(f"{source_id}*.md"):
            return p
        return None

    def extract_evidence_quote(self, content: str) -> str:
        """Extract quoted verbatim text from evidence atom markdown."""
        # Check blockquote: > "text" or > text
        blockquotes = re.findall(r"^>\s*[\"«]?(.*?)[\"»]?\s*$", content, re.MULTILINE)
        if blockquotes:
            return " ".join(blockquotes).strip()

        # Check section: ## Content or ## Contenu
        section_match = re.search(
            r"##\s*(?:Content|Contenu|Citation|Verbatim)\s*\n+(.*?)(?=\n##|\Z)",
            content,
            re.DOTALL | re.IGNORECASE,
        )
        if section_match:
            raw_text = section_match.group(1).strip()
            # Clean outer quotes if any
            clean_text = raw_text.strip('«»"\'\n ')
            return clean_text

        return ""

    def check(self, evidence_path: Path | str) -> VerbatimCheckResult:
        evd_file = Path(evidence_path)
        if not evd_file.exists():
            return VerbatimCheckResult(
                is_valid=False,
                evidence_id=evd_file.stem,
                source_id="",
                locator="",
                message=f"Evidence file not found: {evd_file}",
            )

        content = evd_file.read_text(encoding="utf-8")

        # Parse basic frontmatter values
        evd_id_m = re.search(r"^id:\s*([A-Z]{3}-\d{4}-\d{3,})\b", content, re.MULTILINE)
        evd_id = evd_id_m.group(1) if evd_id_m else evd_file.stem

        src_id_m = re.search(r"^source:\s*([A-Z]{3}-\d{4}-\d{3,})\b", content, re.MULTILINE)
        if not src_id_m:
            # Check links: source_of or based_on
            src_id_m = re.search(r"source:\s*([A-Z]{3}-\d{4}-\d{3,})", content)

        source_id = src_id_m.group(1) if src_id_m else ""
        locator_m = re.search(r"^locator:\s*[\"']?(.*?)[\"']?\s*$", content, re.MULTILINE)
        locator = locator_m.group(1).strip() if locator_m else ""

        if not source_id:
            return VerbatimCheckResult(
                is_valid=False,
                evidence_id=evd_id,
                source_id="",
                locator=locator,
                message="Missing required 'source' (SRC-*) in Evidence frontmatter.",
            )

        source_file = self.find_source_file(source_id)
        if not source_file:
            return VerbatimCheckResult(
                is_valid=False,
                evidence_id=evd_id,
                source_id=source_id,
                locator=locator,
                message=f"Referenced source file for '{source_id}' was not found in /sources/.",
            )

        source_content = source_file.read_text(encoding="utf-8")
        quote = self.extract_evidence_quote(content)

        if not quote:
            return VerbatimCheckResult(
                is_valid=False,
                evidence_id=evd_id,
                source_id=source_id,
                locator=locator,
                message="No quote or observation text found in Evidence body (must contain blockquote or ## Content).",
            )

        norm_quote = normalize_whitespace(quote)
        norm_source = normalize_whitespace(source_content)

        if norm_quote in norm_source:
            return VerbatimCheckResult(
                is_valid=True,
                evidence_id=evd_id,
                source_id=source_id,
                locator=locator,
                message="Mechanical verbatim verification succeeded: quote matched in source text.",
                matched_snippet=norm_quote[:80] + ("..." if len(norm_quote) > 80 else ""),
            )
        else:
            return VerbatimCheckResult(
                is_valid=False,
                evidence_id=evd_id,
                source_id=source_id,
                locator=locator,
                message="Mechanical verbatim verification failed: quoted text was not found verbatim in source.",
            )
