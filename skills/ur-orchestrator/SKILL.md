---
name: ur-orchestrator
description: >-
  Master orchestrator for User Research (UR) knowledge repositories (socle-ur-spec v0.6).
  Pilots repository setup, validation profiles (starter, standard, strict), module activation,
  the weekly ritual of the steward, and health checks across the 5 researcher gestures.
---

# Skill: UR Orchestrator — Master Repository Orchestrator

This skill orchestrates the lifecycle and governance of the User Research (UR) knowledge repository according to [socle-ur-spec v0.6](../../docs/spec/socle-ur-spec-v0.5.md).

---

> [!IMPORTANT]
> **Deliverable Language Rule (Section 3 of AGENTS.md):**
> Repository structure, folder names, keys, and technical identifiers remain strictly in English (`PRJ-YYYY-NNN`, `status`, `authored_by`).
> However, **all deliverable textual content (titles, summaries, body sections, insights, notes) MUST be authored in the language of the user** (e.g., French if prompting in French).

---

## The 5 Gestes du Chercheur (Human Operating Model)

```
1. Capture        ==>  2. Check           ==>  3. Link            ==>  4. Approve         ==>  5. Ask
(skill: ur-capture)    (skill: ur-check)       (skill: ur-link)        (skill: ur-approve)     (skill: ur-ask)
(SRC, EVD, PAR)        (30 rules, verbatim)    (triangulation, context)(4 DoDs, double valid)  (Trust badges, gap map)
```

---

## Step-by-Step Instructions for the Agent

### Step 1: Repository Initialization & Health Check
When setting up a new repository or verifying an existing one:
1. Run initialization via CLI:
   ```bash
   python -m ur_tools.cli init
   ```
2. Verify that `schema/profile.yaml` matches the team maturity level:
   - `starter`: core only, warnings except for IDs, links, and anonymisation (PII). Single researcher approval.
   - `standard`: all enabled modules validated strictly; exceptions require double validation.
   - `strict`: blocking accessibility dimensions, exception expiration, and participant health data restrictions (DPO).

### Step 2: Steward Weekly Ritual (Section 20.5)
Guide the designated steward through the weekly 20-minute curation ritual:
1. Generate fresh views:
   ```bash
   python -m ur_tools.cli generate-views
   ```
2. Inspect `views/to-review.md`: identify atoms left in `to_review` or pending exceptions.
3. Inspect `views/gap-map.md`: identify empty (`⭕`), thin (`⚠️`), or stale knowledge areas.
4. Check for open contradictions (`contradicts`) requiring context arbitration (`schema/context.yaml`).
5. Retire obsolete atoms by setting `status: obsolete` or creating replacement links (`replaces`).

### Step 3: Guiding the 5 Gestures
Direct the user to the appropriate companion skill based on their immediate intent:
- Handing over interview notes, recordings, or transcripts ➔ **`ur-capture`**
- Verifying verbatim quotes or linting the repository ➔ **`ur-check`**
- Connecting evidence to insights, jobs, or personas ➔ **`ur-link`**
- Validating an atom to `approved` status or handling exceptions ➔ **`ur-approve`**
- Querying knowledge or asking for study recommendations ➔ **`ur-ask`**
- Modeling or exploring complex arborescent user journeys ➔ **`ur-journey`**
