"""
Mô-đun quản lý các thành phần giao diện tương tác (Interactive Discord UI Components).
Chứa các Buttons (Lật Bài, Xin Thêm Lời Khuyên) và Dropdown Select Menus cho trải bài.
"""

from __future__ import annotations

import logging
from typing import List, Optional

import discord

from src.services.tarot_service import TarotDraw
from src.services.gemini_service import interpret_tarot_spread

logger = logging.getLogger("TarotBot.UIViews")


class TarotActionView(discord.ui.View):
    """
    View chứa các nút tương tác sau khi trải bài:
    - [🃏 Lật Bài / Xem Biểu Tượng]: Xem chi tiết hình ảnh & ý nghĩa từng lá bài.
    - [🔮 Xin Thêm Lời Khuyên]: Gọi LLM đưa ra lời khuyên hành động bổ sung.
    """

    def __init__(
        self,
        draws: List[TarotDraw],
        question: Optional[str] = None,
        author_id: int = 0,
        timeout: float = 300.0,
    ) -> None:
        super().__init__(timeout=timeout)
        self.draws = draws
        self.question = question
        self.author_id = author_id

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        """Chỉ cho phép người bốc bài tương tác với các nút này."""
        if self.author_id and interaction.user.id != self.author_id:
            await interaction.response.send_message(
                "⚠️ Quẻ bài này dành riêng cho người bốc. Bạn hãy dùng `/tarot` để mở quẻ bài của chính mình nhé!",
                ephemeral=True,
            )
            return False
        return True

    @discord.ui.button(label="Chi Tiết Thẻ Bài", emoji="🃏", style=discord.ButtonStyle.secondary)
    async def flip_cards_button(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        """Xem nhanh biểu tượng chi tiết của từng lá bài."""
        embed = discord.Embed(
            title="🔍 Chi Tiết Biểu Tượng Các Lá Bài Đã Khai Mở",
            color=discord.Color.dark_purple(),
        )

        for d in self.draws:
            state_desc = "Năng lượng ngược: trở ngại nội tâm, chậm trễ hoặc bài học tiềm ẩn." if d.is_reversed else "Năng lượng xuôi: hiển lộ trực tiếp, thuận dòng phát triển."
            embed.add_field(
                name=f"{d.position}: {d.card.name_vi}",
                value=f"• **Trạng thái:** {d.orientation}\n• **Thể loại:** {d.card.type} Arcana\n• **Gợi ý:** {state_desc}",
                inline=False,
            )

        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="Xin Thêm Lời Khuyên", emoji="🔮", style=discord.ButtonStyle.primary)
    async def extra_advice_button(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        """Kêu gọi thêm một lời khuyên hành động từ trí tuệ Tarot & LLM."""
        button.disabled = True
        button.label = "Đã Nhận Thêm Lời Khuyên"
        await interaction.response.edit_message(view=self)

        # Gửi thông điệp chờ
        followup_msg = await interaction.followup.send(
            "✨ *Đang chiêm nghiệm sâu hơn từ vũ trụ để gửi gắm thêm lời khuyên cho bạn...*",
            ephemeral=True,
        )

        extra_q = f"Dựa trên 3 lá bài vừa bốc và câu hỏi '{self.question or 'cuộc sống'}', hãy cho Querent một hành động cụ thể nhất có thể làm ngay hôm nay để chuyển hóa năng lượng tích cực."
        extra_advice = await interpret_tarot_spread(self.draws, question=extra_q)

        embed = discord.Embed(
            title="🌟 Lời Khuyên Hành Động Bổ Sung Từ Vũ Trụ",
            description=extra_advice,
            color=discord.Color.gold(),
        )
        embed.set_footer(text="Hành động xuất phát từ tâm thức sẽ kiến tạo nên tương lai.")
        await interaction.followup.send(embed=embed, ephemeral=True)


class SpreadSelectMenu(discord.ui.Select):
    """Dropdown Menu lựa chọn thể loại trải bài."""

    def __init__(self) -> None:
        options = [
            discord.SelectOption(
                label="Quá Khứ • Hiện Tại • Tương Lai",
                value="time_3",
                description="Trải bài 3 lá kinh điển nhìn nhận dòng thời gian",
                emoji="⏳",
            ),
            discord.SelectOption(
                label="Tình Yêu & Mối Quan Hệ",
                value="love_3",
                description="3 lá: Bạn - Đối phương - Tương lai kết nối",
                emoji="💖",
            ),
            discord.SelectOption(
                label="Sự Nghiệp & Tài Lộc",
                value="career_3",
                description="3 lá: Thực trạng - Cơ hội/Thách thức - Lời khuyên",
                emoji="💼",
            ),
            discord.SelectOption(
                label="Thấu Hiểu Bản Thân (Thân - Tâm - Trí)",
                value="mind_3",
                description="3 lá: Thể chất - Cảm xúc tâm lý - Khai sáng tinh thần",
                emoji="🧘",
            ),
        ]
        super().__init__(
            placeholder="🔮 Chọn chủ đề trải bài bạn mong muốn...",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: discord.Interaction) -> None:
        """Xử lý khi người dùng chọn một kiểu trải bài."""
        from src.services.tarot_service import tarot_deck
        from src.helpers.image_helper import create_spread_image

        spread_type = self.values[0]

        spread_configs = {
            "time_3": ("Quá Khứ • Hiện Tại • Tương Lai", ["Quá khứ", "Hiện tại", "Tương lai"]),
            "love_3": ("Tình Yêu & Mối Quan Hệ", ["Bản thân bạn", "Đối phương / Năng lượng chung", "Xu hướng kết nối"]),
            "career_3": ("Sự Nghiệp & Định Hướng", ["Thực trạng công việc", "Cơ hội & Thách thức", "Lời khuyên hành động"]),
            "mind_3": ("Thấu Hiểu Thân - Tâm - Trí", ["Thân (Hành động)", "Tâm (Cảm xúc)", "Trí (Nhận thức tinh thần)"]),
        }

        title, positions = spread_configs.get(spread_type, ("Trải Bài 3 Lá", ["Quá khứ", "Hiện tại", "Tương lai"]))

        # Bốc bài theo các vị trí đã chọn
        draws = tarot_deck.draw_cards(count=3, custom_positions=positions)

        await interaction.response.defer()

        # Tạo ảnh composite nằm ngang
        img_buf = create_spread_image(draws)
        file = discord.File(img_buf, filename="spread.png") if img_buf else None

        # Gọi LLM luận giải
        reading = await interpret_tarot_spread(draws, question=f"Chủ đề trải bài: {title}")

        embed = discord.Embed(
            title=f"🔮 Trải Bài: {title}",
            color=discord.Color.from_rgb(42, 17, 59),
            timestamp=discord.utils.utcnow(),
        )
        embed.set_author(name=f"Quẻ bài của {interaction.user.display_name}", icon_url=interaction.user.display_avatar.url)

        cards_summary = "\n".join([
            f"• **{d.position}:** {d.card.name_vi} — *{d.orientation}*" for d in draws
        ])
        embed.add_field(name="🃏 Các Lá Bài Khai Mở", value=cards_summary, inline=False)

        if len(reading) > 4000:
            reading = reading[:3990] + "..."
        embed.description = f"### 📜 Luận Giải Chuyên Sâu\n\n{reading}"

        if file:
            embed.set_image(url="attachment://spread.png")
        elif draws[1].card.image_url:
            embed.set_thumbnail(url=draws[1].card.image_url)

        embed.set_footer(text=f"Trải bài {title} • Rider-Waite & Gemini AI")

        view = TarotActionView(draws=draws, question=title, author_id=interaction.user.id)
        if file:
            await interaction.followup.send(embed=embed, file=file, view=view)
        else:
            await interaction.followup.send(embed=embed, view=view)


class SpreadMenuView(discord.ui.View):
    """View chứa Dropdown Menu trải bài."""

    def __init__(self, author_id: int = 0) -> None:
        super().__init__(timeout=120.0)
        self.author_id = author_id
        self.add_item(SpreadSelectMenu())

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if self.author_id and interaction.user.id != self.author_id:
            await interaction.response.send_message("⚠️ Bạn hãy tự dùng `/spread` để chọn kiểu trải bài của mình nhé!", ephemeral=True)
            return False
        return True
