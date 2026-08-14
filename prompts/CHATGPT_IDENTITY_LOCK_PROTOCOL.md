# CHATGPT_IDENTITY_LOCK_PROTOCOL — 对话框直接执行版 V0.1

## 1. 使用场景

适用于普通 ChatGPT 对话：用户上传封面标题、授权真人/IP 图、车型实拍图、配件实拍图、字体/版式参考图，然后调用“创建图片/图像生成”。

目标：先保证本人身份与真实证据，再做姿态、构图、光影和标题设计。

---

## 2. 用户最短调用语句

用户可以直接说：

> 按 `66Workshop ChatGPT Cover Identity-Lock Skill V0.1` 执行。标题：`<填标题>`。用我上传的 IP 图锁定本人身份，车型图和配件图作为真实证据，字体图只作为字体视觉风格参考。做 3:4 66Workshop 封面。先自动做素材角色绑定和姿态风险判断，选择最安全的 A/B/C 身份路线，再创建图片；出图后必须做人脸、车型、配件和文字 QA。不是本人就直接判失败，不接受相似脸，按回退规则重做。

---

## 3. ChatGPT 执行前内部协议

在调用图像工具前必须先完成：

```text
TITLE = ...
PERSON_IDENTITY_PRIMARY = Image ?
PERSON_IDENTITY_SECONDARY = Image ? / none
PERSON_POSE_SOURCE = Image ? / same as primary
VEHICLE_EVIDENCE = Image ?
PRODUCT_EVIDENCE = Image ?
FONT_STYLE_REFERENCE = Image ?
LAYOUT_REFERENCE = Image ? / none
POSE_DELTA = LOW | MEDIUM | HIGH
IDENTITY_ROUTE = A | B | C
LAYOUT = P01 | P02 | P03 | P04
```

不要把所有图片都当成同一类“参考图”。

---

## 4. Route A — PIXEL_LOCK_COMPOSITE 指令骨架

优先使用。适用于真人姿态基本可用。

```text
Create a 3:4 66Workshop automotive social-media cover.

IDENTITY:
Image <X> is PERSON_IDENTITY_PRIMARY and is the only primary identity source.
Use the same authorized real person as the foreground IP subject.
Preserve the real person's face/head identity and facial proportions.
Treat the person source as a real visual asset to integrate into the composition, not as a style reference for recreating a similar person.
Do not reinterpret, beautify, redesign, or substitute the face.
Keep pose changes LOW. Prefer crop, scale, placement, scene integration, contact shadow, rim light and global color/light matching instead of rebuilding the face/head.

VEHICLE EVIDENCE:
Image <Y> is the real vehicle evidence. Preserve model-defining body lines, lights, wheels, stance and badges visible in the source.

PRODUCT EVIDENCE:
Image <Z> is the real product evidence. Preserve visible product geometry, logo/model text and identifying structure. Do not invent unsupported detail.

TYPOGRAPHY:
Image <F> is FONT_STYLE_REFERENCE only. It controls title energy/stroke feel/hierarchy only; it must not affect the person's identity or vehicle/product design.
Exact title: <TITLE>
Verify every Chinese character, brand name, model number, number and unit.

LAYOUT:
Use 66Workshop visual language: black/white/red with restrained yellow emphasis, real workshop/industrial feel, strong hook, clean 3:4 composition, no cheap e-commerce UI, no 9-grid parameter clutter, no neon nightclub CG.
```

---

## 5. Route B — SOURCE_EDIT_MINIMAL 指令骨架

用于中等姿态调整。

```text
Use Image <X> as the base authorized person source.
Keep the same real person's face/head identity unchanged in character and proportions.
Edit the smallest possible non-face region required for the composition.
Prefer changes to arms, shoulders, torso, crop, placement, contact geometry and background integration.
Keep the head direction and facial expression close to the source.
Do not redesign the eyes, eyebrows, nose, mouth, jawline, chin, hairline, age cues or skin identity.

All vehicle/product/font role constraints remain the same as Route A.
POSE_DELTA = MEDIUM.
If the edit requires reconstructing the head/face to satisfy the pose, stop and use a closer real person source instead of forcing the pose.
```

---

## 6. Route C — GENERATIVE_IDENTITY_REFERENCE 指令骨架

最后手段，只生成候选。

```text
Image <X> is the primary identity anchor for the same authorized person.
Image <A>, <B> are optional secondary identity anchors only; they confirm identity and must not introduce a different target pose or style.
Generate the same authorized person, not a lookalike, not a reinterpretation, not a generic male model.
Preserve the recognizable facial proportions and identity cues from the primary anchor.
Avoid large head-angle changes and dramatic expression changes.

This result is a candidate only and must pass IDENTITY_4/5 QA plus human approval before acceptance.
```

如果同一路线连续两次低于 `IDENTITY_4`，停止 C，回退 B/A。

---

## 7. 负面词的正确定位

可以追加：

```text
No face substitution.
No lookalike.
No beauty-filter face.
No celebrity-style face.
No anime/3D/cartoon reinterpretation of the person.
No invented vehicle/product logo or model number.
```

但这些只是强化约束，不能代替：

- 角色绑定
- 主身份锚点选择
- A/B/C 路由
- 姿态降级
- 出图后 QA

---

## 8. 出图后 ChatGPT 必须执行的 QA 指令

不要直接说“做好了”。先做：

```text
Compare the generated person against PERSON_IDENTITY_PRIMARY.
Score IDENTITY_1 to IDENTITY_5.
Check face shape, eye shape/spacing, eyebrows, nose, mouth, jaw/chin, hairline, age cues and skin identity.
Then verify vehicle, product evidence, exact title text and layout.

If IDENTITY < 4, mark FAIL even if the cover looks attractive.
If only text/product/background fails while identity passes, repair only that local region.
If identity fails, do not keep regenerating the face locally; reduce pose/reference complexity or fall back to a safer identity route.
```

输出：

```text
IDENTITY: x/5
HUMAN IDENTITY APPROVAL: PENDING
VEHICLE: PASS/FAIL
PRODUCT: PASS/FAIL
TITLE: PASS/FAIL
LAYOUT: PASS/FAIL
ROUTE: A/B/C
POSE: LOW/MEDIUM/HIGH
VERDICT: ACCEPT/REPAIR/FALLBACK/STOP
```

---

## 9. 本人已经正确时的局部修复语句

### 只修标题

> 保持人物、脸、车型、配件和整体构图完全不动，只修标题区域。精确文字为：`<标题>`。修完后重新逐字检查，不重新生成已通过的人脸。

### 只修车型/配件

> 保持已通过的人物脸部与身份不动，只修车辆/配件区域，使其回到上传的 `VEHICLE_EVIDENCE / PRODUCT_EVIDENCE` 真实结构；不要重生整张图。

### 只修背景融合

> 保持人物脸、人物主体、车辆和配件不动，只调整背景、接触阴影、环境光和轮廓光，使人物与车间空间关系更自然。

---

## 10. 强制停止语句

如果多次生成后仍不是本人：

> **Identity-safe output not achieved. 当前真实人物素材与目标姿态组合不足，不接受相似脸作为最终封面。请换一张更接近目标姿态/头部角度的授权真人图，再继续。**

---

## 11. 推荐生产习惯

每次正式封面尽量只给图像模型：

- 1 张主身份图
- 0–2 张身份补充图
- 1–3 张真正需要露出的车型/配件证据
- 1 张字体风格参考
- 0–1 张版式参考

素材库可以很多；单次任务引用必须克制。
