# Design Lab Prompts Skill

[![CI](https://github.com/niceShare/design-lab-prompts-skill/actions/workflows/ci.yml/badge.svg)](https://github.com/niceShare/design-lab-prompts-skill/actions/workflows/ci.yml)
[![代码许可：MIT](https://img.shields.io/badge/%E4%BB%A3%E7%A0%81%E8%AE%B8%E5%8F%AF-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-3776AB.svg)](https://www.python.org/)

[English](README.md)

一个可离线安装的 Codex skill 与零依赖 CLI，用于检索、比较和应用 [Design Lab](https://design-lab-yanliu.vercel.app/) 公开收录的 77 种前端视觉风格。

项目把网页快照整理成结构化目录、双语 prompt 合集、项目类型推荐器和可落地的 Codex 工作流。目前包含 174 条中文 prompt、144 条英文 prompt，以及 144 条策展推荐记录。

> [!IMPORTANT]
> 本项目是参考 Design Lab 公开网站进行研究和工具化实现的**非官方、独立开源学习项目**。原站标注为“Curated by Dreameryanyan”。本项目与 Design Lab 或其策展人不存在隶属、合作、赞助或背书关系。仓库原创代码和原创文档采用 MIT License；来自原站的 prompt、风格说明和元数据不属于本项目原创，也不包含在 MIT 授权中，仅供学习、研究、设计分析和非商业交流。使用或再分发数据前请阅读 [参考来源与使用声明](ATTRIBUTION.md) 和 [NOTICE](NOTICE.md)。

## 功能

- 可直接安装的 Codex skill，按需加载索引、prompt 与完整目录。
- 仅使用 Python 标准库的 CLI，支持列表、精确查询、全文搜索、prompt 复制和风格推荐。
- 77 个规范化风格对象，包含说明、特征、色板、CSS、prompt、do/don't 规则。
- 全部 77 个风格的中文源数据，以及其中 67 个风格的英文源数据。
- 原站 12 类项目 × 4 档创新程度的推荐矩阵。
- 确定性 Markdown 生成、SHA-256 清单、完整性测试和 4 个端到端案例。
- 用于更新快照的安全字面量解析器，不执行网页中的 JavaScript 代码。

## 快速开始

### 安装 Codex skill

```bash
git clone https://github.com/niceShare/design-lab-prompts-skill.git
cd design-lab-prompts-skill
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R skill/design-lab-prompts "${CODEX_HOME:-$HOME/.codex}/skills/design-lab-prompts"
```

在新的 Codex 任务中调用：

```text
$design-lab-prompts 为 AI 开发者 dashboard 推荐 3 种视觉方向，创新程度 3/4，并生成可直接用于实现的完整 prompt。
```

### 直接使用 CLI

需要 Python 3.10 或更高版本，不需要安装第三方包。

```bash
cd skill/design-lab-prompts

python3 scripts/query_prompts.py stats
python3 scripts/query_prompts.py list --lang zh --filter trend
python3 scripts/query_prompts.py show glass --lang en
python3 scripts/query_prompts.py search "温暖 编辑 SaaS" --lang all --limit 5
python3 scripts/query_prompts.py prompt luxury --lang zh --kind advanced
python3 scripts/query_prompts.py recommend "AI developer dashboard" --lang en --level 3
```

`stats`、`show`、`search`、`prompt` 和 `recommend` 支持 `--json`。

## 数据覆盖

| 项目 | 数量 |
|---|---:|
| 风格 | 77 |
| 双语风格 | 67 |
| 仅中文风格 | 10 |
| 中文 prompt | 174 |
| 英文 prompt | 144 |
| 推荐类别 | 12 |
| 创新等级 | 4 |
| 推荐记录 | 144 |

十个新增风格在当前快照中只有中文源数据。CLI 会明确提示并回退到中文原文，不会擅自生成英文翻译。完整案例见 [examples/cases.md](examples/cases.md)，采集与体系分析见 [research/analysis.md](research/analysis.md)。

## 开发与验证

维护工具需要 Python 3.10+ 和 Node.js 20+。

```bash
python3 -m unittest discover -s tests -v
python3 -m compileall -q skill tools tests
node --check tools/extract_site_data.mjs
python3 tools/build_reference_files.py \
  skill/design-lab-prompts/references/catalog.json \
  skill/design-lab-prompts
git diff --exit-code
```

更新快照时必须向采集器提供采集时间：

```bash
node tools/extract_site_data.mjs \
  path/to/site-inline.js \
  work/catalog.json \
  --captured-at 2026-07-16T17:29:57+08:00
```

采集器只解析数据字面量，不执行远程页面代码；函数、调用表达式、计算表达式和模板插值都会被拒绝。

## 权利与使用边界

这是一个混合权利范围的仓库：

- 本项目原创工具代码和原创文档采用 [MIT License](LICENSE)。
- 来自 Design Lab 的 prompt、风格说明、推荐文案及元数据不包含在 MIT 授权中。
- 上游参考网址：[Design Lab](https://design-lab-yanliu.vercel.app/)，原站署名“Curated by Dreameryanyan”。
- 本项目是非官方独立项目，不代表原站或其策展人。

上游内容快照仅供学习、研究、设计分析和非商业交流，不授予商业再分发、转售、再许可或制作衍生数据集的权利。公开或商业使用前，请自行确认授权。完整声明见 [ATTRIBUTION.md](ATTRIBUTION.md) 和 [NOTICE.md](NOTICE.md)。

## 参与项目

提交改动前请阅读 [CONTRIBUTING.md](CONTRIBUTING.md)。安全问题请按 [SECURITY.md](SECURITY.md) 私下报告。当前内部代码审核与整改记录见 [AUDIT.md](AUDIT.md)。
