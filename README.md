# 66XiaohongshuIPcover

66Workshop 小红书 IP 封面图工作流与 Skill 仓库。

目标：把已验证有效的 **真人 IP + 真实车辆/配件证据 + 强钩子书法标题 + 3:4 小红书封面** 做成可复用、可审计、可版本化的生产系统。

> 当前阶段：V0.1 受控生产工作流。人物、字体风格参考和成功案例均为用户明确授权素材。

## V0.1 当前能力

- `SKILL.md`：统一生产规则与视觉语法
- `assets/authorized/`：授权人物与字体风格参考预览
- `examples/successful/`：4 个已验证成功案例预览
- `assets/manifests/`：资产 ID、路径、SHA256 与授权角色
- `schemas/job.schema.json`：任务合同
- `jobs/`：pending / approved / archived 生命周期
- `records/`：产出与人工 QA 留痕
- `scripts/validate_job.py`：任务校验
- `scripts/validate_repo.py`：仓库与资产完整性校验
- `.github/workflows/validate.yml`：CI 门禁

## 重要边界

GitHub 中的人物/成功案例文件是为 **规则调用、版式识别和资产完整性校验** 制作的轻量预览 derivative，不替代原始高分辨率授权文件。真正需要“真人像素锁死”的生产合成，应调用原始授权素材，而不是让生成模型参考这些预览去仿脸。

字体部分只保存用户授权的 **视觉风格参考图**，不存放或再分发字体文件。

## 默认生产原则

1. 人物身份保真 > 视觉炫技
2. 人脸不可重绘、不可仿脸、不可美颜换脸
3. 车辆/配件以真实证据为锚点
4. 标题优先黑/红书法强钩子，保持手机缩略图可读
5. 每个任务必须通过机器校验 + 人工 QA
6. V0.1 不自动调用第三方生图 API

## 受控试运行目标

连续 20 个真实封面任务后，以数据判断是否进入 V0.2：

- identity pass rate ≥ 95%
- title correctness ≥ 98%
- first-pass usable rate ≥ 60%
- average rework time reduction ≥ 30%

详见 `docs/AUDIT_V0.1.md` 和 `docs/superpowers/specs/2026-08-13-xhs-ip-cover-controlled-production-design.md`。
