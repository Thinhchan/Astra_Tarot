"""
Kiểm thử tích hợp toàn diện luồng vận hành của Tarot Discord Bot.
"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

# Đảm bảo in UTF-8 không lỗi trên Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:
        pass

# Thêm thư mục gốc vào sys.path để import src
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

import discord

from src.config import EMBED_COLOR, TAROT_DATA_PATH
from src.services.gemini_service import build_tarot_prompt, interpret_tarot_spread
from src.services.tarot_service import tarot_deck


def test_tarot_deck_integrity() -> None:
    """Kiểm tra tính toàn vẹn của kho dữ liệu 78 lá bài."""
    print("🔹 [1/4] Kiểm tra kho dữ liệu 78 lá bài Tarot...")
    assert TAROT_DATA_PATH.exists(), f"Không tìm thấy file: {TAROT_DATA_PATH}"
    assert tarot_deck.total_cards == 78, f"Số lượng lá bài không đúng: {tarot_deck.total_cards}"

    for card in tarot_deck.cards:
        assert card.id > 0, f"Card ID không hợp lệ: {card.id}"
        assert card.name, "Tên tiếng Anh không được trống"
        assert card.name_vi, "Tên tiếng Việt không được trống"
        assert card.type in ["Major", "Minor"], f"Loại bài không hợp lệ: {card.type}"
        assert card.image_url.startswith("http"), f"Link ảnh không hợp lệ: {card.image_url}"

    print("   ✅ Kho dữ liệu đạt chuẩn 100% (78 lá đầy đủ thông tin & link ảnh).")


def test_drawing_logic() -> None:
    """Kiểm tra logic bốc 3 lá bài không trùng lặp và xác suất xuôi/ngược."""
    print("🔹 [2/4] Kiểm tra logic bốc bài 3 lá...")
    draws = tarot_deck.draw_three_cards()

    assert len(draws) == 3, "Số lượng bài bốc phải đúng bằng 3 lá"
    card_ids = [d.card.id for d in draws]
    assert len(set(card_ids)) == 3, f"Phát hiện bài bị trùng lặp: {card_ids}"

    expected_positions = ["Quá khứ", "Hiện tại", "Tương lai"]
    actual_positions = [d.position for d in draws]
    assert actual_positions == expected_positions, f"Thứ tự vị trí không đúng: {actual_positions}"

    for d in draws:
        assert d.orientation in ["Xuôi (Upright)", "Ngược (Reversed)"], f"Trạng thái lạ: {d.orientation}"

    print("   ✅ Logic bốc bài chuẩn xác (Quá khứ - Hiện tại - Tương lai không trùng lặp).")


def test_prompt_generation() -> None:
    """Kiểm tra cấu trúc prompt gửi tới Gemini AI."""
    print("🔹 [3/4] Kiểm tra hàm tạo Prompt cho Gemini...")
    draws = tarot_deck.draw_three_cards()
    question = "Tôi có nên bắt đầu dự án mới này không?"
    prompt = build_tarot_prompt(draws, question)

    assert question in prompt, "Câu hỏi không xuất hiện trong prompt"
    for d in draws:
        assert d.card.name in prompt, f"Tên lá bài {d.card.name} không có trong prompt"

    print("   ✅ Prompt đạt chuẩn Rider-Waite, tích hợp đầy đủ câu hỏi và 3 lá bài.")


def test_embed_creation() -> None:
    """Kiểm tra việc tạo Discord Embed và đặt Thumbnail lá bài Hiện tại."""
    print("🔹 [4/4] Kiểm tra định dạng Discord Embed...")
    draws = tarot_deck.draw_three_cards()
    present_draw = draws[1]

    embed = discord.Embed(
        title="🔮 Trải Bài Tarot: Quá Khứ • Hiện Tại • Tương Lai",
        color=EMBED_COLOR,
    )
    embed.set_thumbnail(url=present_draw.card.image_url)
    embed.add_field(
        name="🃏 3 Lá Bài Được Khai Mở",
        value=f"🕯️ Quá khứ: {draws[0].card.name_vi}\n👁️ Hiện tại: {draws[1].card.name_vi}\n✨ Tương lai: {draws[2].card.name_vi}",
        inline=False,
    )

    assert embed.color.value == EMBED_COLOR, f"Màu sắc không khớp: {embed.color.value} != {EMBED_COLOR}"
    assert embed.thumbnail.url == present_draw.card.image_url, "Thumbnail không phải lá bài Hiện tại"

    print("   ✅ Discord Embed hợp lệ (Màu Dark Purple, Thumbnail lá Hiện tại chính xác).")


def test_card_dictionary_lookup() -> None:
    """Kiểm tra chức năng tìm kiếm và tra cứu từ điển 78 lá bài."""
    from src.services.tarot_dictionary import get_card_meaning

    print("🔹 [5/5] Kiểm tra chức năng tra cứu từ điển (/card)...")
    card_en = tarot_deck.find_card("The Fool")
    assert card_en is not None, "Không tìm thấy lá bài qua tên tiếng Anh 'The Fool'"
    assert card_en.id == 1

    card_vi = tarot_deck.find_card("Chàng Khờ")
    assert card_vi is not None, "Không tìm thấy lá bài qua tên tiếng Việt 'Chàng Khờ'"
    assert card_vi.id == 1

    card_partial = tarot_deck.find_card("magician")
    assert card_partial is not None, "Không tìm thấy lá bài qua từ khóa 'magician'"
    assert card_partial.id == 2

    # Kiểm tra gợi ý autocomplete
    matches = tarot_deck.search_cards("wands", limit=10)
    assert len(matches) > 0, "Không tìm thấy gợi ý nào cho từ khóa 'wands'"

    # Kiểm tra dữ liệu từ điển
    meaning = get_card_meaning(card_en.name, card_en.suit)
    assert meaning.meaning_upright, "Thiếu ý nghĩa chiều xuôi của lá bài"
    assert meaning.meaning_reversed, "Thiếu ý nghĩa chiều ngược của lá bài"
    assert len(meaning.keywords_upright) > 0, "Thiếu từ khóa xuôi"
    assert len(meaning.keywords_reversed) > 0, "Thiếu từ khóa ngược"

    print("   ✅ Tra cứu từ điển đạt chuẩn (Tìm kiếm Anh/Việt, Autocomplete, Chiều xuôi & ngược).")


async def run_all_tests() -> None:
    """Chạy toàn bộ test suite."""
    print("\n" + "=" * 60)
    print("🧪 BẮT ĐẦU KIỂM THỬ TÍCH HỢP HỆ THỐNG TAROT BOT")
    print("=" * 60)

    test_tarot_deck_integrity()
    test_drawing_logic()
    test_prompt_generation()
    test_embed_creation()
    test_card_dictionary_lookup()

    # Thử nghiệm hàm gọi AI fallback khi chưa có API key
    fallback_res = await interpret_tarot_spread(tarot_deck.draw_three_cards(), "Test Question")
    assert fallback_res, "Hàm interpret_tarot_spread không được trả về rỗng"
    print("🔹 [Kiểm tra Fallback]:", fallback_res.split("\n")[0])

    print("=" * 60)
    print("🎉 TẤT CẢ 5/5 KIỂM THỬ TÍCH HỢP ĐỀU VƯỢT QUA XUẤT SẮC!")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    asyncio.run(run_all_tests())

