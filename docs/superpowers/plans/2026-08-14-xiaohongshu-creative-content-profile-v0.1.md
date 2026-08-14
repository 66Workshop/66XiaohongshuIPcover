# Xiaohongshu Creative Content Profile V0.1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Onboard `66Workshop/66XiaohongshuIPcover` as an active `creative_content` Core consumer while preserving the existing Identity-Lock Skill and enforcing identity/source/typography/promotion boundaries.

**Architecture:** Keep the existing Skill and repository validators as the domain implementation. Add a small governance layer consisting of immutable Core fixture snapshots, a Core lock, a creative boundary file, a focused validator/test suite, and a stable `governance-ci` workflow that wraps the existing validation. Feature branches remain autonomous; Human Signed Approval is required only for promotion into protected `main`.

**Tech Stack:** Python 3.11 stdlib, `unittest`, GitHub Actions on `ubuntu-latest`, JSON governance files, existing repository validators.

## Global Constraints

- Repository production path: `66Workshop/66XiaohongshuIPcover`.
- Preserve public visibility for V0.1.
- Pin Core ref exactly to `ca393246b5bc05d4896945d5bda8896506d870d1`.
- Task fixture Git blob must equal `cecd362a88d4f494e7dc7d33fc2e93e5d05a660c`.
- Approval fixture Git blob must equal `809b76c1ff59efb6fbee922e28e5d4af5bfd36e5`.
- Existing `SKILL.md`, prompts, approved assets, examples, and layout templates are not redesigned by this plan.
- Original high-resolution identity sources must not be added to this public repository.
- Font binaries must not be added or redistributed.
- Route C / generative identity output remains candidate-only.
- Identity-critical trusted output requires human QA.
- Third-party image-generation API automation remains disabled.
- Self-hosted runners remain disabled.
- Agent iteration remains autonomous on non-protected branches/review-only PRs.
- Human Signed Approval gates promotion/merge only.
- Repository main Golden Governance must be active, bypass-free, squash-only.

---

### Task 1: One-time Organization + Golden Governance bootstrap

**Files:**
- No repository content files changed.
- Admin operation only.

**Interfaces:**
- Consumes: existing personal repository `Simon66-workshop/66XiaohongshuIPcover` at main `3b7ae1355fd5b68a3c34e8e3e4ace59efabba848`.
- Produces: `66Workshop/66XiaohongshuIPcover`, public, squash-only, main-only Golden Governance with strict existing `validate` check during bootstrap.

- [ ] **Step 1: Transfer repository into the Organization**

Run:

```bash
gh api --method POST repos/Simon66-workshop/66XiaohongshuIPcover/transfer \
  -f new_owner=66Workshop
```

Expected: `66Workshop/66XiaohongshuIPcover` becomes accessible and repository visibility remains `public`.

- [ ] **Step 2: Verify current main CI before requiring it**

Run:

```bash
MAIN_SHA=$(gh api repos/66Workshop/66XiaohongshuIPcover/commits/main --jq '.sha')
gh api "repos/66Workshop/66XiaohongshuIPcover/commits/${MAIN_SHA}/check-runs?per_page=100" \
  --jq '.check_runs[] | [.name,.status,.conclusion,.app.id] | @tsv'
```

Expected line:

```text
validate	completed	success	15368
```

- [ ] **Step 3: Install main-only Golden Governance**

Required source policy:

```json
{
  "name": "protect-main-golden-governance",
  "target": "branch",
  "enforcement": "active",
  "bypass_actors": [],
  "conditions": {
    "ref_name": {
      "include": ["~DEFAULT_BRANCH"],
      "exclude": []
    }
  },
  "rules": [
    {"type": "deletion"},
    {"type": "non_fast_forward"},
    {
      "type": "pull_request",
      "parameters": {
        "allowed_merge_methods": ["squash"],
        "dismiss_stale_reviews_on_push": false,
        "require_code_owner_review": false,
        "require_last_push_approval": false,
        "required_approving_review_count": 0,
        "required_review_thread_resolution": true
      }
    },
    {
      "type": "required_status_checks",
      "parameters": {
        "do_not_enforce_on_create": false,
        "required_status_checks": [
          {"context": "validate", "integration_id": 15368}
        ],
        "strict_required_status_checks_policy": true
      }
    }
  ]
}
```

