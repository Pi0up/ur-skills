> **Document** : socle-ur-spec · **Version** : 0.5.0 · **Statut** : draft · **Sources** : chat · **Alias** : socle UR, schema-ur, spec socle, UR schema

# UR knowledge base — core specification v0.5

This specification fixes the conventions shared by every knowledge repository built for user researchers. It is the reference for the validation script, the skills, the researchers and the AI agents.

**Language rule.** The structure is in English: folder names, identifiers, frontmatter keys, types, statuses, relations, vocabularies, script messages. The content of atoms can be written in any language (`language` field). This document is written in French for review, but every identifier it defines is English.

Changes from v0.4:

- **Core, modules and three validation profiles** (section 2.1): a repository starts small and grows.
- **Human operating model** (section 20): roles, five gestures, mandatory views, definition of done, onboarding and adoption measures.
- **Human–AI traceability**: `authored_by` and `reviewed_by`; evidence carries `session_id`, `collected_at` and a `locator`, and quotes are checked against the source.
- **Coherence fixes**: `confidence` is computed, never entered; the level derives from conditions only; status `valid` becomes `approved`; `confirms` and `includes` become derived relations; rule numbering and the Must list are aligned.
- **Identifiers** are allocated by script, file names carry a slug, collisions are handled before merge.
- **Confidence** is read from an ordinal decision table and shown as a band, never as a number; triangulation adds the attitudinal / behavioral axis.
- **Accessibility**: `psychic` becomes `psychosocial`; declarations come from documentary sources by default, not from named participants; blocking `approved` applies in the `strict` profile only; a DPO question is opened.
- **Knowledge areas and gap map** (section 19) and a rules registry for `rule` recommendations.
- **Double validation** gets a fallback for small teams and excludes the AI.
- **Userflows leave the knowledge base.** A design is not knowledge until it has been used; it becomes a journey (JRN) only then, once its use has been proven through one of the channels of section 9.

## 1. Principles

- **Markdown is the source of truth.** Graphs, indexes, views and query tools are derived and rebuildable.
- **One atom = one object = one idea.** An atom must be understandable alone.
- **No duplication.** Each piece of information lives in one atom. Aggregates are views, never hand-written atoms.
- **Observed is not designed.** Evidence comes from observation or measurement. Designed artefacts (userflows, prototypes, design specs) are hypotheses: they never enter the knowledge base as evidence or as journeys until their use has been observed.
- **Calculated is never entered.** Validation levels, scores and views are computed by scripts and stored in `indexes/` or `views/`, never in the frontmatter.
- **Explicit beats implicit.** Every relation is declared in the frontmatter or in a node attribute.
- **Human- and AI-readable.** Short prose, explicit headings, controlled vocabularies, stable identifiers.
- **Anonymised by default.** No directly identifying personal data in the repository.
- **Exceptions need a second pair of eyes.** Forcing a rule is possible, but only with a double validation by another researcher. Permissions are the same for everyone.
- **Start small.** A repository uses the core and the modules it needs. Strictness grows with maturity, not on day one.
- **The human decides, the tool operates.** The researcher never types frontmatter or identifiers. The AI proposes; only a human approves.

## 2. Repository structure

### 2.1 Core, modules and profiles

The schema is large; a repository does not have to use all of it. It is split into a **core**, always active, and **modules**, enabled per repository in `schema/profile.yaml`.

| Part | Atoms and features |
| -------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Core** | PRJ, STU, PAR, EVD, INS, SRC, MET. Links: `based_on`, `from_study`, `produced`, `uses`, `concerns`, `covers`, `source_of`, `replaces`, `contradicts`. Confidence bands, knowledge areas, gap map. |
| Module *jobs-personas* | JOB, PER, participant links, validation level. |
| Module *journeys* | JRN, layers, shared journeys, emotional and friction layers. |
| Module *accessibility* | Coverage tables and declared situations (section 7.3). |
| Module *quant* | Quantitative family, `quant_validated` level, triangulation across families. |
| Module *recommendations* | REC, DEC, rules registry. |
| Module *knowledge* | GLO, GDE, approaches registry. |

**Profiles** set how strict the validation script is:

- `starter`: core only. Every rule is a warning except identifiers, links and anonymisation. One researcher can approve.
- `standard`: enabled modules are fully validated; errors block the commit; exceptions need the double validation.
- `strict`: `standard` plus open accessibility dimensions blocking `approved`, expiry of exceptions, and participant-linked declarations allowed only with DPO approval (section 7.3).

A repository starts in `starter`. Moving up a profile or enabling a module is a team decision, kept in the git history of `schema/profile.yaml`.

### 2.2 Folders

    /sources/              SRC- atoms: cleaned extracted text + pointer (URI, hash) to the original, kept outside the repo
    /knowledge/
      projects/            PRJ-  project context
      studies/             STU-  one study = one atom
      insights/            INS-  finding supported by evidence
      evidence/            EVD-  quotes, observations, data extracts
      participants/        PAR-  pseudonymised participants
      methods/             MET-  method atoms
      jobs/                JOB-  job descriptions in a context
      personas/            PER-  behavioural archetypes built from participants and jobs
      journeys/            JRN-  observed journeys, one arborescent file each
      recommendations/     REC-  studies, strategies, justifications
      decisions/           DEC-  team decisions with their context
      glossary/            GLO-  one atom per concept (study type, model, term)
    /guides/               GDE-  one guide per approach, sections: implement / integrate data / exploit
    /templates/            Starting templates: proto-templates, hosting, supplying, reporting
    /schema/               VERSION, profile, vocabularies, labels.*.yaml, approaches, dimensions, knowledge-areas, rules/
    /indexes/              Generated: navigation indexes, validation levels, coverage tables
    /views/                Generated human views: gap map, to review, changes, insight sheet, journeys (not versioned)
    /scripts/              Validation, generation, graph building

