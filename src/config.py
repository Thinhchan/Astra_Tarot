"""
Module cấu hình ứng dụng (Configuration Management).
Quản lý các biến môi trường, đường dẫn tệp, và các hằng số giao diện cho Tarot Bot.
"""

from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# Xác định đường dẫn gốc của project
BASE_DIR = Path(__file__).resolve().parent.parent

# Tải cấu hình từ file .env
ENV_FILE = BASE_DIR / ".env"
load_dotenv(dotenv_path=ENV_FILE)

# Cấu hình Logging tập trung
LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s:%(funcName)s:%(lineno)d - %(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
logger = logging.getLogger("TarotBot")

# ==========================================
# THÔNG TIN XÁC THỰC VÀ API KEYS
# ==========================================
DISCORD_TOKEN: str = os.getenv("DISCORD_TOKEN", "").strip()
GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "").strip()

# Model AI Gemini được sử dụng (mặc định gemini-3.8-flash)
GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-3.8-flash").strip()

# Guild ID cho môi trường Test (Tùy chọn: giúp slash command đồng bộ ngay lập tức)
_test_guild = os.getenv("TEST_GUILD_ID", "").strip()
TEST_GUILD_ID: Optional[int] = int(_test_guild) if _test_guild.isdigit() else None

# ==========================================
# ĐƯỜNG DẪN DỮ LIỆU
# ==========================================
DATA_DIR: Path = BASE_DIR / "data"
TAROT_DATA_PATH: Path = DATA_DIR / "tarot_data.json"

# ==========================================
# CẤU HÌNH GIAO DIỆN & UI TONE (DISCORD EMBED)
# ==========================================
# Tông màu Tím Đêm Huyền Bí (Dark Mystic Purple) và Đỏ Rượu khi có lỗi
EMBED_COLOR: int = 0x2A113B
EMBED_ERROR_COLOR: int = 0x6E1A24
DEFAULT_TAROT_BACK_IMAGE: str = "https://upload.wikimedia.org/wikipedia/commons/e/eb/Rider-Waite_Tarot_Deck_Back.jpg"

# Thông điệp delay trong lúc xào bài và gọi AI
WAITING_MESSAGE: str = "✨ *Đang kết nối với dòng chảy vũ trụ và xào bài... Xin hãy tịnh tâm đợi trong giây lát.*"


def validate_config(strict: bool = False) -> bool:
    """
    Kiểm tra tính hợp lệ của các biến môi trường thiết yếu.
    
    Args:
        strict: Nếu True, sẽ raise ValueError khi thiếu biến. Nếu False, chỉ in cảnh báo.
        
    Returns:
        bool: True nếu cấu hình đầy đủ, False nếu còn thiếu.
    """
    missing = []
    if not DISCORD_TOKEN:
        missing.append("DISCORD_TOKEN")
    if not GEMINI_API_KEY:
        missing.append("GEMINI_API_KEY")

    if missing:
        msg = f"Cảnh báo: Thiếu các biến môi trường thiết yếu: {', '.join(missing)}. Vui lòng cập nhật file .env!"
        if strict:
            raise ValueError(msg)
        logger.warning(msg)
        return False

    logger.info("Cấu hình môi trường đã được tải thành công.")
    return True
