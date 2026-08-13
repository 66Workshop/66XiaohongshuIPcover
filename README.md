# 66XiaohongshuIPcover

66Workshop 小红书 IP 封面图 Skill 与生产工作流。

## 目标

把已经验证有效的封面语言固化成一套可复用、可审计、可持续迭代的系统：

**真人 IP 锁定 + 真实车辆/配件证据 + 强钩子书法标题 + 3:4 小红书封面 + 人工验收。**

这不是“把提示词放进 GitHub”。真正要解决的是：减少模型自由发挥，让每次任务都走同一套输入、素材、版式、生成和 QA 规则。

## V0.1 适用范围

- 小红书 3:4 IP 封面图
- 汽车改装案例、避坑、方案解释、实测、观点类内容
- 人物主体必须来自仓库登记的授权 IP 素材
- 字体/书法视觉必须来自登记的授权风格参考
- 车、轮毂、刹车、避震等关键证据优先使用真实参考图

## V0.1 不做什么

- 不把 AI 相似脸当本人
- 不允许模型自由重画真人脸
- 不把“Logo 很大”当专业感
- 不追求一键无审核全自动发布
- 不把高真实性车辆/配件细节交给模型随意设计

## 成功案例提炼出的 4 类版式

1. **P01 数据冲突型**：大数字/大结论 + 真人 + 整车 + 实测证据
2. **P02 修复证据型**：真人近景 + 原始问题 + 修复前后小卡
3. **P03 车型决策型**：车型大主体 + 真人 + 配件证据 + 观点标题
4. **P04 产品价值型**：车型/方案 + 真人 + 套件陈列 + 细节证据条

详见 `docs/SUCCESS_CASE_ANALYSIS.md`。

## 仓库结构

```text
.
├── SKILL.md
├── README.md
├── assets/
│   ├── authorized/
│   │   ├── ip/
│   │   └── typography/
│   └── manifests/
├── docs/
│   ├── WORKFLOW.md
│   ├── STYLE_SYSTEM.md
│   ├── SUCCESS_CASE_ANALYSIS.md
│   ├── ASSET_POLICY.md
│   └── AUDIT_V0.1.md
├── examples/
│   ├── job.example.json
│   └── successful/
├── prompts/
│   ├── MASTER_PROMPT.md
│   └── TITLE_ENGINE.md
├── schemas/
│   └── job.schema.json
├── scripts/
│   └── validate_job.py
└── .github/workflows/
    └── validate.yml
```

## 使用方法

1. 选择人物素材 ID、标题类型、版式模板。
2. 提供本次车型/配件真实证据图。
3. 创建 job JSON。
4. 运行校验。
5. 按 `SKILL.md` 组装生成指令。
6. 一次生成 3–4 张候选。
7. 按 QA Gate 人审，只留下通过版本。
8. 记录失败原因与成功模板，回写仓库。

## 最高优先级

**P0：人物身份保真 > 车型/配件证据真实 > 标题可读 > 视觉冲击 > 装饰。**

任何封面只要脸错、车错、配件错或标题错字，直接打回。

## 资产授权

仓库内人物、字体风格参考和成功案例由 66Workshop 授权用于本项目内部生产与训练参考。它们不因公开存储而自动获得二次商业授权。详见 `docs/ASSET_POLICY.md`。