## 3. Identifiers

Format: `PREFIX-YYYY-NNN`, with a sequential number that is never reused.

**Allocation.** Identifiers are allocated by the skill or the script, never typed. The script reads the main branch and the open branches to pick the next number. If two branches still create the same identifier, the script renumbers the later atom and rewrites its links before the merge. This is the only authorised renumbering: once on `main`, an identifier is immutable. The same rule applies to journey node numbers.

**File names.** `ID-slug.md`, for example `INS-2026-014-technicians-skip-alerts.md`, so that a folder stays readable by a human.

<div class="md-table" aria-label="Table" role="region" tabindex="0">

| Prefix | Object |
| -------- | ---------------- |
| PRJ | Project |
| STU | Study |
| INS | Insight |
| EVD | Evidence |
| PAR | Participant |
| MET | Method |
| JOB | Job |
| PER | Persona |
| JRN | Journey |
| REC | Recommendation |
| DEC | Decision |
| SRC | Source |
| GLO | Glossary entry |
| GDE | Guide |

</div>

**Node identifiers** inside a journey use `n-` followed by a sequential number, allocated once and never renumbered when the tree is reordered. A node is addressed as `JRN-2026-003#n-017`.

## 4. Frontmatter

``` yaml
---
id: PER-2026-002              # required
type: persona                 # required, see section 5
title: Field technician in an isolated site   # required
language: fr                  # required, language of the content (ISO 639-1)
status: draft                 # required, see section 14
created: 2026-10-23           # required, ISO 8601
updated: 2026-10-23           # required, ISO 8601
projects: [PRJ-2026-001]      # required, at least one
provenance: observed          # required for evidence, insight, job, persona, journey
authored_by: ai               # required: human | ai | mixed
origin: internal             # required on source: internal | external
origin_detail: null          # required if origin is external: who, what, when
rights: own                  # required on source: own | licensed | public | unknown
scale: journey                # required for journey: job | journey | use_case
sensitive: false              # required; true if the atom holds sensitive data
reviewed_by: null             # git identity of the human reviewer, set on review
context: null                # optional, see section 23
proto_template: null          # optional, template used to start the atom
aliases: [field technician]   # optional, Obsidian-compatible
tags: [field, maintenance]    # optional, Obsidian-compatible
links:                        # optional, typed links (section 13)
  derives_from: [JOB-2026-001]
  represents: [{target: PAR-2026-007, role: primary}]
---
```

The validation level (section 6), the confidence (section 11) and the coverage tables never appear in the frontmatter: they are computed.

An atom with `authored_by: ai` or `mixed` stays `to_review` until a human sets `reviewed_by`. An evidence atom also requires `session_id`, `collected_at` (collection date, not creation date), `source` (an SRC identifier) and a `locator` (page, paragraph or timecode).

The body opens with a summary of two to four sentences, then the sections required by the type.

## 5. Atom types and required sections

<div class="md-table" aria-label="Table" role="region" tabindex="0">

| Type | Required sections |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| project | Context, objectives, audience, timeline |
| study | Research question, method, sample, period, limits |
| insight | Finding, evidence, implications, uncertainty |
| evidence | Content (verbatim quote or observation), collection context, source, locator in the source |
| participant | Segment, usage context, pseudonym (no identifying data) |
| method | Description, when to use, when to avoid, method family |
| job | Activities, context, tools, constraints, variations by context, accessibility coverage (section 7.3) |
| persona | Context, behaviours, motivations, barriers, goals, jobs covered, participants represented, declared situations (section 7.3) |
| journey | Scope, user goal, tree of nodes, layers (section 8.3) |
| recommendation | Recommendation, justification, evidence, confidence calculation, risks |
| decision | Context, decision, date, people involved by role |
| source | Description, origin and origin detail, rights, date received, content type, extraction done |
| glossary | Model, variants, summary, related approaches |
| guide | Approach covered, implement, integrate data, exploit, related atoms |

</div>

## 6. Validation level (the "proto" spectrum)

The validation level measures how far an object is between hypothesis and observation. Its displayed label is **degree of validation**; "proto" stays the internal name.

It applies to **jobs and personas**. A journey has no level: it is observed by definition, and its quality is measured by the number and diversity of its evidence.

<div class="md-table" aria-label="Table" role="region" tabindex="0">

| Level | Indicative condition |
| ------------------- | ---------------------------------------------------------------------------------------------------- |
| `hypothesis` | No observed evidence. Documented or inferred only. |
| `sensed` | Declared or documented by at least one source. Not observed yet. |
| `observed` | Observed qualitatively in at least 3 distinct participants, across at least 2 sessions or methods. |
| `quant_validated` | Confirmed by a quantitative measure (survey, analytics) on a defined sample. |

</div>

Thresholds are starting values, to calibrate on the pilot (v0.6).

**Score (0 to 1)**, computed for sorting only, from distinct participants, method families, freshness of evidence, and presence of quantitative validation. The score never decides the level: the level derives from the conditions above alone. `quant_validated` also requires the `observed` condition, so that a number never stands without an explanation.

**Display.** Views show one three-notch badge, with the detail on demand: `hypothesis` and `sensed` read as “Indice” (●○○), `observed` as “Observé” (●●○), `quant_validated` as “Corroboré” (●●●). Labels come from `schema/labels.*.yaml`; the words “proto” and “sensed” never reach the reader.

