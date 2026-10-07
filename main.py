"""
Tệp khởi chạy chính của Tarot Discord Bot.
Tương thích với cả 'python main.py' lẫn 'python bot.py'.
"""

from bot import bot, TOKEN

if __name__ == "__main__":
    if not TOKEN:
        print("=" * 70)
        print("❌ LỖI: Chưa tìm thấy DISCORD_TOKEN trong file .env!")
        print("=" * 70)
        exit(1)

    bot.run(TOKEN)
