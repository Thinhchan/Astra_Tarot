"""
Script tải và sinh dữ liệu 78 lá bài Tarot chuẩn Rider-Waite-Smith (1909).
Dữ liệu chỉ bao gồm: id, tên lá bài (tiếng Anh & Việt), loại (Major/Minor), suit và link ảnh trực tiếp.
Không chứa nội dung giải nghĩa sẵn để Gemini AI tự do luận giải dựa trên bối cảnh.
"""

from __future__ import annotations

import json
import logging
import sys
import urllib.request
from pathlib import Path
from typing import Any, Dict, List

# Đảm bảo in UTF-8 không bị lỗi trên Windows PowerShell / cmd
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:
        pass

# Cấu hình logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("GenerateTarotData")

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_FILE = DATA_DIR / "tarot_data.json"

SOURCE_URL = "https://raw.githubusercontent.com/metabismuth/tarot-json/master/tarot-images.json"
IMAGE_BASE_URL = "https://raw.githubusercontent.com/metabismuth/tarot-json/master/cards"

# Bản đồ dịch tên tiếng Việt chuẩn Tarot Rider-Waite
VIETNAMESE_NAMES: Dict[str, str] = {
    # 22 Major Arcana
    "The Fool": "Chàng Khờ (The Fool)",
    "The Magician": "Pháp Sư (The Magician)",
    "The High Priestess": "Nữ Giáo Hoàng (The High Priestess)",
    "The Empress": "Nữ Hoàng (The Empress)",
    "The Emperor": "Hoàng Đế (The Emperor)",
    "The Hierophant": "Giáo Hoàng (The Hierophant)",
    "The Lovers": "Đôi Tình Nhân (The Lovers)",
    "The Chariot": "Cỗ Xe (The Chariot)",
    "Strength": "Sức Mạnh (Strength)",
    "The Hermit": "Ẩn Sĩ (The Hermit)",
    "Wheel of Fortune": "Bánh Xe Số Phận (Wheel of Fortune)",
    "Justice": "Công Lý (Justice)",
    "The Hanged Man": "Người Treo Ngược (The Hanged Man)",
    "Death": "Cái Chết (Death)",
    "Temperance": "Tiết Độ (Temperance)",
    "The Devil": "Ác Quỷ (The Devil)",
    "The Tower": "Tòa Tháp (The Tower)",
    "The Star": "Ngôi Sao (The Star)",
    "The Moon": "Mặt Trăng (The Moon)",
    "The Sun": "Mặt Trời (The Sun)",
    "Judgement": "Phán Xét (Judgement)",
    "The World": "Thế Giới (The World)",
}

SUIT_TRANSLATIONS: Dict[str, str] = {
    "Wands": "Gậy",
    "Cups": "Ly",
    "Swords": "Kiếm",
    "Pentacles": "Tiền",
}

RANK_TRANSLATIONS: Dict[str, str] = {
    "Ace": "Át",
    "Two": "2",
    "Three": "3",
    "Four": "4",
    "Five": "5",
    "Six": "6",
    "Seven": "7",
    "Eight": "8",
    "Nine": "9",
    "Ten": "10",
    "Page": "Tiểu Đồng",
    "Knight": "Hiệp Sĩ",
    "Queen": "Hoàng Hậu",
    "King": "Vua",
}


def get_vietnamese_name(name: str, suit: str | None) -> str:
    """Trả về tên tiếng Việt tương ứng cho lá bài."""
    if name in VIETNAMESE_NAMES:
        return VIETNAMESE_NAMES[name]
    
    if suit and " of " in name:
        parts = name.split(" of ")
        rank_en = parts[0]
        suit_en = parts[1]
        rank_vi = RANK_TRANSLATIONS.get(rank_en, rank_en)
        suit_vi = SUIT_TRANSLATIONS.get(suit_en, suit_en)
        return f"{rank_vi} {suit_vi} ({name})"
    
    return name


def generate_tarot_dataset() -> List[Dict[str, Any]]:
    """Tải và chuyển đổi dữ liệu 78 lá bài sang cấu trúc chuẩn."""
    logger.info(f"Đang tải dataset gốc từ: {SOURCE_URL}")
    req = urllib.request.Request(SOURCE_URL, headers={"User-Agent": "Mozilla/5.0"})
    
    with urllib.request.urlopen(req, timeout=15) as response:
        raw_data = json.loads(response.read().decode("utf-8"))
        
    cards_source = raw_data.get("cards", [])
    if len(cards_source) != 78:
        raise ValueError(f"Dữ liệu bài không đủ 78 lá (chỉ có {len(cards_source)} lá)!")
    
    processed_cards: List[Dict[str, Any]] = []
    
    for idx, card in enumerate(cards_source):
        name = card.get("name", "").strip()
        arcana = "Major" if "Major" in card.get("arcana", "") else "Minor"
        suit = card.get("suit")
        img_filename = card.get("img", "")
        
        # Link ảnh chuẩn phân giải cao từ GitHub raw content
        image_url = f"{IMAGE_BASE_URL}/{img_filename}"
        name_vi = get_vietnamese_name(name, suit)
        
        card_entry: Dict[str, Any] = {
            "id": idx + 1,
            "name": name,
            "name_vi": name_vi,
            "type": arcana,
            "suit": suit,
            "image_url": image_url,
        }
        processed_cards.append(card_entry)
        
    return processed_cards


def main() -> None:
    """Chạy quá trình xuất file dữ liệu."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    cards = generate_tarot_dataset()
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(cards, f, ensure_ascii=False, indent=2)
        
    logger.info(f"Đã xuất thành công {len(cards)} lá bài vào: {OUTPUT_FILE}")
    print(f"✅ Hoàn tất! File dữ liệu: {OUTPUT_FILE} ({len(cards)} lá bài)")


if __name__ == "__main__":
    main()