**Rules:**

- The script computes the level from links (`represents`, `validated_by`, `based_on`). Nobody types it.
- An object whose only support is `documented` or `inferred` cannot exceed `sensed`.
- Inferred evidence never counts toward `observed`.
- A manual override is an exception: it requires a written `level_justification` and a double validation (section 6.2).

### 6.1 Proto templates and proto atoms

To help researchers start, the repository provides **proto templates** in `/templates/proto/`. A template is a starting point, not an atom. Examples: `persona-from-job`, `journey-skeleton`, `job-from-documentation`.

Creating a proto atom from a template produces an atom with `status: draft`, a provenance of `inferred`, a `proto_template` value, and a level computed as `hypothesis`. Promoting it is done by linking evidence, not by editing a level. The `persona-from-job` template includes the accessibility checklist of section 7.3.

### 6.2 Double validation

Any exception to a rule needs a second researcher. This covers a level override (section 6), marking a disability dimension as `incompatible` (section 7.3), and any future rule exception.

- The requester writes a justification and records `exception: {kind, justification, requested_by}` in the atom.
- A second researcher, different from the requester, confirms through a git review, recorded as `confirmed_by`.
- All researchers have the same rights. This is a process control, not a permission level.
- The validation script rejects an exception without `confirmed_by`, or where `confirmed_by` equals `requested_by`.
- The identity is the git author. This guards against accidental self-validation, not against deliberate manipulation.
- The AI is never `requested_by` nor `confirmed_by`. If the skill commits under the researcher’s identity, the atom carries `authored_by: ai` and the confirmation must come from another human.
- When no second researcher exists (team of one), the exception stays `pending`, is listed in the “to review” view and expires after 30 days unless confirmed. It never counts as validated in the meantime.

## 7. Jobs, personas and participants

### 7.1 Definitions

- **Job (JOB):** a stable description of a role, its activities and its context. A job is not a person. It may have variations by context (site, status, seniority), described in the atom.
- **Persona (PER):** a behavioural archetype built from one or more participants and one or more jobs. It describes what varies between people: motivations, barriers, ways of working. A persona is not a sum of jobs.

### 7.2 Relations

- `performs`: participant → job. A participant performs one or more jobs.
- `derives_from`: persona → job. A persona rests on one or more jobs.
- `represents`: participant → persona, with `role: primary | secondary`. A participant may represent several personas.

**Rules:**

- A participant is written once. Its jobs and personas are links, never copies.
- A persona with no linked participant stays at `hypothesis` or `sensed`, depending on its provenance.
- A persona built from internal stakeholders' beliefs is supported by `declared` or `inferred` sources, not by observation.

### 7.3 Accessibility coverage (declarative)

The rule is declarative: a disability situation compatible with the exercise of a job must appear in that job's personas.

The disability dimensions are listed in `schema/accessibility-dimensions.yaml`: `visual`, `auditory`, `motor`, `speech`, `cognitive`, `psychosocial`, `chronic_fatigue`. Situational and temporary constraints are outside this table (section 21).

Each job holds a **coverage table**, generated into the index. Each dimension has one of three statuses:

- `covered`: at least one persona of the job declares this situation;
- `incompatible`: the situation is objectively incompatible with the job. The justification is written and the exception is double-validated (section 6.2). Incompatibility concerns the job, not the person;
- `open`: no persona declares this situation yet. It stays open until a researcher adds a declared situation.

**Declaration in personas.** A persona lists its declared situations in a `situations` field: dimension, a short description of the constraints, and `declared_by`, which is a documentary source (`SRC-`) or the researcher’s identifier. A declaration by a researcher has the provenance `inferred`, and the coverage table shows it as `covered (inferred)`, so that a box ticked without evidence stays visible. A participant ID is allowed in `declared_by` only in the `strict` profile (see the health data rule below). The declaration is self-reported. The system does not judge its realism; it checks presence and traceability.

**Rules:**

- Every dimension of a job is `covered`, `incompatible` or `open`. Nothing is implicit.
- A persona can cover several dimensions, and a dimension can be covered by several personas.
- In the `strict` profile, a job with an `open` dimension cannot reach `approved`. In the other profiles, and in `draft`, it produces a warning.
- Declared situations are health data: the atom is `sensitive: true`. By default a declaration is not linked to any participant. A participant-linked declaration is allowed only in the `strict` profile, with the participant’s explicit consent, the DPO’s approval and a documented erasure procedure, because git history is permanent. To be validated with the DPO (section 21).
- No single persona has to combine every situation. A composite persona is a known pitfall: each persona holds a coherent set of situations that a real person could have.

## 8. Journeys

### 8.1 Model

A journey is an observed trajectory, reconstructed from observations, quotes and data. It is focused on the user.

Scales (`scale`):

- `job`: the job-level journey, covering a role across its mission or day.
- `journey`: a trajectory towards a given goal.
- `use_case`: a precise situation within a journey.

A journey is a **tree**. A node can be a process step, which is itself a journey at a finer scale. The tree depth has no fixed limit.

### 8.2 One file, arborescent

Each journey is one file. The whole tree is inside it, so that a tool can show, hide or isolate any level without reading other files.

**Node attributes:**

<div class="md-table" aria-label="Table" role="region" tabindex="0">

