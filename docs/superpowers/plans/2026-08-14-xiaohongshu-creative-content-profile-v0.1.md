# Xiaohongshu Creative Content Profile V0.1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Onboard `66Workshop/66XiaohongshuIPcover` as a governed `creative_content` repository while preserving the existing Identity-Lock Skill and enforcing identity/source/typography/promotion boundaries.

**Architecture:** Keep the existing Skill and repository validators as the domain implementation. Add a narrow governance layer: immutable Core fixture snapshots, Core lock, creative boundary, focused fail-closed tests, and a stable `governance-ci` wrapper. Feature branches remain autonomous; Human Signed Approval is required only when promoting the exact GREEN candidate into protected `main`.

**Tech Stack:** Python 3.11 stdlib, `unittest`, JSON, GitHub Actions on `ubuntu-latest`, existing repository validators.

## Global Constraints

- Production repository path is `66Workshop/66XiaohongshuIPcover`.
- Preserve public visibility for V0.1.
- Pin Core exactly to `ca393246b5bc05d4896945d5bda8896506d870d1`.
- Task fixture Git blob must equal `cecd362a88d4f494e7dc7d33fc2e93e5d05a660c`.
- Approval fixture Git blob must equal `809b76c1ff59efb6fbee922e28e5d4af5bfd36e5`.
- Do not redesign `SKILL.md`, prompts, approved assets, examples, schemas, or layout templates.
- Original high-resolution identity sources must not enter this public repository.
- Font binaries must not be added or redistributed.
- Route C / generated identity-reference output remains candidate-only.
- Identity-critical trusted output requires human QA.
- Third-party generation API automation remains disabled.
- Self-hosted runners remain disabled.
- Agent iteration remains autonomous on non-protected feature branches/review-only PRs.
- Human Signed Approval gates promotion/merge only.
- Core Registry registration is a **separate subsystem**. Generate its plan only after this repository has a real squash merge SHA and real Ruleset ID; do not guess those values here.

---

### Task 1: One-time Organization + Golden Governance bootstrap

**Files:**
- No repository content files changed.
- Admin operation only.

**Interfaces:**
- Consumes: `Simon66-workshop/66XiaohongshuIPcover` main `3b7ae1355fd5b68a3c34e8e3e4ace59efabba848` with successful `validate` GitHub Actions check.
- Produces: `66Workshop/66XiaohongshuIPcover`, public, squash-only, protected main, feature-branch autonomy preserved.

- [ ] **Step 1: Transfer repository into the Organization**

Run:

```bash
gh api --method POST repos/Simon66-workshop/66XiaohongshuIPcover/transfer \
  -f new_owner=66Workshop
```

Expected: `66Workshop/66XiaohongshuIPcover` resolves and `.visibility == "public"`.

- [ ] **Step 2: Verify the existing check before requiring it**

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

- [ ] **Step 3: Install bootstrap Golden Governance**

Create/update repository Ruleset `protect-main-golden-governance` with:

```json
{
  "target": "branch",
  "enforcement": "active",
  "bypass_actors": [],
  "conditions": {"ref_name": {"include": ["~DEFAULT_BRANCH"], "exclude": []}},
  "rules": [
    {"type": "deletion"},
    {"type": "non_fast_forward"},
    {"type": "pull_request", "parameters": {
      "allowed_merge_methods": ["squash"],
      "dismiss_stale_reviews_on_push": false,
      "require_code_owner_review": false,
      "require_last_push_approval": false,
      "required_approving_review_count": 0,
      "required_review_thread_resolution": true
    }},
    {"type": "required_status_checks", "parameters": {
      "do_not_enforce_on_create": false,
      "required_status_checks": [{"context": "validate", "integration_id": 15368}],
      "strict_required_status_checks_policy": true
    }}
  ]
}
```

Also set repository merge settings to squash-only, auto-merge off, delete branch on merge.

- [ ] **Step 4: Verify main protection and Agent Autonomy**

Run:

```bash
gh api repos/66Workshop/66XiaohongshuIPcover/rules/branches/main
gh api repos/66Workshop/66XiaohongshuIPcover/rules/branches/feature/chatgpt-identity-lock-v0.1
```

Expected:

```text
main: deletion + non_fast_forward + pull_request + required_status_checks
feature/chatgpt-identity-lock-v0.1: []
```

---

### Task 2: Intentional RED for the Creative Content governance contract

**Files:**
- Create: `tests/test_creative_governance.py`
- Create: `scripts/validate_creative_governance.py`

**Interfaces:**
- Consumes: existing person/visual manifests.
- Produces: `validate_creative_governance(root_dir: str | Path = ".") -> dict`.

- [ ] **Step 1: Write failing tests first**

