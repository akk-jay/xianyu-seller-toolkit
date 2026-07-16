# 🐟 闲鱼卖家工具链 (Xianyu Seller Toolkit)

> 虚拟产品卖家的一站式内容生产管线——从原始 Markdown 到精美商品展示图 + HTML 交付件，全流程 AI 驱动。

[![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.11+-green)](https://python.org)
[![Bun](https://img.shields.io/badge/runtime-bun-orange)](https://bun.sh)

---

## 🎯 解决什么问题

在闲鱼卖虚拟资料（教程、清单、模板、代码合集等），你需要：

| 环节 | 传统做法 | 本工具链 |
|------|---------|---------|
| 内容排版 | 手动调格式 | AI 一键润色 |
| 商品图 | PS/Canva 慢慢做 | AI 自动生成 5 张套图 |
| 交付文件 | 发 .md，顾客不会打开 | 发精美 HTML，双击浏览器看 |
| 宝贝描述 | 憋半天写不出来 | AI 生成标题+描述+卖点+话术 |
| 竞品调研 | 手动翻闲鱼 | 关键词监控 + AI 分析 |

## 🧰 工具链架构

```
xianyu-seller-toolkit
├── 📝 内容润色        baoyu-format-markdown
├── 🖼️ 展示图生成      baoyu-image-cards + baoyu-imagine
├── 🎴 社交卡片        guizang-social-card-skill
├── 🌐 HTML 交付       baoyu-markdown-to-html
├── ✍️ AI 文案         FishClaw prompt_tools
├── 🎨 AI 生图         FishClaw generate_image_tools
└── 🔍 竞品调研        ai-goofish
```

## 🚀 快速开始

### 环境要求

- Python 3.11+
- Bun (JavaScript runtime)
- DashScope API Key（阿里云通义万相）

### 安装

```bash
# 克隆仓库
git clone https://github.com/YOUR_USERNAME/xianyu-seller-toolkit.git
cd xianyu-seller-toolkit

# 安装 Python 依赖
cd FishClaw_MCP && pip install -e . && cd ..

# 安装 JS 依赖
cd guizang-social-card-skill && npm install && cd ..

# 配置 API Key
cp FishClaw_MCP/.env.example FishClaw_MCP/.env
# 编辑 .env 填入你的 DASHSCOPE_API_KEY
```

### 使用

在 Claude Code 中，直接说：

```
用卖家工具链处理 <你的文件.md>
```

工具链会自动执行完整管线：

```
原始 .md
  → AI 润色排版
  → 生成 5 张商品展示图 (1080×1440)
  → 转换为精美 HTML 交付件
  → 生成闲鱼标题 + 描述 + 话术
```

### 手动使用各工具

```bash
# 内容润色
bun scripts/format.ts your-file.md

# Markdown → HTML
bun scripts/convert.ts your-file.md --theme modern --color blue

# 生成展示图（通过 Claude Code Skill）
# 在对话中说："用 baoyu-image-cards 生成这个内容的卡片"

# 竞品调研
cd ai-goofish && python web_server.py
# 打开 http://localhost:5000 配置监控任务
```

## 📂 项目结构

```
xianyu-seller-toolkit/
├── CLAUDE.md                         # Claude Code 项目指南
├── README.md                         # 本文件
├── .gitignore
├── .claude/skills/
│   └── xianyu-seller-toolkit/
│       └── SKILL.md                  # 工具链 Skill 定义
├── guizang-social-card-skill/        # 归藏社交卡片技能
├── FishClaw_MCP/                     # 闲鱼文案+生图工具
│   ├── tools/
│   │   ├── prompt_tools.py           # AI 文案生成
│   │   └── generate_image_tools.py   # AI 图片生成
│   └── publish_semi_auto.py          # 半自动发布脚本
└── ai-goofish/                       # 闲鱼竞品监控
```

> 💡 把你的虚拟产品资料（.md 文件）放在项目根目录，用 `卖家工具链` 一键处理。产品文件不会被提交到 Git。

## ⚠️ 重要说明

- **本工具链只做内容生产**，不自动操作闲鱼（登录/发布/回复）
- 闲鱼网页版发布功能受限，建议用 App 手动发布
- 所有 AI 能力依赖 DashScope API，需自行申请
- 请遵守闲鱼平台规则，本工具仅供学习交流

## 📄 License

MIT License

## 🙏 致谢

- [guizang-social-card-skill](https://github.com/op7418/guizang-social-card-skill) - 社交卡片设计系统
- [FishClaw_MCP](https://github.com/TnoobT/FishClaw_MCP) - 闲鱼 MCP 工具
- [ai-goofish](https://github.com/avehub/ai-goofish) - 闲鱼智能监控
