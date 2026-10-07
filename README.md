# 🔮 Astra Tarot Bot (Rider-Waite & Google Gemini AI)

<p align="center">
  <a href="https://discord.com/oauth2/authorize?client_id=1557095376836632636&permissions=277025770560&scope=bot+applications.commands">
    <img src="https://img.shields.io/badge/🤖_THÊM_BOT_VÀO_SERVER_NGAY-5865F2?style=for-the-badge&logo=discord&logoColor=white" alt="Invite Bot">
  </a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Status-Online%2024/7-brightgreen?style=for-the-badge" alt="Status">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Discord.py-2.7+-5865F2?style=for-the-badge&logo=discord&logoColor=white" alt="Discord.py">
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License">
</p>

Một Discord Bot xem bói và tra cứu Tarot toàn diện, kết hợp chuẩn hệ thống **78 lá bài Rider-Waite 1909** cùng trí tuệ nhân tạo **Google Gemini AI**. Bot mang phong thái của một Reader huyền bí, sâu sắc và chữa lành, hỗ trợ cả giao diện nút bấm tương tác lẫn ảnh trải bài trực quan!

---

## 🌟 Tính Năng Nổi Bật

- 🧠 **Luận Giải Chuyên Sâu Bằng Gemini AI**: Phân tích bối cảnh, kết nối dòng năng lượng giữa các lá bài (*Quá khứ - Hiện tại - Tương lai*) và đưa ra lời khuyên thực tế thay vì trả lời máy móc.
- 🃏 **Bộ Bài Chuẩn 78 Lá Rider-Waite**: Tích hợp đầy đủ 22 lá Đại Bí Tích (*Major Arcana*) và 56 lá Tiểu Bí Tích (*Minor Arcana*), hỗ trợ chuẩn xác cả chiều xuôi (*Upright*) lẫn chiều ngược (*Reversed*).
- 🖼️ **Ghép Ảnh Trải Bài Trực Quan Tự Động**: Tự động ghép các lá bài nằm ngang liền mạch, xoay 180° đối với các lá bài ngược chân thực như trải bài thực tế.
- 🔘 **Giao Diện Tương Tác Hiện Đại (Interactive UI)**:
  - **Nút bấm (Buttons)**: Lật xem chi tiết ý nghĩa từng thẻ bài hoặc bấm *Xin thêm lời khuyên hành động* từ AI ngay bên dưới quẻ bài.
  - **Dropdown Menu (`/spread`)**: Lựa chọn linh hoạt các chủ đề trải bài chuyên biệt (*Tình yêu, Sự nghiệp, Thân - Tâm - Trí, Dòng thời gian*).
- 📖 **Từ Điển Tarot Tích Hợp (Kèm Autocomplete)**: Tra cứu nhanh ý nghĩa, từ khóa, nguyên tố và biểu tượng của bất kỳ lá bài nào với tính năng gợi ý tên thông minh khi gõ.
- ⚡ **Rút Nhanh Mượt Mà (`/draw`)**: Hỗ trợ rút nhanh 1, 3, 5 lá bài kèm hình ảnh trực quan không cần gọi AI khi muốn kiểm tra năng lượng ngày mới.

---

## 📜 Hướng Dẫn Cách Trải Bài (Dễ Hiểu Trong 1 Phút)

### 1. Nguyên Tắc Trải Bài 3 Lá Cốt Lõi:
- **Quá khứ (Past)**: Nguồn gốc, gốc rễ của vấn đề hoặc những trải nghiệm đã định hình nên trạng thái hiện tại của bạn.
- **Hiện tại (Present)**: Thực trạng hiện nay, nguồn năng lượng chủ đạo đang bao quanh bạn và thách thức trước mắt.
- **Tương lai (Future)**: Xu hướng phát triển tự nhiên nếu bạn tiếp tục hành trình hiện tại, kèm bài học vũ trụ gửi gắm.

### 2. Chiều Xuôi & Chiều Ngược:
- **Chiều Xuôi (Upright)**: Năng lượng hiển lộ rõ nét, thuận dòng phát triển và phát huy tối đa tiềm năng của lá bài.
- **Chiều Ngược (Reversed)**: Năng lượng bị tắc nghẽn, trở ngại nội tâm, chậm trễ hoặc bài học tiềm ẩn cần bạn soi chiếu lại chính mình.

---

## ⌨️ Bảng Lệnh Dành Cho Người Dùng

Bot hỗ trợ đầy đủ cả **Lệnh gạch chéo (`/`)** lẫn **Lệnh tiền tố (`!`)**:

| Lệnh Slash | Lệnh Prefix | Ý Nghĩa / Cách Dùng |
| :--- | :--- | :--- |
| **`/tarot [câu_hỏi]`** | `!tarot [câu_hỏi]` *(hoặc `!bocbai`, `!boi`)* | Bốc trải bài 3 lá và nhận lời luận giải chuyên sâu từ AI (kèm nút tương tác) |
| **`/spread`** | — | Mở menu lựa chọn chủ đề trải bài (*Tình duyên, Công việc, Thân-Tâm-Trí*) |
| **`/draw [số_lượng]`** | — | Rút nhanh 1, 3 hoặc 5 lá bài kèm ảnh trực quan (không gọi AI) |
| **`/card [tên_lá_bài]`** | `!card <tên>` *(hoặc `!tracuu`, `!dict`)* | Tra cứu từ điển ý nghĩa chuẩn 78 lá bài (hỗ trợ gợi ý tự động khi gõ) |
| **`/ping`** | `!ping` | Kiểm tra độ trễ mạng và tốc độ phản hồi của bot |

