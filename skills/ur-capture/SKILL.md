---
name: ur-capture
description: >-
  Companion skill for Gesture 1 (Capture). Ingests raw qualitative or quantitative research material
  (interview notes, transcripts, observation logs, survey summaries). Conducts interactive context inquiries,
  enforces value rejection thresholds, and produces substantial EVD- atoms with crossed verbatims and explicit findings.
---

# Skill: UR Capture — Gesture 1 (Capture & Ingestion)

This skill operationalizes the **Capture** gesture (Section 20.2 of [socle-ur-spec v0.6](../../docs/spec/socle-ur-spec-v0.5.md)).
The researcher hands over a source document, notes, or survey results. The skill asks clarifying context questions, eliminates naked opinions, and extracts grounded evidence atoms.

---

> [!IMPORTANT]
> **Normative Capture Rules (v0.6):**
> 1. **No bare quotes without finding, no finding without crossing**: A single isolated verbatim is too small to carry research value. Every evidence atom (`EVD-`) must formulate an explicit finding supported by at least two corroborating quotes or observed facts.
> 2. **Rejection threshold (no naked opinions)**: Subjective opinions or generic preferences lacking concrete observed facts or behavioral friction are strictly rejected at ingestion.
> 3. **Interactive context questions**: Before extracting atoms, the agent must ask:
>    - *What / Task context*: What user task or objective was being observed or questioned?
>    - *With whom / Sample*: Who was observed (segment, participant PAR, or survey sample size)?
>    - *When / Period*: Date of collection (`YYYY-MM-DD` or documented partial `YYYY-MM`). **The value `collected_at: null` is strictly forbidden.**
> 4. **Anonymisation by default (Rule 11)**: Never store real names, phone numbers, emails, or direct personal identifiers.
> 5. **Traceability & Study connection (Rule 24 & 30)**: Every evidence atom must specify `session_id`, `collected_at`, `source`, `locator`, and link to a parent study `from_study: STU-YYYY-NNN`.
> 6. **AI Authorship & Status**: All atoms created by this skill must carry `authored_by: ai` and `status: to_review`.
> 7. **Verbatim integrity**: Quotes must match character-by-character the text stored in the cleaned source (`SRC-YYYY-NNN`).

---

## Step-by-Step Instructions for the Agent

### Step 1: Interactive Context Inquiry & Ingest Source (`SRC-YYYY-NNN`)
1. Inquire with the researcher:
   - What was the specific task or user situation?
   - Who were the participants (individual interview or aggregated survey)?
   - When was the data collected (year, month)?
2. Allocate an ID for the source:
   ```bash
   python -m ur_tools.cli allocate-id --prefix SRC --title "<source title>"
   ```
3. Create the file in `/sources/SRC-YYYY-NNN-<slug>.md`:
   - Specify `origin`: `internal` or `external` (if external, provide `origin_detail`).
   - Specify `rights`: `own`, `licensed`, `public`, or `unknown`.
   - Store the cleaned extracted text and the external pointer (URI and SHA-256 hash).

### Step 2: Pseudonymise Participants (`PAR-YYYY-NNN`)
For individual interviews or observational sessions:
1. Allocate an ID:
   ```bash
   python -m ur_tools.cli allocate-id --prefix PAR --title "<segment-pseudonym>"
   ```
2. Create the atom in `/knowledge/participants/PAR-YYYY-NNN-<slug>.md`.
*(Note: If ingesting an aggregated or anonymous quantitative survey, participants are not individualized; record sample sizes directly in the evidence quant block).*

### Step 3: Extract Substantial Evidence (`EVD-YYYY-NNN`)
1. **Apply Value & Rejection Threshold**:
   - Filter out isolated phrases, compliments, or generic complaints without an observable behavior or factual friction.
   - Group 2 to 3 converging verbatims or observations from the same session/source that prove a single consistent finding.
2. Allocate an Evidence ID:
   ```bash
   python -m ur_tools.cli allocate-id --prefix EVD --title "<finding title>"
   ```
3. Create the file in `/knowledge/evidence/EVD-YYYY-NNN-<slug>.md` with mandatory frontmatter:
   ```yaml
   ---
   id: EVD-YYYY-NNN
   type: evidence
   title: "[Constat factuel synthétique de l'observation ou déclaration]"
   language: fr
   status: to_review
   created: YYYY-MM-DD
   updated: YYYY-MM-DD
   projects: [PRJ-YYYY-NNN]        # Obligatoire, au moins un projet
   provenance: declared            # declared pour les répondants/utilisateurs, observed pour le chercheur
   authored_by: ai
   reviewed_by: null
   sensitive: false
   source: SRC-YYYY-NNN
   locator: "p. 3, § 2"
   session_id: "SESS-01"
   collected_at: "YYYY-MM"         # ISO 8601 complet (YYYY-MM-DD) ou partiel (YYYY-MM). Interdit: null
   context: null                   # Dimensions ou null ("contexte non spécifié")
   quant:                          # Bloc optionnel si données quantitatives
     sample_size: null             # n : effectif analysé
     population: null              # N : population totale
     metric: null                  # Indicateur mesuré
     value: null                   # Valeur mesurée
   links:
     from_study: STU-YYYY-NNN      # Obligatoire : étude parente
     concerns: null                # PAR-YYYY-NNN si individuel, sinon null
   ---

   ## Résumé
   [Résumé obligatoire de deux à quatre phrases formulant le constat empirique et sa portée.]

   ## Constat & Limites
   - **Constat** : [Ce que les observations démontrent concrètement.]
   - **Représentativité & Limites** : [Échantillon associé, avis minoritaire vs récurrent, limites méthodologiques.]

   ## Preuves (Verbatims ou Mesures)
   > "[Première citation textuelle exacte mot à mot vérifiée dans SRC]" (locator 1)

   > "[Deuxième citation ou élément probant concordant croisé confirmant le constat]" (locator 2)

   ## Contexte de recueil
   - **Moment / Déclencheur** : [Phase de test, moment du protocole ou tâche observée.]
   - **Question ou Tâche posée** : [Tâche demandée ou question posée.]
   ```
4. Verify mechanical verbatim compliance immediately:
   ```bash
   python -m ur_tools.cli check-verbatim --evidence knowledge/evidence/EVD-YYYY-NNN-<slug>.md
   ```
