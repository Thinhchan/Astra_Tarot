"""
Discord Cog quản lý toàn bộ Slash Commands Tarot:
- /tarot [câu_hỏi]: Lệnh chính bốc bài, kết nối LLM AI, kèm Interactive Buttons và ảnh trải bài ghép ngang.
- /draw [số_lượng]: Rút nhanh 1, 3 hoặc 5 lá bài, trả về hình ảnh trực quan không cần gọi AI.
- /spread: Chọn thể loại trải bài qua Dropdown Select Menu (Tình yêu, Công việc, Thân-Tâm-Trí, Dòng thời gian).
"""

from __future__ import annotations

import logging
from typing import List, Literal, Optional

import discord
from discord import app_commands
from discord.ext import commands

from src.config import EMBED_COLOR, EMBED_ERROR_COLOR, WAITING_MESSAGE
from src.helpers.image_helper import create_spread_image
from src.helpers.ui_views import SpreadMenuView, TarotActionView
from src.services.gemini_service import interpret_tarot_spread
from src.services.tarot_dictionary import get_card_meaning
from src.services.tarot_service import tarot_deck

logger = logging.getLogger("TarotBot.TarotCog")


class TarotCog(commands.Cog, name="Tarot"):
    """Cog xử lý giao diện người dùng và lệnh Discord."""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    # --------------------------------------------------------------------------
    # 1. LỆNH CHÍNH /tarot [câu_hỏi]
    # --------------------------------------------------------------------------
    @app_commands.command(
        name="tarot",
        description="Bốc trải bài Tarot 3 lá và nhận luận giải sâu sắc từ AI (Kèm nút tương tác)",
    )
    @app_commands.describe(
        question="Câu hỏi hoặc vấn đề bạn muốn vũ trụ soi sáng (không bắt buộc)"
    )
    @app_commands.checks.cooldown(1, 15.0, key=lambda i: (i.guild_id, i.user.id))
    async def tarot_slash(
        self,
        interaction: discord.Interaction,
        question: Optional[str] = None,
    ) -> None:
        """Slash command /tarot [question] với nút tương tác và ảnh trải bài ngang."""
        # 1. Defer response ngay lập tức để tránh timeout 3s
        await interaction.response.defer(thinking=True)

        try:
            # 2. Bốc 3 lá bài ngẫu nhiên tại backend (không để LLM tự chọn)
            draws = tarot_deck.draw_three_cards()
            past, present, future = draws[0], draws[1], draws[2]

            # 3. Tạo ảnh ghép 3 lá nằm ngang (lá ngược xoay 180 độ)
            img_buf = create_spread_image(draws)
            file = discord.File(img_buf, filename="spread.png") if img_buf else None

            # 4. Gọi Gemini LLM luận giải theo bộ System Prompt chuẩn 5 phần
            ai_reading = await interpret_tarot_spread(draws, question)

            # 5. Xây dựng giao diện Discord Embed cao cấp
            embed = discord.Embed(
                title="🔮 Trải Bài Tarot: Quá Khứ • Hiện Tại • Tương Lai",
                color=discord.Color.from_rgb(42, 17, 59),
                timestamp=discord.utils.utcnow(),
            )
            embed.set_author(
                name=f"Quẻ bài của {interaction.user.display_name}",
                icon_url=interaction.user.display_avatar.url,
            )

            if question and question.strip():
                embed.add_field(
                    name="❓ Câu Hỏi Của Bạn",
                    value=f"> *\"{question.strip()}\"*",
                    inline=False,
                )

            cards_summary = (
                f"🕯️ **Quá khứ:** {past.card.name_vi}\n"
                f"└ Trạng thái: **{past.orientation}**\n\n"
                f"👁️ **Hiện tại:** {present.card.name_vi}\n"
                f"└ Trạng thái: **{present.orientation}**\n\n"
                f"✨ **Tương lai:** {future.card.name_vi}\n"
                f"└ Trạng thái: **{future.orientation}**"
            )
            embed.add_field(name="🃏 3 Lá Bài Được Khai Mở", value=cards_summary, inline=False)

            if len(ai_reading) > 4000:
                ai_reading = ai_reading[:3990] + "..."
            embed.description = f"### 📜 Luận Giải Từ Vũ Trụ & Rider-Waite\n\n{ai_reading}"

            # Gắn ảnh ghép 3 lá làm ảnh chính. Nếu không tạo được ảnh ghép mới fallback sang thumbnail (tránh thừa ảnh trùng lặp phía trên)
            if file:
                embed.set_image(url="attachment://spread.png")
            elif present.card.image_url:
                embed.set_thumbnail(url=present.card.image_url)

            embed.set_footer(
                text=f"Lá bài trung tâm: {present.card.name} • Rider-Waite Tarot 1909",
            )

            # 6. Gắn Interactive Buttons (Lật bài / Xin thêm lời khuyên)
            view = TarotActionView(draws=draws, question=question, author_id=interaction.user.id)

            if file:
                await interaction.followup.send(embed=embed, file=file, view=view)
            else:
                await interaction.followup.send(embed=embed, view=view)

        except Exception as e:
            logger.exception(f"Lỗi khi thực thi /tarot: {e}")
            err_embed = discord.Embed(
                title="⚠️ Đã Xảy Ra Lỗi Khi Trải Bài",
                description="Dòng năng lượng vũ trụ tạm thời bị gián đoạn. Vui lòng thử lại sau!",
                color=discord.Color.red(),
            )
            await interaction.followup.send(embed=err_embed)

    # --------------------------------------------------------------------------
    # 2. LỆNH RÚT BÀI NHANH /draw [số_lượng: 1, 3, 5]
    # --------------------------------------------------------------------------
    @app_commands.command(
        name="draw",
        description="Rút nhanh 1, 3 hoặc 5 lá bài ngẫu nhiên (chỉ trả về hình ảnh và tên lá bài)",
    )
    @app_commands.describe(count="Số lượng lá bài bạn muốn rút (1, 3 hoặc 5 lá)")
    async def draw_slash(
        self,
        interaction: discord.Interaction,
        count: Literal[1, 3, 5] = 3,
    ) -> None:
        """Rút bài nhanh trực quan không tốn thời gian gọi AI."""
        await interaction.response.defer()

        draws = tarot_deck.draw_cards(count=count)
        img_buf = create_spread_image(draws)
        file = discord.File(img_buf, filename="draw.png") if img_buf else None

        embed = discord.Embed(
            title=f"🃏 Kết Quả Rút Nhanh {count} Lá Bài Tarot",
            color=discord.Color.from_rgb(42, 17, 59),
            timestamp=discord.utils.utcnow(),
        )
        embed.set_author(name=f"Lượt rút của {interaction.user.display_name}", icon_url=interaction.user.display_avatar.url)

        cards_desc = []
        for d in draws:
            cards_desc.append(f"• **{d.card.name_vi}** — Trạng thái: **{d.orientation}** ({d.card.type} Arcana)")

        embed.description = "\n".join(cards_desc)
        if file:
            embed.set_image(url="attachment://draw.png")
        elif draws and draws[0].card.image_url:
            embed.set_thumbnail(url=draws[0].card.image_url)

        embed.set_footer(text="Dùng /tarot để nhận luận giải chuyên sâu từ AI!")

        if file:
            await interaction.followup.send(embed=embed, file=file)
        else:
            await interaction.followup.send(embed=embed)

    # --------------------------------------------------------------------------
    # 3. LỆNH TRẢI BÀI CHỦ ĐỀ /spread (Dropdown Menu)
    # --------------------------------------------------------------------------
    @app_commands.command(
        name="spread",
        description="Chọn chủ đề trải bài chuyên biệt qua Dropdown menu tương tác",
    )
    async def spread_slash(self, interaction: discord.Interaction) -> None:
        """Mở menu thả xuống cho phép chọn chủ đề trải bài."""
        embed = discord.Embed(
            title="🔮 Chọn Chủ Đề Trải Bài Tarot Của Bạn",
            description=(
                "Hãy chọn một chủ đề trải bài từ danh sách bên dưới để bắt đầu khai mở thông điệp:\n\n"
                "⏳ **Quá Khứ • Hiện Tại • Tương Lai:** Dòng thời gian và sự phát triển\n"
                "💖 **Tình Yêu & Mối Quan Hệ:** Bạn, đối phương và xu hướng gắn kết\n"
                "💼 **Sự Nghiệp & Tài Lộc:** Thực trạng, thử thách và chìa khóa thành công\n"
                "🧘 **Thấu Hiểu Bản Thân:** Khám phá khía cạnh Thân - Tâm - Trí"
            ),
            color=discord.Color.gold(),
        )
        embed.set_footer(text="Chọn trong menu bên dưới để bốc bài ngay lập tức.")
        view = SpreadMenuView(author_id=interaction.user.id)
        await interaction.response.send_message(embed=embed, view=view)

    # --------------------------------------------------------------------------
    # 4. LỆNH TRA CỨU TỪ ĐIỂN /card [tên_lá_bài] (Kèm Autocomplete)
    # --------------------------------------------------------------------------
    @app_commands.command(
        name="card",
        description="Tra cứu từ điển ý nghĩa chuẩn của 1 lá bài Tarot cụ thể (bao gồm chiều xuôi & ngược)",
    )
    @app_commands.describe(name="Tên lá bài bạn muốn tra cứu (gõ tên tiếng Việt hoặc tiếng Anh)")
    async def card_slash(self, interaction: discord.Interaction, name: str) -> None:
        """Tra cứu từ điển ý nghĩa chuẩn của 1 lá bài cụ thể."""
        card = tarot_deck.find_card(name)
        if not card:
            await interaction.response.send_message(
                f"❌ Không tìm thấy lá bài nào khớp với tên `\"{name}\"`. Vui lòng chọn từ danh sách gợi ý khi gõ nhé!",
                ephemeral=True,
            )
            return

        meaning = get_card_meaning(card.name, card.suit)

        embed = discord.Embed(
            title=f"📖 Từ Điển Tarot: {card.name_vi}",
            color=discord.Color.from_rgb(42, 17, 59),
            timestamp=discord.utils.utcnow(),
        )
        embed.set_author(
            name="Rider-Waite-Smith 1909 • Tra Cứu Ý Nghĩa Chuẩn",
            icon_url=self.bot.user.display_avatar.url if self.bot.user else None,
        )

        # Thông tin phân loại & nguyên tố
        embed.add_field(
            name="🏷️ Thông Tin Tổng Quan",
            value=(
                f"• **Tên tiếng Anh:** `{card.name}`\n"
                f"• **Phân loại:** {card.type} Arcana\n"
                f"• **Nguyên tố:** {meaning.element}"
            ),
            inline=False,
        )

        # Ý nghĩa Chiều Xuôi (Upright)
        embed.add_field(
            name="☀️ Ý Nghĩa Chiều Xuôi (Upright)",
            value=(
                f"• **Từ khóa:** *{', '.join(meaning.keywords_upright)}*\n"
                f"• **Luận giải:** {meaning.meaning_upright}"
            ),
            inline=False,
        )

        # Ý nghĩa Chiều Ngược (Reversed)
        embed.add_field(
            name="🌙 Ý Nghĩa Chiều Ngược (Reversed)",
            value=(
                f"• **Từ khóa:** *{', '.join(meaning.keywords_reversed)}*\n"
                f"• **Luận giải:** {meaning.meaning_reversed}"
            ),
            inline=False,
        )

        # Biểu tượng cốt lõi
        embed.add_field(
            name="👁️ Biểu Tượng Cốt Lõi & Lời Khuyên",
            value=f"> *\"{meaning.symbolism}\"*",
            inline=False,
        )

        # Hình ảnh lá bài
        if card.image_url:
            embed.set_thumbnail(url=card.image_url)

        embed.set_footer(text=f"Mã lá bài: #{card.id} • Dùng /tarot để bốc bài và trải nghiệm")
        await interaction.response.send_message(embed=embed)

    @card_slash.autocomplete("name")
    async def card_name_autocomplete(
        self,
        interaction: discord.Interaction,
        current: str,
    ) -> List[app_commands.Choice[str]]:
        """Gợi ý tự động tên 78 lá bài khi người dùng gõ."""
        matches = tarot_deck.search_cards(current, limit=25)
        return [
            app_commands.Choice(name=f"{c.name_vi} ({c.name})", value=c.name)
            for c in matches
        ]

    @commands.command(name="card", aliases=["tracuu", "dict"])
    async def card_prefix(self, ctx: commands.Context, *, name: str = "") -> None:
        """Hỗ trợ tra cứu từ điển bằng Prefix command: !card [tên lá bài]."""
        if not name:
            await ctx.send("⚠️ Cách dùng: `!card <tên lá bài>` (Ví dụ: `!card The Fool` hoặc `!card Chàng Khờ`)")
            return

        card = tarot_deck.find_card(name)
        if not card:
            await ctx.send(f"❌ Không tìm thấy lá bài nào khớp với tên `\"{name}\"`. Vui lòng kiểm tra lại chính tả!")
            return

        meaning = get_card_meaning(card.name, card.suit)
        embed = discord.Embed(
            title=f"📖 Từ Điển Tarot: {card.name_vi}",
            color=discord.Color.from_rgb(42, 17, 59),
            timestamp=discord.utils.utcnow(),
        )
        embed.set_author(name="Rider-Waite-Smith 1909 • Tra Cứu Ý Nghĩa Chuẩn")
        embed.add_field(name="🏷️ Thông Tin Tổng Quan", value=f"• **Tên tiếng Anh:** `{card.name}`\n• **Phân loại:** {card.type} Arcana\n• **Nguyên tố:** {meaning.element}", inline=False)
        embed.add_field(name="☀️ Ý Nghĩa Chiều Xuôi (Upright)", value=f"• **Từ khóa:** *{', '.join(meaning.keywords_upright)}*\n• **Luận giải:** {meaning.meaning_upright}", inline=False)
        embed.add_field(name="🌙 Ý Nghĩa Chiều Ngược (Reversed)", value=f"• **Từ khóa:** *{', '.join(meaning.keywords_reversed)}*\n• **Luận giải:** {meaning.meaning_reversed}", inline=False)
        embed.add_field(name="👁️ Biểu Tượng Cốt Lõi", value=f"> *\"{meaning.symbolism}\"*", inline=False)
        if card.image_url:
            embed.set_thumbnail(url=card.image_url)
        embed.set_footer(text=f"Mã lá bài: #{card.id} • Dùng /tarot để bốc bài và giải quẻ")
        await ctx.send(embed=embed)

    # --------------------------------------------------------------------------
    # XỬ LÝ LỖI COOLDOWN (Rate Limiting)
    # --------------------------------------------------------------------------
    async def cog_app_command_error(
        self,
        interaction: discord.Interaction,
        error: app_commands.AppCommandError,
    ) -> None:
        if isinstance(error, app_commands.CommandOnCooldown):
            retry_after = round(error.retry_after, 1)
            msg = f"⏳ **Bạn đang kết nối với vũ trụ quá nhanh!** Vui lòng tịnh tâm đợi thêm `{retry_after}s` nữa để dùng lại lệnh nhé."
            if interaction.response.is_done():
                await interaction.followup.send(msg, ephemeral=True)
            else:
                await interaction.response.send_message(msg, ephemeral=True)
        else:
            logger.error(f"Lỗi lệnh trong TarotCog: {error}")


async def setup(bot: commands.Bot) -> None:
    """Đăng ký TarotCog."""
    await bot.add_cog(TarotCog(bot))
    logger.info("Đã đăng ký TarotCog thành công.")
