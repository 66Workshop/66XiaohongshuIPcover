# WORKFLOW — 66Workshop ChatGPT Cover Identity-Lock V0.1

## 1. Objective

在普通 ChatGPT“创建图片/图像编辑”工作流内，以最小人物重构换取最高身份稳定性，同时锁定真实车型、配件和标题事实。

> Route A `SOURCE_PRESERVE_COMPOSITE` 是“最大化沿用真人源”的策略名，不代表原生 ChatGPT 有真正不可写的像素锁区。

## 2. State machine

### STATE 0 — PREFLIGHT

调用图片工具前：

1. 读取标题/主题。
2. 检查全部上传图。
3. 每张图绑定一个主角色。
4. 选择 `PERSON_IDENTITY_PRIMARY`。
5. 最多再选 2 张 `PERSON_IDENTITY_SECONDARY`。
6. 识别车型/配件证据。
7. 将姿态差分标记为 LOW / MEDIUM / HIGH。
8. 判断 P0 证据是否缺失。

缺关键资产时不要盲生成。

### STATE 1 — ROUTE_SELECT

固定安全顺序：

1. `SOURCE_PRESERVE_COMPOSITE`
2. `SOURCE_EDIT_MINIMAL`
3. `GENERATIVE_IDENTITY_REFERENCE`

只选择能完成任务的最低生成风险路线。

### STATE 2 — COMPOSITION_PLAN

内部先锁定：

```text
CANVAS: 3:4
LAYOUT: P01/P02/P03/P04
PERSON: 位置 + 占比
VEHICLE: 位置 + 占比
PRODUCT EVIDENCE: 位置 + 尺寸
TITLE: 位置 + 行数
SAFE FACE AREA: 禁止文字/产品覆盖
SAFE VEHICLE AREA: 保关键灯组/轮毂/徽标
```

构图优先适配真实人物源，而不是强迫真人去适配任意海报姿态。

### STATE 3 — IMAGE_CREATE_OR_EDIT

必须明确写出素材角色。

#### Route A

- 把真实人物源作为主体锚点。
- 最大化保留脸/头身份。
- 姿态只做 LOW 级变化。
- 优先改裁切、位置、大小、环境、接触阴影和画面其他元素。
- 不把 A 误称为硬像素锁。

#### Route B

- 从授权真人源图开始编辑，不从空白重生人物。
- 只修改完成动作所需的最小身体区域。
- 头部方向、表情尽量贴近源图。

#### Route C

- 1 张主身份源 + 最多 2 张身份补充图。
- 只生成候选，不自动通过。
- 避免大幅头部角度和表情变化。

### STATE 4 — QA_GATE

固定检查顺序：

1. Identity
2. Vehicle
3. Product evidence
4. Exact title text
5. Layout
6. Brand language

P0 失败即停止接受。

### STATE 5 — REPAIR_OR_FALLBACK

只修最小失败区域：

- 文字错 → text-only repair
- 背景差 → background-only repair
- 车型漂 → 恢复车型证据或减少露出
- 配件漂 → 恢复配件证据或隐藏不确定细节
- 人脸漂 → 不继续局部重生脸；降低姿态、减少身份参考、换源图或回退路线

身份回退：

```text
C -> B -> A
B -> A
A -> 选择更接近目标姿态的真实授权源
```

同一路线连续 2 次 identity fail = 强制换路线或换源图。

### STATE 6 — RECORD

记录：

```json
{
  "identity_route": "SOURCE_PRESERVE_COMPOSITE|SOURCE_EDIT_MINIMAL|GENERATIVE_IDENTITY_REFERENCE",
  "pose_delta": "LOW|MEDIUM|HIGH",
  "primary_identity_asset": "",
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

## 3. Pose policy

### LOW

- crop / position / scale
- 轻微躯干倾斜视觉感
- 少量手部可见性变化
- 背景/光影融合

优先 A。

### MEDIUM

- 手臂/肩膀/躯干明显变化
- 站姿/坐姿附近变化
- 但脸角度仍贴近源图

优先 B。

### HIGH

- 正脸变全侧脸
- 大幅低头/仰头
- 大头部旋转
- 戏剧性表情
- 极端透视/大幅全身重构

V0.1 不承诺 HIGH 的稳定身份锁定。优先补更接近姿态的授权真人源。

## 4. Reference-count policy

默认单次：

- 1 primary person identity
- 0–2 secondary identity
- 1–3 与画面可见细节真正相关的车/配件证据
- 1 font-style reference
- 0–1 layout reference

身份漂移时先**减少**身份参考，不先增加。

## 5. Prompt policy

强控制来自角色与流程，不是负面词。

优先写：

- “Image 1 is the only primary identity source.”
- “Keep the same authorized person; preserve facial proportions and identity cues.”
- “Image 4 is typography style only and must not affect the person.”

`don't change the face / no fake face / 100% lock face` 只能做辅助强化，不能当控制系统。

## 6. Repair granularity

人物已经正确时，绝不因局部错误重生整张：

- 人正确 + 汉字错 → 只修字
- 人正确 + 卡钳 Logo 错 → 只修/替换配件区域
- 人正确 + 融合差 → 只修背景/阴影/环境光

## 7. Existing controlled-production loop

继续保留：

- `P01_DATA_CONFLICT / P02_BEFORE_AFTER / P03_VEHICLE_DECISION / P04_PRODUCT_VALUE`
- 成功案例回写 `examples/successful/`
- 失败模式记录 `face_drift / car_drift / product_hallucination / title_error / layout_overload / weak_hook / fake_evidence`
- 每 20 个真实任务复盘

## 8. Acceptance

只有同时满足以下条件才可标记可用：

- identity = `IDENTITY_4` 或 `IDENTITY_5`
- 人工确认本人身份通过
- vehicle pass
- product pass
- title pass
- 缩略图版式可读

视觉再漂亮的相似脸也属于失败。
