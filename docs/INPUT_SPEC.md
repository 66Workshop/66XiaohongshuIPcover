# INPUT_SPEC — 66Workshop ChatGPT Cover Identity-Lock V0.1

## 1. Purpose

This file defines what must be present before ChatGPT calls image creation/editing. The goal is to reduce identity drift before prompting begins.

## 2. Minimum job inputs

Required:

- cover title / main hook
- at least 1 authorized person image
- at least 1 real vehicle image when a specific vehicle is shown
- at least 1 real product/part image when a specific part is shown

Optional:

- 1–2 secondary person identity references
- font-style screenshot/reference
- layout reference
- workshop/background reference

## 3. Person identity assets

### 3.1 Primary identity image

Choose one `PERSON_IDENTITY_PRIMARY` image.

Preferred qualities:

- face is sharp and sufficiently large in frame
- no motion blur
- no heavy beauty filter
- no severe shadow across the face
- no sunglasses or large object covering facial features
- hairline, eyebrows, eyes, nose, mouth, jawline are visible enough for comparison
- face angle is close to the desired output
- body pose is close to the desired cover pose

Green-screen or transparent-background person assets are preferred because they allow composition around the real person rather than forcing the model to recreate the person.

### 3.2 Secondary identity images

Use 0–2 `PERSON_IDENTITY_SECONDARY` images only when they add useful identity evidence.

Good secondary images:

- same person
- similar age/time period
- similar haircut
- clear face
- complementary angle

Bad secondary images:

- old photos with large age difference
- different haircut + strong stylization + poor lighting all at once
- screenshots with heavy beauty filters
- blurred video frames
- multiple expressions and head angles that conflict with the target pose

Default rule: **one strong primary image beats many conflicting references.**

## 4. Pose-source requirement

If the requested pose differs from the primary identity image, classify it:

- `POSE_LOW`: same head direction; crop/placement/scale/minor body adjustment
- `POSE_MEDIUM`: visible torso/arm/shoulder change but face angle stays close
- `POSE_HIGH`: major head direction change, profile generation, extreme low/high angle, dramatic expression, severe foreshortening

For `POSE_HIGH`, first search the uploaded authorized person assets for a closer real pose. Do not assume prompt wording can preserve identity under arbitrary pose reconstruction.

## 5. Green-screen person asset standard

Preferred source:

- full body or at least waist-up
- even green background
- no green clothing touching the background color
- clean focus around hair and shoulders
- no strong motion blur around hands
- consistent lighting across face and body

Allowed preprocessing:

- remove green background
- edge cleanup
- green spill reduction
- crop/scale/position
- global exposure/temperature/contrast match
- contact shadow
- subtle rim light/environment light

Forbidden person preprocessing:

- face replacement
- skin smoothing that changes identity cues
- eye enlargement
- nose reshaping
- jaw slimming
- lip replacement
- age change
- synthetic expression change

## 6. Vehicle evidence assets

For a specific vehicle, prefer:

- 2–4 real photos
- one main 3/4 exterior view
- one side/front/rear view when those details matter
- wheel/brake close-up when the cover shows the wheel/brake system
- enough resolution to verify lights, bumpers, wheel design, trim, stance and badges

If only one weak vehicle image exists, reduce how much unsupported vehicle detail is exposed.

Do not infer a different model year, body kit, wheel or lamp design just to improve composition.

## 7. Product evidence assets

For brakes, wheels, suspension or other hardware, prefer:

- product in real lighting
- logo/model text readable when it is important
- body geometry visible
- mounting/interface details visible if claimed
- multiple angles when the cover needs a non-source angle

If a product logo/model cannot be verified from the source, do not invent it.

## 8. Font/style reference assets

A screenshot or image of typography is `FONT_STYLE_REFERENCE` only.

It can guide:

- brush/handwriting feel
- stroke thickness
- black/red/yellow hierarchy
- slant
- spacing
- title energy

It does **not** prove the exact font file is available.

Never claim exact font-file reproduction unless the production environment really has and uses that authorized font file.

## 9. Layout references

A layout reference controls composition only:

- title placement
- person/vehicle scale relationship
- evidence-card placement
- visual rhythm

It must not override identity, vehicle, or product evidence.

## 10. Asset-role map

Before image creation, ChatGPT should internally produce a role map similar to:

```text
Image 1 → PERSON_IDENTITY_PRIMARY
Image 2 → PERSON_IDENTITY_SECONDARY
Image 3 → VEHICLE_EVIDENCE
Image 4 → PRODUCT_EVIDENCE
Image 5 → FONT_STYLE_REFERENCE
Image 6 → LAYOUT_REFERENCE
```

Each image receives one primary role.

## 11. Blocking conditions

Do not call the image tool blindly when any of these are true:

- no usable authorized person identity image
- only a tiny/blurred face is available
- requested pose is `POSE_HIGH` and no suitable identity/pose source exists
- a specific vehicle must be shown but no trustworthy vehicle source is provided
- a specific product must be shown accurately but no trustworthy product source is provided

When blocked, state the exact missing evidence and request only that missing asset.

## 12. Best-practice upload pack for repeated 66Workshop use

Recommended long-term identity pack:

- 3–5 clear frontal / near-frontal green-screen images
- 2–3 left 3/4 views
- 2–3 right 3/4 views
- seated pose set
- standing pose set
- pointing/explaining/open-hands pose set
- neutral and light-smile expressions

The purpose is not to give every image to the model at once. The purpose is to let the Skill choose the **closest real pose** and therefore reduce generative reconstruction.