---

## 📸 Giao Diện Thực Tế Khi Xem Quẻ

```text
🔮 Trải Bài Tarot: Quá Khứ • Hiện Tại • Tương Lai
Quẻ bài của @Username

❓ Câu Hỏi Của Bạn:
> "Định hướng công việc của tôi trong những tháng tới sẽ ra sao?"

🃏 3 Lá Bài Được Khai Mở:
🕯️ Quá khứ: The Fool (Chàng Khờ) — Trạng thái: Chiều Xuôi
👁️ Hiện tại: Eight of Pentacles (Tám Tiền) — Trạng thái: Chiều Xuôi
✨ Tương lai: The Sun (Mặt Trời) — Trạng thái: Chiều Xuôi

[ 🖼️ Ảnh Ghép 3 Lá Bài Nằm Ngang Tuyệt Đẹp ]

📜 Luận Giải Từ Vũ Trụ & Rider-Waite:
1. Tổng quan năng lượng: Bạn đã bước ra khỏi vùng an toàn với sự nhiệt huyết...
2. Quá khứ (The Fool): Quyết định khởi đầu đầy dũng cảm...
3. Hiện tại (8 of Pentacles): Giai đoạn bạn đang rèn giũa kỹ năng, kiên trì tích lũy...
4. Tương lai (The Sun): Thành quả rực rỡ và sự thấu suốt sẽ đến khi bạn không ngừng nỗ lực...
5. Lời khuyên hành động: Hãy vững tin vào lộ trình phát triển hiện tại...

[🔘 Chi Tiết Thẻ Bài]   [🔮 Xin Thêm Lời Khuyên]
```

---

## 💻 Dành Cho Lập Trình Viên (Tự Host & Triển Khai)

Nếu bạn muốn tự chạy bot trên máy cá nhân hoặc triển khai lên hosting (VPS, Wispbyte, Discloud,...):

### 1. Cài đặt trên máy cục bộ

```bash
# 1. Clone repository về máy
git clone https://github.com/Thinhchan/Astra_Tarot.git
cd Astra_Tarot

# 2. Cài đặt các thư viện cần thiết
pip install -r requirements.txt

# 3. Tạo file cấu hình môi trường .env
cp .env.example .env
```

Mở file `.env` và điền các khóa API tương ứng:
```env
# Token lấy từ Discord Developer Portal
DISCORD_TOKEN=your_discord_bot_token_here

# API Key lấy miễn phí từ Google AI Studio (https://aistudio.google.com/)
GEMINI_API_KEY=your_gemini_api_key_here

# (Tùy chọn) ID Server Discord thử nghiệm để đồng bộ Slash Command tức thì
TEST_GUILD_ID=
```

Khởi chạy bot:
```bash
python bot.py
```

---

### 2. Cấu trúc Thư mục Dự án

```text
Astra_Tarot/
├── data/
│   ├── cache/                # Bộ nhớ đệm hình ảnh 78 lá bài Tarot
│   └── tarot_data.json       # Cơ sở dữ liệu 78 lá bài chuẩn Rider-Waite
├── scripts/
│   └── generate_tarot_data.py # Script tự động sinh dữ liệu lá bài
├── src/
│   ├── cogs/
│   │   └── tarot_cog.py      # Quản lý toàn bộ Slash Commands & Cooldown
│   ├── helpers/
│   │   ├── image_helper.py   # Xử lý ghép ảnh trải bài và xoay bài ngược
│   │   └── ui_views.py       # Discord Interactive Buttons & Dropdown Menus
│   ├── services/
│   │   ├── gemini_service.py # Xử lý prompt & kết nối Google Gemini AI
│   │   ├── tarot_dictionary.py # Từ điển tra cứu chi tiết 78 lá bài
│   │   └── tarot_service.py  # Xử lý rút bài, xáo bài và trạng thái lá bài
│   └── config.py             # Cấu hình biến môi trường & giao diện
├── .env.example              # Mẫu biến môi trường
├── .gitignore                # Danh sách file loại trừ (bảo mật token)
├── bot.py                    # Khởi động Bot, xử lý events & prefix commands
├── discloud.config           # File cấu hình deploy Discloud
└── requirements.txt          # Danh sách thư viện phụ thuộc
```

---

## 📄 Bản Quyền & Tác Giả

- Tác giả: **[Thinhchan](https://github.com/Thinhchan)**
- Mã nguồn: **[GitHub - Astra_Tarot](https://github.com/Thinhchan/Astra_Tarot)**
- Phát hành dưới giấy phép mã nguồn mở **MIT License**.
