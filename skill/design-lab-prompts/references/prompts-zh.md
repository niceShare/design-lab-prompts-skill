# Design Lab prompts — Chinese

Source snapshot: <https://design-lab-yanliu.vercel.app/> at `2026-07-16T17:29:57+08:00`.
Prompt wording is preserved from the captured source.

## 01. 粗野主义 (`brutalism`)

> 粗野主义风格，粗黑边框+硬边阴影

### 基础 Prompt

使用Brutalist风格：3px以上粗黑边框、硬边阴影(box-shadow: Npx Npx 0 #000)、等宽字体、大写标题、高对比黑白+一个亮色。

### 进阶 Prompt

设计Brutalist卡片：背景亮黄色(#FFDE59)，所有边框3px黑色，阴影用offset硬边(无blur)，hover时阴影缩小。文字monospace+uppercase。带"故意不精致"的raw感。

### 关键词

Brutalist, raw, thick borders, hard shadows, monospace, uppercase, high contrast, offset

## 02. 玻璃拟态 (`glass`)

> 玻璃拟态，磨砂模糊+半透明层叠

### 基础 Prompt

使用Glassmorphism风格：底层彩色渐变(紫→蓝→粉)，卡片用rgba(255,255,255,0.15)+backdrop-filter:blur(20px)磨砂玻璃。边框rgba白色，圆角20px。

### 进阶 Prompt

Glassmorphism Dashboard：底层animated mesh gradient。所有卡片毛玻璃效果。每层模糊度和透明度有微妙差异创造层次。

### 关键词

Glassmorphism, frosted glass, backdrop-filter, translucent, gradient background, layered

## 03. 新拟态 (`neo`)

> 新拟态，双向柔和阴影+统一底色

### 基础 Prompt

使用Neomorphism风格：背景#E4E9F0。组件同色背景，通过双向box-shadow(右下暗色#BEC8D4、左上亮色#FFFFFF)创造立体感。按钮按下用inset。

### 进阶 Prompt

新拟态设置面板：开关/滑块/输入框用凸起效果，交互状态用凹陷。激活的开关球体用渐变色+微弱发光。整体浅灰。

### 关键词

Neomorphism, soft UI, dual shadow, light gray, inset/outset, emboss, deboss

## 04. 极简主义 (`minimal`)

> 极简主义，大量留白+克制配色

### 基础 Prompt

极简设计：只用黑白灰。留白(padding/margin 32px+)。标题用衬线体，装饰只用极细线条(1px #EAEAEA)。无阴影、无渐变、无图标。

### 进阶 Prompt

极简落地页：标题用Cormorant Garamond衬线体48px+。页面80%是留白。分区只用细线。按钮只有文字+下划线。行高1.7-1.8。传达「克制的高级感」。

### 关键词

Minimalist, whitespace, restrained, serif, monochrome, thin separators, elegant simplicity

## 05. 千禧风 (`y2k`)

> Y2K千禧风，糖果色渐变+气泡圆角

### 基础 Prompt

Y2K风格：渐变粉(#FF6B9D)→紫(#C66AFF)→青(#00D4FF)。白色卡片+大圆角24px+彩色投影。药丸按钮+hover上浮。星星(✦✧)闪烁装饰。

### 进阶 Prompt

Y2K落地页：粉紫渐变+漂浮气泡。chrome金属文字(白→灰→白gradient+background-clip:text)。药丸按钮+渐变。✦twinkle动画。甜美、闪亮、怀旧未来感。

### 关键词

Y2K, candy gradient, chrome, bubbly, pill buttons, sparkle, glossy, pink-purple-cyan

## 06. 暗黑奢华 (`luxury`)

> 暗黑奢华，深色底+金色点缀+衬线体

### 基础 Prompt

Dark Luxury风格：背景#0A0A0A，文字暖白(#F5E6C8)，标题衬线体。金色(#C5A55A)做边框和标签。分隔线渐变(透明→金→透明)。按钮hover金色填充。

### 进阶 Prompt

暗黑奢华产品页：深色底+微妙金色径向光晕。小标签全大写+0.3em字间距+9px。分隔线渐变金色。按钮透明底+金色描边。金色只做点缀，不要大面积。

### 关键词

Dark luxury, black, gold accent, serif, wide letter-spacing, gradient divider, restrained, premium

## 07. 有机自然 (`organic`)

> 有机自然，大地色+不规则圆角+温暖质感

### 基础 Prompt

Organic风格：暖米色(#F4EDE4)底。主色橄榄绿(#6B8F71)，辅色暖棕。圆角24px，柔和阴影。有机blob装饰。药丸按钮+绿色。温暖自然感。

### 进阶 Prompt

Wellness App：米色底+淡绿blob装饰。图标用不规则圆角容器。文字用绿色系层级。卡片暖白(#FBF8F4)+暖色阴影。全部圆润无直角。

### 关键词

Organic, nature, earthy, olive green, warm beige, blob shapes, rounded, soft shadow, wellness

## 08. 赛博朋克 (`cyber`)

> 赛博朋克，霓虹粉青+发光+削角造型

### 基础 Prompt

Cyberpunk风格：背景#0D0221。霓虹粉(#FF2E97)+青(#00FFF0)。clip-path削角。发光效果(text-shadow/box-shadow)。扫描线(repeating-linear-gradient)。monospace字体。

### 进阶 Prompt

赛博朋克数据面板：深紫黑+扫描线叠加。主面板clip-path削角，品红→青渐变边框。标题品红+发光。数据青色monospace。输入框focus发光。glitch hover效果。

### 关键词

Cyberpunk, neon, magenta, cyan, glow, scanlines, clip-path, glitch, monospace, futuristic

## 09. 粘土风 (`clay`)

> 粘土风，超大圆角+彩色厚阴影+柔和配色

### 基础 Prompt

Claymorphism风格：浅灰底(#F0F0F3)。超大圆角24px+白色半透明边框+彩色offset阴影(不blur，多层)。按钮渐变粉/紫+同色阴影。软软的可以捏的感觉。

### 进阶 Prompt

粘土风任务App：浅灰底。卡片白色+厚彩色阴影(每张不同色)。图标渐变色方块+自身颜色阴影。主/次按钮区分。圆角至少20px。3D粘土渲染感。

### 关键词

Claymorphism, clay, soft 3D, big radius, colored offset shadow, pastel, playful, white border

## 10. 编辑排版风 (`editorial`)

> 编辑排版，字体大小对比+衬线混搭

### 基础 Prompt

Editorial风格：奶白底。标题Playfair Display 48px+ font-weight 900。小标签IBM Plex Mono 9px全大写+0.3em字间距。2px粗线分隔。一种强调色(#E63946)。杂志排版感。

### 进阶 Prompt

编辑风博客：超大衬线标题(64-80px)+斜体副标题+等宽小号日期。2px实线分隔。两栏grid布局。页面中间红色小色块(24px×3px)装饰。黑白灰+一点红。

### 关键词

Editorial, magazine, serif headline, monospace labels, extreme type scale, grid, one accent color

## 11. 扁平设计 (`flat`)

> 扁平设计，纯色块+零阴影+清晰层级

### 基础 Prompt

Flat Design风格：白色背景，不要任何阴影和渐变。用纯色块区分层级。主色用Google Blue(#4285F4)。圆角8px。按钮纯色填充，hover变深一档。干净利落。

### 关键词

Flat design, no shadows, solid colors, clean, simple, Google Material-like, primary colors

## 12. 材质设计 (`material`)

> Material Design，海拔阴影+涟漪+大胆配色

### 基础 Prompt

Material Design风格：白色卡片+elevation阴影系统(低：2px blur, 中：8px, 高：16px)。主色深紫(#6200EA)。药丸按钮+大写文字。圆角12px。

### 关键词

Material Design, elevation, shadow levels, ripple, FAB button, purple theme, rounded corners

## 13. 瑞士极简 (`swiss`)

> 瑞士极简，网格对齐+红色强调+无衬线

### 基础 Prompt

Swiss Style风格：白底+黑字+一个红色(#E63946)做唯一强调色。所有元素严格网格对齐。无衬线字体，字重对比做层级。左侧4px红色竖线。不要任何装饰。

### 关键词

Swiss style, International Typographic Style, grid, Helvetica, red accent, rational, functional

## 14. 蒸汽波 (`vapor`)

> 蒸汽波，粉紫渐变+霓虹+复古网格

### 基础 Prompt

Vaporwave风格：深紫渐变底。霓虹粉(#FF71CE)和青(#01CDFE)做强调。文字带微弱发光。卡片半透明深色+霓虹色边框。大写标签。复古怀旧+未来感。

### 关键词

Vaporwave, retro, neon pink, cyan, purple gradient, nostalgic, grid, aesthetic

## 15. 装饰艺术 (`artdeco`)

> 装饰艺术，金色几何+对称+衬线体

### 基础 Prompt

Art Deco风格：深蓝底(#1A2332)+金色(#D4AF37)装饰。中心对称排版。标题衬线体。金色细边框+◆钻石符号装饰。小标签用超宽字间距(0.4em)全大写。

### 关键词

Art Deco, gold, geometric, symmetrical, 1920s, luxury serif, diamond shapes, ornamental

## 16. 包豪斯 (`bauhaus`)

> 包豪斯，三原色+几何形+功能主义

### 基础 Prompt

Bauhaus风格：暖白底+黑色粗边框(2px)。只用三原色(红#E63946/蓝#2D5FD8/黄#FFD43B)做点缀。标签黄底黑字。圆形和方形几何装饰。无衬线粗体标题。

### 关键词

Bauhaus, primary colors, geometric, functional, black border, circle square triangle, modernist

## 17. 终端风 (`terminal`)

> 终端风，黑底绿字+等宽字体+命令行

### 基础 Prompt

Terminal风格：黑底(#111)+绿色文字(#00FF41)。所有字体用等宽体。卡片顶部加●●●窗口按钮。标题前加"> "提示符。标签前加"$ cat "。边框用#333。

### 关键词

Terminal, CLI, green on black, monospace, command prompt, hacker aesthetic, retro computing

## 18. 单色风 (`mono`)

> 单色风，纯黑白+强对比+字重层级

### 基础 Prompt

Monochrome风格：纯黑白设计，不要任何色彩。黑底白字。用字重(粗/细)和字号差异创造层级。标签暗灰。直角无圆角。按钮白底黑字+hover反转。

### 关键词

Monochrome, black and white, zero color, contrast, typographic hierarchy, stark, bold

## 19. 粗体排版 (`boldtype`)

> 粗体排版，超大字号+极端字重对比

### 基础 Prompt

Bold Typography风格：标题用condensed无衬线体(如Bebas Neue) 42px+。配一个强调色做标签(红/橙)。正文小而克制。文字大小差距要极端，形成视觉冲击。按钮全大写+宽字间距。

### 关键词

Bold typography, oversized, condensed font, extreme weight contrast, type-driven, impactful

## 20. Web3 风 (`web3`)

> Web3风，深色底+紫蓝渐变+微光效果

### 基础 Prompt

Web3风格：深色底(#0A0A1A)。卡片半透明+紫蓝渐变边框。按钮紫蓝渐变+发光阴影。标签紫色背景透明。整体科技感+未来感。backdrop-filter:blur做毛玻璃。

### 关键词

Web3, crypto, dark UI, purple gradient, indigo, glow, frosted, futuristic, DeFi aesthetic

## 21. 工业风 (`industrial`)

> 工业风，金属灰+琥珀色+等宽大写

### 基础 Prompt

Industrial风格：金属灰底(#333330)。琥珀/黄色(#F5A623)做强调。等宽字体+大写+宽字间距。边框用深灰。按钮描边琥珀色。整体实用主义、工厂感。

### 关键词

Industrial, metallic gray, amber, monospace, uppercase, utilitarian, rugged, tool-like

## 22. 学术风 (`academia`)

> 学术风，纸张质感+衬线体+脚注格式

### 基础 Prompt

Academia风格：纸张底色(#F5F1E8)。衬线字体(Crimson Pro)为主。标签用[方括号]包裹+等宽小字。描述用斜体。分隔线用棕色。整体像学术论文的排版。

### 关键词

Academia, scholarly, serif, paper texture, footnotes, brackets, italic, warm tones

## 23. SaaS 风格 (`saas`)

> SaaS风格，白底+蓝紫渐变+微妙阴影

### 基础 Prompt

SaaS风格：白底+微妙卡片阴影(0 1px 3px + 0 4px 16px)。主色蓝(#3B82F6)。按钮蓝紫渐变+发光阴影。标签浅蓝底+蓝字。圆角14px。现代专业感。

### 关键词

SaaS, clean, professional, blue gradient, subtle shadow, modern, trustworthy, rounded

## 24. 报纸风 (`news`)

> 报纸风，泛黄底+衬线标题+分栏排版

### 基础 Prompt

Newsprint风格：泛黄底(#F0EBDD)。标题Playfair Display大衬线+3px double下边框。日期等宽8px全大写。描述文字用两栏排版(CSS columns)。像传统报纸的排版。

### 关键词

Newsprint, newspaper, serif headline, columns, double border, dateline, aged paper

## 25. 极繁主义 (`maximal`)

> 极繁主义，多色彩+多装饰+有组织的混乱

### 基础 Prompt

Maximalism风格：多色渐变背景(红/黄/青/紫)。卡片白色+黑色粗边框+多色阴影(红+青offset)。顶部彩虹渐变条。标签黄底+黑色描边。按钮青色+黑色描边+硬阴影。✦装饰。

### 关键词

Maximalism, colorful, layered, decorative, multi-shadow, organized chaos, bold, energetic

## 26. 手绘风 (`sketch`)

> 手绘风，不规则圆角+虚线+草稿质感

### 基础 Prompt

Sketch/手绘风格：纸白底色。边框2px实线+不规则圆角(12px 4px 12px 4px)。分隔线用虚线(dashed)。标签用dashed边框+暖橙色。整体有铅笔画草稿的未完成感。

### 关键词

Sketch, hand-drawn, dashed border, irregular radius, pencil, draft, warm paper

## 27. 植物风 (`botanical`)

> 植物风，奶油底+深绿+衬线体+自然元素

### 基础 Prompt

Botanical风格：奶油底(#F7F3EE)。文字深绿(#2E3D20)。标题用Crimson Pro衬线体。标签浅绿底。按钮橄榄绿。边框用暖棕(#D5CDB8)。整体精致自然，像植物学图鉴。

### 关键词

Botanical, plant, cream background, olive green, serif, natural, elegant, floral

## 28. 现代暗色 (`moddark`)

> 现代暗色，近黑底+微灰层次+蓝色强调

### 基础 Prompt

Modern Dark风格：背景#111113，卡片#18181B。边框#27272A做层级区分。蓝色(#3B82F6)做唯一强调色。圆角14px。文字白色层级：#FAFAFA > #A1A1AA > #71717A。

### 关键词

Modern dark, dark mode, zinc, blue accent, subtle borders, professional, developer-focused

## 29. 几何趣味 (`geo`)

> 几何趣味，明亮色彩+几何装饰+粗边框

### 基础 Prompt

Playful Geometric风格：浅色底+彩色几何装饰(圆形/方形用色块和描边)。卡片白色+2px黑边框+20px圆角。按钮黄底+黑描边+药丸形状。顶部彩色条。标签绿底。活泼有趣。

### 关键词

Playful, geometric, colorful, circles, squares, bold border, fun, energetic, children

## 30. 动感风 (`kinetic`)

> 动感风，倾斜元素+对角线+红橙渐变

### 基础 Prompt

Kinetic风格：深色底+对角线条纹背景(subtle)。卡片微倾斜(rotate -1deg)。红→橙渐变做按钮和装饰条。标签红色半透明底+大写。充满运动感和动态能量。

### 关键词

Kinetic, dynamic, diagonal, rotated, red-orange gradient, energetic, motion, sporty

## 31. 极光风 (`aurora`)

> 极光风，深色底+紫蓝流动渐变+毛玻璃+柔和光晕

### 基础 Prompt

Aurora极光风格：深色底(#0F0C29到#302B63渐变)。叠加紫蓝色径向渐变光斑，微妙呼吸动画。卡片半透明毛玻璃+1px白色透明边框+18px圆角。蓝紫渐变按钮。整体梦幻宇宙感。

### 关键词

Aurora, northern lights, gradient glow, dreamy, cosmic, blue-purple, frosted glass, ethereal, ambient

## 32. 孟菲斯 (`memphis`)

> 孟菲斯，80s大胆几何+鲜艳色彩+offset阴影+虚线

### 基础 Prompt

Memphis孟菲斯风格：明黄底色。卡片白底+3px黑边框+offset彩色阴影(6px)。无圆角。大胆几何装饰(圆形/方形做背景)。青绿色标签。红色按钮+黑描边。虚线分割线。趣味活泼的80年代感。

### 关键词

Memphis, 80s, bold geometric, squiggles, offset shadow, bright colors, coral, teal, purple, playful, postmodern

## 33. 像素风 (`pixel`)

> 像素风，方块化+无圆角+等宽字体+复古游戏色

### 基础 Prompt

Pixel Art像素风格：深蓝黑底(#1A1C2C)。卡片深色+3px实色边框+无圆角。4px offset阴影。等宽字体(monospace)。红色按钮+像素感。标签绿底。有限色板(4-6色)。8-bit复古游戏感。

### 关键词

Pixel art, 8-bit, retro gaming, monospace, no border-radius, limited palette, sharp edges, blocky, nostalgic

## 34. 日式北欧 (`japandi`)

> 日式北欧，大地色+衬线字体+极度留白+微阴影

### 基础 Prompt

Japandi日式北欧风格：暖白底(#F5F0EB)。卡片微白+极小阴影+4px小圆角。大地色系(米/棕/灰褐)。衬线字体做标题。极简装饰—只用2px线条和留白。标签用细边框+大写小字。传达安静克制的美感。

### 关键词

Japandi, wabi-sabi, Scandinavian, muted earth tones, serif, whitespace, minimal, warm neutral, zen

## 35. 霓虹灯光 (`neon`)

> 霓虹灯光，纯黑底+粉色/青色发光+text-shadow光晕

### 基础 Prompt

Neon Glow霓虹风格：纯黑底(#0A0A0A)。卡片透明+霓虹粉(#FF0080)边框+box-shadow发光效果。标签霓虹青(#00FFFF)+text-shadow发光。按钮霓虹粉描边+发光。文字适度添加text-shadow光晕。都市夜晚氛围。

### 关键词

Neon, glow, neon pink, cyan, text-shadow, box-shadow, dark background, nightlife, fluorescent, luminous

## 36. 纸质风 (`paper`)

> 纸质风，米白底+纸纹+衬线字体+虚线装饰

### 基础 Prompt

Paper纸质风格：暖米底色(#F4EDE4)+微噪点纹理。卡片纸白底+柔和阴影+2px小圆角。衬线字体(serif)做标题。虚线(dashed)做分割线和标签装饰。焦糖色(#C1A87D)做强调。深褐色按钮。温暖的手工文具感。

### 关键词

Paper, stationery, craft, serif, dashed lines, warm beige, parchment, handmade, cozy, analog

## 37. 科幻 HUD (`hud`)

> 科幻HUD，深空黑+青色扫描线+切角边框+等宽大写

### 基础 Prompt

Sci-Fi HUD风格：深空黑底(#040810)+扫描线纹理(repeating-linear-gradient)。卡片透明青色+切角边框(clip-path polygon)。等宽字体+大写+大字间距(letter-spacing .1em+)。主色#00C8FF+发光效果。军事/航天科幻感。

### 关键词

HUD, sci-fi, heads-up display, clip-path, scanlines, cyan, monospace, uppercase, military tech, space

## 38. 柔和粉彩 (`pastel`)

> 柔和粉彩，多色粉彩渐变+大圆角+柔和彩色阴影

### 基础 Prompt

Pastel Soft柔和粉彩风格：多色粉彩渐变背景(粉→蓝→绿)。卡片白底+24px大圆角+柔和彩色阴影。粉蓝渐变按钮+20px药丸圆角。标签淡紫色背景。整体温柔治愈感，像糖果色彩。

### 关键词

Pastel, soft, candy colors, pink blue lavender, large border-radius, gentle shadow, cute, healing, kawaii

## 39. 做旧风 (`grunge`)

> 做旧风，暗褐底+噪点纹理+锈红强调+无圆角+等宽

### 基础 Prompt

Grunge做旧风格：暗褐底(#1C1A17)+噪点/纸纹纹理。卡片深色+细边框+无圆角。锈红色(#A83232)做强调色和按钮。等宽字体+大写标签。灰棕色文字。粗糙磨损的质感。独立摇滚/反叛态度。

### 关键词

Grunge, distressed, rough texture, noise, dark brown, rust red, monospace, worn, rebellious, underground

## 40. 企业蓝 (`corp`)

> 企业蓝，蓝白配色+8px圆角+细边框+专业规整

### 基础 Prompt

Corporate企业蓝风格：浅灰白底(#F0F4F8)。卡片白底+1px灰色边框+8px圆角+微阴影。蓝色(#2563EB)按钮和标签。深灰标题。清晰的信息层级。专业可靠的商务感。DM Sans或无衬线字体。

### 关键词

Corporate, blue-white, professional, clean, trustworthy, enterprise, business, reliable, conventional, safe

## 41. 新粗野主义 (`neubr`)

> 新粗野主义，糖果色+黑粗边框+硬边阴影+圆角

### 基础 Prompt

Neubrutalism风格：明亮糖果色背景(粉紫#F9E4FF)，2px黑色粗边框，4px偏移硬边阴影，12px圆角。标签用亮黄#FFE566+黑框。整体bold但friendly。

### 关键词

Neubrutalism, candy colors, thick borders, offset shadow, playful, bold, Figma-style

## 42. 拟物设计 (`skeu`)

> 拟物设计，真实材质纹理+渐变高光+内阴影

### 基础 Prompt

Skeuomorphism拟物风格：皮革/金属质感渐变，多重box-shadow(外阴影+inset高光)。按钮用金色渐变+内高光+外阴影模拟凸起按钮。

### 关键词

Skeuomorphism, realistic, texture, gradient, embossed, inset shadow, leather, metal, 3D depth

## 43. 复古未来主义 (`retfut`)

> 复古未来主义，橙+青绿+奶油底+不对称圆角

### 基础 Prompt

Retro Futurism风格：奶油色底(#FBF5E6)，橙色(#E8743A)和青绿色(#2A9D8F)双色搭配。不对称大圆角。Georgia衬线字体。50年代太空时代的浪漫乐观感。

### 关键词

Retro futurism, space age, atomic age, teal-orange, serif, cream, 1950s, optimistic

## 44. 便当盒网格 (`bento`)

> 便当盒网格，Apple风格+白底+大圆角+微阴影

### 基础 Prompt

Bento Box风格：纯白卡片、18px大圆角、微妙阴影(0 2px 12px rgba(0,0,0,.07))。iOS蓝(#007AFF)做强调色。系统字体。多尺寸网格布局，像Apple Keynote。

### 关键词

Bento box, grid, Apple keynote, clean, white cards, rounded, subtle shadow, system font

## 45. AI原生界面 (`ainative`)

> AI原生界面，深黑底+紫蓝渐变+微光晕边框

### 基础 Prompt

AI Native UI风格：深黑底(#111)，紫色(#8B5CF6)→蓝色(#3B82F6)渐变做强调。卡片有微妙紫色光晕边框。标签药丸形+半透明紫色底。ChatGPT/Claude式界面感。

### 关键词

AI native, dark mode, purple-blue gradient, chat bubble, conversational, LLM, streaming

## 46. 液态玻璃 (`liqglass`)

> 液态玻璃，高透明+强模糊+内高光+浅灰底

### 基础 Prompt

Liquid Glass风格（Apple 2025）：浅灰蓝底色上，高透明面板(rgba(255,255,255,.45))+blur(32px)。边框白色70%不透明度。内高光(inset 0 1px white 80%)。圆角26px+。比Glassmorphism更通透。

### 关键词

Liquid glass, Apple 2025, iOS 26, translucent, frosted, high blur, inset highlight, soft, refraction

## 47. 空间界面 (`spatial`)

> 空间界面，多层漂浮+超大圆角+极深阴影+强模糊

### 基础 Prompt

Spatial UI风格（VisionOS）：浅灰底色，面板rgba(255,255,255,.35)+blur(40px)。超大圆角28px+。多层box-shadow模拟Z轴深度(0 20px 60px)。内边距32px+。面板间有明显的层次关系。

### 关键词

Spatial UI, VisionOS, XR, floating panels, z-depth, large radius, heavy blur, layered

## 48. 3D超写实 (`hyper3d`)

> 3D超写实，彩色阴影+立体按钮+鲜艳渐变+大圆角

### 基础 Prompt

3D Hyperrealism风格：白色卡片+22px大圆角。关键是彩色阴影（不是灰色，而是主色系的半透明阴影）。按钮用渐变+底部硬阴影模拟3D按压效果。鲜艳的多色渐变装饰条。

### 关键词

3D hyperrealism, colored shadow, vibrant gradient, depth, Blender-style, thick shadow, playful

## 49. OLED纯黑 (`oled`)

> OLED纯黑，纯黑底+高对比白字+极少蓝色点缀

### 基础 Prompt

OLED Dark风格：纯黑背景#000（不是深灰！）。白色文字#fff。极细边框1px #1A1A1A。强调色只用iOS蓝(#0A84FF)，极少使用。整体极致克制纯净。

### 关键词

OLED, pure black, high contrast, minimal color, #000, energy saving, iOS dark

## 50. 动效驱动 (`motionui`)

> 动效驱动，微倾斜+红橙渐变+动感能量条+彩色投影

### 基础 Prompt

Motion Driven风格：白色卡片微倾斜(skewY -1deg)。红→橙渐变做能量条和按钮。彩色投影(不是灰色阴影)。一切设计暗示"运动中"——倾斜、渐变、动感。

### 关键词

Motion driven, animation, skew, energetic, gradient, dynamic, red-orange, velocity

## 51. 动态字体 (`kintype`)

> 动态字体，深黑底+巨大白字+红色线+极简

### 基础 Prompt

Kinetic Typography风格：深黑底(#111)。标题用32px+ 900weight的超大粗体白字，letter-spacing负值让字母紧凑。红色(#FF3300)全宽装饰线。标签用红色大写+超大字间距。几乎没有装饰元素。

### 关键词

Kinetic typography, oversized text, bold, animated text, dark, editorial, red accent, weight 900

## 52. 视差叙事 (`parallax`)

> 视差叙事，奶油色调+衬线字体+极致留白+金棕细线

### 基础 Prompt

Parallax Storytelling风格：温暖奶油底(#F2ECE4)。Cormorant Garamond衬线字体做标题(26px+)。金棕色(#C8A87A)细线做分隔。大量留白。描述用斜体。按钮只是一条下划线。整体像阅读一本精美的散文集。

### 关键词

Parallax, storytelling, scroll, serif, warm, cream, editorial, narrative, chapter, elegant

## 53. 电子墨水 (`eink`)

> 电子墨水，暖灰纸色+零阴影+衬线体+零圆角

### 基础 Prompt

E-Ink Digital风格：暖灰底(#F9F6F0)。Georgia衬线字体。零阴影零装饰。边框1px #D8D0C4。标签用IBM Plex Mono等宽体+大写+大字间距。按钮纯黑底白字无圆角。像Kindle阅读器的界面。

### 关键词

E-ink, Kindle, paper, warm gray, serif, no shadow, minimal, reading, zero decoration

## 54. 色差分离 (`chroma`)

> 色差分离，深黑底+红青RGB偏移+等宽体+故障感

### 基础 Prompt

Chromatic Aberration风格：深黑底(#0A0A10)。标题用text-shadow: 2px 0 rgba(255,51,0,.5), -2px 0 rgba(0,255,255,.5)制造RGB色差。等宽字体+大写。红(#FF3300)和青(#00FFFF)双色体系。按钮青色边框+红色text-shadow。

### 关键词

Chromatic aberration, RGB split, glitch, red-cyan, monospace, dark, experimental, lens distortion

## 55. 复古胶片 (`vintage`)

> 复古胶片，暖棕金色调+衬线体+内发光+做旧

### 基础 Prompt

Vintage Analog风格：暖奶油底(#F5E8CC)。棕金色系(#C4A060/#8B5E3C)。Cormorant Garamond衬线字体。分隔线用淡入淡出渐变。按钮用金色渐变模拟金属质感。描述文字斜体。整体营造胶片摄影般的温暖怀旧感。

### 关键词

Vintage, analog, film, warm, sepia, gold-brown, serif, nostalgic, retro, grain

## 56. 维度层叠 (`dimlayer`)

> 维度层叠，深蓝底+多层阴影+半透明面板+蓝紫光

### 基础 Prompt

Dimensional Layering风格：深蓝紫渐变背景(#1A1A2E→#0F3460)。面板半透明(rgba白色6%)+blur(20px)。关键是多层box-shadow(至少3层)模拟不同深度。浅蓝(#4FC3F7)和淡紫(#CE93D8)做强调色。

### 关键词

Dimensional, layering, z-depth, multi-shadow, translucent, dark, navy, blue-purple, stacked

## 57. 夸张极简 (`exmin`)

> 夸张极简，纯白+零装饰+超大标题+极细线

### 基础 Prompt

Exaggerated Minimalism风格：纯白背景，零阴影零边框零圆角。标题用36px+ 800weight超大粗体。辅助文字极小(8-10px)且极浅灰色(#CCC)。按钮只是一条下划线。分隔线几乎不可见(#F0F0F0)。大小对比是唯一的设计手段。

### 关键词

Exaggerated minimalism, ultra-white, oversized title, hairline, contrast, void, dramatic, empty

## 58. 活力色块 (`vibrant`)

> 活力色块，大面积纯色+硬边拼接+粗体文字

### 基础 Prompt

Vibrant Block Based风格：用大面积纯色色块(#FF6B35橙、#004E89蓝、#FCBF49黄)构建布局。每个section一个颜色，色块之间硬边衔接无过渡。文字用粗体白色或黑色。零渐变零阴影，纯平面设计。

### 关键词

Vibrant blocks, color sections, flat, bold, Mondrian, primary colors, hard edges, sectioned layout

## 59. 柔性UI进化 (`softui`)

> 柔性UI，双阴影+凸起凹陷+柔和渐变+高圆角

### 基础 Prompt

Soft UI Evolution风格：浅灰蓝背景(#E8EDF5)上用双层box-shadow创造凸起效果(亮影#F0F4FA在左上，暗影#D1D9E6在右下)。圆角16px+。按钮用凸起效果，输入框用凹陷效果(inset shadow)。整体色调柔和统一。

### 关键词

Soft UI, neumorphism evolved, dual shadow, emboss, deboss, pillow effect, accessible, subtle gradient

## 60. Z世代混沌 (`genz`)

> Z世代混沌，荧光撞色+歪斜元素+贴纸装饰+字体混搭

### 基础 Prompt

Gen Z Chaos Maximalism风格：荧光色系(品红#FF00FF、荧光绿#00FF88、电光黄#FFE600)随机撞色。元素带1-3度随机旋转。黑色粗边框+彩色阴影偏移。到处散落emoji和贴纸装饰。字体大小极端对比，混搭手写、像素和衬线体。

### 关键词

Gen Z, chaos, maximalism, neon clash, stickers, emoji, tilted, meme aesthetic, TikTok, anti-design

## 61. 反精致美学 (`rawpol`)

> 反精致，手绘线条+粗糙边缘+裸露结构+等宽字体

### 基础 Prompt

Anti-Polish Raw风格：暖白纸色背景(#F5F0EB)上用虚线边框(dashed)和手绘感线条。字体用Courier New等宽体。图片不裁剪，保留粗糙边缘。无圆角无阴影。露出网格线和参考线。颜色极少，主要靠黑白+一个棕褐色(#8B7355)点缀。

### 关键词

Anti-polish, raw, unfinished, hand-drawn, rough edges, exposed grid, monospace, authentic, rebellion

## 62. 触感数字 (`tactile`)

> 触感数字，纹理表面+材质色调+微妙凹凸+温暖质感

### 基础 Prompt

Tactile Digital风格：亚麻白底(#F7F3EE)加微妙纸张纹理(noise SVG或CSS grain)。边框用砂石色(#D4C5B2)。卡片有微弱阴影模拟凸起感。色调温暖：皮革棕(#8B7355)、深木色(#3D3027)。字体用衬线体(Source Serif)增强印刷质感。

### 关键词

Tactile, texture, paper grain, fabric, warm materials, emboss, physical, haptic, organic surface

## 63. 渐变网格 (`gradmesh`)

> 渐变网格，多点渐变+半透明层+模糊效果+流动色彩

### 基础 Prompt

Gradient Mesh风格：用多点渐变背景(靛蓝#667EEA→深紫#764BA2→粉紫#F093FB)。卡片半透明白色+backdrop-filter blur(8px)。边框用rgba白色(0.2透明度)。阴影带渐变主色调。圆角20px。整体如梦如幻的色彩流动感。

### 关键词

Gradient mesh, multi-stop gradient, aurora, flowing colors, blur, translucent, dreamy, vibrant depth

## 64. 3D产品展示 (`prod3d`)

> 3D产品展示，深色背景+高光阴影+悬浮效果+电影光影

### 基础 Prompt

3D Product Preview风格：深黑背景(#0A0A0A)上产品3D渲染图悬浮居中。微弱的rgba白色边框(0.08)。巨大的阴影(0 20px 60px)模拟悬浮。文字用银灰(#E0E0E0)。点缀色用科技蓝(#00D4FF)做CTA和高光。圆角16px。

### 关键词

3D product, dark stage, floating, cinematic lighting, hero render, deep shadow, tech showcase, premium

## 65. 交互光标 (`cursor`)

> 交互光标，自定义光标+跟随动画+磁吸效果+轨迹视觉化

### 基础 Prompt

Interactive Cursor风格：深黑背景(#1A1A1A)。隐藏默认光标(cursor:none)，用JS自定义圆形光标。光标跟随用lerp缓动。悬停按钮时光标放大+变色(信号红#FF4444)。留下微妙的鼠标轨迹。元素在鼠标接近时微微"磁吸"偏移。

### 关键词

Custom cursor, magnetic hover, follow animation, trail, interactive, playful, motion, mouse tracking

## 66. 微交互 (`microix`)

> 微交互，状态动画+弹性缓动+骨架屏+悬停反馈

### 基础 Prompt

Micro Interactions风格：极浅灰背景(#FAFBFC)。每个可交互元素都有transition(.2s cubic-bezier)。按钮hover时微微上移+加深阴影。开关用spring动画。数字变化用滚动效果。加载用骨架屏shimmer。边框浅灰(#E1E4E8)，圆角6px。

### 关键词

Micro interactions, spring animation, skeleton screen, hover feedback, transition, cubic-bezier, alive UI

## 67. 零界面 (`zeroint`)

> 零界面，无UI装饰+内容即界面+手势驱动+上下文感知

### 基础 Prompt

Zero Interface风格：纯白背景，零装饰。没有可见的导航栏——通过手势或滚动触发。没有按钮边框——文字本身就是按钮。没有卡片——内容直接呈现。字体用系统字体(SF Pro)。颜色只有黑(#111)、白(#FFF)、灰(#999)。一切UI痕迹都被消除。

### 关键词

Zero UI, invisible interface, content-first, no chrome, gesture-driven, ambient, contextual, disappearing UI

## 68. 米色柔调 (`cream`)

> Cream SaaS，米色底 + 小衬线 + 暖棕强调

### 基础 Prompt

Cream SaaS 风格：整站背景不用纯白，改成 #F5F1EA 米色。卡片用略浅的 #F7F3EB。标题小衬线（Fraunces / Söhne / Reckless），正文可搭配 Inter。强调色一个暖棕 #8A6E4D。整体给"quiet luxury"感。

### 进阶 Prompt

Cream SaaS Landing：hero 米黄大标题 + 短衬线小 tag + 单一 CTA（深黑填充 pill 按钮）。cards 用非常轻的阴影 0 1px 2px rgba(139,110,77,.06)。避免灰色边框，用略深米色分隔。

### 关键词

Cream, warm white, off-white, quiet luxury, small serif, Fraunces, warm brown accent, no pure white, Attio, Cursor

## 69. 颗粒渐变 (`grain`)

> 颗粒渐变，柔渐变 + SVG 噪点 + 衬线

### 基础 Prompt

Grainy Gradient 风格：hero 背景 135deg 米色到暖灰的柔渐变，叠加一层 SVG turbulence noise（opacity .4, mix-blend-mode:multiply）。标题用 Fraunces 大衬线。强调色 #E85D4E 橙红。

### 进阶 Prompt

Anthropic 风：整站米暖底 + 全局颗粒噪点。hero 用大衬线 headline + 简短 tagline。CTA pill 按钮橙红。次要卡片用 rgba(255,253,248,.85) + backdrop-blur 让颗粒透出。

### 关键词

Grainy, noise texture, feTurbulence, warm gradient, film grain, Anthropic style, Fraunces, warm orange accent

## 70. 编辑级 SaaS (`editorialsaas`)

> 编辑级 SaaS，大衬线 + mono chip + 单一强色

### 基础 Prompt

Editorial SaaS 风格：hero 用超大 Fraunces / Playfair 衬线 headline（60-96px），line-height 1.05。上方一个 8-9px mono chip 作 eyebrow。CTA 一个方形 filled 电蓝按钮 #0038FF。body 用 Inter 13-14px。整站白/米背景。

### 进阶 Prompt

Notion / Cursor 官网风：navbar 极简 + logo + 4 个链接。hero 一个 5-6 词衬线大标题 + 一句 tagline + 单个 CTA。section 之间用 Fraunces 大字号衬线分隔。所有 chip / meta 一律 mono。

### 关键词

Editorial SaaS, display serif, big headline, mono eyebrow, Fraunces, Notion 2025, Cursor, Perplexity, publication meets product

## 71. 环境光 (`ambient`)

> 环境光，暗底 + 柔光晕 + 极细字

### 基础 Prompt

Ambient Glow 风格：背景 #0F0E12 近黑。hero 中央加一个 radial-gradient 光晕（粉+青，blur 40px, opacity .35）。文字用衬线 300 weight 或 Inter 200-300。所有边框 rgba(255,255,255,.08)。CTA pill 按钮半透明。

### 进阶 Prompt

Rive 官网风：整站极暗背景。每 section 一个不同颜色的柔光光晕（顶部粉、中部青、底部橙）。文字全部极细 weight。零硬边、零锐角。cards 用 rgba(255,255,255,.03) + backdrop-blur。

### 关键词

Ambient, glow, radial gradient, soft blur, cinematic, Rive, Linear Method, dark but not cyber, thin type

## 72. 技术规格 (`spec`)

> 技术规格，细网格 + 等宽 + 技术标注

### 基础 Prompt

Spec Sheet 风格：背景 #F4F1EC 米色 + 细网格线（rgba(10,10,10,.05), 20px grid）。所有文字用 IBM Plex Mono。边框 1px 黑色实线，零圆角。加技术编号 SPEC-01 / REV-A2 / FIG-3 作 chip。

### 进阶 Prompt

Neuralink / 1x 硬件页面风：hero 一张产品的技术剖面图（可用 SVG stroke），旁边标注 mm 尺寸、序号、部件名。表格全 mono、无斑马纹、只有细横线分割。CTA 一个方形边框按钮 "> DOWNLOAD SPEC"。

### 关键词

Spec sheet, technical drawing, blueprint, engineering, monospace, grid, Physical Intelligence, 1x, Neuralink, Rivian tech

## 73. ASCII 字符艺术 (`ascii`)

> ASCII 艺术，字符构图 + dashed 边框 + 绿字黑底

### 基础 Prompt

ASCII Art 风格：深黑背景 #0A0A0A。所有文字磷光绿 #00FF41 (IBM Plex Mono)。装饰用大段 ASCII 字符：▓▓▒▒░░ 作分隔、━━━━ 作横线、┌───┐ 作 box。琥珀色 #FFB000 作次要强调。

### 进阶 Prompt

Neal.fun / Every 独立博客风：hero 用一大段 ASCII art logo（几十字符构成图案）。navigation 用 [ ITEM ] 方括号。button 前加 > 箭头。所有边框 dashed 或 dotted。加一行 [SYS] 状态条在底部。

### 关键词

ASCII art, character art, monospace, terminal aesthetic, phosphor green, hacker, Neal.fun, retro computing, no images just characters

## 74. 维多利亚繁复 (`victorian`)

> 维多利亚，酒红深底 + 烫金花体 + 装饰符号

### 基础 Prompt

Victorian Ornate 风格：深酒红 #2A0F14 底 + 烫金 #C9A961 边框和分隔线。标题用 Playfair Display Black Italic 900 号。装饰用 ❦ · ✧ 等花体符号。文字用奶油米 #F5E6C8。

### 进阶 Prompt

Aesop / Loewe 精品商店风：hero 深底 + 单一花体大标题（意大利斜体）+ 烫金细节。产品卡片有装饰性花纹 border。CTA 烫金 pill 或方形，字用 italic serif。整体像 19 世纪印刷广告。

### 关键词

Victorian, ornate, gold on burgundy, Playfair Display, filigree, decorative serif, 19th century, Aesop, luxury, italic

## 75. 原子时代 (`atomic`)

> 原子时代，青橙双色 + 米黄底 + Poppins/Futura + 星芒

### 基础 Prompt

Atomic Age 风格：米黄底 #F5E6D3。青绿 #1A9EB3 + 橙红 #E85D3C 双主色。字体 Futura / Poppins 全大写粗体。装饰用星芒 ✦ 和圆形（原子模型）。硬边阴影 box-shadow: 6px 6px 0 #1A9EB3。

### 进阶 Prompt

Kirby Ferguson / 60s 广告风：hero 一个 Futura Black 大标题（全大写）+ 星芒装饰。cards 有偏移硬阴影（青绿或橙）。按钮矩形无圆角、粗字体、大写字母。加一个大的 boomerang 或圆形装饰在背景。

### 关键词

Atomic Age, mid-century modern, 1950s, 1960s, Futura, teal and orange, boomerang, starburst, Kirby Ferguson, Mad Men

## 76. 复印机杂志 (`zine`)

> Zine 风，黑白高对比 + 旋转错位 + Impact/Courier

### 基础 Prompt

Zine / Xerox 风格：米白背景 #F5F5F0。所有卡片和 chip 都轻微旋转（-2° 到 +2°）。字体 Impact 大标题 + Courier 正文。橙红 #FF3B00 只作警报。cards 有粗黑边框 + 硬阴影。整体像被复印机复印过一次。

### 进阶 Prompt

Riot Grrrl / Substack Notes 独立风：hero 一个 Impact 900 大标题（旋转 .4°）+ 手写风 tag + 剪纸拼贴风的图片框。chip 用 Courier + 方括号或全大写 + 旋转 -1°。CTA 粗黑边框 + 硬偏移 + 大写字体。

### 关键词

Zine, Xerox, photocopy, punk, cut and paste, Impact, Courier, high contrast, rotated cards, DIY, Riot Grrrl

## 77. 波普网点 (`halftone`)

> 波普网点，黑白点 + 双层阴影 + Bangers 大写

### 基础 Prompt

Halftone Comic 风格：米色底 + 全站细网点纹理（radial-gradient 6px spacing）。卡片粗黑 3px 边框 + 双层偏移阴影：先粉后蓝。标题用 Bangers / Impact 全大写。tag 用黄色 + 黑边 + 旋转 -3°。

### 进阶 Prompt

Marvel Comics 官网 / 潮牌风：hero 一个 Bangers 大标题带 pink text-shadow（模拟 CMYK 错版）。CTA 大按钮蓝底 + 粗黑边 + 硬偏移。所有 chip 有 comic bubble 感（细微旋转 + 黑边）。加漫画对话框元素。

### 关键词

Halftone, comic book, Pop Art, Lichtenstein, Marvel, Andy Warhol, Bangers, Impact, dots pattern, hard offset shadow
