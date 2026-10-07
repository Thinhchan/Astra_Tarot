"""
Dịch vụ quản lý bộ bài Tarot (Tarot Deck Service).
Chịu trách nhiệm nạp dữ liệu 78 lá bài vào bộ nhớ RAM khi bot khởi động,
thực hiện xào bài và bốc ngẫu nhiên 3 lá (Quá khứ, Hiện tại, Tương lai) kèm trạng thái Xuôi/Ngược.
"""

from __future__ import annotations

import json
import logging
import random
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

from src.config import TAROT_DATA_PATH

logger = logging.getLogger("TarotBot.TarotService")


@dataclass(frozen=True)
class TarotCard:
    """Đại diện cho một lá bài Tarot."""
    id: int
    name: str
    name_vi: str
    type: str  # "Major" hoặc "Minor"
    suit: Optional[str]
    image_url: str


@dataclass(frozen=True)
class TarotDraw:
    """Đại diện cho một lượt bốc bài trong trải bài."""
    card: TarotCard
    position: str  # "Quá khứ", "Hiện tại", hoặc "Tương lai"
    orientation: str  # "Xuôi (Upright)" hoặc "Ngược (Reversed)"
    is_reversed: bool

    @property
    def display_name(self) -> str:
        """Tên hiển thị bao gồm tên tiếng Việt, tên tiếng Anh và trạng thái."""
        return f"{self.card.name_vi} • {self.orientation}"


class TarotDeck:
    """Lớp quản lý bộ bài Tarot trong RAM."""

    POSITIONS: List[str] = ["Quá khứ", "Hiện tại", "Tương lai"]

    def __init__(self, data_path: Path = TAROT_DATA_PATH) -> None:
        self.data_path = data_path
        self._cards: List[TarotCard] = []
        self.load_cards()

    @property
    def cards(self) -> List[TarotCard]:
        return self._cards

    @property
    def total_cards(self) -> int:
        return len(self._cards)

    def load_cards(self) -> None:
        """Nạp dữ liệu từ tệp JSON vào bộ nhớ."""
        if not self.data_path.exists():
            error_msg = f"Tệp dữ liệu Tarot không tồn tại tại: {self.data_path}"
            logger.error(error_msg)
            raise FileNotFoundError(error_msg)

        try:
            with open(self.data_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            self._cards = [
                TarotCard(
                    id=item["id"],
                    name=item["name"],
                    name_vi=item.get("name_vi", item["name"]),
                    type=item.get("type", "Unknown"),
                    suit=item.get("suit"),
                    image_url=item.get("image_url", ""),
                )
                for item in data
            ]
            logger.info(f"Đã nạp thành công {len(self._cards)} lá bài Tarot vào bộ nhớ RAM.")
        except Exception as e:
            logger.exception(f"Lỗi khi nạp dữ liệu bài Tarot: {e}")
            raise

    def draw_cards(self, count: int = 3, custom_positions: Optional[List[str]] = None) -> List[TarotDraw]:
        """
        Bốc ngẫu nhiên số lượng lá bài theo yêu cầu (1, 3, 5 lá...) không trùng lặp.
        Hoàn toàn được tính toán ngẫu nhiên tại backend (không để LLM tự chọn bài).
        """
        if count > len(self._cards):
            raise ValueError(f"Không thể bốc {count} lá khi bộ bài chỉ có {len(self._cards)} lá.")

        sampled_cards = random.sample(self._cards, count)
        draws: List[TarotDraw] = []

        for i, card in enumerate(sampled_cards):
            if custom_positions and i < len(custom_positions):
                position = custom_positions[i]
            elif count == 3 and i < len(self.POSITIONS):
                position = self.POSITIONS[i]
            else:
                position = f"Lá #{i + 1}"

            is_reversed = random.choice([False, True])
            orientation = "Ngược (Reversed)" if is_reversed else "Xuôi (Upright)"
            draws.append(
                TarotDraw(
                    card=card,
                    position=position,
                    orientation=orientation,
                    is_reversed=is_reversed,
                )
            )

        return draws

    def draw_three_cards(self) -> List[TarotDraw]:
        """Bốc 3 lá bài chuẩn Quá khứ - Hiện tại - Tương lai."""
        return self.draw_cards(count=3, custom_positions=self.POSITIONS)

    def find_card(self, query: str) -> Optional[TarotCard]:
        """Tìm chính xác hoặc gần đúng lá bài theo tên tiếng Anh hoặc tiếng Việt."""
        q = query.strip().lower()
        if not q:
            return None

        # 1. Khớp chính xác
        for c in self._cards:
            if c.name.lower() == q or c.name_vi.lower() == q:
                return c

        # 2. Khớp chuỗi con
        for c in self._cards:
            if q in c.name.lower() or q in c.name_vi.lower():
                return c

        return None

    def search_cards(self, query: str, limit: int = 25) -> List[TarotCard]:
        """Tìm kiếm danh sách lá bài phù hợp phục vụ Autocomplete."""
        q = query.strip().lower()
        if not q:
            return self._cards[:limit]

        matches = []
        for c in self._cards:
            if q in c.name.lower() or q in c.name_vi.lower():
                matches.append(c)
                if len(matches) >= limit:
                    break
        return matches


# Khởi tạo một phiên bản singleton dùng chung trong toàn bộ ứng dụng
tarot_deck = TarotDeck()
