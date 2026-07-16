"""
FishClaw MCP Server
===================
通用 MCP 服务器，将闲鱼自动化工具暴露为 MCP 协议。
不依赖任何 Agent 框架，纯 Python 实现。

工具列表
--------
  闲鱼工具：
    login                     检查登录状态 / 触发扫码登录
    search_market             关键词搜索闲鱼商品
    draft_item                填写商品草稿并截图
    publish_item              发布已填写的草稿（不可撤销）
    get_selling_items         获取所有在售商品列表
    manage_item               下架或永久删除指定商品（不可撤销）
    get_page_content          读取当前浏览器页面可见文字
    simulate_farming          模拟养号（需 ENABLE_FARMING=true）
  图像生成：
    generate_image            调用 DashScope 生成图片
  文案生成：
    generate_image_prompt     生成科技感英文生图提示词
    generate_product_description  生成闲鱼商品描述文案

Claude Desktop 配置示例（claude_desktop_config.json）
----------------------------------------------------
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

环境变量（复制 .env.example 为 .env 并填写）
--------------------------------------------
  必填：AGENT_LLM_API_KEY
  可选：IMAGE_API_KEY, AGENT_LLM_MODEL, PLAYWRIGHT_HEADLESS, PROXY,
        COOKIES_PATH, ENABLE_FARMING, XIANYU_HOME_URL
"""
from __future__ import annotations

import asyncio
import concurrent.futures
import functools
import os
from pathlib import Path
from typing import Literal

from dotenv import load_dotenv

# ── mcp/ 目录即为独立项目根 ────────────────────────────────────────
_MCP_ROOT = Path(__file__).resolve().parent
load_dotenv(_MCP_ROOT / ".env")

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

from tools.xianyu_tools import FishClawTools
from tools.generate_image_tools import GenerateImageTools
from tools.prompt_tools import PromptTools

# ── MCP 服务器实例 ──────────────────────────────────────────────────
mcp = FastMCP(
    "FishClaw",
    instructions=(
        "闲鱼（咸鱼）自动化助手，支持发布商品、管理在售列表、市场调研、生成封面图和商品文案。\n"
        "发布流程：generate_image_prompt → generate_image → "
        "generate_product_description → draft_item → publish_item\n"
        "管理流程：get_selling_items → manage_item\n"
        "注意：所有工具均为纯 Python 实现，不依赖任何 Agent 框架。"
    ),
)

# ── 环境变量 ────────────────────────────────────────────────────────
_COOKIES_PATH = os.environ.get(
    "COOKIES_PATH",
    str(_MCP_ROOT / ".cache" / "cookies" / "xianyu_cookies.json"),
)
_HEADLESS = os.environ.get("PLAYWRIGHT_HEADLESS", "false").lower() == "true"
_PROXY = os.environ.get("PROXY") or None
_ENABLE_FARMING = os.environ.get("ENABLE_FARMING", "false").lower() == "true"

# ── 专属单线程 Executor（sync_playwright 必须在无 asyncio 事件循环的线程中运行）
# max_workers=1 确保所有 Playwright 操作在同一线程内串行执行，浏览器状态安全共享。
_playwright_executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)


async def _run_sync(fn, *args, **kwargs):
    """在专属 Playwright 线程中执行同步函数，避免与 asyncio 事件循环冲突。"""
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(
        _playwright_executor,
        functools.partial(fn, *args, **kwargs),
    )


# ── 懒加载单例（在同一 MCP 会话中复用浏览器实例） ────────────────────
_xianyu: FishClawTools | None = None
_image_tools: GenerateImageTools | None = None
_prompt_tools: PromptTools | None = None


def _get_xianyu() -> FishClawTools:
    global _xianyu
    if _xianyu is None:
        _xianyu = FishClawTools(
            cookies_path=_COOKIES_PATH,
            headless=_HEADLESS,
            proxy=_PROXY,
            enable_farming=_ENABLE_FARMING,
        )
    return _xianyu


def _get_image_tools() -> GenerateImageTools:
    global _image_tools
    if _image_tools is None:
        _image_tools = GenerateImageTools()
    return _image_tools


def _get_prompt_tools() -> PromptTools:
    global _prompt_tools
    if _prompt_tools is None:
        _prompt_tools = PromptTools()
    return _prompt_tools


# ════════════════════════════════════════════════════════════════════
# 闲鱼工具
# ════════════════════════════════════════════════════════════════════

@mcp.tool()
async def login(timeout_seconds: int = 180) -> str:
    """检查闲鱼登录状态。已登录则直接返回；未登录则打开浏览器展示二维码，
    等待用户手动扫码，登录成功后自动保存 Cookies。

    Args:
        timeout_seconds: 等待扫码的最大秒数，默认 180。
    """
    return await _run_sync(_get_xianyu().login, timeout_seconds=timeout_seconds)


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
async def search_market(keyword: str, max_results: int = 20) -> str:
    """在闲鱼搜索指定关键词，采集结果列表（标题、价格、链接），用于竞品调研和定价参考。

    Args:
        keyword: 搜索关键词，不能为空。
        max_results: 最多返回结果数量，默认 20。
    """
    return await _run_sync(_get_xianyu().search_market, keyword=keyword, max_results=max_results)


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
async def draft_item(image: str, description: str, price: float = 100.0) -> str:
    """在闲鱼发布页面填写商品草稿（图片、描述、分类、价格），填写完成后自动截图。
    返回文本中包含截图路径，确认无误后调用 publish_item 正式发布。

    Args:
        image: 商品图片，支持本地绝对路径或网络 URL（http/https）。
        description: 商品描述文字。
        price: 商品售价（元），默认 100.0。
    """
    return await _run_sync(_get_xianyu().draft_item, image=image, description=description, price=price)


