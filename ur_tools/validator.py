"""Normative 30-Rule Validator for UR Knowledge Repositories.
Implements Section 17 of socle-ur-spec v0.6.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Set

import yaml

from ur_tools.id_allocator import ID_PATTERN
from ur_tools.verbatim_checker import VerbatimChecker

EMAIL_PATTERN = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b")
PHONE_PATTERN = re.compile(r"\b(?:\+?\d{1,3}[-.\s]?)?(?:\(?\d{2,4}\)?[-.\s]?)?\d{2,4}[-.\s]?\d{2,4}[-.\s]?\d{2,4}\b")
PARTIAL_DATE_PATTERN = re.compile(r"^\d{4}(-\d{2}(-\d{2})?)?$")


@dataclass
class ValidationIssue:
    rule_number: int
    rule_name: str
    severity: str  # "ERROR" or "WARNING"
    file_path: Path
    atom_id: str | None
    message: str


@dataclass
class ValidationReport:
    profile: str
    errors: List[ValidationIssue] = field(default_factory=list)
    warnings: List[ValidationIssue] = field(default_factory=list)

    @property
    def is_valid(self) -> bool:
        return len(self.errors) == 0


class RepoValidator:
    def __init__(self, repo_root: Path | str | None = None) -> None:
        if repo_root is None:
            self.repo_root = Path.cwd()
        else:
            self.repo_root = Path(repo_root)

        self.profile = "starter"
        self.enabled_modules: Set[str] = set()
        self.vocabularies: Dict[str, Any] = {}
        self.knowledge_areas: Set[str] = set()
        self.approaches: List[Dict[str, Any]] = []
        self.verbatim_checker = VerbatimChecker(self.repo_root)

        self._load_schema()

    def _load_schema(self) -> None:
        """Load profile and vocabularies from schema/ directory."""
        profile_file = self.repo_root / "schema" / "profile.yaml"
        if profile_file.exists():
            try:
                data = yaml.safe_load(profile_file.read_text(encoding="utf-8")) or {}
                self.profile = data.get("profile", "starter")
                self.enabled_modules = set(data.get("enabled_modules", []))
            except Exception:
                pass

        vocab_file = self.repo_root / "schema" / "vocabularies.yaml"
        if vocab_file.exists():
            try:
                self.vocabularies = yaml.safe_load(vocab_file.read_text(encoding="utf-8")) or {}
            except Exception:
                pass

        areas_file = self.repo_root / "schema" / "knowledge-areas.yaml"
        if areas_file.exists():
            try:
                data = yaml.safe_load(areas_file.read_text(encoding="utf-8")) or {}
                self.knowledge_areas = {a["id"] for a in data.get("areas", []) if "id" in a}
            except Exception:
                pass

        approaches_file = self.repo_root / "schema" / "approaches.yaml"
        if approaches_file.exists():
            try:
                data = yaml.safe_load(approaches_file.read_text(encoding="utf-8")) or {}
                self.approaches = data.get("approaches", [])
            except Exception:
                pass

    def _parse_markdown(self, path: Path) -> tuple[Dict[str, Any], str]:
        """Extract YAML frontmatter and markdown body."""
        content = path.read_text(encoding="utf-8")
        if not content.startswith("---"):
            return {}, content
        parts = content.split("---", 2)
        if len(parts) < 3:
            return {}, content
        try:
            fm = yaml.safe_load(parts[1]) or {}
            return fm, parts[2]
        except Exception:
            return {}, parts[2]

    def validate_all(self) -> ValidationReport:
        report = ValidationReport(profile=self.profile)

        # Collect all atoms
        atom_files: List[Path] = []
        search_dirs = [
            self.repo_root / "knowledge",
            self.repo_root / "sources",
            self.repo_root / "guides",
        ]
        for sdir in search_dirs:
            if sdir.exists():
                atom_files.extend(sdir.rglob("*.md"))

        parsed_atoms: Dict[str, tuple[Path, Dict[str, Any], str]] = {}
        all_ids: Set[str] = set()
        id_to_paths: Dict[str, List[Path]] = {}

        # First pass: collect IDs and verify basic formation & file naming
        for file_path in atom_files:
            fm, body = self._parse_markdown(file_path)
            atom_id = fm.get("id")

            # Rule 3: Atom identifiers unique and well formed
            if not atom_id or not ID_PATTERN.match(str(atom_id)):
                report.errors.append(ValidationIssue(
                    rule_number=3,
                    rule_name="Identifier well-formed",
                    severity="ERROR",
                    file_path=file_path,
                    atom_id=str(atom_id) if atom_id else None,
                    message=f"Missing or malformed ID in frontmatter: '{atom_id}'. Must match PREFIX-YYYY-NNN."
                ))
            else:
                atom_id = str(atom_id)
                id_to_paths.setdefault(atom_id, []).append(file_path)
                all_ids.add(atom_id)
                parsed_atoms[atom_id] = (file_path, fm, body)

            # Rule 4: File name starts with identifier, followed by a slug
            if atom_id:
                stem = file_path.stem
                if not (stem == atom_id or stem.startswith(f"{atom_id}-")):
                    severity = "WARNING" if self.profile == "starter" else "ERROR"
                    getattr(report, f"{severity.lower()}s").append(ValidationIssue(
                        rule_number=4,
                        rule_name="File name formatting",
                        severity=severity,
                        file_path=file_path,
                        atom_id=atom_id,
                        message=f"File name '{file_path.name}' must start with ID '{atom_id}' followed by slug."
                    ))

        # Check for ID collisions (Rule 3)
        for aid, paths in id_to_paths.items():
            if len(paths) > 1:
                for p in paths:
                    report.errors.append(ValidationIssue(
                        rule_number=3,
                        rule_name="Identifier uniqueness",
                        severity="ERROR",
                        file_path=p,
                        atom_id=aid,
                        message=f"Duplicate identifier '{aid}' found in multiple files: {[str(x) for x in paths]}"
                    ))

        # Build link graph for Rule 8 (orphan check)
        outgoing_links: Dict[str, Set[str]] = {aid: set() for aid in parsed_atoms}
        incoming_links: Dict[str, Set[str]] = {aid: set() for aid in parsed_atoms}

        for aid, (file_path, fm, body) in parsed_atoms.items():
            links = fm.get("links", {}) or {}
            for rel, targets in links.items():
                if targets is None:
                    continue
                if isinstance(targets, list):
                    for t in targets:
                        tid = (t.get("target") if isinstance(t, dict) else str(t)).split("#")[0]
                        if tid:
                            outgoing_links[aid].add(tid)
                            incoming_links.setdefault(tid, set()).add(aid)
                elif isinstance(targets, str):
                    tid = targets.split("#")[0]
                    if tid:
                        outgoing_links[aid].add(tid)
                        incoming_links.setdefault(tid, set()).add(aid)
            if fm.get("source"):
                sid = str(fm.get("source"))
                outgoing_links[aid].add(sid)
                incoming_links.setdefault(sid, set()).add(aid)

        # Second pass: validate each atom against rules
        for aid, (file_path, fm, body) in parsed_atoms.items():
            self._validate_atom(aid, file_path, fm, body, all_ids, report, outgoing_links, incoming_links)

        # Rule 22: Registered approaches have glossary and guide
        for approach in self.approaches:
            gid = approach.get("glossary_id")
            gde = approach.get("guide_id")
            severity = "WARNING" if self.profile == "starter" else "ERROR"
            if gid and gid not in all_ids:
                getattr(report, f"{severity.lower()}s").append(ValidationIssue(
                    rule_number=22,
                    rule_name="Approach glossary exists",
                    severity=severity,
                    file_path=self.repo_root / "schema" / "approaches.yaml",
                    atom_id=gid,
                    message=f"Approach '{approach.get('id')}' references missing glossary atom '{gid}'"
                ))
            if gde and gde not in all_ids:
                getattr(report, f"{severity.lower()}s").append(ValidationIssue(
                    rule_number=22,
                    rule_name="Approach guide exists",
                    severity=severity,
                    file_path=self.repo_root / "schema" / "approaches.yaml",
                    atom_id=gde,
                    message=f"Approach '{approach.get('id')}' references missing guide '{gde}'"
                ))

        return report

    def _validate_atom(
        self,
        atom_id: str,
        path: Path,
        fm: Dict[str, Any],
        body: str,
        all_ids: Set[str],
        report: ValidationReport,
        outgoing_links: Dict[str, Set[str]],
        incoming_links: Dict[str, Set[str]],
    ) -> None:
        def issue(rule: int, name: str, msg: str, force_error: bool = False):
            if force_error or self.profile != "starter":
                report.errors.append(ValidationIssue(rule, name, "ERROR", path, atom_id, msg))
            else:
                report.warnings.append(ValidationIssue(rule, name, "WARNING", path, atom_id, msg))

        atom_type = fm.get("type")
        status = fm.get("status")
        authored_by = fm.get("authored_by")
        reviewed_by = fm.get("reviewed_by")

        # Rule 1: Required frontmatter fields
        required_common = ["id", "type", "title", "language", "status", "created", "updated", "authored_by", "sensitive"]
        for req in required_common:
            if req not in fm:
                issue(1, "Required frontmatter", f"Missing required frontmatter field '{req}'")

        # Rule 1 (projects): must be non-empty list of project identifiers
        if atom_type in ("evidence", "insight", "study", "job", "persona", "journey"):
            projs = fm.get("projects")
            if projs is None or not isinstance(projs, list) or len(projs) == 0 or not any(p for p in projs if p):
                issue(1, "Required frontmatter: projects", "Field 'projects' must be a non-empty list of project identifiers.")

        # Rule 2: Controlled vocabularies
        valid_statuses = self.vocabularies.get("statuses", ["draft", "to_review", "approved", "obsolete", "replaced"])
        if status and status not in valid_statuses:
            issue(2, "Controlled vocabulary: status", f"Invalid status '{status}'. Must be one of {valid_statuses}")

        valid_types = self.vocabularies.get("atom_types", {})
        if atom_type and atom_type not in valid_types:
            issue(2, "Controlled vocabulary: type", f"Invalid type '{atom_type}'")

        # Rule 5: Every link target exists (Strict check)
        links = fm.get("links", {}) or {}
        for rel, targets in links.items():
            if isinstance(targets, list):
                for target in targets:
                    tid = target.get("target") if isinstance(target, dict) else str(target)
                    base_tid = tid.split("#")[0]
                    if base_tid and base_tid not in all_ids:
                        report.errors.append(ValidationIssue(
                            rule_number=5,
                            rule_name="Link target exists",
                            severity="ERROR",
                            file_path=path,
                            atom_id=atom_id,
                            message=f"Broken link target: '{tid}' in relation '{rel}' does not exist."
                        ))

        # Rule 7: Required sections present for the type
        if atom_type == "evidence":
            has_resume = bool(re.search(r"^##\s*(Résumé|Resume)", body, re.MULTILINE | re.IGNORECASE))
            has_constat = bool(re.search(r"^##\s*Constat", body, re.MULTILINE | re.IGNORECASE))
            has_preuves = bool(re.search(r"^##\s*(Preuves|Contenu)", body, re.MULTILINE | re.IGNORECASE))
            has_contexte = bool(re.search(r"^##\s*Contexte\s+de\s+recueil", body, re.MULTILINE | re.IGNORECASE))

            missing_sections = []
            if not has_resume:
                missing_sections.append("Résumé")
            if not has_constat:
                missing_sections.append("Constat & Limites")
            if not has_preuves:
                missing_sections.append("Preuves ou Contenu")
            if not has_contexte:
                missing_sections.append("Contexte de recueil")

            if missing_sections:
                issue(7, "Required sections for evidence", f"Evidence atom missing required section(s): {', '.join(missing_sections)}")

        # Rule 8: No orphan atom (has neither incoming nor outgoing links)
        if atom_type not in ("source", "project"):
            total_links = len(outgoing_links.get(atom_id, set())) + len(incoming_links.get(atom_id, set()))
            if total_links == 0:
                issue(8, "No orphan atom", f"Atom '{atom_id}' is an orphan (has neither incoming nor outgoing links).")

        # Rule 11: No personal data pattern (Strict check)
        clean_body = re.sub(r"`[^`]*`", "", body)
        clean_body = re.sub(r"\[.*?\]\(.*?\)", "", clean_body)
        if EMAIL_PATTERN.search(clean_body):
            report.errors.append(ValidationIssue(
                rule_number=11,
                rule_name="Anonymisation (PII)",
                severity="ERROR",
                file_path=path,
                atom_id=atom_id,
                message="Personal data detected: found email address pattern in atom text."
            ))

        # Rule 16: No calculated field in frontmatter
        calculated_keys = {"validation_level", "confidence_band", "confidence_score", "score", "coverage_table"}
        for ck in calculated_keys:
            if ck in fm:
                issue(16, "Calculated fields in frontmatter", f"Calculated field '{ck}' must not be typed in frontmatter.")

        # Rule 20: Double validation of exceptions
        exc = fm.get("exception")
        if exc and isinstance(exc, dict):
            req_by = exc.get("requested_by")
            conf_by = exc.get("confirmed_by")
            if not req_by or not conf_by:
                issue(20, "Exception double validation", "Exception must have both 'requested_by' and 'confirmed_by'.")
            elif req_by == conf_by:
                issue(20, "Exception self-validation", f"Exception 'requested_by' and 'confirmed_by' cannot be identical ({req_by}).")
            elif req_by == "ai" or conf_by == "ai":
                issue(20, "AI in exception validation", "AI cannot be requested_by or confirmed_by for exceptions.")

        # Rule 24: Evidence requirements & Verbatim check
        if atom_type == "evidence":
            for req_evd in ["session_id", "collected_at", "source", "locator"]:
                if req_evd not in fm or fm[req_evd] is None:
                    issue(24, "Evidence frontmatter", f"Evidence atom missing or null required field '{req_evd}'")

            # Validate date format of collected_at (cannot be null)
            col_at = fm.get("collected_at")
            if col_at is not None:
                col_str = str(col_at).strip()
                if not PARTIAL_DATE_PATTERN.match(col_str):
                    issue(24, "Evidence collected_at format", f"Invalid format for 'collected_at': '{col_at}'. Must match YYYY-MM-DD, YYYY-MM, or YYYY.")

            # Verbatim check
            res = self.verbatim_checker.check(path)
            if not res.is_valid:
                issue(24, "Verbatim verification", res.message)

            # Check crossed verbatims / bare quote threshold:
            quotes = re.findall(r"^>\s*«?(.*?)»?$", body, re.MULTILINE)
            clean_quotes = [q.strip() for q in quotes if q.strip() and not q.strip().startswith("[!")]
            if len(clean_quotes) < 2 and not re.search(r"^##\s*Constat", body, re.MULTILINE | re.IGNORECASE):
                issue(24, "Evidence crossed verbatims", "Evidence must formulate an explicit finding supported by crossed quotes or facts (single bare quote without finding is rejected).")

            # Check provenance: respondent quotes must be declared
            prov = fm.get("provenance")
            if prov == "documented" and any(term in body for term in ["Commentaires des utilisateurs", "répondant", "repondant", "verbatim"]):
                issue(24, "Evidence provenance", "Verbatim statements from respondents/participants must carry 'provenance: declared', not 'documented'.")

        # Rule 25: Authored_by and Approved status
        if authored_by in ("ai", "mixed") and status == "approved" and not reviewed_by:
            issue(25, "AI review before approval", "Atom authored by AI/mixed cannot be 'approved' without a human 'reviewed_by'.", force_error=True)

        # Rule 27: Covers knowledge area target exists
        covers = links.get("covers", [])
        if isinstance(covers, list):
            for cov in covers:
                if str(cov).startswith("area-") and cov not in self.knowledge_areas:
                    issue(27, "Knowledge area exists", f"Covered area '{cov}' not found in schema/knowledge-areas.yaml")

        # Rule 28: Rule recommendation cites valid rule
        if atom_type == "recommendation" and fm.get("provenance") == "rule":
            rule_id = fm.get("rule_id") or fm.get("rule")
            if not rule_id or not (self.repo_root / "schema" / "rules" / f"{rule_id}.yaml").exists():
                issue(28, "Rule recommendation exists", f"Recommendation cites missing rule in schema/rules/: '{rule_id}'")

        # Rule 30: Evidence parent study link
        if atom_type == "evidence":
            from_stu = links.get("from_study")
            if not from_stu:
                issue(30, "Evidence study link", "Evidence atom must link to a parent study via 'links.from_study'.")