Expected: main effective rules include deletion, non-fast-forward, PR, strict required status; bypass actors = 0.

- [ ] **Step 4: Verify Agent Autonomy on an existing feature branch**

Run:

```bash
gh api repos/66Workshop/66XiaohongshuIPcover/rules/branches/feature/chatgpt-identity-lock-v0.1
```

Expected:

```json
[]
```

- [ ] **Step 5: Record bootstrap evidence outside protected main**

No content mutation is required. Save machine evidence in the implementation PR body when it is opened.

---

### Task 2: Add intentional RED Core-consumer governance tests

**Files:**
- Create: `tests/test_creative_governance.py`
- Create later in Task 3: `scripts/validate_creative_governance.py`
- Create later in Task 3: `governance/core-lock.json`
- Create later in Task 3: `governance/creative-boundary.json`
- Create later in Task 3: `governance/core-fixtures/task-contract-v0.1.json`
- Create later in Task 3: `governance/core-fixtures/approval-contract-v0.2.json`

**Interfaces:**
- Consumes: existing `assets/manifests/person_assets.json`, `assets/manifests/visual_assets.json`.
- Produces: failing tests that describe the creative governance contract before implementation exists.

- [ ] **Step 1: Write the failing governance test module**

Create `tests/test_creative_governance.py` with tests that import:

```python
from scripts.validate_creative_governance import validate_creative_governance
```

Required assertions:

```python
self.assertTrue(result["ok"], result["errors"])
self.assertEqual(result["profile"], "creative_content")
```

Sandbox negative cases must mutate copies and assert `ok is False` for:

```text
pinned_core_ref drift
one-byte task fixture drift
one-byte approval fixture drift
profile != creative_content
public_repo_original_identity_source_allowed = true
repo_identity_assets != derivative_preview_only
human_identity_qa_required = false
generated_identity_reference_output != candidate_only
typography_binary_redistribution_allowed = true
third_party_generation_api_enabled = true
self_hosted_enabled = true
person asset role != identity_reference_derivative
missing face_no_redraw / identity_lock / no_beautify
typography role != style_reference_only
missing do_not_treat_as_redistributable_font_file
forbidden governance keys: private_key, pat, token, secret
```

- [ ] **Step 2: Run the RED test**

Run:

```bash
python -m unittest tests.test_creative_governance -v
```

Expected: FAIL because `scripts.validate_creative_governance` does not exist yet.

- [ ] **Step 3: Add minimal module shell only**

Create `scripts/validate_creative_governance.py` exposing exactly:

```python
def validate_creative_governance(root_dir: str | Path = ".") -> dict:
    return {"ok": False, "errors": ["creative governance assets missing"], "profile": None}
```

- [ ] **Step 4: Re-run RED and verify failure is governance-specific**

Run:

```bash
python -m unittest tests.test_creative_governance -v
```

Expected: tests fail because Core lock / fixtures / creative boundary are missing or invalid, not because of import/syntax errors.

- [ ] **Step 5: Commit RED evidence**

```bash
git add tests/test_creative_governance.py scripts/validate_creative_governance.py
git commit -m "test: define creative content governance contract"
```

---

### Task 3: Add immutable Core lock, fixtures, and creative boundary

**Files:**
- Create: `governance/core-lock.json`
- Create: `governance/creative-boundary.json`
- Create: `governance/core-fixtures/task-contract-v0.1.json`
- Create: `governance/core-fixtures/approval-contract-v0.2.json`
- Modify: `scripts/validate_creative_governance.py`

**Interfaces:**
- Consumes: Core commit `ca393246b5bc05d4896945d5bda8896506d870d1` and two exact fixture blobs.
- Produces: `validate_creative_governance(root_dir) -> {ok: bool, errors: list[str], profile: str | None}`.

- [ ] **Step 1: Write Core lock exactly**

Create `governance/core-lock.json`:

```json
{
  "schema_version": "0.1",
  "core_repository": "66Workshop/66-ai-workflow-core",
  "pinned_core_ref": "ca393246b5bc05d4896945d5bda8896506d870d1",
  "profile": "creative_content",
  "task_contract_version": "0.1",
  "approval_contract_version": "0.2",
  "task_fixture_blob": "cecd362a88d4f494e7dc7d33fc2e93e5d05a660c",
  "approval_fixture_blob": "809b76c1ff59efb6fbee922e28e5d4af5bfd36e5",
  "self_hosted_enabled": false
}
```