`tests/test_creative_governance.py` must import:

```python
from scripts.validate_creative_governance import validate_creative_governance
```

Positive contract:

```python
result = validate_creative_governance(sandbox)
self.assertTrue(result["ok"], result["errors"])
self.assertEqual(result["profile"], "creative_content")
```

Negative cases must mutate sandbox copies and assert `ok is False` for each of these independently:

```text
pinned_core_ref drift
one-byte task fixture drift
one-byte approval fixture drift
profile drift
public_repo_original_identity_source_allowed=true
repo_identity_assets not derivative_preview_only
human_identity_qa_required=false
generated_identity_reference_output not candidate_only
typography_binary_redistribution_allowed=true
third_party_generation_api_enabled=true
self_hosted_enabled=true
person role not identity_reference_derivative
missing face_no_redraw
missing identity_lock
missing no_beautify
typography role not style_reference_only
missing do_not_treat_as_redistributable_font_file
forbidden governance keys: private_key/privatekey/pat/token/secret
```

- [ ] **Step 2: Verify setup RED**

Run:

```bash
python -m unittest tests.test_creative_governance -v
```

Expected: FAIL because the implementation module/governance assets are incomplete.

- [ ] **Step 3: Add minimal fail-closed module shell**

Use exactly:

```python
from pathlib import Path


def validate_creative_governance(root_dir: str | Path = ".") -> dict:
    return {
        "ok": False,
        "errors": ["creative governance assets missing"],
        "profile": None,
    }
```

- [ ] **Step 4: Verify formal RED is governance-specific**

Run the same unittest command.

Expected: FAIL due to missing/incomplete governance assets, with no import or syntax error.

- [ ] **Step 5: Commit RED**

```bash
git add tests/test_creative_governance.py scripts/validate_creative_governance.py
git commit -m "test: define creative content governance contract"
```

---

### Task 3: Immutable Core provenance + Creative boundary + GREEN

**Files:**
- Create: `governance/core-lock.json`
- Create: `governance/creative-boundary.json`
- Create: `governance/core-fixtures/task-contract-v0.1.json`
- Create: `governance/core-fixtures/approval-contract-v0.2.json`
- Modify: `scripts/validate_creative_governance.py`

**Interfaces:**
- Consumes: trusted Core commit and existing repository asset manifests.
- Produces: fail-closed governance validator with byte-level provenance.

- [ ] **Step 1: Write `governance/core-lock.json` exactly**

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

- [ ] **Step 2: Write `governance/creative-boundary.json` exactly**

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

- [ ] **Step 3: Vendor Core fixtures byte-for-byte**

Run:

```bash
mkdir -p governance/core-fixtures

gh api -H 'Accept: application/vnd.github.raw+json' \
  'repos/66Workshop/66-ai-workflow-core/contents/fixtures/task-contract-v0.1.json?ref=ca393246b5bc05d4896945d5bda8896506d870d1' \
  > governance/core-fixtures/task-contract-v0.1.json

gh api -H 'Accept: application/vnd.github.raw+json' \
  'repos/66Workshop/66-ai-workflow-core/contents/fixtures/approval-contract-v0.2.json?ref=ca393246b5bc05d4896945d5bda8896506d870d1' \
  > governance/core-fixtures/approval-contract-v0.2.json

git hash-object governance/core-fixtures/task-contract-v0.1.json
git hash-object governance/core-fixtures/approval-contract-v0.2.json
```

Expected hashes, in order:

```text
cecd362a88d4f494e7dc7d33fc2e93e5d05a660c
809b76c1ff59efb6fbee922e28e5d4af5bfd36e5
```

- [ ] **Step 4: Implement the validator**

Use Git blob hashing:

```python
def git_blob_sha(path: Path) -> str:
    data = path.read_bytes()
    header = f"blob {len(data)}\0".encode("utf-8")
    return hashlib.sha1(header + data).hexdigest()
```

The validator must verify exact Core ref/profile/blobs, every Creative boundary value, person derivative roles + identity constraints, typography style-reference role + redistribution guard, and recursively reject governance keys `private_key`, `privatekey`, `pat`, `token`, `secret`.

Return shape is always:

```python
{"ok": bool, "errors": list[str], "profile": str | None}
```

- [ ] **Step 5: GREEN new tests and all old tests**

Run:

```bash
python -m unittest tests.test_creative_governance -v
python -m unittest discover -s tests -v
python scripts/validate_repo.py
```

Expected: all unit tests PASS and repository prints `VALID`.

- [ ] **Step 6: Commit GREEN**

```bash
git add governance scripts/validate_creative_governance.py tests/test_creative_governance.py
git commit -m "feat: add Creative Content Profile V0.1 governance"
```