| Attribute | Meaning |
| -------------- | --------------------------------------------------------------------------------------------------------------------- |
| `kind` | `step`, `screen`, `action`, `wait`, `external` (exchange outside the product), `ref` (reference to another journey) |
| `parent` | ID of the parent node, or `root` |
| `actor` | Who performs the node |
| `state` | State of the screen or of the situation |
| `applies_to` | Jobs or personas for which the node is valid (default: all) |
| `disruption` | Optional: probable interruption and the state to keep in memory |

</div>

Node headings use the stable identifier, so that a sub-tree can be isolated and linked:

``` markdown
### n-017 · Check alerts
- kind: step
- parent: n-011
- actor: technician
- state: connected
- applies_to: [JOB-2026-001]
```

### 8.3 Layers

Layers are sections of the same file, separated and identified by name. Each layer refers to nodes by identifier, so no step is copied.

<div class="md-table" aria-label="Table" role="region" tabindex="0">

| Layer | Content |
| ------------- | ------------------------------------------------- |
| `emotional` | Emotional state per node |
| `friction` | Points of effort or blocking |
| `tools` | Tools and supports used |
| `channels` | Interaction channels (app, email, phone, paper) |

</div>

Verbatims and observations are evidence atoms linked to nodes with `illustrates`. They are not written in the journey file.

Each layer entry carries a provenance: `declared` (said by a participant, with the quote linked) or `inferred` (interpreted by a researcher or an AI). Inferred entries are visibly marked in views and carry their own confidence. An emotional layer without any `declared` or `observed` entry cannot exceed `sensed`.

### 8.4 Shared journeys

When a sub-journey is common to several jobs, it becomes its own journey atom. A parent journey reaches it through a `ref` node:

``` markdown
### n-023 · Request spare part
- kind: ref
- parent: n-011
- target: JRN-2026-010
- applies_to: [JOB-2026-001, JOB-2026-004]
```

Differences between jobs are expressed by `applies_to` on child nodes of the parent or of the shared journey, not by copies. If the divergence between jobs becomes large, the shared journey is split into two. The threshold is to be calibrated (v0.6). Changing a shared journey changes every parent that references it, which is the intent, and this is why its changes are reviewed.

### 8.5 Exploitability requirements

The future explorer tool depends on the file structure, so these rules are checked:

- node identifiers are unique and never reused;
- every `parent` exists, and the tree has no cycle;
- `kind` takes a value from the vocabulary;
- every `ref` target exists;
- layer entries point to existing nodes;
- the script generates a Mermaid rendering of the tree in `/views/`: a journey must be readable without editing the file (Must).

### 8.6 Concurrency

A single file per journey creates git conflicts when several researchers edit it at the same time. Mitigations: one owner per journey at a time, one branch per study, small commits, and layers kept in separate sections.

## 9. Userflows: outside the knowledge base

A userflow is a designed artefact: a bet about future use, not something observed. The repository therefore stores no userflow and no UFL atom, and no link points to a design.

**Entry point.** A designed flow enters the repository as a journey (JRN) only once its use has been proven. Proof can come from several channels, each recorded as evidence with its own provenance:

| Channel | Family and axis | Provenance | What it shows |
| ----------------------------------------- | ----------------------------------------------------------- | ---------------------------------------------------------------------- | -------------------------------------------------------- |
| Field observation of real use | qualitative, behavioral | `observed` | What people actually do, with a locator in the notes |
| Usability test on the flow | qualitative, behavioral (task) and attitudinal (comments) | `observed` | Where people stall, and why, in their own words |
| Interview about past use | qualitative, attitudinal | `declared` | What people say they did; weaker than observation |
| Usage data (events, funnels, drop-offs) | quantitative, behavioral | `documented`, through an SRC atom pointing to the query or dashboard | How many people take the path, and where they leave it |

**Threshold (to calibrate).** A flow becomes a JRN when at least one behavioral channel (observation or test) shows it in use. Usage data alone shows volumes and drop-offs but not the reasons, so it supports a journey without creating one. Each channel adds to the journey’s evidence, and the gap map (section 19) records it.

The design file stays in the design tool. It may be referenced as a `documented` source (SRC) to trace the intent, so that the gap between what was designed and what is done stays visible.

**Why this order.** Storing a design as knowledge would let a hypothesis look like evidence. Designing flows is a design practice; this base only holds what users have actually done.

## 10. Quali, quanti and triangulation

### 10.1 Two families

<div class="md-table" aria-label="Table" role="region" tabindex="0">

|  | Qualitative | Quantitative |
| ------------------- | --------------------------------------------------------- | ------------------------------------------------------- |
| Question answered | Why and how | How much, how many |
| Typical methods | Interviews, observation, usability tests, diary studies | Surveys, analytics, large-scale tests |
| Sample | Small, chosen for variety, read until patterns repeat | Large, drawn to represent a population |
| Output | Quotes, observations, mechanisms | Proportions, rates, comparisons with margins of error |
| Limit | Cannot estimate frequency | Cannot explain causes on its own |

</div>

Two other families are recorded but do not validate on their own:

- **documentary**: existing documents, prior studies, reports;
- **expert**: stakeholder knowledge, expert review.

They add context and can justify a hypothesis, but they never raise an object above `sensed`.

### 10.2 Triangulation

Each evidence atom declares its method family through the method it belongs to. The confidence of an insight depends on the **number of distinct families** supporting it, not on the number of methods:

- two interviews (both qualitative) add little more than one;
- an interview and a survey (qualitative and quantitative) are corroboration, and raise confidence most;
- a documented finding confirmed by an interview is a partial corroboration.

Triangulation is what makes an insight more reliable. The scoring rules are in section 11.

