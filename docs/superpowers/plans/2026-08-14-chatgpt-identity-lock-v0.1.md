# 66Workshop ChatGPT Cover Identity-Lock V0.1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Upgrade the existing 66Workshop Xiaohongshu cover workflow into a ChatGPT-native identity-preservation Skill that prioritizes the real authorized person over generative restyling, routes requests by pose risk, and rejects lookalike outputs.

**Architecture:** Keep `SKILL.md` as the operational entry point. Detailed contracts live in input assets, route/state machine, QA, failure fallback, benchmark, and a copy-ready ChatGPT prompt protocol. The system stays model-agnostic and does not invent unsupported image-model parameters.

**Tech Stack:** Markdown Skill instructions, existing GitHub-controlled asset manifests, existing job/record lifecycle, ChatGPT image creation/editing, human identity approval.

## Global Constraints

- Person identity fidelity is P0 and outranks layout aesthetics.
- Native ChatGPT image generation cannot be described as a mathematical/pixel identity guarantee.
- Use one primary identity anchor and at most two secondary anchors for generative identity reference.
- Prefer the least-generative route: `SOURCE_PRESERVE_COMPOSITE` → `SOURCE_EDIT_MINIMAL` → `GENERATIVE_IDENTITY_REFERENCE`.
- Route A means “maximize source preservation”; it is not a hard pixel lock.
- `IDENTITY_1`, `IDENTITY_2`, and `IDENTITY_3` are always rejected.
- Final production identity approval requires human owner review.
- Do not store or redistribute font files; font screenshots are style references only.
- Do not add third-party face-swap or training dependencies in V0.1.

---

### Task 1: Replace the main Skill with route-based identity control

**Files:** `SKILL.md`

- [x] Replace the current single-pass generation flow with the three identity routes and state-machine production flow.
- [x] Add strict role binding for every uploaded image.
- [x] Add pose-delta classification and a hard rule that HIGH pose deltas cannot be promised as identity-locked.
- [x] Add explicit retry/fallback rules and lookalike rejection.
- [x] Add links to detailed docs.

### Task 2: Define production input assets

**Files:** `docs/INPUT_SPEC.md`

- [x] Define preferred person-source set: one primary source plus optional secondary identity images.
- [x] Define green-screen, angle, sharpness, occlusion, expression, and pose requirements.
- [x] Define vehicle/product evidence requirements.
- [x] Define font-style reference limitations.
- [x] Define blocking conditions that force a safer pose or asset request instead of blind generation.

### Task 3: Define ChatGPT generation/editing workflow

**Files:** `docs/WORKFLOW.md`, `prompts/CHATGPT_IDENTITY_LOCK_PROTOCOL.md`

- [x] Implement `PREFLIGHT → ROUTE_SELECT → COMPOSITION_PLAN → IMAGE_CREATE_OR_EDIT → QA_GATE → REPAIR_OR_FALLBACK → RECORD`.
- [x] Add copy-ready prompt structure with positive constraints rather than relying on negative prompts.
- [x] Add a no-full-regeneration rule when only text or a localized non-face region fails.
- [x] Add the two-failures-then-fallback identity rule.

### Task 4: Add identity and evidence QA

**Files:** `docs/QA_CHECKLIST.md`

- [x] Define the facial geometry comparison rubric.
- [x] Set production pass threshold to `IDENTITY_4` or `IDENTITY_5` plus human approval.
- [x] Add vehicle/product/text/brand checks.
- [x] Add veto rules for wrong person, wrong model, fabricated product detail, and text errors.

### Task 5: Add failure routing and repair policy

**Files:** `docs/FAILURE_PLAYBOOK.md`

- [x] Map identity drift to reference reduction, pose reduction, source replacement, or route fallback.
- [x] Map vehicle/product drift to source anchoring or reduced visibility.
- [x] Map title failure to text-only repair.
- [x] Define stop conditions where the system must admit identity-safe output was not achieved.

### Task 6: Add controlled benchmark

**Files:** `docs/TEST_PLAN.md`

- [x] Define 20-job test matrix across LOW/MEDIUM/HIGH pose deltas and multiple vehicle/product types.
- [x] Define required record fields and acceptance thresholds.
- [x] Define V0.2 promotion/rollback criteria.

### Task 7: Update repository entry documentation

**Files:** `README.md`

- [x] Explain the new identity-route architecture.
- [x] Document the exact ChatGPT conversation input sequence.
- [x] Explain the hard product limit: arbitrary pose generation and exact face lock cannot both be guaranteed by prompt alone.
- [x] Link to benchmark and V0.2 criteria.

### Task 8: Repository verification

- [ ] Compare `main...feature/chatgpt-identity-lock-v0.1` and confirm only intended files changed.
- [ ] Inspect the PR patch for unsupported parameter claims, TODO/TBD placeholders, stale `PIXEL_LOCK_COMPOSITE` terminology, and contradictory identity thresholds.
- [ ] Check existing repository CI/status if available.
- [ ] Open PR with design rationale, known limitations, benchmark gate, and rollback conditions.
