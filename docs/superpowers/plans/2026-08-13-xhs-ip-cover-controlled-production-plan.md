# Xiaohongshu IP Cover Controlled Production V0.1 Implementation Plan

> **For agentic workers:** use the controlled-production design and execute tasks in order.

**Goal:** 把 V0.1 做成资产真实入库、任务可验证、结果可审计、PR 可合并的受控生产仓库。

**Architecture:** GitHub 作为唯一规则与版本源。人物、字体视觉参考和成功案例使用轻量 derivative 存入仓库；manifest 同时记录 derivative SHA256 与原始授权源 SHA256；jobs 和 records 形成生产合同；Python validator + GitHub Actions 负责机器门禁；不接生图 API。

## Constraints

- 不重绘/仿制人物脸部
- 仅使用用户明确授权素材
- 默认输出比例 3:4
- V0.1 不接第三方生图 API
- 不上传字体文件，只存字体风格参考图
- 先 feature branch 验证，再 PR 合入 main

## Tasks

### 1. Authorized reference assets
- [x] 3 张人物参考 derivative
- [x] 1 张字体风格参考 derivative
- [x] 4 张成功案例参考 derivative

### 2. Machine-verifiable manifests
- [x] person manifest
- [x] visual manifest
- [x] flattened assets manifest
- [x] derivative SHA256 + source SHA256

### 3. Tests and validators
- [x] valid job passes
- [x] unknown person ID fails
- [x] unknown font ID fails
- [x] invalid aspect ratio fails
- [x] repo asset/hash/structure validation

### 4. Job lifecycle
- [x] `jobs/pending/job-001-wj-m8-ap9321.json`
- [x] `jobs/approved/`
- [x] `jobs/archived/`
- [x] `records/job-001-wj-m8-ap9321.record.json`

### 5. CI
- [x] unit tests
- [x] repo validator
- [x] every job validator
- [x] JSON syntax gate

### 6. Delivery
- [ ] feature branch machine verification on GitHub
- [ ] PR to `main`
- [ ] checks pass
- [ ] merge
- [ ] post-merge verification
