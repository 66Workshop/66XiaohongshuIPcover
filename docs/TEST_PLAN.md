# TEST_PLAN — 66Workshop ChatGPT Cover Identity-Lock V0.1

## 1. 测试目标

V0.1 不以“某一张做得很像”验收，而以连续真实任务的可重复表现验收。

最小受控 Benchmark：**20 个真实封面任务**。

Route A 正式名称：`SOURCE_PRESERVE_COMPOSITE`。它代表原生 ChatGPT 内的“最大化源人物保留”路线，不代表硬像素锁。

---

## 2. 20 任务测试矩阵

建议分布：

- 8 个 `POSE_LOW`
- 8 个 `POSE_MEDIUM`
- 4 个 `POSE_HIGH`

内容类型至少覆盖：

- 5 个 `P01_DATA_CONFLICT`
- 5 个 `P02_BEFORE_AFTER`
- 5 个 `P03_VEHICLE_DECISION`
- 5 个 `P04_PRODUCT_VALUE`

混合：正脸/3/4 侧脸、坐姿/站姿/解释手势/开放手势、不同车身颜色/车间背景、卡钳/碟盘/轮毂/避震、简单标题与含英文型号/数字的高风险标题。

`POSE_HIGH` 的作用是测边界，不是强行制造高通过率。

---

## 3. 每个任务记录

```json
{
  "job_id": "",
  "date": "",
  "cover_type": "P01|P02|P03|P04",
  "identity_route": "SOURCE_PRESERVE_COMPOSITE|SOURCE_EDIT_MINIMAL|GENERATIVE_IDENTITY_REFERENCE",
  "pose_delta": "LOW|MEDIUM|HIGH",
  "primary_identity_asset": "",
  "secondary_identity_asset_count": 0,
  "vehicle_evidence_count": 0,
  "product_evidence_count": 0,
  "identity_score": 1,
  "identity_human_pass": false,
  "vehicle_pass": false,
  "product_pass": false,
  "title_pass": false,
  "layout_pass": false,
  "first_pass_usable": false,
  "rework_count": 0,
  "final_status": "ACCEPT|REPAIR|FALLBACK|STOP",
  "primary_failure": "",
  "notes": ""
}
```

---

## 4. 关键指标

### Identity

`human-approved identity pass rate = identity_human_pass jobs / total completed jobs`

目标：**≥ 95%**。

任何 `IDENTITY_1/2/3` 被人工接受，都视为流程错误。

### Title correctness

目标：**≥ 98%**。

品牌、型号、数字、单位任一错误都算 fail。

### Vehicle / evidence correctness

目标：**≥ 95%**。

车型关键特征或配件结构明显错误即 fail。

### First-pass usable rate

目标：**≥ 60%**。

定义：第一次候选无需 P0 修复即可进入人工可用状态。

### Rework

跟踪：

- 平均 `rework_count`
- identity rework 占比
- title-only repair 占比
- route fallback 次数

---

## 5. 路线级分析

每 20 个任务分别计算：

- A `SOURCE_PRESERVE_COMPOSITE` 使用率与 identity pass rate
- B `SOURCE_EDIT_MINIMAL` 使用率与 identity pass rate
- C `GENERATIVE_IDENTITY_REFERENCE` 使用率与 identity pass rate

预期需要被数据验证，而不是预设：A 是否真的比 B/C 更稳定；如果不是，复盘素材选择和执行方式。

---

## 6. 姿态级分析

分别统计 LOW / MEDIUM / HIGH identity fail rate。

HIGH 若成为主失败源，优化顺序：

1. 扩充真实授权姿态库
2. 改布局适配真实姿态
3. 再评估非生成式合成/本地 QA/API 编排

不是先堆提示词。

---

## 7. 继续 / 修改 / 停止条件

### CONTINUE

- identity ≥ 95%
- vehicle/evidence ≥ 95%
- title ≥ 98%
- first-pass usable ≥ 60%

则 V0.1 进入稳定受控生产。

### MODIFY

任一出现：

- identity 80–94.9%
- MEDIUM pose 持续高失败
- average rework_count > 2
- A 路线占比很低，说明工作流过度依赖人物生成

优先修改身份资产库、主锚点选择、姿态分级和路线选择。

### STOP / ROLLBACK SPECIFIC ROUTE

- identity < 80%
- C 持续出现 lookalike
- 同一任务同一路线连续 2 次 identity fail

停止该路线的自动接受资格。

---

## 8. V0.2 晋级条件

只解决数据证明的瓶颈：

- 私有/本地 face embedding QA
- 非生成式自动绿幕抠图与预合成
- 更大的授权姿态资产库
- API 多阶段编排

若未来业务硬要求“源脸像素必须完全不变”，优先测试非生成式 compositor，而不是继续升级负面提示词。

V0.1 没跑够 20 个真实任务前，不因为新工具更先进就加复杂度。

---

## 9. 最重要的反证问题

> **什么现实证据能够证明“这个 Skill 已经解决锁脸问题”的判断是错的？**

最直接证据：用户看到成图仍反复说“这不是我”。一旦超过验收阈值，就必须判定当前版本没有解决核心问题。