Each method also declares an **axis** in `schema/methods.yaml`: `attitudinal` (what people say) or `behavioral` (what people do). An interview and a usability test are both qualitative, yet corroboration across the two axes counts like a second family.

## 11. Confidence

### 11.1 Recommendations

Two modes, distinguished by provenance:

- **`rule`**: the recommendation follows from an explicit, versioned rule. Its confidence is fixed by the rule, in the very-high band. The atom cites the rule ID; rules live in `/schema/rules/`, one versioned file per rule.
- **`inferred`**: the recommendation results from reasoning. It requires a written justification, at least two `based_on` links to evidence, and a computed confidence.

### 11.2 Insight and recommendation confidence (ordinal, to calibrate on the pilot)

The band is read from an ordinal decision table, which a non-expert can follow, rather than from a weighted sum:

- **low**: a single independent evidence, or only `inferred`, documentary or expert support;
- **medium**: at least two independent evidence from one family or axis, or converging support with an open contradiction;
- **high**: at least three independent evidence from two families or axes, no unresolved contradiction;
- **very high**: an explicit rule only (section 11.1).

Factors to calibrate on the pilot:

- base score from the number of **independent** evidence atoms (two quotes from the same session count as one);
- bonus for each additional family of method supporting the insight;
- a larger bonus when both qualitative and quantitative families support it;
- no contribution from `inferred` evidence;
- contributions from documentary and expert sources are capped, and their total cannot raise confidence above the cap set for them;
- contradictions not resolved lower the score;
- coverage of the brief's scope is a factor for recommendations.

The band is computed and stored in `indexes/`, never typed. The atom keeps the written reasoning (which evidence, which families, which contradictions) so a researcher can contest it point by point. Views show the band label, not a number.

## 12. Glossary, approaches and guides

Each study type or concept has a **glossary atom** (`GLO`). The approach registry, `schema/approaches.yaml`, lists the research approaches of the repository: interview, usability test, survey, diary study, card sorting, field observation, persona building, journey mapping, userflow design, and others as they appear.

For each approach in the registry, the repository contains:

- a **glossary atom** describing the model, its variants, a short summary and its related approaches;
- a **guide** in `/guides/`, with three sections:
  - `implement`: how to run it, step by step;
  - `integrate data`: how to bring the results into the repository (which atoms to create, how to link them);
  - `exploit`: how to use the results (which views, which decisions they support, what they cannot tell).

**Creating a new approach:** add it to the registry, create the glossary atom and the guide from their templates, and link them to the method atoms they describe. The validation script checks that each registered approach has both.

## 13. Typed links

<div class="md-table" aria-label="Table" role="region" tabindex="0">

| Relation | From → to | Meaning |
| ---------------- | ------------------------------------------------------- | -------------------------------------------------------- |
| `based_on` | insight, recommendation → evidence | Support (never a userflow) |
| `from_study` | evidence → study | Collected in this study |
| `produced` | study → insight | Study that produced the insight |
| `covers` | study, insight → project, knowledge area (section 19) | Scope |
| `uses` | study → method | Method used |
| `concerns` | evidence → participant | Source participant |
| `illustrates` | evidence → journey node | Evidence attached to a node |
| `performs` | participant → job | Job performed |
| `derives_from` | persona → job | Persona rests on this job |
| `represents` | participant → persona (role) | Participant represented by a persona |
| `part_of` | journey → journey | Hierarchy across files |
| `serves` | journey → job | Journey that serves a job |
| `includes` | journey node (ref) → journey | Generated from `ref` nodes, never written by hand |
| `validated_by` | persona → evidence | Observation validating a persona |
| `contradicts` | insight, evidence → insight, evidence | Tension to resolve |
| `confirms` | evidence → insight | Generated inverse of `based_on`, never written by hand |
| `replaces` | atom → atom | Replacement |
| `recommends` | recommendation → study, method | Proposed object |
| `informs` | decision → recommendation | Decision taken from a recommendation |
| `source_of` | source → evidence, study | Origin document |
| `documents` | guide → method | Guide covering an approach |
| `explains` | glossary → method | Glossary entry for an approach |

</div>

Any relation absent from this table is invalid. A change goes through a schema version bump (section 16).

``` mermaid
graph LR
  JOB[job] -->|derives_from| PER[persona]
  PAR[participant] -->|performs| JOB
  PAR -->|represents| PER
  EVD[evidence] -->|concerns| PAR
  EVD -->|illustrates| JRN[journey node]
  JRN -->|serves| JOB
  STU[study] -->|produced| INS[insight]
  INS -->|based_on| EVD
```

## 14. Controlled vocabularies

**Statuses:** `draft`, `to_review`, `approved`, `obsolete`, `replaced`. A `replaced` atom must link to its replacement with `replaces`.

**Provenances:** `observed` (seen directly by a researcher), `declared` (said by a participant), `documented` (external source), `inferred` (deduced by judgement or by an AI), `rule` (explicit rule, for recommendations).

**Method families:** `qualitative`, `quantitative`, `documentary`, `expert`.

**Method axes:** `attitudinal`, `behavioral`. **Authorship:** `human`, `ai`, `mixed`. **Profiles:** `starter`, `standard`, `strict`.

**Validation levels:** `hypothesis`, `sensed`, `observed`, `quant_validated`.

**Scales:** `job`, `journey`, `use_case`.

**Node kinds:** `step`, `screen`, `action`, `wait`, `external`, `ref`.

**Layers:** `emotional`, `friction`, `tools`, `channels`.

**Methods (examples, full list in `/schema/methods.yaml`):** `interview`, `usability_test`, `survey`, `diary_study`, `card_sorting`, `field_observation`, `analytics_review`, `document_review`, `benchmark`.

