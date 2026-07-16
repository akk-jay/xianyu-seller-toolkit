# FishClaw MCP

<p align="center">
  <img src="assets/logo.png" alt="FishClaw MCP Logo" width="150" height="150">
</p>

<p align="center">
  通用 MCP 服务器，将闲鱼自动化工具封装为 MCP 协议。<br>
  纯 Python 实现，不依赖任何 Agent 框架，可供 Claude Desktop、Cursor 等 MCP 客户端直接调用。<br>
  用自然语言完成商品发布、在售管理、市场调研，无需编写任何代码。
</p>

---

有兴趣可以看一下Agno智能体调用FishClaw工具[链接](https://github.com/TnoobT/FishClaw)

---


## 免责声明

> **警告：本项目仅供学习交流使用，请勿用于任何商业或非法用途，否则后果自负。**

<details>
<summary>点击展开完整免责声明</summary>

本项目仅供学习交流使用，请勿用于任何商业或非法用途。任何违反法律法规、侵犯他人合法权益的行为，均与本项目及其开发者无关，后果由用户自行承担。

下载、保存或使用本项目源代码，即表示您已阅读并同意本声明的全部内容。

</details>

---

## 工具列表

| 工具 | 说明 | 注意 |
|------|------|------|
| `login` | 检查登录状态；未登录则弹出浏览器等待扫码 | |
| `search_market` | 关键词搜索闲鱼商品，采集标题、价格、链接 | |
| `draft_item` | 填写商品草稿（图片/描述/分类/价格）并截图 | |
| `publish_item` | 点击发布按钮完成商品发布 | ⚠️ 不可撤销 |
| `get_selling_items` | 获取所有在售商品列表 | |
| `manage_item` | 对指定商品执行下架或永久删除 | ⚠️ 不可撤销 |
| `get_page_content` | 读取当前浏览器页面可见文字 | |
| `simulate_farming` | 模拟真人随机浏览养号 | 需 `ENABLE_FARMING=true` |
| `generate_image` | 调用 DashScope 生成商品封面图 | |
| `generate_image_prompt` | 根据技术主题生成科技感英文生图提示词 | |
| `generate_product_description` | 根据技术主题生成闲鱼商品描述文案 | |

---

## 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/your-username/fishclaw-mcp.git
cd fishclaw-mcp
```

### 2. 安装依赖

```bash
# 推荐使用 uv
uv sync

# 或使用 pip
pip install -e .
```

### 3. 安装 Playwright 浏览器

```bash
playwright install chromium
```

### 4. 配置环境变量

```bash
cp .env.example .env
```

编辑 `.env`，至少填写 `AGENT_LLM_API_KEY`：

```env
# 必填：用于 LLM 推理和文案生成
AGENT_LLM_API_KEY=your-dashscope-api-key

# 可选：用于生成商品封面图（不填则使用内置默认图片）
IMAGE_API_KEY=your-dashscope-api-key
```

### 5. 验证服务器可以启动

```bash
python server.py
```

看到 `Starting MCP server` 字样即表示启动成功，`Ctrl+C` 退出。

---

### 6. 上架示例
<p align="center">
  <img src="assets/example.png" alt="FishClaw MCP Logo" width="800" height="400">
</p>


## 接入 MCP 客户端

### Claude Desktop

找到配置文件（macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`，Windows: `%APPDATA%\Claude\claude_desktop_config.json`），添加以下内容：

**推荐方式：python 直接运行**

```json
{
  "mcpServers": {
    "fishclaw": {
      "command": "python",
      "args": ["D:/acode/py/study/FishClaw_MCP/server.py"],
      "env": {
        "AGENT_LLM_API_KEY": "your-dashscope-api-key"
      }
    }
  }
}
```

**或使用 uv**

```json
{
  "mcpServers": {
    "fishclaw": {
      "command": "uv",
      "args": ["--directory", "/your/path/to/fishclaw-mcp", "run", "server.py"]
    }
  }
}
```

> 将路径替换为本项目的实际绝对路径。环境变量也可以在 `.env` 文件中配置。

### Cursor

在 `~/.cursor/mcp.json`（或项目级 `.cursor/mcp.json`）中添加同上的配置。

---

## 使用示例

接入后，在对话中直接用自然语言操作即可：

```
帮我发布一个 Python 爬虫技术服务，价格 99 元
→ 自动生成封面图 → 生成文案 → 填写表单 → 截图确认 → 发布

查看我现在在售的商品
→ 跳转个人中心，列出所有在售商品

把第二个商品下架
→ 进入商品详情，点击下架并确认

搜索 Python 教程，看看竞品定价
→ 采集前 20 条结果的标题和价格
```

---

## 项目结构

```
fishclaw-mcp/
├── server.py                   # MCP 服务器入口（使用 FastMCP）
├── pyproject.toml              # 项目依赖
├── .env.example                # 环境变量模板
├── assets/
│   └── default_agent.png       # 生图 API 不可用时的兜底图片
└── tools/
    ├── xianyu_tools.py         # 闲鱼 Playwright 自动化（纯 Python 类）
    ├── generate_image_tools.py # DashScope 图像生成（纯 Python 类）
    ├── prompt_tools.py         # LLM 提示词与文案生成（纯 Python 类）
    └── xconfig.py              # 日志配置
```

---

## 环境变量说明

| 变量 | 必填 | 默认值 | 说明 |
|------|------|--------|------|
| `AGENT_LLM_API_KEY` | 是 | — | 阿里云 DashScope API Key |
| `AGENT_LLM_MODEL` | 否 | `qwen-max` | 推理模型名称 |
| `AGENT_LLM_BASE_URL` | 否 | DashScope 兼容地址 | LLM 接口地址 |
| `AGENT_LLM_TEMPERATURE` | 否 | `0.5` | 推理温度 |
| `IMAGE_API_KEY` | 否 | — | 图像生成 API Key（不填用默认图片） |
| `PLAYWRIGHT_HEADLESS` | 否 | `false` | 是否无头模式（建议保持 false 降低风控） |
| `PROXY` | 否 | — | 代理地址，如 `http://127.0.0.1:7890` |
| `COOKIES_PATH` | 否 | `.cache/cookies/xianyu_cookies.json` | Cookie 持久化路径 |
| `XIANYU_HOME_URL` | 否 | `https://www.goofish.com` | 闲鱼首页地址 |
| `ENABLE_FARMING` | 否 | `false` | 设为 `true` 时注册 `simulate_farming` 工具 |

---

## 技术栈

| 层次 | 技术 |
|------|------|
| **MCP 协议** | [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) — FastMCP |
| **浏览器自动化** | [Playwright](https://playwright.dev/python/) + playwright-stealth |
| **工具实现** | 纯 Python 类，不依赖任何 Agent 框架 |
| **LLM / 图像生成** | 阿里云 DashScope（`qwen-max` + `z-image-turbo`） |
