# 上游来源与更新

## 唯一登记处

[`upstream.json`](../upstream.json) 记录每个 skill 的来源和状态。保留原目录便于比较；参考、脚本、模板和 `agents/` 元数据都在比较范围内。

| 字段 | 含义 |
| --- | --- |
| `name` / `local_path` | 本地名称和目录 |
| `status` | `unmodified` 原样保留；`adapted` 实际有本地改动；`new` 本地新增；`removed` 有意移除 |
| `upstream_path` / `base_commit` / `base_tree` | 上游目录、精确来源提交及目录 Git tree SHA；新增项均为 null |
| `last_reviewed_commit` | 最近完整评估该 skill 上游差异的提交；初始等于来源提交 |
| `rationale` / `principles` | 保留、改动或移除的原因及对应 P1 至 P8；无差异时原则列表可为空 |
| `validation` | 实际验证及限制；未来场景不能写成通过 |

当前全部 skill 为 `unmodified`，根目录维护文档和分类索引变化不改变单个 skill 状态。首改 skill 时标记 `adapted` 并写明理由；只改参考或元数据也算改动。拆分/改名须维护映射，停用项保留 `removed` 记录。新增上游 skill 连同其依赖一起评估。

`base_commit` 是本地内容比较的共同起点；`last_reviewed_commit` 可以更晚，表示变化已看过但未必吸收。选择性吸收默认保留原起点，在该项 `validation` 记录候选 SHA 和取舍。只有明确重建完整比较基线才推进 `base_commit`，不得仅为消除 diff 改它。

## 检查当前声明

需要 Python 3 和 Git，不需要 npm、UE 或联网。

```sh
python scripts/check_skills.py
git diff --check
```

检查器核对技能覆盖、来源对象和 `unmodified` 的文件内容；意外修改、增删资源或漏登记会失败。它不会证明技能决策正确，也不会把 `adapted` 标为 UE 验收通过。正常 clone 保留来源 Git 对象；浅克隆缺对象时获取指定提交，不能改用 HEAD 糊弄检查。

## 获取候选更新

首次配置上游 remote，已存在时先核实 URL：

```sh
git remote add upstream https://github.com/mattpocock/skills.git
git fetch upstream main
python scripts/check_skills.py --upstream-ref upstream/main
```

检查器将 ref 固定解析为提交，只读报告各 skill 自 `last_reviewed_commit` 起的目录变化及未登记的新 skill。上游目录消失可能是删除或改名，需要核查；报告不是删除许可。

分别比较上游变化与本地差异，使用清单真实值替换占位符；目录改名时导出各自路径后比较：

```sh
git diff <last_reviewed_commit> <candidate_commit> -- <upstream_path>
git diff <base_commit> -- <local_path>
```

## 评估与采用

1. 阅读 [UE 基准](ue-principles.md)、受影响入口、引用和调用方，分类为直接采用、需要适配、暂不采用。
2. 在更新分支准备具体 diff。原样 skill 可从固定上游提交取完整目录；已适配 skill 对照共同基线整合。已删网站和发布材料不因同步自动恢复。
3. 检查是否重新要求每票完整 UE 副本、逐条重启 PIE、重复确认、仅末尾审查，或将待验收工作当完成。无 Git 冲突不等于无行为冲突。
4. 只更新实际评估的清单项，记录 SHA、取舍和实际验证。运行来源、引用及相称的无副作用场景检查；真实 UE 验证另按目标项目范围执行。
5. 交付可审查变更；合并与安装遵守本次授权，正在执行的任务不切换技能版本。上游已解决的问题应减少本地补丁。

每项变更能追到“来源版本 → 本地理由 → 验证结果”。README 给人看，AGENTS.md 提供维护入口，清单供工具比对，不另建易漂移的手工状态表。

## 安装边界

这是源文件仓库，不再发布上游 Claude 插件或 npm 发布包。现有安装不因本次提交改变。安装时选择明确提交和所需 skill，连同内部资源一起安装；同名 skill 只保留一个生效来源。

单独安装 skill 时，根 AGENTS.md 和 `docs/` 未必随包安装。运行时 UE 规则必须随 skill 发布，不能依赖维护文档隐式覆盖原版指令。新增 UE 名称时同步调用方、引用和清单，才算入口完整。
