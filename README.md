# 🔮 Tarot Discord Bot (Rider-Waite & Google Gemini AI)

Bot Discord xem bói Tarot 3 lá (Quá khứ - Hiện tại - Tương lai) kết hợp trí tuệ nhân tạo Gemini để giải nghĩa chuẩn lý thuyết Rider-Waite với phong thái Reader huyền bí và sâu sắc.

---

## 📁 Cấu trúc Dự án (Project Structure)

```text
Tarot/
├── .task_logs/              # Nhật ký thực hiện các task phát triển
├── data/                    # Chứa dataset 78 lá bài Tarot chuẩn Rider-Waite
│   └── tarot_data.json
├── scripts/                 # Công cụ tạo & cập nhật dữ liệu Tarot
│   └── generate_tarot_data.py
├── src/
│   ├── cogs/                # Discord Slash Commands & UI Components
│   │   ├── __init__.py
│   │   └── tarot_cog.py
│   ├── services/            # Tầng xử lý nghiệp vụ
│   │   ├── __init__.py
│   │   ├── gemini_service.py # Prompting & kết nối Gemini AI
│   │   └── tarot_service.py  # Load deck, bốc 3 lá, random xuôi/ngược
│   ├── __init__.py
│   └── config.py            # Quản lý cấu hình, biến môi trường & hằng số
├── .env.example             # File mẫu biến môi trường
├── .gitignore               # Loại bỏ file nhạy cảm và virtual environment
├── main.py                  # Entry point khởi chạy bot
├── requirements.txt         # Danh sách thư viện Python
└── README.md                # Tài liệu dự án
```

---

## 🛠️ Cài đặt & Chuẩn bị

1. **Cài đặt thư viện phụ thuộc:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Cấu hình môi trường:**
   - Sao chép file `.env.example` thành `.env`:
     ```bash
     cp .env.example .env
     ```
   - Điền `DISCORD_TOKEN` từ [Discord Developer Portal](https://discord.com/developers/applications).
   - Điền `GEMINI_API_KEY` từ [Google AI Studio](https://aistudio.google.com/app/apikey).
