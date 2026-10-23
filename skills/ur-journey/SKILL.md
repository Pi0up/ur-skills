---
name: ur-journey
description: >-
  Companion skill for Journey modeling and maintenance. Manages observed, arborescent, single-file
  JRN- atoms, node trees (n-NNN), multidimensional layers (emotional, friction, tools, channels),
  shared sub-journeys, and Mermaid graph exports.
---

# Skill: UR Journey — Observed Journeys & Layers

This skill operationalizes the authoring, structuring, and maintenance of **Observed Journeys** (`JRN-YYYY-NNN`) according to Section 8 of [socle-ur-spec v0.5](../../docs/spec/socle-ur-spec-v0.5.md).

---

> [!IMPORTANT]
> **Cardinal Principle: Observed is not Designed (Section 9 & Rule 12)**
> A userflow or design prototype is an untested hypothesis. It **NEVER** enters the knowledge base as a Journey until its real use has been proven on the field (field observation, usability test, interview, or telemetry drop-off).
> A design file stays outside the repository or is cited only as a documentary source (`SRC-`).

---

## Journey Architecture: One File, Arborescent (Section 8.2)

Every journey lives in a single file containing its complete node tree and layer sections:

```
JRN-2026-001-technician-field-intervention.md
├── Frontmatter (id, type, scale, projects, links...)
├── Résumé & Périmètre
├── Arbre des nœuds
│   ├── ### n-001 · Prise de poste (kind: step, parent: root)
│   ├── ### n-002 · Consultation des alertes (kind: action, parent: n-001)
│   └── ### n-003 · Commande de pièce (kind: ref, target: JRN-2026-002)
└── Couches (Layers)
    ├── Couche émotionnelle (Emotional)
    ├── Couche des frictions (Friction)
    ├── Couche des outils (Tools)
    └── Couche des canaux (Channels)
```

---

## Step-by-Step Instructions for the Agent

### Step 1: Allocate and Scaffold a Journey Atom
1. Allocate an ID and create the file:
   ```bash
   python -m ur_tools.cli allocate-id --prefix JRN --title "<observed journey title>"
   ```
2. Use the proto template `/templates/proto/journey-skeleton.md`.
3. Set the appropriate `scale`:
   - `job`: Role-level journey covering an entire day or broad mission.
   - `journey`: Trajectory towards a specific user goal.
   - `use_case`: Precise situation within a journey (must link to parent via `part_of: [JRN-...]`).

### Step 2: Model Tree Nodes (`n-NNN`)
- Assign sequential node numbers `n-001`, `n-002`, `n-003`.
- **Node attributes**:
  - `kind`: `step`, `screen`, `action`, `wait`, `external` (interaction outside product), `ref` (reference to another shared journey).
  - `parent`: `root` or another node ID (`n-xxx`).
  - `actor`: who performs the action.
  - `state`: screen state or user situation.
  - `applies_to`: `[JOB-...]` or `[PER-...]` (default: all).
  - `disruption`: interruption or memory retention requirement.

### Step 3: Populate Separate Layers (Section 8.3)
Add entries referring to nodes by their ID without duplicating steps:
- **Couche émotionnelle** : Emotional state per node with provenance (`declared` or `inferred`).
- **Couche des frictions** : Points of pain, confusion, or blockages.
- **Couche des outils** : Physical or software tools used during the step.
- **Couche des canaux** : Phone, email, paper sheet, web portal, mobile app.
- Attach evidence quotes directly to nodes using relation `links: { illustrates: [JRN-2026-001#n-002] }` in `EVD-` atoms.

### Step 4: Generate Mermaid Visualisation
Generate the readable graph view:
```bash
python -m ur_tools.cli generate-views
```
The Mermaid diagram will be exported into `views/journeys/JRN-YYYY-NNN.mmd`.
