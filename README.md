# Matt Pocock Skills for UE

基于 [mattpocock/skills](https://github.com/mattpocock/skills) 的精简 fork，用于逐步适配 UE 的重型构建、资产编辑和 PIE 验证环境。

**当前已精简仓库，并对首批执行、拆票、测试与路由入口作了 UE 适配。** 逐技能改动和验证见来源清单；源码修改没有安装或替换本机技能，也尚未通过真实 UE 任务验证效率。

## 从这里开始

- **维护 agent**：[AGENTS.md](AGENTS.md) 提供按需读取入口。
- **设计与评估**：[UE 适配基准](docs/ue-principles.md) 记录原则、复盘教训、适用边界和首批适配范围。
- **来源与差异**：[upstream.json](upstream.json) 逐技能记录精确上游版本、状态、改动理由和实际验证。
- **吸收新版本**：[上游同步约定](docs/upstream-sync.md) 说明如何比较、选择性采用及保持安装版本稳定。

来源基线：[`6fd947921b935b7e1e69293a200400f0fdd5c15f`](https://github.com/mattpocock/skills/commit/6fd947921b935b7e1e69293a200400f0fdd5c15f)。后续每个 skill 可以有不同的已审阅版本，以清单为准。

## 内容与边界

```text
skills/                 技能入口及其参考、脚本、模板和 agents 元数据
docs/ue-principles.md    UE 适配决策依据
docs/upstream-sync.md    上游更新与安装边界
upstream.json           逐技能来源和差异登记
scripts/check_skills.py  离线来源检查及候选上游差异报告
AGENTS.md / CLAUDE.md    仓库维护入口
LICENSE                 上游许可与版权声明
```

保留全部技能，避免在基础整理阶段擅自裁掉某类能力。保留原路径便于比对：

- [engineering](skills/engineering/README.md)：工程工作流。
- [productivity](skills/productivity/README.md)：通用工作方式。
- [misc](skills/misc/README.md)：专项工具，按任务选择。
- [in-progress](skills/in-progress/README.md)：上游实验性技能。
- [deprecated](skills/deprecated/README.md)：当前为空。

删除上游网站说明页、营销内容、发布历史与 changesets、Claude 插件打包、npm 发布依赖、上游仓库的分诊/发布自动化及专用维护材料。技能自身依赖和第三方归属保留。旧内容仍能通过 Git 历史查看。

## 怎样识别已改造技能

清单的 `status` 是唯一状态登记：`unmodified` 为上游原样，`adapted` 为有本地改动，`new` 为本地新增，`removed` 为有意移除。只修改引用、脚本或元数据也要更新状态。改造原因引用 UE 基准中的原则，`validation` 记录实际结果和限制。

维护原则不会自动覆盖已安装的上游 skill。适配后的运行约束已写入相应 skill：按实际资源调度，区分低成本测试与重型验证，保留独立审查和验收证据。agent 自选角色、工具与实现路线；失败记录仅描述证实的错误及适用边界。尚未实测的提速效果不作承诺。

## 检查与使用

正常 clone 后运行，需要 Python 3 和 Git：

```sh
python scripts/check_skills.py
git diff --check
```

检查覆盖来源记录和原样声明，不代替技能行为验证。上游更新的获取及比较命令见 [同步约定](docs/upstream-sync.md)。

本仓库提供 skill 源文件，不提供上游插件或 npm 发布包。安装时固定提交、按需选择完整 skill 目录，并核对技能间依赖；已安装的同名技能应只有一个生效来源。项目的实际资源限制、MCP 与 deadend 入口由其自身工作契约提供，本仓库不自动改写它们。

## 归属

上游作者 Matt Pocock，许可为 [MIT](LICENSE)。[PR skill 的第三方归属](skills/engineering/pr/CREDITS.md) 一并保留。本 fork 的 UE 维护基准源于本地任务复盘，与上游实现状态分别记录。
