---
name: ur-ask
description: >-
  Companion skill for Gesture 5 (Ask). Answers research questions and brief inquiries,
  cites stable atom IDs with trust badges (●○○, ●●○, ●●●), consults the gap map,
  enforces explicit context mentions ([Contexte : non spécifié]), and recommends future studies.
---

# Skill: UR Ask — Gesture 5 (Ask & Gap Exploration)

This skill operationalizes the **Ask** gesture (Section 20.2 & 19 of [socle-ur-spec v0.6](../../docs/spec/socle-ur-spec-v0.5.md)).
It allows researchers and stakeholders to query the knowledge base, receive answers grounded in empirical evidence, and identify knowledge gaps.

---

## Output Rules for Responses
When answering a question:
1. **Always cite atom identifiers**: Refer explicitly to `[INS-YYYY-NNN]`, `[EVD-YYYY-NNN]`, or `[JOB-YYYY-NNN]`.
2. **State the trust badge**: Display the 3-notch badge (●○○, ●●○, ●●●) indicating the degree of corroboration:
   - ●○○ (*Indice / Faible*) : Hypothèse, source déclarative unique ou documentaire.
   - ●●○ (*Observé / Moyenne*) : Observé qualitativement ou corroboré sur un axe.
   - ●●● (*Corroboré / Élevée*) : Triangulé qualitativement et quantitativement sans contradiction.
3. **Respect context and scope (Section 23.3)**:
   - If an insight was observed on a specific site or app (e.g. `site: site-north`), state: *"Observé sur le site Nord, non vérifié ailleurs"*.
   - **Mandatory missing context mention**: If an evidence or insight has `context: null` or no context specified, the skill MUST explicitly append `[Contexte : non spécifié]`. It must never generalize silently as if valid everywhere.
4. **Be honest about gaps**: If the repository holds no evidence or only thin data, say so clearly and point to the gap map.

---

## Step-by-Step Instructions for the Agent

### Step 1: Interrogate the Knowledge Base
1. Search relevant insights, journeys, personas, and evidence matching the user's question or brief.
2. Group the findings by theme or knowledge area (`area-*`).
3. Synthesize the empirical answer using the trust badges and file links. Always include the context status (e.g. `[Contexte : non spécifié]` or `[Contexte : application cadre-v4]`).

### Step 2: Consult the Gap Map (`views/gap-map.md`)
1. Identify the knowledge areas (`schema/knowledge-areas.yaml`) touched by the inquiry.
2. Check the status of each area:
   - `⭕ Vide (empty)`: 0 evidence atoms. Complete blind spot.
   - `⚠️ Mince (thin)`: 1-2 evidence atoms or single session. Requires consolidation.
   - `⚠️ Obsolète (stale)`: Evidence older than method freshness threshold (e.g. > 90 days for telemetry).
   - `✅ Couvert`: Well triangulated.

### Step 3: Recommend Research Studies (`REC-YYYY-NNN`)
When the user asks how to address a knowledge gap:
1. **Rule-based recommendation (`provenance: rule`)**:
   - Check if an explicit rule in `schema/rules/RUL-*.yaml` applies (e.g., minimum sample size for discovery).
   - If a rule matches, recommend the study with **Confiance Très élevée (●●●)** citing the rule ID.
2. **Inferred recommendation (`provenance: inferred`)**:
   - Synthesize a research strategy based on existing evidence gaps.
   - Allocate an ID: `python -m ur_tools.cli allocate-id --prefix REC --title "<study title>"`.
   - Provide explicit justification, required method families, and sample criteria.