- [ ] **Step 2: Write creative boundary exactly**

Create `governance/creative-boundary.json`:

```json
{
  "schema_version": "0.1",
  "profile": "creative_content",
  "identity_source_policy": "original_authorized_source_required_for_identity_critical_production",
  "repo_identity_assets": "derivative_preview_only",
  "generated_identity_reference_output": "candidate_only",
  "human_identity_qa_required": true,
  "vehicle_and_part_evidence_required": true,
  "typography_binary_redistribution_allowed": false,
  "third_party_generation_api_enabled": false,
  "public_repo_original_identity_source_allowed": false,
  "self_hosted_enabled": false
}
```

- [ ] **Step 3: Vendor the two Core fixture files byte-for-byte**

Fetch from Core:

```bash
gh api -H 'Accept: application/vnd.github.raw+json' \
  'repos/66Workshop/66-ai-workflow-core/contents/fixtures/task-contract-v0.1.json?ref=ca393246b5bc05d4896945d5bda8896506d870d1' \
  > governance/core-fixtures/task-contract-v0.1.json

gh api -H 'Accept: application/vnd.github.raw+json' \
  'repos/66Workshop/66-ai-workflow-core/contents/fixtures/approval-contract-v0.2.json?ref=ca393246b5bc05d4896945d5bda8896506d870d1' \
  > governance/core-fixtures/approval-contract-v0.2.json
```

Verify Git blob IDs:

```bash
git hash-object governance/core-fixtures/task-contract-v0.1.json
git hash-object governance/core-fixtures/approval-contract-v0.2.json
```

Expected:

```text
cecd362a88d4f494e7dc7d33fc2e93e5d05a660c
809b76c1ff59efb6fbee922e28e5d4af5bfd36e5
```

- [ ] **Step 4: Implement focused validator**

`validate_creative_governance()` must:

```text
1. parse core-lock.json and creative-boundary.json
2. compute Git blob SHA1 for vendored fixtures
3. assert exact Core ref/profile/blob identities
4. assert all creative boundary fields exactly
5. inspect person_assets.json and require derivative role + identity constraints
6. inspect visual_assets.json and require typography style-reference role + redistribution guard
7. recursively reject governance keys private_key/privatekey/pat/token/secret
8. return fail-closed errors rather than silently normalizing bad data
```

Use this Git blob helper:

```python
def git_blob_sha(path: Path) -> str:
    data = path.read_bytes()
    header = f"blob {len(data)}\0".encode("utf-8")
    return hashlib.sha1(header + data).hexdigest()
```

- [ ] **Step 5: Run governance tests GREEN**

```bash
python -m unittest tests.test_creative_governance -v
```

Expected: all creative governance positive/negative tests PASS.

- [ ] **Step 6: Run existing repository tests to prove no Skill regression**

```bash
python -m unittest discover -s tests -v
python scripts/validate_repo.py
```

Expected: all existing tests PASS and repository prints `VALID`.

- [ ] **Step 7: Commit governance implementation**

```bash
git add governance scripts/validate_creative_governance.py tests/test_creative_governance.py
git commit -m "feat: add Creative Content Profile V0.1 governance"
```

---

### Task 4: Add stable governance-ci wrapper and immutable Actions

**Files:**
- Modify: `.github/workflows/validate.yml`
- Create: `.github/workflows/governance-ci.yml`

**Interfaces:**
- Consumes: existing unit/repo/job/JSON checks and new creative validator.
- Produces: stable required status `governance-ci` while keeping `validate` workflow coverage available during migration.

- [ ] **Step 1: Pin existing workflow Actions immutably**

Replace:

```yaml
actions/checkout@v4
actions/setup-python@v5
```

with:

```yaml
actions/checkout@11d5960a326750d5838078e36cf38b85af677262
actions/setup-python@a26af69be951a213d495a4c3e4e4022e16d87065
```

and add under checkout:

```yaml
with:
  persist-credentials: false
```

- [ ] **Step 2: Create `governance-ci.yml`**

Use:

