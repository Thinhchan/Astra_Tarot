import os
import sys
import json
import random
import asyncio
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

from src.services.tarot_service import tarot_deck
from src.services.gemini_service import interpret_tarot_spread
from src.config import EMBED_COLOR, EMBED_ERROR_COLOR, TEST_GUILD_ID

# 1. Cấu hình UTF-8 cho console Windows
sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)

# 2. Nạp cấu hình từ file .env
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

# 3. Khởi tạo Intents
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

# Tin nhắn delay thông báo xào bài
WAITING_MESSAGE = "✨ *Đang kết nối với dòng chảy vũ trụ và xào bài... Xin hãy tịnh tâm đợi trong giây lát.*"


# ----------------- HÀM TIỆN ÍCH HỖ TRỢ GỬI TIN NHẮN & INTERACTION -----------------

async def send_msg(dest, content=None, embed=None):
    """Gửi tin nhắn an toàn hỗ trợ cả Channel lẫn Interaction, tự động fallback nếu tương tác hết hạn."""
    try:
        if isinstance(dest, discord.Interaction):
            if dest.response.is_done():
                return await dest.followup.send(content=content, embed=embed)
            else:
                return await dest.response.send_message(content=content, embed=embed)
        else:
            return await dest.send(content=content, embed=embed)
    except discord.errors.NotFound:
        # Tương tác Slash bị quá hạn 3s do mạng lag -> Tự động gửi thẳng vào kênh chat bình thường
        if isinstance(dest, discord.Interaction) and dest.channel:
            try:
                return await dest.channel.send(content=content, embed=embed)
            except Exception:
                pass
    except discord.errors.Forbidden:
        print("⚠️ Bot bị thiếu quyền (Forbidden) khi gửi tin nhắn vào kênh!")
        if isinstance(dest, discord.Interaction) and dest.channel:
            try:
                await dest.channel.send(
                    "❌ **Bot không có quyền gửi tin nhắn hoặc gắn liên kết trong kênh này!**\n"
                    "👉 Hãy cấp quyền 'Gửi tin nhắn' và 'Gắn liên kết' (Embed Links) cho bot nhé!"
                )
            except Exception:
                pass
    except Exception as e:
        print(f"⚠️ Không thể gửi tin nhắn: {e}")


async def safe_defer(interaction: discord.Interaction):
    """Defer interaction an toàn, chặn lỗi Unknown interaction nếu mạng bị trễ quá 3 giây."""
    try:
        await interaction.response.defer()
    except (discord.errors.NotFound, discord.errors.HTTPException):
        pass


# ----------------- SỰ KIỆN BOT DISCORD (EVENTS) -----------------

@bot.event
async def setup_hook():
    """Khởi tạo và nạp các Cog mở rộng trước khi kết nối."""
    try:
        await bot.load_extension("src.cogs.tarot_cog")
        print("📦 Đã nạp thành công extension: src.cogs.tarot_cog")
    except Exception as e:
        print(f"❌ Lỗi khi nạp TarotCog: {e}")


@bot.event
async def on_ready():
    activity = discord.Activity(
        type=discord.ActivityType.listening,
        name="/tarot • Dòng chảy vũ trụ 🔮",
    )
    await bot.change_presence(status=discord.Status.online, activity=activity)

    bot_id = bot.user.id if bot.user else 0
    invite_url = f"https://discord.com/oauth2/authorize?client_id={bot_id}&permissions=277025770560&scope=bot%20applications.commands"

    print("=" * 65)
    print(f"🔮 Bot Tarot đã online: {bot.user} (ID: {bot_id})")
    print(f"🌐 Đang có mặt tại {len(bot.guilds)} máy chủ:")
    for guild in bot.guilds:
        print(f"   • {guild.name} (ID: {guild.id})")
    if len(bot.guilds) == 0:
        print(f"⚠️ Bot CHƯA tham gia server nào! Link mời bot:\n{invite_url}")
    print(f"🔗 Link mời Bot: {invite_url}")
    print("=" * 65)

    # Đồng bộ Slash Commands
    try:
        if TEST_GUILD_ID:
            guild_obj = discord.Object(id=TEST_GUILD_ID)
            bot.tree.copy_global_to(guild=guild_obj)
            synced_guild = await bot.tree.sync(guild=guild_obj)
            print(f"⚡ Đã đồng bộ {len(synced_guild)} lệnh Slash vào Test Guild ({TEST_GUILD_ID}) thành công!")

        synced = await bot.tree.sync()
        print(f"✅ Đã đồng bộ {len(synced)} lệnh Slash (/) toàn cầu thành công!")
    except Exception as e:
        print(f"❌ Lỗi khi đồng bộ Slash Command: {e}")


@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    """Xử lý lỗi cho Slash Command, chặn traceback đỏ chói khi mạng lag hoặc timeout."""
    if isinstance(error, app_commands.CommandInvokeError) and isinstance(error.original, discord.errors.NotFound):
        if error.original.code == 10062:
            cmd_name = interaction.command.name if interaction.command else "lệnh"
            print(f"ℹ️ [Mạng lag] Lệnh /{cmd_name} bị Discord quá hạn 3s, đã xử lý an toàn.")
            return
    cmd_name = interaction.command.name if interaction.command else "lệnh"
    print(f"⚠️ Lỗi lệnh /{cmd_name}: {error}")


# ----------------- XỬ LÝ LOGIC CÁC LỆNH (COMMAND HANDLERS) -----------------