---

### Task 4: Stable `governance-ci` + immutable GitHub Actions

**Files:**
- Modify: `.github/workflows/validate.yml`
- Create: `.github/workflows/governance-ci.yml`

**Interfaces:**
- Consumes: existing repository checks + Creative governance validator.
- Produces: stable required status `governance-ci`.

- [ ] **Step 1: Pin existing workflow Actions**

Replace moving tags with:

```yaml
actions/checkout@11d5960a326750d5838078e36cf38b85af677262
actions/setup-python@a26af69be951a213d495a4c3e4e4022e16d87065
```

Checkout must include:

```yaml
with:
  persist-credentials: false
```

- [ ] **Step 2: Create `governance-ci.yml`**

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

- [ ] **Step 3: Push and require both checks to succeed once**

Expected candidate checks:

```text
validate = completed/success
governance-ci = completed/success
```

- [ ] **Step 4: Promote the Ruleset required check from `validate` to `governance-ci`**

Only after `governance-ci` has a real successful check-run, update the existing Ruleset required status to:

```json
{"context": "governance-ci", "integration_id": 15368}
```

Re-read main effective rules and require strict=true.

- [ ] **Step 5: Commit CI hardening**

```bash
git add .github/workflows
git commit -m "ci: add hosted creative governance gate"
```

---

### Task 5: Durable P1 task → red-team → Promotion Ready → one Human Gate

**Files:**
- Create: `tasks/xiaohongshu-creative-content-profile-v0.1.json`

**Interfaces:**
- Consumes: final candidate with real GREEN checks.
- Produces: exact frozen promotion candidate.

- [ ] **Step 1: Create durable P1 task**

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

- [ ] **Step 2: Fresh current-head CI**

After the task commit, do not reuse earlier GREEN checks. Require the new exact head to have:

```text
governance-ci = completed/success
```

- [ ] **Step 3: Red-team the changed-file surface**

Allowed onboarding files only:

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

Any onboarding diff touching existing original/derivative images, successful example images, prompts, `SKILL.md`, job schema, or existing business copy is a red-team failure.

- [ ] **Step 4: Verify governance/autonomy**

Require:

```text
main = protected by deletion + non_fast_forward + pull_request + strict governance-ci
implementation feature branch effective rules = []
self-hosted = absent
review threads = 0
```

- [ ] **Step 5: Resolve exact PR number and freeze exact head**

Run on the implementation branch:

```bash
PR_NUMBER=$(gh pr list \
  --repo 66Workshop/66XiaohongshuIPcover \
  --head governance/creative-content-profile-v0.1 \
  --state open \
  --json number \
  --jq '.[0].number')

EXACT_SHA=$(gh pr view "$PR_NUMBER" \
  --repo 66Workshop/66XiaohongshuIPcover \
  --json headRefOid \
  --jq '.headRefOid')

printf 'PR_NUMBER=%s\nEXACT_SHA=%s\n' "$PR_NUMBER" "$EXACT_SHA"
```

Expected: one real open PR number and one 40-hex current head SHA. Mark the PR Promotion Ready and make no further commit unless a defect is found.

- [ ] **Step 6: Human Signed Approval only now**

Create append-only tag using real runtime values:

```bash
TIMESTAMP=$(date -u +%Y%m%dT%H%M%SZ)
TAG="approval/xiaohongshu-creative-content-profile-v0.1/pr-${PR_NUMBER}/${EXACT_SHA}/attempt-${TIMESTAMP}"
printf '%s\n' "$TAG"
```

The approval transaction must verify:

```text
subject SHA = EXACT_SHA
tagger email = 188361883@qq.com
GitHub verified = true
GitHub reason = valid
```

- [ ] **Step 7: Expected-head squash merge**

Run:

```bash
gh api --method PUT \
  "repos/66Workshop/66XiaohongshuIPcover/pulls/${PR_NUMBER}/merge" \
  -f merge_method=squash \
  -f sha="$EXACT_SHA"
```

Expected: merge succeeds only if the PR head still equals `EXACT_SHA`.

- [ ] **Step 8: Post-merge evidence**

Read the returned real merge SHA into `MERGE_SHA`, then require:

```bash
gh api "repos/66Workshop/66XiaohongshuIPcover/commits/${MERGE_SHA}/check-runs?per_page=100"
```

Expected: merge-head `governance-ci=completed/success`.

This completes repository onboarding.

## Follow-up subsystem

After Task 5 completes, create a **new** plan for Core Registry registration using the actual `MERGE_SHA` and actual Xiaohongshu repository Ruleset ID. That plan must independently run Core RED→GREEN and require Human Signed Approval only at Core promotion. It is intentionally not specified with guessed IDs or SHAs here.
