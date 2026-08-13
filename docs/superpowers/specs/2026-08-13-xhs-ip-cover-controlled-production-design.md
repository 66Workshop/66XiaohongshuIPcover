# 66Workshop Xiaohongshu IP Cover Controlled Production V0.1 Design

## Goal

把 `66XiaohongshuIPcover` 从规则文档仓库升级为可执行、可验证、可审计的受控生产仓库。V0.1 不自动调用生图 API，只负责把授权素材、任务合同、验证、记录、CI 和主分支交付打通。

## Scope

- 3 张授权人物素材参考预览真实入库
- 1 张黑红书法视觉参考真实入库
- 4 张已验证成功案例参考预览真实入库
- manifest 路径、角色与 SHA256 可机器核验
- `jobs/pending|approved|archived` 任务入口
- `records/` 产出与人工 QA 留痕
- repo/job 自动验证
- GitHub Actions CI
- 一个真实问界 M8 AP9321 示例任务
- feature branch 通过 PR 合入 `main`

## Non-goals

- 自动调用图像生成 API
- 自动抠绿幕/像素合成
- OCR/视觉模型自动判脸、判车型、判配件
- 自动发布小红书

## Architecture

1. Rule source: `SKILL.md`, `prompts/`, `docs/`
2. Authorized refs: `assets/authorized/ip/`, `assets/authorized/typography/`
3. Successful refs: `examples/successful/`
4. Asset registry: `assets/manifests/*.json`
5. Job contract: `schemas/job.schema.json`, `jobs/**/*.json`
6. Validators: `scripts/validate_job.py`, `scripts/validate_repo.py`
7. Audit trail: `records/*.record.json`
8. CI gate: `.github/workflows/validate.yml`

## Identity Lock

人物文件在仓库中承担“授权身份参考预览”角色，不是让生成模型自由仿脸的素材。正式生产需要最高身份一致性时，应调用用户保存的原始高分辨率授权素材做独立抠图/合成；如果工具只能依据预览图重新生成相似人物，应标记 `IDENTITY_HIGH_RISK`。

## Asset Integrity

正式资产必须同时满足：

- 文件实际存在于 Git tree
- manifest 有唯一 ID 与 repo-relative path
- `sha256` 对仓库 derivative 可复验
- `source_sha256` 记录用户原始授权源的指纹
- `status = approved`
- 字体仅保存视觉风格参考，禁止误当成可再分发字体文件

## Job Lifecycle

`pending -> approved -> archived`

每个任务至少记录人物资产、模板、标题、证据素材、候选数、选中结果、返工次数、失败原因和 QA。

## QA Gates

### P0 identity/content
- 真人身份源正确
- 中文标题无错字
- 车型/项目无事实性错误

### P1 visual evidence
- 人、车、配件层级清楚
- 主证据足以证明标题
- 3:4 手机缩略图仍可读

### P2 brand/style
- 黑/红书法标题层级明确
- 66Workshop 视觉语法一致
- 不堆参数、不做廉价硬广

## Success Metrics after 20 real jobs

- identity pass rate ≥ 95%
- title correctness ≥ 98%
- first-pass usable rate ≥ 60%
- average rework time reduction ≥ 30%

## Delivery Gate

只有在资产、manifest、job、validators、tests、CI、审计全部通过，并经 PR 合入 `main` 后，V0.1 才标记为 `CONTROLLED_PRODUCTION_READY`。