```yaml
name: Governance CI

on:
  pull_request:
  push:
    branches:
      - main
  workflow_dispatch:

permissions:
  contents: read

jobs:
  governance-ci:
    runs-on: ubuntu-latest
    timeout-minutes: 15
    steps:
      - name: Checkout
        uses: actions/checkout@11d5960a326750d5838078e36cf38b85af677262
        with:
          persist-credentials: false

      - name: Setup Python
        uses: actions/setup-python@a26af69be951a213d495a4c3e4e4022e16d87065
        with:
          python-version: '3.11'

      - name: Unit tests
        run: python -m unittest discover -s tests -v

      - name: Validate repository assets and structure
        run: python scripts/validate_repo.py

      - name: Validate Creative Content governance
        run: python scripts/validate_creative_governance.py

      - name: Validate all jobs
        shell: bash
        run: |
          while IFS= read -r -d '' file; do
            python scripts/validate_job.py "$file"
          done < <(find jobs -name '*.json' -print0)

      - name: Validate JSON syntax
        shell: bash
        run: |
          while IFS= read -r -d '' file; do
            python -m json.tool "$file" >/dev/null
          done < <(find assets/manifests schemas jobs records governance -name '*.json' -print0)
```

- [ ] **Step 3: Push and verify both workflows GREEN on the candidate branch**

Expected check runs:

```text
validate = completed/success
governance-ci = completed/success
```

- [ ] **Step 4: Update Golden Governance required check from temporary `validate` to stable `governance-ci`**

After `governance-ci` has succeeded at least once, update the repository Ruleset required status check to:

```json
{"context":"governance-ci","integration_id":15368}
```

Then re-read main effective rules and verify strict=true.

- [ ] **Step 5: Commit CI hardening**

```bash
git add .github/workflows
git commit -m "ci: add hosted creative governance gate"
```

---

### Task 5: Durable P1 task, red-team audit, and Promotion Ready freeze

**Files:**
- Create: `tasks/xiaohongshu-creative-content-profile-v0.1.json`

**Interfaces:**
- Consumes: final machine-green implementation candidate.
- Produces: frozen P1 promotion candidate for Human Signed Approval.

- [ ] **Step 1: Create durable task snapshot**

```json
{
  "schema_version": "0.1",
  "task_id": "xiaohongshu-creative-content-profile-v0.1",
  "repository": "66Workshop/66XiaohongshuIPcover",
  "task_type": "creative_content_profile_onboarding",
  "risk_level": "P1",
  "status": "NEEDS_REVIEW",
  "required_checks": ["governance-ci"],
  "human_approval_required": true,
  "evidence": [
    "profile:creative_content",
    "core:66Workshop/66-ai-workflow-core@ca393246b5bc05d4896945d5bda8896506d870d1",
    "task_fixture_blob:cecd362a88d4f494e7dc7d33fc2e93e5d05a660c",
    "approval_fixture_blob:809b76c1ff59efb6fbee922e28e5d4af5bfd36e5",
    "boundary:DERIVATIVE_PREVIEW_ONLY=true",
    "boundary:HUMAN_IDENTITY_QA_REQUIRED=true",
    "boundary:FONT_BINARY_REDISTRIBUTION=false",
    "boundary:THIRD_PARTY_GENERATION_API=false",
    "boundary:SELF_HOSTED=false"
  ],
  "rollback": "Revert the Creative Content Profile onboarding while preserving the pre-existing Identity-Lock Skill and approved repository assets."
}
```

- [ ] **Step 2: Run fresh current-head CI**

Do not reuse the pre-task GREEN run. Required current-head result:

```text
governance-ci = completed/success
```

- [ ] **Step 3: Machine red-team changed-file surface**

Expected onboarding surface only:

```text
.github/workflows/validate.yml
.github/workflows/governance-ci.yml
docs/superpowers/specs/2026-08-14-xiaohongshu-creative-content-profile-v0.1-design.md
docs/superpowers/plans/2026-08-14-xiaohongshu-creative-content-profile-v0.1.md
governance/core-lock.json
governance/creative-boundary.json
governance/core-fixtures/task-contract-v0.1.json
governance/core-fixtures/approval-contract-v0.2.json
scripts/validate_creative_governance.py
tests/test_creative_governance.py
tasks/xiaohongshu-creative-content-profile-v0.1.json
```

