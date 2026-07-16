---
name: xianyu-seller-toolkit
description: 闲鱼虚拟产品卖家一站式内容工具链。触发词包括"调用 xianyu-seller-toolkit""卖家工具链""上架闲鱼""虚拟资料处理"。具身智能：根据用户具体需求自动判断执行完整管线还是只调用其中某个工具。
---

# 闲鱼卖家工具链 (Xianyu Seller Toolkit)

> 所有工具只做**内容层**，不碰平台操作。

## ⚡ 核心原则：按需调用

**被触发时，必须先判断用户意图，只执行需要的步骤，不要总是跑全流程。**

## 🧠 智能路由表

根据用户的话，匹配对应工具：

| 用户说了什么 | 调用哪个工具 | 
|-------------|-------------|
| "处理这个资料""准备上架""完整走一遍" | → 完整管线（流程A） |
| "润色一下""排版优化""格式化" | → 只用 `baoyu-format-markdown` |
| "生成展示图""做几张卡片""商品图" | → 只用 `baoyu-image-cards` + `baoyu-imagine` |
| "生成封面图""做张图" | → 只用 `baoyu-imagine` 或 `FishClaw generate_image_tools` |
| "转成HTML""HTML交付版""浏览器打开" | → 只用 `baoyu-markdown-to-html` |
| "写文案""宝贝描述""闲鱼标题" | → 只用 `FishClaw prompt_tools` |
| "竞品调研""看看闲鱼上怎么卖的""定价参考" | → 只用 `ai-goofish` |
| "社交卡片""小红书图文" | → 只用 `guizang-social-card-skill` |

## 工具清单

| # | 工具 | 做什么 | 输入 | 输出 |
|---|------|--------|------|------|
| 1 | `baoyu-format-markdown` | 润色排版 + 优化标题 | .md 文件 | 润色版 .md |
| 2 | `baoyu-image-cards` + `baoyu-imagine` | 内容→5张商品展示图 | .md 文件内容 | 5张 PNG (1080×1440) |
| 3 | `guizang-social-card-skill` | Markdown→社交卡片 | .md 文件 | PNG 卡片 |
| 4 | `baoyu-markdown-to-html` | .md→精美HTML | .md 文件 | .html (浏览器打开) |
| 5 | `FishClaw prompt_tools` | AI写闲鱼文案 | 商品主题 | 标题+描述+卖点+话术 |
| 6 | `FishClaw generate_image_tools` | AI生成封面图 | 主题描述 | PNG 图片 |
| 7 | `ai-goofish` | 闲鱼关键词监控+竞品分析 | 关键词 | 竞品数据 |

## 流程 A：完整管线

仅当用户明确要求**完整处理**或**准备上架**时执行：

```
原始 .md
  → [1] baoyu-format-markdown → 润色版 .md
  → [2] baoyu-image-cards → 5张展示图 (会先确认风格)
  → [3] 去商品信息区 → 交付版 .md
  → [4] baoyu-markdown-to-html → 交付版 .html (modern+blue)
  → [5] FishClaw prompt_tools → 闲鱼描述文案
```

## 环境

| 工具 | 状态 |
|------|------|
| baoyu-format-markdown | ✅ |
| baoyu-image-cards + baoyu-imagine | ✅ DashScope qwen-image-2.0-pro |
| baoyu-markdown-to-html | ✅ |
| guizang-social-card-skill | ✅ |
| FishClaw prompt_tools | ✅ |
| ai-goofish | ⚠️ 需配置 |