**Coverage statuses:** `covered`, `incompatible`, `open`.

**Disability dimensions:** `visual`, `auditory`, `motor`, `speech`, `cognitive`, `psychosocial`, `chronic_fatigue`.

**Confidence bands:**

<div class="md-table" aria-label="Table" role="region" tabindex="0">

| Range | Label | Use |
| ------------- | ----------- | ---------------------------------------------------------------- |
| 0.90 – 1.00 | very high | Explicit rule applied to valid data |
| 0.70 – 0.89 | high | Insight supported by converging evidence from several families |
| 0.40 – 0.69 | medium | Limited or partly contradictory evidence |
| 0.00 – 0.39 | low | Hypothesis, to validate |

</div>

## 15. Sensitive data and anonymisation

- Participants are identified by a `PAR-` pseudonym. The correspondence table, if any, is never in the repository.
- Evidence contains no name, address, email, phone number, or detail that would allow re-identification. Verbatims are reviewed and cleaned before ingestion.
- Personas carry fictional names, never those of a real participant.
- Raw audio, video and transcripts are not versioned. The repository keeps the cleaned extracted text (SRC) and a pointer (URI and SHA-256) to the original, stored elsewhere.
- Atoms holding health data (including disability, section 7.3), opinions or other sensitive categories are flagged `sensitive: true`. Git history is permanent: a sensitive datum linked to an identifiable participant cannot be erased without rewriting history, which is why section 7.3 forbids that link by default. Access rules remain out of scope for this version.

**Origin and rights of sources.** Two fields are distinct from provenance:

- `origin` says where the information comes from: `internal` (produced or held by the organisation, including its own studies, support tickets and internal documents) or `external` (produced outside it: a partner, a supplier, a client, a benchmark, public data, academic or press literature).
- `provenance` says how the content was established: `observed`, `declared`, `documented`, `inferred`. An interview run by an external agency has `origin: external` and `provenance: declared`.

Rules:

- Every source carries `origin` and `rights`. An external source also requires `origin_detail` (who produced it, what it is, when it was published or received).
- `rights: unknown` lets a source be captured, but its atoms cannot reach `approved` in `standard` or `strict`. In `starter` it is a warning. `ur-ask` may cite such a source only with the mention "source externe, droits non vérifiés".
- An external source containing personal data is `sensitive: true`. It is ingested only with a documented basis, to be confirmed with the DPO (section 21).
- Excerpts are kept only where they serve as evidence, with their locator. The repository never reproduces a full external document, even where `rights` is `licensed`, unless the licence explicitly allows it. The pointer (URI and SHA-256) is kept instead.
- Origin is computed, never typed, on evidence and insights: an evidence atom inherits the origin of its source, and an insight shows the mix of its sources (`internal`, `external`, `mixed`). Views show a short origin label on each evidence and insight.
- Origin does not change the validation level directly. External documented sources remain subject to the cap on documentary sources (section 17).

## 16. Versioning and compatibility

- The repository is versioned with git. Each change is a commit in the format `type(scope): description`, for example `feat(personas): add PER-2026-002 field technician`.
- Commit types: `feat`, `fix`, `docs`, `refactor`, `schema`.
- The schema has a semantic version in `/schema/VERSION`. A change to vocabularies or frontmatter bumps at least the minor version; a breaking change bumps the major version.
- Each skill declares the schema versions it supports. A repository on an incompatible version is flagged before any write.

## 17. Validation rules

The script checks, on each commit and on demand:

1.  Required frontmatter fields are present and valid.
2.  Controlled vocabularies are respected (types, statuses, provenances, relations, methods, scales, kinds, layers, families, coverage statuses, dimensions).
3.  Atom identifiers are unique and well formed.
4.  The file name starts with the identifier, followed by a slug.
5.  Every link target exists, including node identifiers.
6.  Frontmatter links and `[[ID]]` references in the body are consistent.
7.  Required sections are present for the type.
8.  No orphan atom (no incoming or outgoing link). A warning in `draft` and in the `starter` profile.
9.  Replacement chains contain no loop.
10. Inferred recommendations have at least two evidence links and a confidence calculation.
11. No personal data pattern (email, phone) in atoms.
12. No journey is created from a design artefact before its use is proven by a channel of section 9: a design alone never produces a JRN.
13. A `use_case` journey has at least one `part_of` link to a journey.
14. Every layer entry has a provenance; inferred entries are marked.
15. A persona or job with no linked participant has a provenance of `documented` or `inferred`.
16. No calculated field (level, score, confidence, coverage status) appears in the frontmatter.
17. Every level override has a `level_justification`.
18. Every job has a coverage table in which each disability dimension is `covered`, `incompatible` or `open`. In the `strict` profile an `open` dimension blocks `approved`; otherwise it warns.
19. Every `covered` dimension is declared by at least one persona of the job, with a `declared_by` value.
20. Every `exception` has `requested_by` and `confirmed_by`, and they are different human identities, never the AI.
21. Journey files: unique node identifiers, existing parents, no cycle, valid kinds, existing `ref` targets.
22. Every registered approach has a glossary atom and a guide.
23. Atoms holding disability or health data are flagged `sensitive: true`.
24. Every evidence atom has `session_id`, `collected_at`, `source` and `locator`; for a text source, the quoted text appears verbatim at the locator.
25. Every atom has `authored_by`. An atom authored by `ai` or `mixed` without `reviewed_by` cannot be `approved`.
26. Identifiers are allocated by the script; collisions are detected before merge.
27. Every `covers` target exists in `schema/knowledge-areas.yaml`.
28. Every `rule` recommendation cites an existing file in `/schema/rules/`.
29. Rules apply to the enabled modules only. In the `starter` profile, every rule except 3, 5 and 11 is a warning.