Any modification to original authorized images, successful examples, prompts, `SKILL.md`, schemas/job logic, or existing business copy is a red-team failure for this onboarding.

- [ ] **Step 4: Verify main protection and feature-branch autonomy**

Expected:

```text
main effective rules = deletion + non_fast_forward + pull_request + required_status_checks
feature branch effective rules = []
```

- [ ] **Step 5: Freeze exact GREEN head and mark PR Promotion Ready**

Update PR body with exact SHA, check-run evidence, Core provenance, creative boundary, Agent Autonomy evidence, and known observations. Do not commit again after this point unless a machine/human review finds a defect.

- [ ] **Step 6: Human Signed Approval only now**

Create append-only SSH signed tag bound to exact PR head:

```text
approval/xiaohongshu-creative-content-profile-v0.1/pr-{PR}/{EXACT_SHA}/attempt-YYYYMMDDTHHMMSSZ
```

Required GitHub verification:

```text
verified=true
reason=valid
tagger_email=188361883@qq.com
```

- [ ] **Step 7: Expected-head squash merge**

```bash
gh pr merge <PR> --repo 66Workshop/66XiaohongshuIPcover --squash --match-head-commit <EXACT_SHA>
```

If head changed, stop and invalidate the approval.

- [ ] **Step 8: Post-merge CI**

Run/read merge SHA checks. Required:

```text
governance-ci = completed/success
```

Only this merge-head evidence completes repository onboarding.

---

### Task 6: Register the trusted creative consumer in Core

**Files in `66Workshop/66-ai-workflow-core`:**
- Modify: `registry/consumers.json`
- Modify: `scripts/validate-consumer-registry.py`
- Modify: `scripts/validate-core.sh`
- Create: `tasks/register-xiaohongshu-creative-content-consumer-v0.1.json`
- Create: `docs/superpowers/plans/2026-08-14-register-xiaohongshu-creative-content-consumer-v0.1.md`

**Interfaces:**
- Consumes: actual trusted squash merge SHA and actual Xiaohongshu Ruleset ID from Task 5.
- Produces: active `creative_content` consumer record in protected Core Registry.

- [ ] **Step 1: Intentional RED**

First change Core registry validator required consumer set to include:

```text
66Workshop/66XiaohongshuIPcover
```

without adding the record.

Run Core `governance-ci`.

Expected: FAIL specifically because required Core consumer is missing.

- [ ] **Step 2: Add actual consumer record**

Record must use runtime-resolved values from completed repository onboarding:

```json
{
  "repository": "66Workshop/66XiaohongshuIPcover",
  "profile": "creative_content",
  "status": "active",
  "default_branch": "main",
  "consumer_ref": "main",
  "consumer_merge_sha": "<actual 40-hex squash merge SHA from Task 5>",
  "pinned_core_ref": "ca393246b5bc05d4896945d5bda8896506d870d1",
  "required_checks": ["governance-ci"],
  "human_gate": "solo_owner_ssh_signed_tag",
  "golden_governance": {
    "status": "active_main_only",
    "ruleset_id": 1,
    "required_checks": ["governance-ci"]
  },
  "creative_boundary": {
    "repo_identity_assets": "derivative_preview_only",
    "generated_identity_reference_output": "candidate_only",
    "human_identity_qa_required": true,
    "typography_binary_redistribution_allowed": false,
    "third_party_generation_api_enabled": false,
    "public_repo_original_identity_source_allowed": false
  },
  "self_hosted_enabled": false
}
```

When executing, replace only `consumer_merge_sha` and `golden_governance.ruleset_id` with the actual machine-resolved values; do not guess them.

- [ ] **Step 3: GREEN + durable P1 task + red-team**

Run Core `governance-ci`, write durable P1 task, re-run fresh current-head CI, verify changed-file surface and Core main/feature autonomy.

- [ ] **Step 4: Human Signed Approval only at Core promotion**

Bind the exact GREEN Core registry head, squash merge with expected SHA, and require merge-head `governance-ci=success`.

- [ ] **Step 5: Detached completion receipt**

Write final promotion evidence to the merged PR conversation. Do not create an extra protected-main merge solely to change task status from `NEEDS_REVIEW` to `DONE`.