@mcp.tool(annotations=ToolAnnotations(destructiveHint=True))
async def publish_item() -> str:
    """点击发布按钮完成商品发布。
    ⚠️ 不可撤销操作，请先调用 draft_item 填写草稿并确认截图后再调用。
    """
    return await _run_sync(_get_xianyu().publish_item)


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
async def get_selling_items() -> str:
    """获取当前账号所有在售商品列表（标题、价格、链接）。
    内部自动跳转个人中心并滚动加载全部商品，无需手动导航。
    """
    return await _run_sync(_get_xianyu().get_selling_items)


@mcp.tool(annotations=ToolAnnotations(destructiveHint=True))
async def manage_item(item_url: str, action: Literal["delist", "delete"]) -> str:
    """对指定商品执行下架或删除操作，内部自动跳转商品详情页并处理确认弹窗。
    ⚠️ delete 操作永久删除商品，不可恢复。
    请先调用 get_selling_items 获取商品链接，再传入此工具。

    Args:
        item_url: 商品详情页 URL（从 get_selling_items 结果中获取）。
        action: delist=下架（转为草稿，可重新上架）；delete=永久删除。
    """
    return await _run_sync(_get_xianyu().manage_item, item_url=item_url, action=action)


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
async def get_page_content() -> str:
    """读取当前浏览器页面的可见文字内容（最多 3000 字符），供分析页面状态或提取信息。
    可在导航到某个页面后调用，让 AI 感知当前浏览器状态。
    """
    return await _run_sync(_get_xianyu().get_page_content)


@mcp.tool()
async def restart_browser() -> str:
    """重新初始化 Playwright 浏览器进程，无需重启 MCP 服务器。
    当出现以下情况时调用：
      - 浏览器窗口已被手动关闭
      - 页面长时间无响应或报错
      - 提示"浏览器进程已关闭"等异常
    重启后需重新调用 login 验证登录状态，再继续执行后续操作。
    """
    global _xianyu
    def _do_restart():
        global _xianyu
        if _xianyu is not None:
            try:
                _xianyu._close_browser()
            except Exception:
                pass
            _xianyu = None
        # 预先初始化新实例（触发浏览器启动）
        _get_xianyu()

    await _run_sync(_do_restart)
    return (
        "浏览器已重新初始化成功！\n"
        "请调用 login 重新验证登录状态，然后再继续执行 draft_item / publish_item 等操作。"
    )


if _ENABLE_FARMING:
    @mcp.tool()
    async def simulate_farming(duration_minutes: int = 5) -> str:
        """模拟真人在闲鱼首页随机浏览（滚动、点击进帖、返回），用于账号养号。
        仅模拟正常用户行为，不做任何交易操作。
        需在环境变量中设置 ENABLE_FARMING=true 才会注册此工具。

        Args:
            duration_minutes: 模拟浏览持续时长（分钟），默认 5。
        """
        return await _run_sync(_get_xianyu().simulate_farming, duration_minutes=duration_minutes)


# ════════════════════════════════════════════════════════════════════
# 图像生成工具
# ════════════════════════════════════════════════════════════════════

@mcp.tool()
def generate_image(prompt: str, size: str = "1024*1024") -> str:
    """根据文本提示词调用阿里云 DashScope 生成图像，图像缓存到本地后返回路径。
    未配置 IMAGE_API_KEY 时自动回退到项目内置的默认图片。

    Args:
        prompt: 图像生成的文本描述（支持中英文混合）。
        size: 图像尺寸，格式为"宽*高"，如"1120*1440"，默认"1024*1024"。
    """
    return _get_image_tools().generate_image(prompt=prompt, size=size)


# ════════════════════════════════════════════════════════════════════
# 文案生成工具
# ════════════════════════════════════════════════════════════════════

@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def generate_image_prompt(topic: str) -> str:
    """根据技术主题生成适合图像生成模型的英文提示词（赛博朋克/科技感风格）。
    生成结果可直接传入 generate_image 工具使用。

    Args:
        topic: 技术主题，如"AIGC"、"Python爬虫"、"区块链"等。
    """
    return _get_prompt_tools().generate_image_prompt(topic=topic)


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def generate_product_description(topic: str) -> str:
    """根据技术主题生成闲鱼商品描述文案（自我介绍 + 服务分类 + 技术关键词三段式）。
    生成结果可直接传入 draft_item 的 description 参数。

    Args:
        topic: 技术主题或服务内容，如"AIGC绘画"、"Python爬虫"等。
    """
    return _get_prompt_tools().generate_product_description(topic=topic)


# ════════════════════════════════════════════════════════════════════
# 入口
# ════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import sys

    # 支持命令行参数选择运行模式
    # python server.py              -> stdio 模式（默认，用于 Claude Desktop）
    # python server.py --http       -> HTTP 模式（用于 Agno 等 HTTP 客户端）
    transport = "stdio"
    if "--http" in sys.argv:
        transport = "streamable-http"
        print("FishClaw MCP Server 启动中（HTTP 模式）...")
        print("监听地址: http://localhost:8000/mcp")
        print("按 Ctrl+C 停止服务器\n")

    mcp.run(transport=transport)