async def handle_tarot(channel, user, question: str = None, dest=None):
    """Bốc trải bài Tarot 3 lá Quá khứ - Hiện tại - Tương lai và gửi Embed giải nghĩa."""
    target_dest = dest or channel

    # 1. Gửi thông báo chờ xào bài
    waiting_msg = None
    if isinstance(target_dest, discord.Interaction):
        # Nếu đã defer thì gửi followup, chưa thì gửi response
        if not target_dest.response.is_done():
            await target_dest.response.send_message(WAITING_MESSAGE)
    else:
        waiting_msg = await channel.send(WAITING_MESSAGE)

    try:
        # 2. Rút 3 lá bài không trùng lặp
        draws = tarot_deck.draw_three_cards()
        past, present, future = draws[0], draws[1], draws[2]

        # 3. Luận giải bài (gọi Gemini AI hoặc fallback cổ điển mượt mà)
        ai_reading = await interpret_tarot_spread(draws, question)

        # 4. Tạo Discord Embed tông tím đen huyền bí
        embed = discord.Embed(
            title="🔮 Trải Bài Tarot: Quá Khứ • Hiện Tại • Tương Lai",
            color=discord.Color.from_rgb(42, 17, 59),  # Dark Mystic Purple
            timestamp=discord.utils.utcnow(),
        )

        embed.set_author(
            name=f"Quẻ bài của {user.display_name}",
            icon_url=user.display_avatar.url,
        )

        # Câu hỏi của người bốc
        if question and question.strip():
            embed.add_field(
                name="❓ Câu Hỏi Của Bạn",
                value=f"> *\"{question.strip()}\"*",
                inline=False,
            )

        # Danh sách 3 lá bài đã bốc
        cards_summary = (
            f"🕯️ **Quá khứ:** {past.card.name_vi}\n"
            f"└ Trạng thái: **{past.orientation}**\n\n"
            f"👁️ **Hiện tại:** {present.card.name_vi}\n"
            f"└ Trạng thái: **{present.orientation}**\n\n"
            f"✨ **Tương lai:** {future.card.name_vi}\n"
            f"└ Trạng thái: **{future.orientation}**"
        )
        embed.add_field(name="🃏 3 Lá Bài Được Khai Mở", value=cards_summary, inline=False)

        # Nội dung giải nghĩa
        if len(ai_reading) > 4000:
            ai_reading = ai_reading[:3990] + "..."
        embed.description = f"### 📜 Luận Giải Từ Vũ Trụ & Rider-Waite\n\n{ai_reading}"

        # Thumbnail lá bài Hiện tại
        if present.card.image_url:
            embed.set_thumbnail(url=present.card.image_url)

        embed.set_footer(
            text=f"Lá bài trung tâm: {present.card.name} • Rider-Waite Tarot 1909",
        )

        # 5. Cập nhật lại tin nhắn ban đầu với Embed hoàn chỉnh
        if isinstance(target_dest, discord.Interaction):
            await target_dest.edit_original_response(content="", embed=embed)
        elif waiting_msg:
            await waiting_msg.edit(content="", embed=embed)
        else:
            await channel.send(embed=embed)

    except Exception as e:
        print(f"❌ Lỗi khi thực hiện trải bài Tarot: {e}")
        err_embed = discord.Embed(
            title="⚠️ Đã Xảy Ra Lỗi Khi Trải Bài",
            description="Dòng năng lượng vũ trụ tạm thời bị gián đoạn. Vui lòng thử lại sau giây lát!",
            color=discord.Color.red(),
        )
        if isinstance(target_dest, discord.Interaction):
            try:
                await target_dest.edit_original_response(content="", embed=err_embed)
            except Exception:
                pass
        elif waiting_msg:
            await waiting_msg.edit(content="", embed=err_embed)


async def handle_ping(channel, dest=None):
    """Kiểm tra độ trễ mạng của bot."""
    target_dest = dest or channel
    latency_ms = round(bot.latency * 1000)
    embed = discord.Embed(
        title="🏓 Pong!",
        description=f"Độ trễ bot: `{latency_ms} ms`",
        color=discord.Color.green(),
    )
    await send_msg(target_dest, embed=embed)


# ----------------- PREFIX COMMANDS (LỆNH TIỀN TỐ !) -----------------

@bot.command(name="tarot", aliases=["bocbai", "boi"])
async def cmd_tarot(ctx, *, question: str = ""):
    await handle_tarot(ctx.channel, ctx.author, question=question, dest=ctx)

@bot.command(name="ping")
async def cmd_ping(ctx):
    await handle_ping(ctx.channel, dest=ctx)


# ----------------- SLASH COMMANDS (LỆNH TIỆN ÍCH) -----------------

@bot.tree.command(name="ping", description="Kiểm tra độ trễ (latency) của bot")
async def slash_ping(interaction: discord.Interaction):
    await handle_ping(interaction.channel, dest=interaction)


# ----------------- KHỞI CHẠY BOT -----------------
if __name__ == "__main__":
    if not TOKEN:
        print("=" * 70)
        print("❌ LỖI: Chưa tìm thấy DISCORD_TOKEN trong file .env!")
        print("=" * 70)
        sys.exit(1)

    try:
        bot.run(TOKEN)
    except discord.errors.PrivilegedIntentsRequired:
        print("\n" + "=" * 70)
        print("❌ LỖI: BOT CHƯA ĐƯỢC BẬT 'MESSAGE CONTENT INTENT' TRÊN DEVELOPER PORTAL!")
        print("=" * 70)
        print("1. Truy cập: https://discord.com/developers/applications")
        print("2. Bấm vào bot của bạn -> chọn mục 'Bot'")
        print("3. Bật 'MESSAGE CONTENT INTENT' -> Save Changes")
        print("=" * 70 + "\n")
    except Exception as e:
        print(f"❌ Lỗi khởi chạy bot: {e}")
