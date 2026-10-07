"""
Helper xử lý và ghép nối hình ảnh các lá bài Tarot (Image Helper).
Hỗ trợ tải ảnh có cache, xoay 180 độ đối với lá bài Ngược (Reversed),
và ghép các lá bài nằm ngang thành một bức tranh trải bài (Spread Image) hoàn chỉnh.
"""

from __future__ import annotations

import io
import logging
import urllib.request
from pathlib import Path
from typing import Dict, List, Optional

from PIL import Image

from src.services.tarot_service import TarotDraw

logger = logging.getLogger("TarotBot.ImageHelper")

# Bộ nhớ đệm ảnh trong RAM để không phải tải lại cùng một lá bài
_IMAGE_CACHE: Dict[str, Image.Image] = {}

# Thư mục cache ảnh trên ổ đĩa
CACHE_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "cache"


def _get_card_image(image_url: str) -> Optional[Image.Image]:
    """Tải và lưu cache hình ảnh một lá bài."""
    if not image_url:
        return None

    if image_url in _IMAGE_CACHE:
        return _IMAGE_CACHE[image_url].copy()

    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    file_name = image_url.split("/")[-1]
    local_path = CACHE_DIR / file_name

    try:
        if local_path.exists():
            img = Image.open(local_path).convert("RGBA")
        else:
            req = urllib.request.Request(image_url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=8) as resp:
                data = resp.read()
            with open(local_path, "wb") as f:
                f.write(data)
            img = Image.open(io.BytesIO(data)).convert("RGBA")

        _IMAGE_CACHE[image_url] = img
        return img.copy()
    except Exception as e:
        logger.warning(f"Không thể tải ảnh từ {image_url}: {e}")
        return None


def create_spread_image(draws: List[TarotDraw], card_height: int = 350, gap: int = 20) -> Optional[io.BytesIO]:
    """
    Ghép các lá bài trong trải bài thành một ảnh ngang duy nhất.
    Lá bài Ngược (Reversed) sẽ được xoay 180 độ chân thực.
    
    Args:
        draws: Danh sách các lượt bốc bài (TarotDraw).
        card_height: Chiều cao chuẩn hóa của từng lá bài (px).
        gap: Khoảng cách giữa các lá bài (px).
        
    Returns:
        io.BytesIO chứa dữ liệu ảnh PNG hoặc None nếu không tải được ảnh.
    """
    card_images: List[Image.Image] = []

    for draw in draws:
        img = _get_card_image(draw.card.image_url)
        if img:
            # Xoay ngược 180 độ nếu lá bài ở trạng thái Ngược (Reversed)
            if draw.is_reversed:
                img = img.rotate(180, expand=True)

            # Resize tỷ lệ chuẩn
            aspect = img.width / img.height
            new_width = int(card_height * aspect)
            img_resized = img.resize((new_width, card_height), Image.Resampling.LANCZOS)
            card_images.append(img_resized)

    if not card_images:
        return None

    total_width = sum(img.width for img in card_images) + gap * (len(card_images) + 1)
    total_height = card_height + gap * 2

    # Tạo canvas nền tối màu tím đen đồng bộ giao diện Tarot
    canvas = Image.new("RGBA", (total_width, total_height), (26, 11, 38, 255))

    current_x = gap
    for img in card_images:
        canvas.paste(img, (current_x, gap), img)
        current_x += img.width + gap

    output = io.BytesIO()
    canvas.save(output, format="PNG", optimize=True)
    output.seek(0)
    return output
