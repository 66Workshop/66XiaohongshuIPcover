# 66XiaohongshuIPcover

66Workshop 小红书 / 抖音 IP 封面图工作流与 Skill 仓库。

当前主线：**66Workshop ChatGPT Cover Identity-Lock Skill V0.1**。

目标不是让图像模型“画一个像辉哥的人”，而是把 **授权真人 IP + 真实车型/配件证据 + 强钩子标题 + 3:4 66Workshop 视觉语言** 做成可复用、可审计、可迭代的 ChatGPT 原生生产流程。

---

## 1. V0.1 解决什么问题

典型输入：

- 封面标题
- 绿幕/透明背景真人 IP 图
- 车型实拍图
- 卡钳/碟盘/轮毂/避震等配件实拍图
- 字体/书法风格参考图
- 可选的成功封面版式参考

典型执行：

1. ChatGPT 先识别每张图的角色。
2. 选择最安全的人物身份路线。
3. 先定构图，再调用创建图片/图像编辑。
4. 出图后对照真人、车型、配件、标题做 QA。
5. 人脸不是本人时直接 FAIL，不接受“相似脸”。
6. 失败按固定回退规则降低姿态/生成自由度，而不是继续盲抽。

---

## 2. Identity-Lock 核心架构

固定优先级：

**人物身份保真 > 车型身份保真 > 配件/证据保真 > 标题正确 > 版式冲击 > 装饰效果**

### Route A — `PIXEL_LOCK_COMPOSITE`

首选。真人绿幕/透明 PNG 姿态基本可用时，优先把真人作为真实视觉资产使用，构图围绕真人适配；尽量不重新生成脸/头。

### Route B — `SOURCE_EDIT_MINIMAL`

次选。以真实授权人物图作为编辑底图，只改完成构图所必需的最小身体区域，脸/头保持接近源图。

### Route C — `GENERATIVE_IDENTITY_REFERENCE`

最后手段。使用 1 张主身份锚点 + 最多 2 张补充身份图，仅生成候选；必须通过 `IDENTITY_4/5` + 人工确认。

连续两次同路线身份失败，强制降级/换真人源图，不继续抽图。

---

## 3. 一个关键现实边界

**原生 ChatGPT 图像生成/编辑不是一个带“100% 人脸锁定参数”的身份引擎。**

所以 V0.1 不靠“不能换脸”“100% lock face”之类提示词做虚假保证，而靠：

- 真实人物源优先
- 角色绑定
- 主身份锚点选择
- 姿态风险分级
- A/B/C 路由
- 最小编辑
- 出图 QA
- 失败回退

来提高可重复的人物身份一致性。

“任意大幅姿态变化”与“确定性锁定同一张脸”在原生生成工作流里存在真实冲突。`POSE_HIGH` 优先补更接近目标动作的真人授权素材，而不是硬让模型重画脸。

---

## 4. 在 ChatGPT 对话框怎么用

### 上传

建议单次正式任务只上传/选用：

- 1 张 `PERSON_IDENTITY_PRIMARY`
- 0–2 张 `PERSON_IDENTITY_SECONDARY`
- 1–3 张真正需要露出的车型/配件证据
- 1 张字体风格参考
- 0–1 张版式参考

素材库可以更多，但**单次不要把所有自拍全部塞给模型**。

### 调用

直接说：

> 按 `66Workshop ChatGPT Cover Identity-Lock Skill V0.1` 执行。标题：`<填标题>`。用我上传的 IP 图锁定本人身份，车型图和配件图作为真实证据，字体图只作为字体视觉风格参考。做 3:4 66Workshop 封面。先自动做素材角色绑定和姿态风险判断，选择最安全的 A/B/C 身份路线，再创建图片；出图后必须做人脸、车型、配件和文字 QA。不是本人就直接判失败，不接受相似脸，按回退规则重做。

完整对话协议见：`prompts/CHATGPT_IDENTITY_LOCK_PROTOCOL.md`。

---

## 5. 仓库结构

### 核心规则

- `SKILL.md` — ChatGPT Cover Identity-Lock 主 Skill
- `docs/INPUT_SPEC.md` — 输入素材标准与角色绑定
- `docs/WORKFLOW.md` — PREFLIGHT → 路由 → 出图 → QA → 回退状态机
- `docs/QA_CHECKLIST.md` — Identity / Vehicle / Product / Text / Layout QA
- `docs/FAILURE_PLAYBOOK.md` — face drift、车型漂移、配件幻觉等失败处理
- `docs/TEST_PLAN.md` — 20 个真实任务 Benchmark
- `prompts/CHATGPT_IDENTITY_LOCK_PROTOCOL.md` — 对话框直接执行协议

### 现有受控生产资产

- `assets/authorized/` — 授权人物与字体风格参考预览
- `assets/manifests/` — 资产 ID、路径、SHA256、授权角色
- `examples/successful/` — 已验证成功案例
- `jobs/` — pending / approved / archived 生命周期
- `records/` — 产出与人工 QA 留痕
- `schemas/job.schema.json` — 任务合同
- `scripts/validate_job.py` — 任务校验
- `scripts/validate_repo.py` — 仓库与资产完整性校验
- `.github/workflows/validate.yml` — CI 门禁

### 设计与实施记录

- `docs/superpowers/specs/2026-08-14-chatgpt-identity-lock-v0.1-design.md`
- `docs/superpowers/plans/2026-08-14-chatgpt-identity-lock-v0.1.md`

---

## 6. 授权素材边界

GitHub 中的人物/成功案例图片是为规则调用、版式识别、资产完整性校验准备的轻量 derivative。

**正式生产若要求最高身份一致性，应优先使用用户本次对话直接上传的原始高分辨率授权人物素材。**

不要拿仓库里的低清预览去要求模型重新“仿”一个人。

字体部分只保存授权视觉风格参考，不存放或再分发字体文件。

---

## 7. V0.1 Benchmark

连续 20 个真实封面任务后，以数据验收：

- human-approved identity pass rate ≥ 95%
- title correctness ≥ 98%
- vehicle/evidence correctness ≥ 95%
- first-pass usable rate ≥ 60%
- 不允许 `IDENTITY_1 / 2 / 3` 被标为通过

同时统计：

- A/B/C 路线占比和成功率
- LOW/MEDIUM/HIGH 姿态失败率
- 平均返工次数
- 最大失败模式

### 判断规则

- 达标 → CONTINUE，进入稳定受控生产
- identity 80–94.9% → MODIFY，先补姿态资产库/路由
- identity < 80% 或 C 路线持续 lookalike → STOP/ROLLBACK 该路线

V0.1 没跑够真实 Benchmark 前，不因为新工具“更先进”就增加换脸、训练或复杂 API 链路。

---

## 8. 最关键的验收问题

> **如果把标题和车型都遮住，用户能不能 1 秒确认“这就是我本人”？**

不能，就不是 Identity-Lock 成功。
