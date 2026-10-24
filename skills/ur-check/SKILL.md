---
name: ur-check
description: >-
  Companion skill for Gesture 2 (Check). Performs rigorous automated validation of the 30 normative rules
  (Section 17 of socle-ur-spec v0.6), runs mechanical verbatim audits, checks evidence substance (findings, crossed quotes),
  and detects personal data or broken links.
---

# Skill: UR Check — Gesture 2 (Check & Validation)

This skill operationalizes the **Check** gesture (Section 20.2 of [socle-ur-spec v0.6](../../docs/spec/socle-ur-spec-v0.5.md)).
It allows researchers to audit proposed atoms side-by-side against their source documents, execute automated compliance checks across the 30 normative rules, and enforce repository integrity.

---

## When to Activate This Skill
- Right after ingesting or capturing new atoms via `ur-capture`.
- Before promoting any atom to `approved`.
- As a continuous pre-commit or pre-merge integrity audit.

---

## Step-by-Step Instructions for the Agent

### Step 1: Run Full Repository Validation
Execute the normative validation script:
```bash
python -m ur_tools.cli validate
```
Optionally test against higher maturity profiles:
```bash
python -m ur_tools.cli validate --profile standard
python -m ur_tools.cli validate --profile strict
```

### Step 2: Audit Results Against the 30 Rules (Section 17)
Analyze and guide the researcher to fix any detected errors or warnings:
1. **Rule 1 & 2 (Frontmatter & Controlled Vocabularies)**: Verify all mandatory keys, ensure `projects: [PRJ-...]` contains at least one non-empty project ID, and check valid types/statuses.
2. **Rule 3 & 4 (Identifiers & Slug filenames)**: Verify format `PREFIX-YYYY-NNN` and file naming `ID-slug.md`.
3. **Rule 5 & 6 (Link Integrity)**: Ensure every target atom ID exists and that body `[[ID]]` links are consistent with frontmatter relations.
4. **Rule 7 (Mandatory Body Sections)**: Ensure every evidence atom contains `## Résumé` (2–4 sentences), `## Constat & Limites`, `## Preuves` (or `## Contenu`), and `## Contexte de recueil`.
5. **Rule 8 (No Orphan Atoms)**: Ensure every atom has at least one incoming or outgoing typed link.
6. **Rule 11 (Zero PII)**: Fix any accidental email, phone number, or person's direct identity.
7. **Rule 16 (No Calculated Values)**: Ensure confidence bands, scores, and validation levels are never hand-typed in frontmatter.
8. **Rule 20 (Double Validation)**: Check that exceptions have both `requested_by` and `confirmed_by` from distinct human researchers.
9. **Rule 24 (Substantial Evidence & Verbatim Match)**:
   - `collected_at`: Must be an ISO 8601 date (`YYYY-MM-DD` or documented partial `YYYY-MM`/`YYYY`). **Strictly forbid `null`.**
   - Quotes match character-by-character in the source at the locator.
   - Evidence articulates an explicit finding supported by at least two corroborating quotes or observed facts (no bare quotes).
   - Rejection of opinions without observable facts.
10. **Rule 30 (Study Linkage)**: Ensure every evidence links to a parent study via `from_study: STU-YYYY-NNN`.

### Step 3: Run Mechanical Verbatim Check on Targeted Evidence
To verify a single evidence atom:
```bash
python -m ur_tools.cli check-verbatim --evidence knowledge/evidence/EVD-YYYY-NNN-<slug>.md
```
If verification fails, present the diff between the proposed quote and the source text to the researcher for correction.
