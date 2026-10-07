# Task Log: Hỗ trợ mời Bot và cập nhật cơ chế On-Ready

- **Thời gian thực hiện:** 2026-10-07 01:30 (GMT+7)
- **Tác vụ:** Giải quyết vấn đề người dùng không thấy bot trong server, giải mã Client ID từ token và bổ sung URL mời OAuth2 trực tiếp vào [`main.py`](file:///d:/Project/BotDiscord/Tarot/main.py).

---

## 1. Tóm tắt yêu cầu (Request Overview)
- Người dùng đã chạy lệnh `python main.py` nhưng không thấy Bot xuất hiện trong máy chủ Discord.
- Cần xác định nguyên nhân (bot chưa được cấp quyền gia nhập server qua OAuth2) và cung cấp đường link mời chính xác 100% kèm hướng dẫn khắc phục.

---

## 2. Các bước đã thực hiện (Actions Taken)
- Kiểm tra file cấu hình [`.env`](file:///d:/Project/BotDiscord/Tarot/.env), giải mã phần định danh từ `DISCORD_TOKEN` (`MTU1NzA5NTM3NjgzNjYzMjYzNg...`) để xác định chính xác Application / Client ID của bot là: `1557095376836632636`.
- Nâng cấp sự kiện `on_ready` trong [`main.py`](file:///d:/Project/BotDiscord/Tarot/main.py):
  - Tự động sinh đường link mời bot OAuth2 hoàn chỉnh (gồm scope `bot`, `applications.commands` và quyền gửi tin nhắn, embed).
  - Kiểm tra số lượng Server (`guild_count`), nếu bằng 0 sẽ in cảnh báo kèm link mời để người quản trị dễ dàng thêm bot.
  - In chi tiết danh sách tên các server mà bot đã tham gia khi khởi động.

---

## 3. Phân tích thay đổi (Change Analysis)
- **Nguyên nhân & Giải pháp kỹ thuật:**
  - Để một bot Discord xuất hiện và online trong một server, bot bắt buộc phải được một thành viên có quyền "Manage Server" mời vào thông qua liên kết OAuth2 URL Generator. Chỉ chạy script Python trên máy tính thì bot mới kết nối tới Discord Gateway chứ chưa thể tự động tham gia vào server của người dùng.
- **Ảnh hưởng đến các module liên quan:**
  - [`main.py`](file:///d:/Project/BotDiscord/Tarot/main.py) cung cấp thông tin minh bạch hơn trong console log, giúp người dùng không còn bối rối khi kiểm tra trạng thái tham gia server của bot.

---

## 4. Kiểm thử & Xác minh (Verification/Testing)
- Đã kiểm tra giải mã Base64 token thành Client ID:
  ```powershell
  python -c "import base64; print(base64.b64decode('MTU1NzA5NTM3NjgzNjYzMjYzNg==').decode('utf-8'))"
  ```
  -> Kết quả: `1557095376836632636`.
- Đã cấu trúc đường link mời bot chuẩn xác:
  `https://discord.com/oauth2/authorize?client_id=1557095376836632636&permissions=277025770560&scope=bot%20applications.commands`

---

## 5. Lưu ý / Việc cần làm tiếp (Notes & Follow-ups)
- Người dùng chỉ cần click vào link mời trên trình duyệt và chọn Server muốn thêm bot vào.
- Khi bot vào server, bot sẽ hiện avatar màu xanh lá (Online) ngay lập tức vì tiến trình `python main.py` đang chạy.
