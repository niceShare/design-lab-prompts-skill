# 使用案例

下面四个案例展示“推荐 → 复制原文 → 追加项目约束”的完整用法。原始 Design Lab prompt 保持独立，项目扩展不会冒充站点原文。

## 案例一：AI 开发者 Dashboard

用户请求：

> 给一个面向 API 开发者的 AI 调试平台做 dashboard，希望明显差异化，但仍然可读。

查询：

```bash
python3 scripts/query_prompts.py recommend "AI developer dashboard" --lang en --level 3
python3 scripts/query_prompts.py prompt terminal --lang en --kind basic
```

推荐器返回 Terminal、Kinetic、Neomorphism。选择 Terminal，因为开发者工具的语义与命令行视觉天然一致，而且不需要用高强度动画牺牲数据可读性。

Source style instructions used during planning:

> Terminal style: black background. Green (#00FF88) or amber text. Everything monospace. Cards look like terminal windows with `$` prompt prefix. Buttons styled as `[ EXECUTE ]`. Add blinking cursor animation.

Project-specific extension:

- 使用左侧会话列表、中央请求/响应 diff、右侧运行指标三栏布局。
- 错误、警告和成功不能只靠颜色区分，同时使用图标和文本标签。
- 移动端改为单栏 tab；代码区允许横向滚动，不压缩长行。
- 光标闪烁只用于空闲输入区，并尊重 `prefers-reduced-motion`。

## 案例二：高端腕表电商

用户请求：

> 为小众机械腕表品牌做新品发布页，要有奢华感但不能俗气。

查询：

```bash
python3 scripts/query_prompts.py recommend "luxury watch ecommerce" --category ecom --lang zh --level 3
python3 scripts/query_prompts.py prompt luxury --lang zh --kind advanced
```

Source style instructions used during planning:

> 暗黑奢华产品页：深色底+微妙金色径向光晕。小标签全大写+0.3em字间距+9px。分隔线渐变金色。按钮透明底+金色描边。金色只做点缀，不要大面积。

Project-specific extension:

- 页面顺序为全屏机芯特写、三项工艺、规格表、限量编号、预约 CTA。
- 金色仅用于分隔线、编号和按钮边缘；正文使用暖白。
- 产品图不套厚重卡片，保留大面积黑色负空间。
- 规格表提供高对比模式，键盘焦点使用暖白外环而不是低对比金线。

## 案例三：Editorial SaaS 新风格回退

用户请求：

> 做一个知识管理 SaaS 的官网，希望像深度杂志，而不是蓝紫渐变模板。

查询：

```bash
python3 scripts/query_prompts.py show editorialsaas --lang en
python3 scripts/query_prompts.py prompt editorialsaas --lang en --kind basic
```

当前源站没有这个新增风格的英文数据，CLI 会明确显示 `[English source unavailable; showing original Chinese prompt.]`，然后返回中文原文：

> Editorial SaaS 风格：hero 用超大 Fraunces / Playfair 衬线 headline（60-96px），line-height 1.05。上方一个 8-9px mono chip 作 eyebrow。CTA 一个方形 filled 电蓝按钮 #0038FF。body 用 Inter 13-14px。整站白/米背景。

Project-specific extension:

- Hero 标题控制在 6–9 个英文词或 12–18 个中文字符。
- 产品功能用三段“编辑部专栏”结构，而不是 dashboard 卡片墙。
- 正文小字号仅用于桌面辅助信息；移动端正文不得小于 16px。
- 保留唯一电蓝 CTA，避免再加入紫色渐变和装饰 icon。

## 案例四：年轻美妆新品页

用户请求：

> 给 18–24 岁用户的新彩妆系列做社交传播落地页，要甜、闪亮、有怀旧感。

查询：

```bash
python3 scripts/query_prompts.py recommend "young beauty ecommerce" --category ecom --lang zh --level 3
python3 scripts/query_prompts.py prompt y2k --lang zh --kind advanced
```

Source style instructions used during planning:

> Y2K落地页：粉紫渐变+漂浮气泡。chrome金属文字(白→灰→白gradient+background-clip:text)。药丸按钮+渐变。✦twinkle动画。甜美、闪亮、怀旧未来感。

Project-specific extension:

- 首屏只放系列名、单张产品主图和“试色” CTA，避免装饰遮挡产品。
- 气泡和星光为非交互层，设置 `pointer-events: none`。
- 动画使用透明度和 transform，低动态偏好下完全静止。
- 保持购买按钮、价格和色号文字达到 WCAG AA 对比度，不用 chrome 渐变承载关键信息。
