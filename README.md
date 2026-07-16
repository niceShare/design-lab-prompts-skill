# Design Lab Prompts Skill

把 [Design Lab](https://design-lab-yanliu.vercel.app/) 当前版本中的设计风格 prompt 做成一个可离线检索、推荐和复用的 Codex skill。

> v0.1.1 · 快照时间 2026-07-16 · 77 个风格 · 318 条双语语言项

> [!IMPORTANT]
> 这是一个参考 Design Lab 公开网站进行研究、整理和工具化设计的非官方开源学习项目，与 Design Lab 或 Dreameryanyan 没有隶属、合作或背书关系。项目代码采用 MIT License；收录的上游 prompt、风格说明及相关元数据不属于本项目原创，也不包含在 MIT 授权中，仅作为学习、研究与交流资料提供。详情见 [参考来源与使用声明](ATTRIBUTION.md) 和 [NOTICE](NOTICE.md)。

## 参考来源

- 参考网站：[Design Lab / Design Style Laboratory](https://design-lab-yanliu.vercel.app/)
- 原站署名：Curated by Dreameryanyan
- 本项目性质：参考原站公开内容进行离线归档、结构化研究和 Codex skill 设计
- 官方关系：本项目为非官方独立项目，不代表原站或策展人

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
ATTRIBUTION.md                  中英双语参考来源与使用声明
```

## 重新生成引用文件

维护者先用浏览器把当前页面唯一的内嵌脚本完整保存为 `.js`，再运行：

```bash
node tools/extract_site_data.mjs path/to/site-inline.js work/catalog.json
python3 tools/build_reference_files.py work/catalog.json skill/design-lab-prompts
python3 -m unittest discover -s tests -v
```

采集时必须分片读取长脚本；当前内嵌源码有 294,111 个字符，单次跨浏览器读取会在 200KB 附近被截断。

## 开源范围与数据声明

本仓库原创代码与原创文档采用 MIT License，可以依照该许可证使用、修改和分发。Design Lab 的 prompt 原文、风格说明和相关元数据归原作者或权利人所有，不属于 MIT 授权范围。

仓库中的上游内容快照仅供学习、研究、设计分析与非商业交流使用；这项声明不代表本项目取得了上游内容的再许可权，也不授予商业再分发、转售、再授权或制作衍生数据集的权利。公开发布、商业使用或大规模再分发前，请自行确认授权并在需要时联系原权利人。

使用或分享本项目时，请保留以下参考说明：

> 本项目参考 Design Lab（https://design-lab-yanliu.vercel.app/）的公开设计风格资料进行研究与工具化实现；原站标注为 Curated by Dreameryanyan。本项目为非官方学习项目。

完整条款：[ATTRIBUTION.md](ATTRIBUTION.md) · [NOTICE.md](NOTICE.md) · [LICENSE](LICENSE)

## English summary

An unofficial open-source learning project inspired by and referencing the public [Design Lab](https://design-lab-yanliu.vercel.app/) website, credited there as “Curated by Dreameryanyan.” It provides an offline Codex skill with 77 styles, 174 Chinese prompt entries, 144 upstream English prompt entries, and the original 144-record recommender. Original project code is MIT-licensed; copied upstream content is excluded from that license and is bundled solely for study, research, and non-commercial exchange. See `ATTRIBUTION.md` and `NOTICE.md`.
