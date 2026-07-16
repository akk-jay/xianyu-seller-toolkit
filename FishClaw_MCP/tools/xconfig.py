import logging
from pathlib import Path
from datetime import datetime
# ── 配置日志 ──────────────────────────────────────────────────
_LOG_DIR = Path(__file__).resolve().parent.parent / "logs"
_LOG_DIR.mkdir(exist_ok=True)

_log_file = _LOG_DIR / f"xianyu_tools_{datetime.now().strftime('%Y%m%d')}.log"
_file_handler = logging.FileHandler(_log_file, encoding='utf-8')
_file_handler.setLevel(logging.DEBUG)
_file_handler.setFormatter(
    logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
)

_logger = logging.getLogger("prompt_tools")
_logger.setLevel(logging.DEBUG)
_logger.addHandler(_file_handler)

def _log(message: str, level: str = "info"):
    """统一的日志记录函数"""
    if level == "info":
        _logger.info(message)
    elif level == "warning":
        _logger.warning(message)
    elif level == "error":
        _logger.error(message)
    elif level == "debug":
        _logger.debug(message)