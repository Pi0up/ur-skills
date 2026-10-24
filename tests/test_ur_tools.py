"""Comprehensive test suite for UR Tools (socle-ur-spec v0.6)."""

import tempfile
import unittest
from pathlib import Path

from ur_tools.id_allocator import IdAllocator, slugify
from ur_tools.init_repo import init_repository
from ur_tools.triangulation import compute_confidence_band, compute_validation_level
from ur_tools.validator import RepoValidator
from ur_tools.verbatim_checker import VerbatimChecker
from ur_tools.views_generator import ViewsGenerator


class TestUrTools(unittest.TestCase):
    def test_slugify(self):
        self.assertEqual(slugify("Les techniciens ignorent les alertes"), "les-techniciens-ignorent-les-alertes")
        self.assertEqual(slugify("Check alerts & notifications!"), "check-alerts-notifications")

    def test_id_allocation(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            allocator = IdAllocator(tmp_path)

            atom_id, filename = allocator.allocate("INS", "Technicians skip alerts", year=2026)
            self.assertEqual(atom_id, "INS-2026-001")
            self.assertEqual(filename, "INS-2026-001-technicians-skip-alerts.md")

            # Simulate creating the file
            (tmp_path / "knowledge" / "insights").mkdir(parents=True)
            (tmp_path / "knowledge" / "insights" / filename).write_text("id: INS-2026-001\n", encoding="utf-8")

            # Next allocation
            next_id, next_file = allocator.allocate("INS", "Second finding", year=2026)
            self.assertEqual(next_id, "INS-2026-002")
            self.assertEqual(next_file, "INS-2026-002-second-finding.md")

    def test_verbatim_checker(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            sources_dir = tmp_path / "sources"
            evd_dir = tmp_path / "knowledge" / "evidence"
            sources_dir.mkdir(parents=True)
            evd_dir.mkdir(parents=True)

            # Create source
            src_file = sources_dir / "SRC-2026-001-interview-transcript.md"
            src_file.write_text(
                "---\nid: SRC-2026-001\ntype: source\n---\nLe technicien a précisé : « Quand l'alarme sonne, je clique sur ignorer car elle sonne pour rien. » Ensuite il a continué sa tournée.",
                encoding="utf-8"
            )

            # Create matching evidence
            evd_ok = evd_dir / "EVD-2026-001-skips-alarm.md"
            evd_ok.write_text(
                "---\nid: EVD-2026-001\ntype: evidence\nsource: SRC-2026-001\nlocator: 'p. 1'\nsession_id: 'SESS-01'\ncollected_at: 2026-10-23\n---\n## Contenu\n> « Quand l'alarme sonne, je clique sur ignorer car elle sonne pour rien. »",
                encoding="utf-8"
            )

            # Create mismatch evidence
            evd_fail = evd_dir / "EVD-2026-002-skips-alarm-altered.md"
            evd_fail.write_text(
                "---\nid: EVD-2026-002\ntype: evidence\nsource: SRC-2026-001\nlocator: 'p. 1'\nsession_id: 'SESS-01'\ncollected_at: 2026-10-23\n---\n## Contenu\n> « J'ignore toujours systématiquement toutes les alarmes sans exception. »",
                encoding="utf-8"
            )

            checker = VerbatimChecker(tmp_path)
            res_ok = checker.check(evd_ok)
            self.assertTrue(res_ok.is_valid)

            res_fail = checker.check(evd_fail)
            self.assertFalse(res_fail.is_valid)

    def test_triangulation_confidence(self):
        # Rule recommendation
        band, badge, label = compute_confidence_band("rule", [])
        self.assertEqual(band, "very_high")
        self.assertEqual(badge, "●●●")

        # Single session -> low
        evd_single = [{"id": "EVD-1", "session_id": "SESS-1", "method_family": "qualitative", "method_axis": "attitudinal", "provenance": "declared"}]
        band, badge, _ = compute_confidence_band("observed", evd_single)
        self.assertEqual(band, "low")
        self.assertEqual(badge, "●○○")

        # 2 sessions, 1 family -> medium
        evd_two = [
            {"id": "EVD-1", "session_id": "SESS-1", "method_family": "qualitative", "method_axis": "attitudinal", "provenance": "declared"},
            {"id": "EVD-2", "session_id": "SESS-2", "method_family": "qualitative", "method_axis": "attitudinal", "provenance": "declared"},
        ]
        band, badge, _ = compute_confidence_band("observed", evd_two)
        self.assertEqual(band, "medium")
        self.assertEqual(badge, "●●○")

        # 3 sessions, 2 families (qual + quant), no contradiction -> high
        evd_triangulated = [
            {"id": "EVD-1", "session_id": "SESS-1", "method_family": "qualitative", "method_axis": "behavioral", "provenance": "observed"},
            {"id": "EVD-2", "session_id": "SESS-2", "method_family": "qualitative", "method_axis": "attitudinal", "provenance": "declared"},
            {"id": "EVD-3", "session_id": "SESS-3", "method_family": "quantitative", "method_axis": "behavioral", "provenance": "documented"},
        ]
        band, badge, _ = compute_confidence_band("observed", evd_triangulated)
        self.assertEqual(band, "high")
        self.assertEqual(badge, "●●●")

    def test_compute_validation_level(self):
        # Inferred only
        lvl, badge, _ = compute_validation_level("inferred", [], [])
        self.assertEqual(lvl, "hypothesis")
        self.assertEqual(badge, "●○○")

        # Declared or 1 participant
        lvl, badge, _ = compute_validation_level("declared", ["PAR-001"], ["SESS-01"])
        self.assertEqual(lvl, "sensed")
        self.assertEqual(badge, "●○○")

        # >= 3 participants across >= 2 sessions
        lvl, badge, _ = compute_validation_level("observed", ["PAR-001", "PAR-002", "PAR-003"], ["SESS-01", "SESS-02"])
        self.assertEqual(lvl, "observed")
        self.assertEqual(badge, "●●○")

        # Corroborated with quant confirmation
        lvl, badge, _ = compute_validation_level("observed", ["PAR-001", "PAR-002", "PAR-003"], ["SESS-01", "SESS-02"], has_quant_confirmation=True)
        self.assertEqual(lvl, "quant_validated")
        self.assertEqual(badge, "●●●")

    def test_init_repository_and_views(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            init_repository(tmp_path)
            self.assertTrue((tmp_path / "knowledge" / "insights").exists())
            self.assertTrue((tmp_path / "sources").exists())

            views_gen = ViewsGenerator(tmp_path)
            res = views_gen.generate_all()
            self.assertTrue(res["gap_map"].exists())
            self.assertTrue(res["to_review"].exists())
            self.assertTrue(res["what_changed"].exists())

    def test_validator_rules_v06(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            init_repository(tmp_path)

            # Create test project and study
            (tmp_path / "knowledge" / "projects" / "PRJ-2026-001-core.md").write_text(
                "---\nid: PRJ-2026-001\ntype: project\ntitle: Core Project\nlanguage: fr\nstatus: approved\ncreated: 2026-01-01\nupdated: 2026-01-01\nauthored_by: human\nsensitive: false\n---\n## Context\nCore context.",
                encoding="utf-8"
            )
            (tmp_path / "knowledge" / "studies" / "STU-2026-001-survey.md").write_text(
                "---\nid: STU-2026-001\ntype: study\ntitle: Survey Study\nlanguage: fr\nstatus: approved\ncreated: 2026-01-01\nupdated: 2026-01-01\nprojects: [PRJ-2026-001]\nauthored_by: human\nsensitive: false\n---\n## Research question\nQuestion.",
                encoding="utf-8"
            )
            (tmp_path / "sources" / "SRC-2026-001-source.md").write_text(
                "---\nid: SRC-2026-001\ntype: source\ntitle: Test Source\nlanguage: fr\nstatus: approved\ncreated: 2026-01-01\nupdated: 2026-01-01\nauthored_by: human\nsensitive: false\n---\nAlpha verbatim text.\nBeta verbatim text.",
                encoding="utf-8"
            )

            # Non-compliant evidence (empty projects, null date, missing sections, bare quote, missing from_study)
            (tmp_path / "knowledge" / "evidence" / "EVD-2026-001-invalid.md").write_text(
                """---
id: EVD-2026-001
type: evidence
title: Bare quote
language: fr
status: to_review
created: 2026-10-23
updated: 2026-10-23
projects: []
provenance: documented
authored_by: ai
reviewed_by: null
sensitive: false
source: SRC-2026-001
locator: "p. 1"
session_id: "SESS-01"
collected_at: null
links:
  from_study: null
---
> « Alpha verbatim text. »
""",
                encoding="utf-8"
            )

            validator = RepoValidator(tmp_path)
            report = validator.validate_all()
            rules_flagged = {issue.rule_number for issue in report.warnings + report.errors if issue.atom_id == "EVD-2026-001"}
            self.assertIn(1, rules_flagged)   # Projects empty
            self.assertIn(7, rules_flagged)   # Missing sections
            self.assertIn(24, rules_flagged)  # collected_at null, bare quote, provenance
            self.assertIn(30, rules_flagged)  # from_study null


if __name__ == "__main__":
    unittest.main()
