# WORKFLOW — 66Workshop ChatGPT Cover Identity-Lock V0.1

## 1. Objective

Run a repeatable ChatGPT-native cover workflow that keeps the authorized person identity stable while preserving real vehicle/product evidence and producing a strong 3:4 cover.

## 2. State machine

### STATE 0 — PREFLIGHT

Before image creation:

1. Read the requested title/topic.
2. Inspect all uploaded images.
3. Assign one primary role to each image.
4. Select `PERSON_IDENTITY_PRIMARY`.
5. Select up to two `PERSON_IDENTITY_SECONDARY` images only if useful.
6. Identify vehicle/product evidence images.
7. Classify pose delta as LOW / MEDIUM / HIGH.
8. Check whether any P0 evidence is missing.

If blocked, do not generate. Ask only for the missing critical asset.

### STATE 1 — ROUTE_SELECT

Select the safest route that can satisfy the brief:

1. `PIXEL_LOCK_COMPOSITE`
2. `SOURCE_EDIT_MINIMAL`
3. `GENERATIVE_IDENTITY_REFERENCE`

Never select Route C just because it is more flexible visually.

### STATE 2 — COMPOSITION_PLAN

Create a short internal composition contract:

```text
CANVAS: 3:4
LAYOUT: P01/P02/P03/P04
PERSON: left/right/center, target % of frame
VEHICLE: position + target %
PRODUCT EVIDENCE: position + size
TITLE: top/side, 1–2 lines
SAFE FACE AREA: no text/product overlap
SAFE VEHICLE AREA: preserve lights/wheels/badges
```

The composition should adapt to the real person source rather than forcing the person to adapt to an arbitrary poster pose.

### STATE 3 — IMAGE_CREATE_OR_EDIT

Use a role-explicit instruction.

Core instruction logic:

- identify the primary identity source by role
- state that the same authorized person must remain the person in the output
- state that the face/head is not a style target and must not be reinterpreted
- state what may change: background, crop, placement, body context, contact shadows, supporting composition
- state which images are factual vehicle/product evidence
- state which image is typography style only
- state the target 3:4 layout

For Route A:

- compose around the real person source
- preserve head/face identity as-is as much as the tool allows
- keep pose changes LOW

For Route B:

- edit from the real person source rather than blank-canvas recreation
- protect head/face identity
- modify the smallest region necessary for torso/arm/body adaptation

For Route C:

- one primary identity source, max two secondary identity sources
- produce a candidate, not an automatic pass
- avoid dramatic head-angle or expression changes

### STATE 4 — QA_GATE

Compare the candidate against the source assets.

Order:

1. Identity
2. Vehicle
3. Product evidence
4. Title text
5. Layout
6. Brand language

A P0 failure stops acceptance even if the cover is visually strong.

### STATE 5 — REPAIR_OR_FALLBACK

Repair the smallest failing region.

Rules:

- wrong text → text-only repair
- weak background → background-only repair
- vehicle drift → restore vehicle evidence or reduce unsupported area
- product drift → restore product evidence or reduce unsupported detail
- identity drift → do NOT keep locally regenerating the face; reduce pose/reference complexity or fall back to a safer route

Identity fallback sequence:

```text
C -> B -> A
B -> A
A -> choose closer real pose asset
```

Two identity failures on the same route = mandatory route change or source change.

### STATE 6 — RECORD

Record:

```json
{
  "identity_route": "PIXEL_LOCK_COMPOSITE | SOURCE_EDIT_MINIMAL | GENERATIVE_IDENTITY_REFERENCE",
  "pose_delta": "LOW | MEDIUM | HIGH",
  "primary_identity_asset": "asset-id-or-upload-index",
  "secondary_identity_assets": [],
  "vehicle_evidence": [],
  "product_evidence": [],
  "identity_score": 1,
  "identity_human_pass": false,
  "vehicle_pass": false,
  "product_pass": false,
  "title_pass": false,
  "layout_pass": false,
  "rework_count": 0,
  "failure_reason": ""
}
```

## 3. Pose adaptation policy

### LOW

Allowed target changes:

- crop
- position
- scale
- mild torso lean illusion
- minor hand visibility change
- background integration

Route A preferred.

### MEDIUM

Allowed only with close source support:

- arm repositioning
- torso posture change
- standing/seated adaptation when head angle remains similar

Route B preferred.

### HIGH

Examples:

- frontal to full profile
- dramatic high/low angle
- large head rotation
- dramatic expression synthesis
- extreme foreshortening

Do not promise identity lock. Prefer another real authorized person source with a closer pose.

## 4. Reference-count policy

More references are not automatically safer.

Default:

- 1 primary person identity image
- 0–2 secondary identity images
- 1–3 vehicle/product evidence images relevant to visible details
- 1 font-style reference
- 0–1 layout reference

If identity drifts, reduce identity reference count before adding more references.

## 5. Prompt policy

Use positive structural instructions first.

Good:

- “Image 1 is the only primary identity source.”
- “Keep the same authorized person; preserve facial proportions and identity cues.”
- “Image 4 is typography style only and must not affect the person.”

Weak as a standalone control:

- “don’t change the face”
- “negative prompt: no fake face”
- “100% lock face”

Those phrases may remain as reinforcement, but they are not the control system.

## 6. Repair granularity

Never regenerate the entire cover when the error is local and the person is already correct.

Examples:

- correct person + wrong Chinese character → repair title only
- correct person + wrong caliper logo → repair/replace product area only
- correct person + weak shadows → repair environment only

This reduces the chance of destroying a previously successful identity result.

## 7. Existing controlled-production loop retained

The previous repository workflow remains valid and is kept:

- route content to `P01_DATA_CONFLICT`, `P02_BEFORE_AFTER`, `P03_VEHICLE_DECISION`, or `P04_PRODUCT_VALUE`
- record successful human-approved outputs in `examples/successful/`
- record failure modes such as `face_drift`, `car_drift`, `product_hallucination`, `title_error`, `layout_overload`, `weak_hook`, and `fake_evidence`
- review every 20 real jobs using measured failure and rework data

## 8. Output acceptance

A candidate can be marked usable only when:

- identity = `IDENTITY_4` or `IDENTITY_5`
- human owner approves identity
- vehicle evidence passes
- product evidence passes
- title passes
- layout is usable at thumbnail size

A visually attractive lookalike is a failed candidate.
