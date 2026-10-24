---
name: ur-link
description: >-
  Companion skill for Gesture 3 (Link). Manages typed relationships, computes method triangulation
  and ordinal confidence bands, detects contradictions, checks study linkage, and arbitrates context dimensions (Section 23).
---

# Skill: UR Link — Gesture 3 (Link & Triangulation)

This skill operationalizes the **Link** gesture (Section 20.2 of [socle-ur-spec v0.6](../../docs/spec/socle-ur-spec-v0.5.md)).
It connects evidence to higher-level objects (insights, jobs, personas, journeys), computes triangulation, and handles tensions or contradictions.

---

## Controlled Typed Relations (Section 13)

| Relation | From → To | Purpose |
| :--- | :--- | :--- |
| `based_on` | insight, recommendation → evidence | Factual support |
| `from_study` | evidence → study | Parent research study (Rule 30) |
| `concerns` | evidence → participant | Pseudonymised source participant |
| `illustrates` | evidence → journey node (`JRN-xxx#n-xxx`) | Concrete observation attached to a step |
| `performs` | participant → job | Role executed by participant |
| `derives_from` | persona → job | Persona rests on this job description |
| `represents` | participant → persona (`role: primary \| secondary`) | Archetypal representation |
| `covers` | study, insight → project, knowledge area (`area-*`) | Scope domain |
| `contradicts` | insight, evidence → insight, evidence | Open tension to arbitrate |

---

## Step-by-Step Instructions for the Agent

### Step 1: Synthesize Findings into Insights (`INS-YYYY-NNN`)
When multiple evidence pieces converge on a recurring finding:
1. Allocate an Insight ID:
   ```bash
   python -m ur_tools.cli allocate-id --prefix INS --title "<concise finding title>"
   ```
2. Create `/knowledge/insights/INS-YYYY-NNN-<slug>.md` with frontmatter linking the evidence:
   ```yaml
   links:
     based_on: [EVD-2026-001, EVD-2026-002, EVD-2026-003]
     covers: [area-core-tasks]
   ```
3. Structure the body with the 4 mandatory sections:
   - `## Constat (Finding)`: 2 to 4 sentences summarizing the observation.
   - `## Preuves (Evidence)`: Links and quotes from linked `EVD-` atoms.
   - `## Implications`: Impact on users, organization, or design.
   - `## Degré d'incertitude (Uncertainty)`: What remains unobserved or pending.

### Step 2: Triangulation and Confidence Band Computation
The skill computes the ordinal confidence band based on Section 11:
- **Faible (●○○)**: Single session, or inferred/documentary only.
- **Moyenne (●●○)**: At least 2 independent evidence from one family or axis.
- **Élevée (●●●)**: At least 3 independent evidence across 2 distinct method families (e.g., qualitative interview + quantitative survey) or 2 axes (attitudinal + behavioral), without unresolved contradictions.
- **Très élevée (●●●)**: Explicit versioned rule only (`schema/rules/RUL-*.yaml`).

### Step 3: Manage Contradictions & Context Dimensions (Section 23.4)
When two pieces of evidence or insights conflict:
1. Link them via `contradicts: [INS-YYYY-NNN]`.
2. Inspect their **Context** (`context: {dimension: value}`).
   - If an atom has missing context, explicitly note `[Contexte : non spécifié]`.
3. If contexts differ (e.g. `site: site-north` vs `site: site-south`), both findings are true within their respective scopes!
4. If contexts are identical or missing, the skill prompts the researcher:
   > *"Under what specific operating conditions was each observation made?"*
   If an unmodeled condition explains the variance, add a new dimension in `schema/context.yaml`.
