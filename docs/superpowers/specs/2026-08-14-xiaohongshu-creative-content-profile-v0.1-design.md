# Xiaohongshu Creative Content Profile V0.1 — Design Spec

Status: approved

## Goal

Onboard `66XiaohongshuIPcover` as the first `creative_content` consumer of `66Workshop/66-ai-workflow-core` without weakening the existing Identity-Lock Skill, without putting original identity source assets or font binaries into GitHub, and without turning ordinary Agent iteration into a human-gated workflow.

## Repository ownership and governance

The repository must be transferred from `Simon66-workshop/66XiaohongshuIPcover` to `66Workshop/66XiaohongshuIPcover` before production onboarding. Preserve current public visibility for V0.1. After transfer, install main-only Golden Governance:

- deletion blocked
- non-fast-forward / force-push blocked
- pull request required
- approvals = 0
- review threads must resolve
- squash-only merge
- strict required status check
- bypass actors = 0
- non-protected feature branches keep effective rules `[]`
- self-hosted remains disabled

During bootstrap, the existing successful GitHub Actions check `validate` is the temporary required check. The implementation may later introduce a stable `governance-ci` wrapper, but it must not remove the repository's existing unit/repo/job validation coverage.

## Agent Autonomy

Governance must preserve Agent autonomy on non-protected feature branches and review-only PRs.

Agent may autonomously:

- create/update feature branches
- create Draft/review-only PRs
- commit and push
- run RED→GREEN TDD
- repair CI failures
- update task/evidence state
- perform machine red-team review
- iterate until the exact candidate head is machine-green

Human Signed Approval gates **promotion/merge into protected `main`**, not ordinary Agent iteration. Any commit after signing makes the prior approval stale, but Agent may continue iterating and request a fresh approval only when a new exact GREEN candidate is ready for promotion.

## Core provenance

Pin to trusted Core commit:

`ca393246b5bc05d4896945d5bda8896506d870d1`

Vendored Core fixtures must be byte-identical to:

- Task fixture blob: `cecd362a88d4f494e7dc7d33fc2e93e5d05a660c`
- Approval fixture blob: `809b76c1ff59efb6fbee922e28e5d4af5bfd36e5`

No runtime cross-private-repository download and no PAT is required. V0.1 uses immutable Core ref + vendored snapshot + blob lock.

## Creative content boundary

Create a machine-readable `governance/creative-boundary.json` with the following invariants:

- `profile = creative_content`
- `identity_source_policy = original_authorized_source_required_for_identity_critical_production`
- `repo_identity_assets = derivative_preview_only`
- `generated_identity_reference_output = candidate_only`
- `human_identity_qa_required = true`
- `vehicle_and_part_evidence_required = true`
- `typography_binary_redistribution_allowed = false`
- `third_party_generation_api_enabled = false`
- `public_repo_original_identity_source_allowed = false`
- `self_hosted_enabled = false`

These are governance claims, not image-model capability claims.

## Existing Skill remains authoritative

Do not rewrite or replace `SKILL.md`, its A/B/C identity routing, pose-risk routing, source-role binding, QA gates, fallback strategy, or benchmark rules as part of V0.1 governance onboarding.

The existing repository already enforces important asset semantics:

- person assets use role `identity_reference_derivative`
- identity constraints include `face_no_redraw`, `identity_lock`, `no_beautify`
- original authorized source is retained for pixel-locked production compositing
- typography is `style_reference_only`
- typography references include `do_not_treat_as_redistributable_font_file`

Creative Content Profile must preserve and machine-check these semantics rather than inventing a second image-generation system.

## Trusted asset lifecycle

Repository lifecycle remains:

`candidate/review-only asset → machine validation → human visual/identity QA → Human Signed Approval for promotion → protected main trusted asset`

Route C / generative identity output is always candidate-only. It cannot self-promote to trusted production asset.

For identity-critical final output, human QA is mandatory even if all machine checks are green.

## Evidence integrity

Machine validation must fail closed on at least:

- Core ref drift
- fixture byte drift
- wrong profile
- public repo allowing original identity sources
- person assets no longer marked derivative previews
- missing identity constraints
- typography redistribution guard removed
- `human_identity_qa_required=false`
- `generated_identity_reference_output` changed from candidate-only
- `third_party_generation_api_enabled=true`
- `self_hosted_enabled=true`
- hidden secret/PAT/private-key fields in governance files

## CI hardening

Keep GitHub-hosted execution only. Pin GitHub Actions to immutable SHAs and set checkout `persist-credentials: false`.

Current tag resolutions captured for V0.1 planning:

- `actions/checkout@v4` → `11d5960a326750d5838078e36cf38b85af677262`
- `actions/setup-python@v5` → `a26af69be951a213d495a4c3e4e4022e16d87065`

The stable required check after implementation should be `governance-ci`, and it must include the existing repository checks rather than bypassing them:

- Python unit tests
- repository asset/structure validation
- all job validation
- JSON syntax validation
- Creative Content/Core consumer governance validation

## Scope exclusions

V0.1 does not:

- change cover visual templates
- redesign the user's identity images
- upload original high-resolution identity sources to GitHub
- distribute font files
- automate publication to Xiaohongshu/Douyin
- call third-party image-generation APIs
- claim deterministic 100% face locking from native generative image editing
- enable self-hosted runners
- change existing approved case imagery or business copy

## Promotion acceptance criteria

A candidate is Promotion Ready only when all are true:

- repository is owned by `66Workshop`
- main Golden Governance is active and bypass-free
- feature branch effective rules are `[]`
- Core ref and fixture blobs are immutable and exact
- Creative boundary passes all positive/negative tests
- existing unit/repo/job/JSON checks pass
- `governance-ci = completed/success` on the exact candidate head
- no self-hosted runner is present
- Human Signed Approval binds the exact GREEN head before squash merge

## Post-merge

After merge-head CI succeeds, register `66Workshop/66XiaohongshuIPcover` in Core `registry/consumers.json` as:

- profile: `creative_content`
- status: `active`
- consumer_ref: `main`
- trusted consumer merge SHA: actual squash merge SHA
- required check: `governance-ci`
- human gate: `solo_owner_ssh_signed_tag`
- Golden Governance ruleset: actual repository ruleset id
- self-hosted: false

The Core Registry update follows the same Agent-autonomous RED→GREEN process and requires Human Signed Approval only at Core promotion.