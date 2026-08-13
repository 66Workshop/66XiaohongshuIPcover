# 审计报告｜66Workshop 小红书 IP 封面 Skill V0.1

## 审计结论

`VERDICT = CONTROLLED_PRODUCTION_READY`

V0.1 的“受控生产”代码、资产、任务合同、测试、CI 与主分支交付已经完成。

这不等于“全自动稳定生图”。V0.1 明确不接第三方生图 API，也不声称已经解决中文生成字、自动锁脸、车型/配件视觉相似度自动判定。

## 已通过

- [x] `SKILL.md` 与 4 类成功版式存在
- [x] 3 张授权人物参考 derivative 实际进入 Git tree
- [x] 1 张授权黑红书法风格参考 derivative 实际进入 Git tree
- [x] 4 张成功案例参考 derivative 实际进入 Git tree
- [x] person / visual / flattened assets manifest 完整
- [x] derivative SHA256 与原始授权 source SHA256 双重记录
- [x] 人物资产包含 `face_no_redraw` / `identity_lock` / `no_beautify`
- [x] 字体只标记为 `style_reference_only`，不分发字体文件
- [x] `jobs/pending|approved|archived` 生命周期存在
- [x] 首个真实任务 `job-001-wj-m8-ap9321` 已入库
- [x] `records/` 审计留痕合同存在
- [x] `validate_job.py` 校验任务结构、模板、人物 ID、字体 ID、3:4 与候选数
- [x] `validate_repo.py` 校验仓库结构、8 个资产路径和 SHA256
- [x] 单元测试通过
- [x] Feature GitHub Actions run #4：`success`
- [x] PR #1 GitHub Actions run #5：`success`
- [x] PR #1 已 squash merge 到 `main`
- [x] Main GitHub Actions run #6：`success`

## 机器证据

- Feature verified commit: `b0d9334ae1209796bb3f8379a55c836248ee044b`
- Feature verified tree: `190c181585a39eacb6ba04413caaca27f9b44adf`
- PR: `#1`
- Squash merge commit: `d050e0150c9d4f8db53186d02810ef85a3e6db2c`
- Feature workflow run: `31692241969` → `success`
- PR workflow run: `31692334735` → `success`
- Main workflow run: `31692389808` → `success`

## 资产策略说明

仓库为公开仓库，因此人物和成功案例保存的是轻量 reference derivative，用于：

- 资产 ID 稳定调用
- 版式/视觉语法参考
- manifest 与 SHA256 机器校验

它们不是“高分辨率人物抠图母版”。需要真正的像素级锁脸时，生产端仍应调用用户保存的原始授权高分辨率源；如果模型只能依据 repo 预览图重新生成相似人物，必须标记为 `IDENTITY_HIGH_RISK`。

## 当前非目标 / 未完成自动化

- [ ] 自动调用图像生成 API/Runner
- [ ] 自动抠绿幕与像素级人物合成
- [ ] OCR / 中文书法标题视觉校验
- [ ] 车型/配件视觉相似度自动 QA
- [ ] 20 个真实任务统计看板
- [ ] 自动发布平台

## 20 次受控试运行门槛

- identity pass rate ≥ 95%
- title correctness ≥ 98%
- first-pass usable rate ≥ 60%
- average rework time reduction ≥ 30%

## 红队结论

### ① 值得做 / 修改 / 放弃
**值得做。V0.1 架构已成立，下一步进入真实任务试运行，不继续无止境堆规则。**

### ② 最大风险
把“规则统一、CI 通过”误判为“视觉输出已经稳定”。机器门禁只能证明仓库合同完整，不能替代真人脸、车型、配件和中文标题的人审。

### ③ 最缺关键证据
连续 20 个完全不同真实项目的一次可用率、身份通过率、标题正确率和返工时间。

### ④ 今天最小可执行一步
用 `job-001-wj-m8-ap9321` 作为第一笔受控生产记录，生成候选图并回写 `records/`。

### ⑤ 继续 / 修改 / 停止条件
- identity failure > 5%：强化原图像素合成，禁止参考生脸
- title error > 2%：生成模型退出文字终排，改后期排字
- first-pass usable < 60%：复盘 Layout/证据图选择，不增加自动化复杂度
- 连续 20 个任务达到指标：进入 V0.2 Runner/API 评估

### ⑥ 置信度
`0.96`（针对仓库受控生产架构已成立；不代表生图质量成功率）
