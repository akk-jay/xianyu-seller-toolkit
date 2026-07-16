---
name: xianyu-seller-toolkit
description: 闲鱼虚拟产品卖家一站式内容工具链。当你需要把虚拟资料上架到闲鱼时使用。直接说"调用 xianyu-seller-toolkit 处理这个资料"即可触发完整管线：内容润色→展示图生成→HTML交付件→商品文案。
---

# 闲鱼卖家工具链 (Xianyu Seller Toolkit)

**调用方式**：在对话中说以下任意一句即可触发：

- "调用 xianyu-seller-toolkit 把这个虚拟资料处理一下，我要上架到平台当虚拟资料卖"
- "调用卖家工具链处理这个文件"
- "帮我把这份资料准备上架闲鱼"
- "/xianyu-seller-toolkit"

工具链只做**内容层**（润色/出图/文案/HTML），不碰平台操作。

## 工具总览

```
┌─────────────────────────────────────────────────────┐
│                闲鱼卖家工具链 v1.0                      │
├──────────────┬──────────────────────────────────────┤
│ 阶段          │ 工具                                  │
├──────────────┼──────────────────────────────────────┤
│ 1. 内容润色    │ baoyu-format-markdown               │
│ 2. 展示图生成  │ baoyu-image-cards + baoyu-imagine    │
│ 3. 社交卡片    │ guizang-social-card-skill            │
│ 4. HTML 交付   │ baoyu-markdown-to-html               │
│ 5. AI 文案     │ FishClaw prompt_tools                │
│ 6. AI 生图     │ FishClaw generate_image_tools        │
│ 7. 竞品调研    │ ai-goofish (闲鱼智能监控)             │
│ 8. 定价参考    │ 内置分析                              │
└──────────────┴──────────────────────────────────────┘
```

## 标准工作流

对一个虚拟资料执行完整上架准备：

### 流程 A：新资料上架（完整管线）

```
原始 .md 文件
  │
  ├─[1] baoyu-format-markdown → 润色版 .md
  │    优化排版、标题、添加商品信息区
  │
  ├─[2] baoyu-image-cards → 5张展示图 PNG (1080×1440)
  │    ai分析内容 → 确认风格 → 生成提示词 → 出图
  │
  ├─[3] 去掉商品信息区 → 交付版 .md
  │
  ├─[4] baoyu-markdown-to-html → 交付版 .html
  │    modern主题 + blue配色 → 浏览器直接打开
  │
  ├─[5] FishClaw prompt_tools → 闲鱼宝贝描述文案
  │    标题 + 描述 + 卖点 + 自动回复话术
  │
  └─[6] 输出清单：
         📄 润色版.md（自己留底）
         📄 交付版.html（发给顾客）⭐
         🖼️ 5张展示图 PNG（上架用）
         📝 闲鱼描述文案.md
```

### 流程 B：竞品调研

```
ai-goofish
  │
  ├─ 配置监控关键词（如"GitHub开源项目"）
  ├─ AI 分析竞品标题/价格/销量
  ├─ 参考定价
  └─ 优化自己的标题和描述
```

## 环境依赖

| 工具 | 依赖 | 状态 |
|------|------|------|
| baoyu-format-markdown | Bun + npm 包 | ✅ |
| baoyu-image-cards | EXTEND.md 已配置 | ✅ DashScope |
| baoyu-imagine | EXTEND.md 已配置 | ✅ qwen-image-2.0-pro |
| baoyu-markdown-to-html | Bun + npm 包 | ✅ |
| guizang-social-card-skill | 已克隆到本地 | ✅ |
| FishClaw prompt_tools | Python + DashScope API Key | ✅ |
| ai-goofish | Python + Playwright + AI API | ⚠️ 需配置 |

## 调用方式

在对话中说以下任意一句即可触发：

- "用卖家工具链处理这个文件"
- "把这个资料准备上架闲鱼"
- "帮我生成这个虚拟产品的展示图"
- "调研一下这个品类在闲鱼上的情况"
- "生成这个资料的 HTML 交付版"

## 项目目录结构

```
GitHub合集/
├── .claude/skills/xianyu-seller-toolkit/SKILL.md  ← 本文件
├── .baoyu-skills/                                   ← 图片/排版技能配置
├── guizang-social-card-skill/                       ← 社交卡片技能
├── FishClaw_MCP/                                    ← 闲鱼工具集
├── ai-goofish/                                      ← 竞品监控
└── image-cards/                                     ← 生成的图片输出
```

## 注意事项

- 所有工具只做**内容生产**，不做平台自动操作
- 闲鱼网页版发布功能受限，建议用 App 手动发布
- DashScope API Key 需要在环境变量中配置
- ai-goofish 为只读监控，风险低但需遵守平台规则
