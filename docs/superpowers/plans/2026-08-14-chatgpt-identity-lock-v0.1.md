# 66Workshop ChatGPT Cover Identity-Lock V0.1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Upgrade the existing 66Workshop Xiaohongshu cover workflow into a ChatGPT-native identity-preservation Skill that prioritizes the real authorized person over generative restyling, routes requests by pose risk, and rejects lookalike outputs.

**Architecture:** Keep `SKILL.md` as the single operational entry point. Move detailed contracts into focused docs: input assets, route/state machine, QA, failure fallback, benchmark, and a copy-ready ChatGPT prompt protocol. The system remains model-agnostic and does not invent unsupported image-model parameters.

**Tech Stack:** Markdown Skill instructions, existing GitHub-controlled asset manifests, existing job/record lifecycle, ChatGPT image creation/editing, human identity approval.

## Global Constraints

- Person identity fidelity is P0 and outranks layout aesthetics.
- Native ChatGPT image generation cannot be described as a mathematical/pixel identity guarantee.
- Use one primary identity anchor and at most two secondary anchors for generative identity reference.
- Prefer the least-generative route: `PIXEL_LOCK_COMPOSITE` → `SOURCE_EDIT_MINIMAL` → `GENERATIVE_IDENTITY_REFERENCE`.
- `IDENTITY_1`, `IDENTITY_2`, and `IDENTITY_3` are always rejected.
- Final production identity approval requires human owner review.
- Do not store or redistribute font files; font screenshots are style references only.
- Do not add third-party face-swap or training dependencies in V0.1.

---

### Task 1: Replace the main Skill with route-based identity control

**Files:**
- Modify: `SKILL.md`

**Interfaces:**
- Consumes: user title + uploaded person/vehicle/product/font images.
- Produces: asset-role map, identity route, pose-delta class, composition contract, QA/fallback behavior.

- [ ] **Step 1:** Replace the current single-pass generation flow with the three identity routes and six-state production flow.
- [ ] **Step 2:** Add strict role binding for every uploaded image.
- [ ] **Step 3:** Add pose-delta classification and a hard rule that HIGH pose deltas cannot be promised as identity-locked.
- [ ] **Step 4:** Add explicit retry/fallback rules and lookalike rejection.
- [ ] **Step 5:** Add links to the detailed docs created in Tasks 2–6.

### Task 2: Define production input assets

**Files:**
- Create: `docs/INPUT_SPEC.md`

**Interfaces:**
- Consumes: uploaded images and title brief.
- Produces: deterministic asset quality/role decision before generation.

- [ ] **Step 1:** Define preferred person-source set: one primary source plus optional secondary identity images.
- [ ] **Step 2:** Define green-screen, angle, sharpness, occlusion, expression, and pose requirements.
- [ ] **Step 3:** Define vehicle/product evidence requirements.
- [ ] **Step 4:** Define font-style reference limitations.
- [ ] **Step 5:** Define blocking conditions that force a safer pose or asset request instead of blind generation.

### Task 3: Define ChatGPT generation/editing workflow

**Files:**
- Create: `docs/WORKFLOW.md`
- Create: `prompts/CHATGPT_IDENTITY_LOCK_PROTOCOL.md`

**Interfaces:**
- Consumes: role-bound inputs from Task 2.
- Produces: route selection, composition contract, image-generation/edit instruction, repair instruction.

- [ ] **Step 1:** Implement `PREFLIGHT → ROUTE_SELECT → COMPOSITION_PLAN → IMAGE_CREATE_OR_EDIT → QA_GATE → REPAIR_OR_FALLBACK → RECORD`.
- [ ] **Step 2:** Add the copy-ready prompt structure with positive constraints rather than relying on negative prompts.
- [ ] **Step 3:** Add a no-full-regeneration rule when only text or a localized non-face region fails.
- [ ] **Step 4:** Add the two-failures-then-fallback identity rule.

### Task 4: Add identity and evidence QA

**Files:**
- Create: `docs/QA_CHECKLIST.md`

**Interfaces:**
- Consumes: candidate image + source assets.
- Produces: `IDENTITY_1..5`, vehicle/evidence/text/layout verdicts, pass/fail.

- [ ] **Step 1:** Define the facial geometry comparison rubric.
- [ ] **Step 2:** Set production pass threshold to `IDENTITY_4` or `IDENTITY_5` plus human approval.
- [ ] **Step 3:** Add vehicle/product/text/brand checks.
- [ ] **Step 4:** Add one-vote veto rules for wrong person, wrong model, fabricated product detail, and text errors.

### Task 5: Add failure routing and repair policy

**Files:**
- Create: `docs/FAILURE_PLAYBOOK.md`

**Interfaces:**
- Consumes: failed QA category + route + pose delta.
- Produces: localized repair or safer-route fallback.

- [ ] **Step 1:** Map identity drift to reference reduction, pose reduction, source replacement, or route fallback.
- [ ] **Step 2:** Map vehicle/product drift to source anchoring or reduced visibility.
- [ ] **Step 3:** Map title failure to text-only repair.
- [ ] **Step 4:** Define stop conditions where the system must admit identity-safe output was not achieved.

### Task 6: Add controlled benchmark

**Files:**
- Create: `docs/TEST_PLAN.md`

**Interfaces:**
- Consumes: 20 real cover jobs.
- Produces: route-level identity pass rate, pose-risk failure rate, first-pass usable rate, title/evidence accuracy, rework count.

- [ ] **Step 1:** Define 20-job test matrix across LOW/MEDIUM/HIGH pose deltas and multiple vehicle/product types.
- [ ] **Step 2:** Define required record fields and acceptance thresholds.
- [ ] **Step 3:** Define V0.2 promotion/rollback criteria.

### Task 7: Update repository entry documentation

**Files:**
- Modify: `README.md`

**Interfaces:**
- Consumes: completed V0.1 files.
- Produces: a clear entry path for ChatGPT use and repository iteration.

- [ ] **Step 1:** Explain the new identity-route architecture.
- [ ] **Step 2:** Document the exact ChatGPT conversation input sequence.
- [ ] **Step 3:** Explain the hard product limit: arbitrary pose generation and exact face lock cannot both be guaranteed by prompt alone.
- [ ] **Step 4:** Link to benchmark and V0.2 criteria.

### Task 8: Repository verification

**Files:**
- Verify: all files above.

**Interfaces:**
- Consumes: feature branch.
- Produces: auditable PR with no placeholders or internal contradictions.

- [ ] **Step 1:** Compare `main...feature/chatgpt-identity-lock-v0.1` and confirm only intended files changed.
- [ ] **Step 2:** Inspect the PR patch for unsupported parameter claims, TODO/TBD placeholders, and contradictory identity thresholds.
- [ ] **Step 3:** Check existing repository CI/status if available.
- [ ] **Step 4:** Open PR with design rationale, known limitations, benchmark gate, and rollback conditions.
