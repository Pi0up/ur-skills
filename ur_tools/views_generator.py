"""Mandatory views generator for UR Knowledge Repositories.
Implements Section 20.4 of socle-ur-spec v0.5.
Generates: gap-map.md, to-review.md, what-changed.md, insight-sheet.md, journeys/*.mmd
"""

from __future__ import annotations

import datetime
import re
from pathlib import Path
from typing import Any, Dict, List

import yaml


class ViewsGenerator:
    def __init__(self, repo_root: Path | str | None = None) -> None:
        if repo_root is None:
            self.repo_root = Path.cwd()
        else:
            self.repo_root = Path(repo_root)

        self.views_dir = self.repo_root / "views"
        self.views_dir.mkdir(parents=True, exist_ok=True)

    def _parse_atoms(self) -> List[Dict[str, Any]]:
        atoms = []
        search_dirs = [self.repo_root / "knowledge", self.repo_root / "sources", self.repo_root / "guides"]
        for sdir in search_dirs:
            if not sdir.exists():
                continue
            for f in sdir.rglob("*.md"):
                content = f.read_text(encoding="utf-8")
                if content.startswith("---"):
                    parts = content.split("---", 2)
                    if len(parts) >= 3:
                        try:
                            fm = yaml.safe_load(parts[1]) or {}
                            fm["_file_path"] = f
                            fm["_body"] = parts[2]
                            atoms.append(fm)
                        except Exception:
                            pass
        return atoms

    def generate_all(self) -> Dict[str, Path]:
        atoms = self._parse_atoms()
        generated = {}
        generated["gap_map"] = self.generate_gap_map(atoms)
        generated["to_review"] = self.generate_to_review(atoms)
        generated["what_changed"] = self.generate_what_changed(atoms)
        generated["insight_sheet"] = self.generate_insight_sheet(atoms)
        generated["journeys"] = self.generate_journeys(atoms)
        return generated

    def generate_gap_map(self, atoms: List[Dict[str, Any]]) -> Path:
        out_path = self.views_dir / "gap-map.md"
        areas_file = self.repo_root / "schema" / "knowledge-areas.yaml"
        areas = []
        if areas_file.exists():
            try:
                data = yaml.safe_load(areas_file.read_text(encoding="utf-8")) or {}
                areas = data.get("areas", [])
            except Exception:
                pass

        lines = [
            "# Cartographie des connaissances et lacunes (Gap Map)",
            f"> Généré le {datetime.date.today().isoformat()} · Source de vérité : Markdown\n",
            "| Domaine de connaissance | Preuves rattachées | État de couverture | Statut |",
            "| :--- | :--- | :--- | :--- |",
        ]

        # Count evidence and insights per area
        area_coverage: Dict[str, int] = {}
        for a in atoms:
            covers = (a.get("links") or {}).get("covers", [])
            for c in covers:
                area_coverage[c] = area_coverage.get(c, 0) + 1

        for area in areas:
            aid = area.get("id")
            label = area.get("label", aid)
            count = area_coverage.get(aid, 0)
            if count == 0:
                status = "⭕ Vide (*empty*)"
                badge = "Aucune preuve"
            elif count < 3:
                status = "⚠️ Mince (*thin*)"
                badge = f"{count} atome(s)"
            else:
                status = "✅ Couvert"
                badge = f"{count} atomes (triangulés)"
            lines.append(f"| **{label}** (`{aid}`) | {badge} | {status} | Actif |")

        lines.append("\n---\n*Légende : Vide (0 preuve) · Mince (1 à 2 preuves ou 1 seule session) · Couvert (≥ 3 preuves triangulées)*\n")
        out_path.write_text("\n".join(lines), encoding="utf-8")
        return out_path

    def generate_to_review(self, atoms: List[Dict[str, Any]]) -> Path:
        out_path = self.views_dir / "to-review.md"
        lines = [
            "# Atomes et exceptions à réviser (To Review)",
            f"> Généré le {datetime.date.today().isoformat()}\n",
            "| Identifiant | Type | Titre | Auteur | Statut actuel | Action attendue |",
            "| :--- | :--- | :--- | :--- | :--- | :--- |",
        ]

        to_review_count = 0
        for a in atoms:
            status = a.get("status")
            authored_by = a.get("authored_by", "human")
            aid = a.get("id", "N/A")
            atype = a.get("type", "N/A")
            title = a.get("title", "Sans titre")

            if status == "to_review" or (authored_by in ("ai", "mixed") and not a.get("reviewed_by")):
                to_review_count += 1
                lines.append(f"| `{aid}` | {atype} | {title} | {authored_by} | `{status}` | Relecture humaine requise |")

        if to_review_count == 0:
            lines.append("| *Aucun atome en attente de révision* | - | - | - | - | - |")

        out_path.write_text("\n".join(lines), encoding="utf-8")
        return out_path

    def generate_what_changed(self, atoms: List[Dict[str, Any]]) -> Path:
        out_path = self.views_dir / "what-changed.md"
        lines = [
            "# Dernières évolutions de la base de connaissances (What Changed)",
            f"> Généré le {datetime.date.today().isoformat()}\n",
            "| Identifiant | Type | Titre | Mis à jour le | Auteur |",
            "| :--- | :--- | :--- | :--- | :--- |",
        ]

        sorted_atoms = sorted(atoms, key=lambda x: str(x.get("updated", "")), reverse=True)
        for a in sorted_atoms[:20]:
            lines.append(f"| `{a.get('id')}` | {a.get('type')} | {a.get('title')} | {a.get('updated')} | {a.get('authored_by')} |")

        out_path.write_text("\n".join(lines), encoding="utf-8")
        return out_path

    def generate_insight_sheet(self, atoms: List[Dict[str, Any]]) -> Path:
        out_path = self.views_dir / "insight-sheet.md"
        lines = [
            "# Synthèse des enseignements clés (Insight Sheet)",
            f"> Généré le {datetime.date.today().isoformat()}\n",
        ]

        insights = [a for a in atoms if a.get("type") == "insight"]
        if not insights:
            lines.append("*Aucun enseignement (INS) dans la base pour le moment.*")
        else:
            for ins in insights:
                aid = ins.get("id")
                title = ins.get("title")
                links = ins.get("links") or {}
                evd_links = links.get("based_on", [])
                lines.append(f"## {aid} · {title}")
                lines.append(f"- **Confiance** : ●●○ (Moyenne)")
                lines.append(f"- **Preuves à l'appui** : {', '.join(str(e) for e in evd_links) if evd_links else 'Aucune preuve liée'}")
                lines.append(f"- **Statut** : `{ins.get('status')}` | **Auteur** : `{ins.get('authored_by')}`")
                lines.append("\n---\n")

        out_path.write_text("\n".join(lines), encoding="utf-8")
        return out_path

    def generate_journeys(self, atoms: List[Dict[str, Any]]) -> Path:
        journeys_dir = self.views_dir / "journeys"
        journeys_dir.mkdir(parents=True, exist_ok=True)
        journeys = [a for a in atoms if a.get("type") == "journey"]

        for jrn in journeys:
            jid = jrn.get("id", "JRN")
            title = jrn.get("title", "Parcours")
            body = jrn.get("_body", "")
            mmd_path = journeys_dir / f"{jid}.mmd"

            mmd_lines = [
                "graph TD",
                f"  %% Journey {jid}: {title}",
            ]

            # Parse nodes: ### n-001 · Title and parent: n-xxx
            node_pattern = re.compile(r"###\s*(n-\d+)\s*[·-]\s*([^\n]+)", re.MULTILINE)
            nodes = node_pattern.findall(body)
            parent_pattern = re.compile(r"parent:\s*(n-\d+|root)", re.MULTILINE)

            # Split by node headings
            sections = re.split(r"(?=###\s*n-\d+)", body)
            for sec in sections:
                nm = re.search(r"###\s*(n-\d+)\s*[·-]\s*([^\n]+)", sec)
                if nm:
                    nid = nm.group(1)
                    nlabel = nm.group(2).strip().replace('"', "'")
                    pm = re.search(r"parent:\s*(n-\d+|root)", sec)
                    parent = pm.group(1) if pm else "root"
                    mmd_lines.append(f'  {nid}["{nid}: {nlabel}"]')
                    if parent != "root":
                        mmd_lines.append(f"  {parent} --> {nid}")

            mmd_path.write_text("\n".join(mmd_lines), encoding="utf-8")

        return journeys_dir
