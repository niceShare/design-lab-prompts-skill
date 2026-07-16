# Design Lab Prompts Skill

把 [Design Lab](https://design-lab-yanliu.vercel.app/) 当前版本中的设计风格 prompt 做成一个可离线检索、推荐和复用的 Codex skill。

> v0.1.0 · 快照时间 2026-07-16 · 77 个风格 · 318 条双语语言项

## 包含什么

- 77 个完整风格对象：名称、说明、特征、色板、CSS、适用规则和禁用规则。
- 174 条中文 prompt，覆盖全部 77 个风格。
- 144 条英文 prompt，覆盖站点已有英文源文的 67 个风格。
- 12 个项目类别 × 4 个创新等级 × 3 个结果，共 144 条站点原生推荐记录。
- 依赖为零的 Python CLI：列表、精确查询、全文搜索、prompt 复制和风格推荐。
- 中文/英文可读 prompt 合集、紧凑风格索引、SHA-256 清单和 4 个使用案例。

搜索引擎缓存仍显示“67 styles / 130+ prompts”，但抓取时的当前页面源码已经扩展到 77 个风格。十个新增风格只有中文数据，本项目如实标为 `zh-only`，没有擅自机翻。

## 安装 Skill

把 skill 目录复制到 Codex 的技能目录：

```bash
cp -R skill/design-lab-prompts "${CODEX_HOME:-$HOME/.codex}/skills/"
```

然后在新任务中调用：

```text
$design-lab-prompts 给我的 AI 开发者工具推荐 3 种视觉风格，创新程度 3/4，并输出可直接用于前端实现的完整 prompt。
```

## 直接查询

```bash
cd skill/design-lab-prompts

python3 scripts/query_prompts.py stats
python3 scripts/query_prompts.py list --lang zh --filter trend
python3 scripts/query_prompts.py show glass --lang en
python3 scripts/query_prompts.py search "温暖 编辑 SaaS" --lang all --limit 5
python3 scripts/query_prompts.py prompt luxury --lang zh --kind advanced
python3 scripts/query_prompts.py recommend "AI developer dashboard" --lang en --level 3
```

`stats`、`show`、`search`、`prompt` 和 `recommend` 均支持 `--json`，便于接入其他自动化流程。

## 项目结构

```text
skill/design-lab-prompts/       可直接安装的 Codex skill
  SKILL.md                      工作流与渐进加载说明
  agents/openai.yaml            Codex UI 元数据
  scripts/query_prompts.py      零依赖检索与推荐 CLI
  references/catalog.json       唯一结构化事实源
  references/style-index.md     77 项紧凑索引
  references/prompts-zh.md      全量中文 prompt 合集
  references/prompts-en.md      全量英文源 prompt 合集
  references/source-notes.md    来源、缺口和权利说明
  references/manifest.json      文件哈希与统计
examples/cases.md               4 个端到端案例
research/analysis.md            站点与 prompt 体系分析
tools/                          采集归一化和引用生成工具
tests/test_catalog.py           完整性与 CLI 测试
```

## 重新生成引用文件

维护者先用浏览器把当前页面唯一的内嵌脚本完整保存为 `.js`，再运行：

```bash
node tools/extract_site_data.mjs path/to/site-inline.js work/catalog.json
python3 tools/build_reference_files.py work/catalog.json skill/design-lab-prompts
python3 -m unittest discover -s tests -v
```

采集时必须分片读取长脚本；当前内嵌源码有 294,111 个字符，单次跨浏览器读取会在 200KB 附近被截断。

## 数据与许可

本仓库原创代码与文档采用 MIT License。Design Lab 的 prompt 原文和元数据归原作者/权利人所有，不属于 MIT 授权范围。抓取页面未发现内容许可；如果要公开再分发数据集，请先阅读 [NOTICE.md](NOTICE.md) 并自行确认授权条件。

来源署名：Design Lab / Design Style Laboratory，Curated by Dreameryanyan。

## English summary

An offline Codex skill for searching and applying the current Design Lab collection: 77 styles, 174 Chinese prompt entries, 144 upstream English prompt entries, complete design tokens, and the original 144-record recommender. Runtime tooling uses only Python's standard library. See `NOTICE.md` before redistributing copied upstream content.

