# 66Workshop ChatGPT Cover Identity-Lock Skill V0.1 — Design

## 1. Goal

Build a reusable GitHub-hosted Skill for the normal ChatGPT image-creation conversation flow:

1. User uploads a cover title.
2. User uploads authorized 66Workshop IP/person images, vehicle photos, product/part photos, and font/style reference images.
3. ChatGPT assigns a strict role to each asset.
4. ChatGPT chooses the safest identity-preservation route before calling image creation/editing.
5. ChatGPT generates a 3:4 66Workshop cover.
6. ChatGPT performs identity, vehicle, product, text, and layout QA before calling the result usable.

Success is not “looks similar.” Success is “the same authorized person remains recognizably the same person, with no invented substitute face, under a repeatable production protocol.”

## 2. Product boundary

### FACT

- ChatGPT image creation/editing can use uploaded images as inputs and can edit existing images.
- The ChatGPT image editor is generative. A selected or protected-looking area is not a cryptographic or guaranteed pixel-level identity lock.
- A reasoning model can plan prompts, route inputs, and perform visual QA, but it is not itself a face-identity enforcement engine.

### Consequence

V0.1 MUST NOT claim that a prompt, negative prompt, or “identity lock” phrase can guarantee identical face pixels when the image model is asked to regenerate the person.

The protocol therefore separates identity preservation into three routes, ordered by generation risk.

## 3. Identity route architecture

### Route A — `SOURCE_PRESERVE_COMPOSITE` — preferred

Use when the uploaded authorized person asset already has a compatible pose or can be used with only crop/scale/position/light integration.

Rules:

- Treat the face/head as the identity anchor to preserve, not a generative style target.
- Do not ask the image model to redesign facial features, expression, hairstyle, head shape, or skin texture.
- Prefer using the real person cutout/green-screen source as the main subject while generating/adapting the rest of the cover around it.
- Pose adaptation is limited to global placement, crop, scale, lean perception, surrounding scene geometry, contact shadow, and light integration.
- If the desired pose requires reconstructing the face/head, Route A is no longer valid.
- The name `SOURCE_PRESERVE_COMPOSITE` deliberately avoids implying an unavailable hard pixel lock. Native ChatGPT editing may still regenerate pixels.

This route is expected to provide the highest practical identity fidelity inside the native ChatGPT workflow, but that expectation must be verified by the benchmark.

### Route B — `SOURCE_EDIT_MINIMAL` — second choice

Use when the user wants modest pose/context adaptation and an uploaded authorized person image can serve as the base image.

Rules:

- Start from one primary person source image, not from a blank canvas.
- Keep face/head instructions explicitly unchanged.
- Edit the smallest possible region outside the face.
- Preserve eye shape, eye spacing, eyebrows, nose, mouth, jaw, hairline, facial proportions, age cues, skin tone, and characteristic marks.
- Limit pose delta: no large head yaw/pitch, no invented profile, no dramatic expression change.
- If the model changes identity, fail the candidate and fall back to Route A or a closer source pose.

### Route C — `GENERATIVE_IDENTITY_REFERENCE` — last resort

Use only when the requested body pose cannot be satisfied by Route A or B.

Rules:

- The output is a candidate, never automatically accepted.
- Use exactly one primary identity anchor and at most two secondary identity anchors.
- Secondary references confirm identity only; they must not introduce a competing pose, lighting style, age, or expression target.
- Do not mix unrelated people in the same identity reference set.
- A candidate that merely “resembles” the person fails.
- If two attempts fail identity QA, stop retrying the same route and choose a closer real pose asset or return to Route A/B.

## 4. Pose adaptation envelope

“Automatically adapt body pose” does not mean arbitrary full-body regeneration at any cost.

V0.1 defines three pose-delta levels:

- `LOW`: crop, position, scale, mild torso lean, hand visibility changes that do not require changing the head orientation. Allowed in A/B.
- `MEDIUM`: torso/arm posture changes with the face remaining close to the source angle. Prefer B; Route C only with strict QA.
- `HIGH`: large head rotation, profile view, extreme foreshortening, major limb reconstruction, dramatic expression change. Do not promise identity lock. Choose another authorized source pose or reject the pose request for this candidate.

## 5. Asset role binding

Every uploaded image must be assigned exactly one primary role before image creation:

- `PERSON_IDENTITY_PRIMARY`
- `PERSON_IDENTITY_SECONDARY`
- `PERSON_POSE_SOURCE`
- `VEHICLE_EVIDENCE`
- `PRODUCT_EVIDENCE`
- `FONT_STYLE_REFERENCE`
- `LAYOUT_REFERENCE`
- `BACKGROUND_REFERENCE`

The prompt must explicitly name each role. Do not let the model infer that a vehicle image is style reference or that a font screenshot is a person reference.

## 6. Identity anchor selection

Select the primary identity anchor by this order:

1. Same face angle as requested scene.
2. Highest face resolution and sharpness.
3. Neutral/usable expression.
4. Least obstruction from hands, glasses, hair, motion blur, or harsh shadow.
5. Closest body pose to requested composition.

Do not use “more references is always better.” Too many conflicting face references can increase identity drift. Default to one primary + zero to two secondary references.

## 7. Green-screen source protocol

Green-screen person images are preferred production assets because they reduce the amount of generative reconstruction needed.

Rules:

- Preserve the original face/head identity whenever possible.
- Green removal intent, edge cleanup, spill reduction, crop, scale, contact shadow, and global light/color matching are allowed.
- Face retouching, skin smoothing, eye enlargement, jaw reshaping, nose reshaping, mouth replacement, expression synthesis, or age alteration are forbidden.
- Do not ask the image model to “recreate the same person from the green-screen image.” Use the image as the source subject/identity anchor.
- If exact source pixels must remain unchanged, a non-generative compositor is required; native ChatGPT alone cannot guarantee that property.

## 8. Vehicle and product evidence lock

Priority after person identity:

`person identity > vehicle identity > product evidence > title correctness > layout impact > decoration`

Vehicle rules:

- Preserve model/year-defining exterior cues visible in the source.
- Do not invent lamps, bumpers, wheels, trim, stance, or badges.
- If exact geometry cannot be preserved, show less of the vehicle rather than fabricate details.

Product rules:

- Treat caliper body shape, rotor structure, logo, model text, bolt locations, wheel spokes, damper shape, and other identifying geometry as evidence.
- Do not create false logos/model numbers.
- If the uploaded source is insufficient for a claimed detail, mark the detail as unknown or hide it.

## 9. Typography protocol

Font reference images are style references unless the user supplies an authorized font file through a supported workflow.

- Do not claim the image model is using an exact font file when it is only looking at a screenshot.
- Main hook: 7–16 Chinese characters preferred, usually two lines.
- Keep one dominant title hierarchy.
- Verify every Chinese character and every product/model token after generation.
- If text correctness fails, repair text separately rather than regenerating the whole person/vehicle composition.

## 10. Generation state machine

### State 0 — `PREFLIGHT`

Verify required assets, identify missing evidence, assign roles, choose primary identity anchor, classify pose delta.

### State 1 — `ROUTE_SELECT`

Choose A/B/C. Route A is default whenever it can satisfy the brief.

### State 2 — `COMPOSITION_PLAN`

Select one of the validated 66Workshop cover layouts and write a short composition contract: person position, vehicle position, product evidence, title block, safe areas.

### State 3 — `IMAGE_CREATE_OR_EDIT`

Generate/edit with the minimum amount of person reconstruction required by the selected route.

### State 4 — `QA_GATE`

Run identity, vehicle, product, text, layout, and brand checks.

### State 5 — `REPAIR_OR_FALLBACK`

Repair only the failing region where possible. If identity fails, do not repair with another face generation. Fall back to a safer route or a closer real person source.

### State 6 — `RECORD`

Record route, source asset IDs, failure reasons, rework count, and human verdict.

## 11. Identity QA rubric

ChatGPT-only visual QA is advisory; human owner review is authoritative for final identity approval.

A candidate passes identity QA only if all are true:

- same facial proportions and overall face shape
- same eye shape and spacing
- same eyebrow shape/position
- same nose structure
- same mouth/lip structure
- same jaw/chin proportions
- same hairline/hair identity cues unless explicitly hidden
- same approximate age cues and skin tone
- no obvious beautification or “AI celebrity” substitution
- no newly invented face in cases where the original face was expected to be preserved

Scoring:

- `IDENTITY_5`: source face highly preserved / effectively indistinguishable for intended cover use
- `IDENTITY_4`: same person; only minor non-identity rendering difference
- `IDENTITY_3`: probably same person but noticeable drift — FAIL
- `IDENTITY_2`: lookalike — FAIL
- `IDENTITY_1`: different person — FAIL

V0.1 production pass threshold: `IDENTITY_4` or `IDENTITY_5`, plus human approval.

## 12. Retry policy

- Never blindly regenerate the full cover more than two times on the same route after identity failure.
- First identity failure: reduce pose delta and reduce number of identity references.
- Second identity failure: fall back C → B or B → A; choose a closer authorized source pose.
- If Route A cannot be used and B/C still fail, return “identity-safe output not achieved” rather than accept a lookalike.

## 13. Benchmark

Minimum controlled benchmark: 20 real cover jobs.

Track:

- identity pass rate
- first-pass usable rate
- title correctness
- vehicle/evidence correctness
- route distribution A/B/C
- identity failure rate by pose-delta class
- average rework count
- human rejection reason

V0.1 target:

- human-approved identity pass rate ≥ 95%
- title correctness ≥ 98%
- vehicle/evidence correctness ≥ 95%
- first-pass usable rate ≥ 60%
- no accepted `IDENTITY_1/2/3` candidates

## 14. Non-goals for V0.1

- No claim of mathematical face-embedding verification inside native ChatGPT.
- No claim of a hard pixel-preservation mask inside native ChatGPT.
- No invented image-model parameters or reference weights that the ChatGPT UI does not expose.
- No third-party face-swap service.
- No training or fine-tuning on the user’s face.
- No requirement to store high-resolution source identity assets publicly in GitHub.

## 15. V0.2 candidates

Only consider after V0.1 benchmark demonstrates the remaining bottleneck:

- optional local/private face-embedding similarity checker for QA
- private asset store for higher-resolution authorized person sources
- non-generative green-screen cutout/compositing when exact source-pixel preservation is required
- pose-library expansion based on observed failure clusters
- API orchestration if it materially improves repeatability over native ChatGPT

## 16. Acceptance criteria

The Skill is accepted when:

1. It can be pasted/referenced in a ChatGPT conversation without requiring hidden model parameters.
2. It explicitly separates person identity, pose, vehicle, product, typography, and layout roles.
3. It routes to the least-generative identity method first.
4. It refuses to label a lookalike as success.
5. It contains a deterministic fallback policy after identity failure.
6. It records enough metadata to compare future versions.
7. It remains compatible with the existing 66XiaohongshuIPcover controlled-production repository and authorized-asset policy.