## 18. Priorities

<div class="md-table" aria-label="Table" role="region" tabindex="0">

| Priority | Element |
| ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Must** | Core and profiles, script-allocated identifiers, frontmatter with `authored_by` / `reviewed_by`, types, vocabularies, typed links, all validation rules of the enabled modules, verbatim check of evidence, the mandatory views (section 20.4), git versioning, anonymisation, design artefacts kept out of the base, declarative accessibility coverage with `open` / `covered` / `incompatible`, double validation of exceptions, quali / quanti families |
| **Should** | Validation level and score computed, proto templates, journey tree with layers and sub-journeys, shared journeys, glossary and guides for the first approaches, ordinal confidence, schema versioning, example repository, cheat sheet, steward role |
| **Could** | Explorer tool for journeys, graph in memory, read-only graph database, quantitative measurement of the gap, extra layers, complex data types (video), external sources (e.g. Azure Application Insights) |

</div>

## 19. Knowledge areas and gap map

A repository can only report what it knows, and what it does not know, against a map. `schema/knowledge-areas.yaml` lists the domains the team needs to understand (by job, journey stage or product area) as a tree with `id`, `label` and `parent`. The skill builds the first version with the team at setup. Studies and insights point to areas with `covers`.

The **gap map** is a generated view. For each area it shows the number of independent evidence atoms, the method families and axes present, the date of the latest evidence, and the validation level of linked objects. An area is *empty* when no atom covers it, *thin* when it rests on one family or one session, and *stale* when its latest evidence is older than the threshold set for its method type in `schema/methods.yaml`.

**Study recommendation.** From a brief, the skill maps the request to areas, reads the gap map, and proposes a study or a strategy of studies. A match with a file in `schema/rules/` gives a `rule` recommendation; otherwise it is `inferred`, with justification and evidence (section 11.1).

## 20. Human operating model

The schema is strict so that the tool can be simple. The researcher should never have to learn it. This section fixes who does what.

### 20.1 Roles

- **Researcher**: decides what is true, relevant and approved.
- **Skill (AI)**: operates. It extracts, writes frontmatter, allocates identifiers, links, commits, checks and proposes.
- **Steward**: one named researcher per repository, who curates it (20.5).
- **Second researcher**: confirms exceptions (section 6.2).

### 20.2 Five gestures

| Gesture | The researcher | The skill |
| ------------- | -------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------ |
| **Capture** | Hands over a document or a note and answers a few questions: what was observed, with whom, when. | Creates SRC, EVD and PAR atoms, fills the frontmatter, proposes atoms. |
| **Check** | Reads each proposed atom next to its source; corrects or rejects. | Shows each quote with its locator; runs the verbatim check. |
| **Link** | Accepts or edits suggested links to insights, jobs and areas. | Suggests links and validates targets. |
| **Approve** | Moves an atom to `approved`. | Refuses if a rule fails. |
| **Ask** | Asks a question or hands over a brief. | Answers from atoms, with trust badge and gaps. |

### 20.3 Rules for the AI

- Every atom written or changed by the skill has `authored_by: ai` or `mixed` and the status `to_review`.
- Only a human sets `reviewed_by` and moves an atom to `approved`. The AI never promotes a status or a level.
- Evidence quotes are checked mechanically against the source text at the locator.
- The AI is never `requested_by` nor `confirmed_by` for an exception.
- When the skill answers a question, it cites atom identifiers, states the band and the gaps, and says so when the repository holds nothing.

### 20.4 Mandatory views

Generated into `/views/` (Must):

- **Gap map** (section 19).
- **To review**: atoms in `to_review`, pending and active exceptions with their due date.
- **What changed**: atoms added or changed since a date, with the kind of author.
- **Insight sheet**: finding, evidence with quotes, trust badge, contradictions.
- **Journey rendering**: Mermaid tree generated from the file (section 8.5).

Labels come from `schema/labels.*.yaml` in the reader’s language; identifiers and keys stay English. Insights and recommendations use the same three notches as levels (section 6): *low* reads ●○○, *medium* ●●○, *high* and *very high* ●●●. Provenance, level, status and band stay in the detail, never at first sight.

### 20.5 Definition of done and curation

An atom can be approved when a human answers yes to three questions: is it understandable alone, in two to four sentences? Can it be traced to a source, with a locator? Is it free of personal data?

The steward holds a short weekly ritual (about 20 minutes): review the `to_review` list, resolve `contradicts` links, handle pending exceptions, retire `obsolete` atoms.

### 20.6 Onboarding and adoption

- An **example repository** ships with the skills: a fictional project, two studies, about fifteen atoms, all views generated. Reading it comes before reading this specification.
- A **one-page cheat sheet**: the five gestures, the trust badge, the definition of done.
- A **pilot** with two or three researchers on one real project, in the `starter` profile, for four to six weeks, before any extension.
- **Adoption measures**: time to the first approved atom; share of AI-authored atoms reviewed within a week; atoms rejected at review (quality of extraction); questions answered with cited atoms that the researcher judged useful.
- A module is enabled only when the team asks for it and the steward can support it.

## 21. Open points

