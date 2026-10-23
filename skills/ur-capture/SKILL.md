---
name: ur-capture
description: >-
  Companion skill for Gesture 1 (Capture). Ingests raw qualitative or quantitative research material
  (interview notes, transcripts, observation logs, survey summaries).
  Creates clean SRC- sources, pseudonymised PAR- participants, and atomic EVD- evidence with strict locators.
---

# Skill: UR Capture — Gesture 1 (Capture)

This skill operationalizes the **Capture** gesture (Section 20.2 of [socle-ur-spec v0.5](../../docs/spec/socle-ur-spec-v0.5.md)).
The researcher hands over a source document, notes, or recording summary, and answers minimal context questions. The skill extracts and structures the atoms.

---

> [!IMPORTANT]
> **Normative Capture Rules:**
> 1. **Anonymisation by default (Rule 11)**: Never store real names, phone numbers, emails, or direct personal identifiers. Generate or link to a pseudonymised participant (`PAR-YYYY-NNN`).
> 2. **AI Authorship & Status**: All atoms created by this skill must carry `authored_by: ai` and `status: to_review`.
> 3. **Traceability (Rule 24)**: Every evidence atom (`EVD-YYYY-NNN`) must record `session_id`, `collected_at` (actual date of collection), `source` (`SRC-YYYY-NNN`), and a precise `locator` (page, paragraph, or timecode).
> 4. **Verbatim integrity**: Quotes must match character-by-character the text stored in the cleaned source (`SRC-YYYY-NNN`).

---

## Step-by-Step Instructions for the Agent

### Step 1: Ingest and Create the Source (`SRC-YYYY-NNN`)
1. Allocate an ID for the source:
   ```bash
   python -m ur_tools.cli allocate-id --prefix SRC --title "<source title>"
   ```
2. Create the file in `/sources/SRC-YYYY-NNN-<slug>.md`:
   - Specify `origin`: `internal` or `external` (if external, provide `origin_detail`).
   - Specify `rights`: `own`, `licensed`, `public`, or `unknown`.
   - Store the cleaned extracted text and the external pointer (URI and SHA-256 hash of original file).

### Step 2: Pseudonymise Participants (`PAR-YYYY-NNN`)
For each distinct individual interviewed or observed:
1. Check if an existing `PAR-` matches the profile, or allocate a new ID:
   ```bash
   python -m ur_tools.cli allocate-id --prefix PAR --title "<segment-pseudonym>"
   ```
2. Create the atom in `/knowledge/participants/PAR-YYYY-NNN-<slug>.md`.
3. Include usage context and segment, ensuring **zero personally identifying information (PII)**.

### Step 3: Extract Atomic Evidence (`EVD-YYYY-NNN`)
For each notable observation or verbatim quote:
1. Allocate an ID:
   ```bash
   python -m ur_tools.cli allocate-id --prefix EVD --title "<short verbatim summary>"
   ```
2. Create the file in `/knowledge/evidence/EVD-YYYY-NNN-<slug>.md` with frontmatter:
   ```yaml
   ---
   id: EVD-YYYY-NNN
   type: evidence
   title: "..."
   language: fr
   status: to_review
   created: YYYY-MM-DD
   updated: YYYY-MM-DD
   projects: [PRJ-YYYY-NNN]
   provenance: observed # or declared, documented
   authored_by: ai
   reviewed_by: null
   sensitive: false # true if health/disability or political/religious opinion
   source: SRC-YYYY-NNN
   locator: "p. 3, § 2" # or timecode "14:32"
   session_id: "SESS-01"
   collected_at: YYYY-MM-DD
   links:
     from_study: STU-YYYY-NNN
     concerns: PAR-YYYY-NNN
   ---
   ```
3. In the body, quote the exact verbatim text inside a blockquote (`> "..."`) or a `## Contenu` section.
4. Immediately verify mechanical verbatim compliance:
   ```bash
   python -m ur_tools.cli check-verbatim --evidence knowledge/evidence/EVD-YYYY-NNN-<slug>.md
   ```
