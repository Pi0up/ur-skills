---
name: ur-approve
description: >-
  Companion skill for Gesture 4 (Approve). Evaluates the 3 Definition of Done questions,
  manages human review traceability (reviewed_by), and handles double validation of rule exceptions.
---

# Skill: UR Approve — Gesture 4 (Approve & Exceptions)

This skill operationalizes the **Approve** gesture (Section 20.2 & 20.5 of [socle-ur-spec v0.5](../../docs/spec/socle-ur-spec-v0.5.md)).
Only a human researcher can promote an atom to `status: approved`. The skill acts as a strict gatekeeper, ensuring all conditions are fulfilled before approval.

---

> [!CAUTION]
> **AI Rule on Approval:**
> The AI agent **NEVER** promotes an atom to `approved` autonomously and **NEVER** sets `reviewed_by` to itself.
> The AI is also strictly forbidden from being `requested_by` or `confirmed_by` for any exception (Rule 20).

---

## Step-by-Step Instructions for the Agent

### Step 1: Evaluate the Definition of Done (3 Questions)
Before presenting an atom to a human researcher for final approval, verify that the researcher can answer **YES** to these 3 questions:
1. **Understandable alone?** Can a reader grasp the finding or object in 2 to 4 sentences without consulting other files?
2. **Traceable to a source?** Does every piece of evidence point to an `SRC-` atom with a verified `locator`?
3. **Free of personal data?** Is the atom completely free of names, emails, phone numbers, or re-identifying details?

### Step 2: Human Review Gatekeeping
1. Run pre-approval validation:
   ```bash
   python -m ur_tools.cli validate
   ```
   If any blocking errors exist, approval is impossible until resolved.
2. If all checks pass, prompt the human researcher to sign off:
   - Record the git identity of the reviewer in `reviewed_by: <git-author-name>`
   - Set `status: approved`
   - Update `updated: YYYY-MM-DD`

### Step 3: Double Validation of Exceptions (Section 6.2)
When an exception to a normative rule is required (e.g. manual validation level override, or marking an accessibility dimension as `incompatible`):
1. The requesting researcher provides a written justification:
   ```yaml
   exception:
     kind: level_override # or accessibility_incompatible
     justification: "Physical impossibility of operating field equipment without sight"
     requested_by: researcher-1
     confirmed_by: researcher-2 # Must be a DIFFERENT human researcher
   ```
2. The skill verifies:
   - `requested_by` and `confirmed_by` are different human identities.
   - Neither is `ai`.
3. In a team of one (solo researcher), the exception remains `status: pending` in `views/to-review.md` and expires after 30 days unless confirmed.