- Calibrate the validation thresholds and the confidence decision table on the pilot (v0.6).
- Place of documentary and expert sources in the decision table (cap).
- Threshold for splitting a shared journey when job divergence grows.
- Calibration of the entry threshold for designed flows (section 9), and the query format of usage-data SRC atoms.
- Definition of `incompatible`: which kinds of requirement qualify (legal, safety, physical), and where the line falls between a difficulty and an incompatibility.
- Situational and temporary constraints (one hand busy, noise, stress): whether they get their own table, outside disability coverage.
- Access rules for `sensitive` atoms; DPO opinion on participant-linked declarations and on the erasure procedure.
- Migration of existing documents: ingest everything, or only ongoing studies?
- Where the originals are stored, and who owns them.
- Whether `chronic_fatigue` stays a disability dimension, since it is of a different nature from the others.
- Success criteria of the pilot (section 20.6).
- Whether a context value stays a plain label, or can be promoted to a context sheet with description and sources, keeping the same identifier (section 23).
- The relation recording that two conflicting pieces of evidence vary by context (section 23).
- Who creates context dimensions: the steward, or a team workshop.
- Whether a researcher's role is a context dimension or an attribute of the persona.


## 22. Storage and synchronisation (pilot)

The repository is a git repository, local or remote. Both use the same format, and the choice between them never changes atoms, identifiers or skill behaviour. Users never have to use git directly: skills speak in terms of work, not of version control.

**Modes.**

- *Local* (default): a git repository on the researcher's machine, with no remote. No account is needed.
- *Shared*: the same repository with a remote, added once per project by the steward through `ur-init`. The remote must be private; the validation script checks this, and a public remote blocks `standard` and `strict`.

Hosting is out of scope for this version. Authentication relies on the git credentials configured in the IDE, never on secrets stored in the repository.

**Vocabulary exposed to researchers.**

| Git action | What the researcher sees |
| --- | --- |
| commit | "Save" (after each validation) |
| pull | "Get the team's updates" (before each action that allocates an identifier) |
| push | "Share" (only after a human validation) |
| conflict | "Two versions of this item: keep mine, keep the team's, or keep both" |

No message shown to a researcher contains a git term. If an operation fails, the skill says what happened and what is already saved.

**Rules.**

- A capture is saved locally before any attempt to share. A connection failure blocks sharing, never the work.
- Identifiers are allocated only after a pull (section 3).
- A conflict on an atom is never resolved automatically, including by the AI. The researcher chooses one of the three options above, and the atom returns to `to_review`.
- In the pilot, all work happens on one shared branch. Branches per study are reserved for `standard` and `strict` profiles. A journey has one owner at a time (section 8.6).
- No secret, token or credential is ever written in the repository.
- Manual edits made outside the skills are detected at the next action and set the atom to `to_review`.

**IDE requirements.** The pilot assumes an IDE in which the assistant can read and write the project files and run the validation and synchronisation scripts in the background, and in which Markdown previews render Mermaid journeys and the generated views. These conditions are checked before the skills are written; they are not optional.

## 23. Context

**Purpose.** Some knowledge applies to a place or a perimeter: a business unit, a site, an application, a product line, a market, a regulation. Context records where a piece of knowledge was observed or where it applies. The schema does not fix the dimensions: each repository declares its own, and their names differ from one organisation to another.

**Principles.**

- Context is optional. A missing context means "context not specified", and skills say so. It never means "valid everywhere".
- Context becomes mandatory only when two pieces of evidence conflict and at least one of them has no context (section 23.4).
- Dimensions are declared in `schema/context.yaml`. The file starts empty. A dimension is created when an observation needs it, and a human validates it.
- Context grows gradually. The first information records the immediate context; the scope widens as evidence arrives. Nothing is required upfront.

**23.1 Declaring dimensions.** Dimensions are flat lists of values:

```yaml
dimensions:
  - id: site
    label: Site
    values:
      - id: site-north
        label: North plant
        status: active        # active | retired
        valid_from: 2024-01-01
        valid_to: null
        aliases: [plant nord]
```

A value is never deleted. A retired value keeps its identifier and stops applying to new decisions (`status: retired`, `valid_to` set). An atom references values by identifier, in the frontmatter:

```yaml
context: {site: site-north, application: app-planner}
```

An atom may hold several values for one dimension (`site: [site-north, site-south]`). The validation script checks each value against the declared list.

**23.2 Inheritance.** Context is declared once, on the source (or on the study or participant, where relevant). Evidence inherits it. An evidence atom may override the inherited context, with a written reason. Views distinguish declared context from inherited context.

**23.3 Scope.** Each insight and recommendation carries a `scope`, computed as the union of the context values of its evidence; it is never typed. A researcher may narrow a scope with a written reason. Widening a scope requires new evidence from the wider context. `ur-ask` never generalises silently: if an answer rests on one value, it says so, for example "observed in the North plant, not tested elsewhere".

**23.4 Contradictions.** Context is mandatory when two atoms are linked by `contradicts` and at least one of them has no context. Neither atom can reach `approved` until context is recorded. The skill asks: "under what conditions was each observation made?" Two outcomes are possible:

- *The contexts differ.* Both can be true, each within its scope. The pair stays linked, and the insight records that the finding varies by context.
- *The contexts are the same.* This is a true contradiction. It must be resolved: one is wrong, outdated, or a study is missing.

A contradiction that no existing dimension explains is a signal that a dimension is missing. This is how dimensions grow, at the moment they are needed.

**23.5 Limits accepted for the pilot.**

- Flat lists: a whole division cannot be selected without listing its values.
- Contradictions are detected only when they are linked. `ur-link` may propose candidates, but detection will never be exhaustive.
- Context can be read per value in the gap map (section 19).

