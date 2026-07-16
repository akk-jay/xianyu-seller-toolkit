"""
半自动发布脚本 - 帮你登录闲鱼，打开发布页，你来手动上传图片填表
用法: python publish_semi_auto.py

流程:
1. 自动打开浏览器，扫码登录
2. 打开发布页
3. 提示你在浏览器中手动完成：
   - 上传5张图片 (image-cards/github-collection-101/01-05.png)
   - 粘贴标题和描述
   - 设置价格
4. 你确认后，脚本帮你点"发布"
"""
import sys, os, time
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from dotenv import load_dotenv
load_dotenv('.env')
from tools.xianyu_tools import FishClawTools
from tools.prompt_tools import PromptTools

# === 你的商品信息 ===
TITLE = "GitHub开源神器清单｜101个项目中文整理好了，照着装就行"
DESC = """GitHub开源神器清单 | 101个项目15个分类

AI/开发/媒体/桌面/安全/教育全覆盖 | 人工精选中文导航
每个项目标注：Star热度 + 编程语言 + 中文用途 + 更新日期
拍下秒发Markdown文件，可编辑可搜索

适合：开发者 | 科技控 | GitHub新手 | 技术博主

虚拟资料，售出不退"""
PRICE = 9.9
IMAGES_DIR = r"C:\Users\29542\Desktop\GitHub合集\image-cards\github-collection-101"

def main():
    print("=" * 60)
    print("  FishClaw - 闲鱼半自动发布工具")
    print("=" * 60)
    print()

    # Step 1: Login
    print("[1/4] 正在打开浏览器...")
    print("      如需要，请用闲鱼APP扫描二维码登录")
    print()

    xtools = FishClawTools(headless=False)
    r = xtools.login(timeout_seconds=180)

    if "登录失败" in r or "超时" in r:
        print(f"\n❌ 登录失败: {r}")
        return

    print(f"✅ 登录成功！")
    print()

    # Step 2: Navigate to publish page
    print("[2/4] 正在打开发布页面...")

    page = xtools._get_page()
    page.goto("https://www.goofish.com", wait_until="networkidle", timeout=30000)
    time.sleep(3)

    # Remove login modal if present
    page.evaluate('() => { document.querySelectorAll(".ant-modal-wrap, [class*=login-modal-wrap]").forEach(m => m.remove()); }')
    time.sleep(1)

    # Click publish sidebar link
    try:
        with xtools._context.expect_page(timeout=10000) as info:
            page.locator('a[href$="/publish"]').first.click()
        ppage = info.value
        ppage.wait_for_load_state("networkidle", timeout=30000)
        time.sleep(3)
        print(f"✅ 发布页已打开: {ppage.url}")
    except Exception as e:
        print(f"⚠️ 自动点击失败，尝试直接导航...")
        page.goto("https://www.goofish.com/publish", wait_until="networkidle", timeout=15000)
        time.sleep(5)

    print()
    print("=" * 60)
    print("  [3/4] 请在浏览器中手动完成以下操作：")
    print("=" * 60)
    print()
    print("  📷 上传图片（按顺序）：")
    print(f"     1. {IMAGES_DIR}\\01-cover-github-collection.png")
    print(f"     2. {IMAGES_DIR}\\02-value-why-need.png")
    print(f"     3. {IMAGES_DIR}\\03-categories-overview.png")
    print(f"     4. {IMAGES_DIR}\\04-top-projects.png")
    print(f"     5. {IMAGES_DIR}\\05-cta-purchase.png")
    print()
    print(f"  📝 标题：")
    print(f"     {TITLE}")
    print()
    print(f"  💰 价格：¥{PRICE}")
    print()
    print(f"  📄 描述（复制下面内容）：")
    print(f"     ---")
    for line in DESC.split('\n'):
        print(f"     {line}")
    print(f"     ---")
    print()
    print("  提示：")
    print("  - 如果网页版发布受限，建议用闲鱼APP发布（图片可AirDrop到手机）")
    print("  - 分类选「虚拟商品」或「其他」")
    print()

    # Step 4: Open images folder and wait
    print("[4/4] 正在打开图片文件夹...")
    os.startfile(IMAGES_DIR)
    print()
    print("=" * 60)
    print("  浏览器已打开发布页，图片文件夹也已打开。")
    print("  请在浏览器中：")
    print("  1. 从文件夹拖拽图片到上传区")
    print("  2. 复制上面的标题和描述粘贴进去")
    print("  3. 设置价格 ¥{}".format(PRICE))
    print("  4. 点击发布！")
    print("=" * 60)
    print()
    print("⏳ 浏览器保持打开，完成后可手动关闭...")
    print("   (按 Ctrl+C 退出脚本)")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n👋 脚本已退出，浏览器窗口请手动关闭。")

if __name__ == "__main__":
    main()
