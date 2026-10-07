# Task Log: Mở rộng tính năng cốt lõi Tarot Bot (Buttons, Dropdown Spread, Draw, Image Stitching & Cooldown)

- **Thời gian thực hiện:** 2026-10-07 02:00 (GMT+7)
- **Tác vụ:** Hoàn thiện bộ tính năng cốt lõi theo đề án Master: Slash Commands (`/tarot`, `/draw`, `/spread`), Interactive Buttons (`[Lật Bài]`, `[Xin thêm lời khuyên]`), Dropdown Select Menu, ghép ảnh trải ngang qua Pillow, cơ chế Rate Limiting/Cooldown và bảo vệ Deferred Responses.

---

## 1. Tóm tắt yêu cầu (Request Overview)
Hiện thực hóa trọn vẹn Phần 1 & Phần 2 của đề án Master:
1. **Slash Commands:**
   - `/tarot [câu_hỏi]`: Lệnh chính bốc bài, kết nối LLM AI, kèm Interactive Buttons và ảnh trải bài ghép ngang.
   - `/draw [số_lượng: 1, 3, 5]`: Rút bài nhanh trực quan, chỉ trả về hình ảnh và tên lá bài (không gọi LLM).
   - `/spread`: Menu Dropdown lựa chọn thể loại trải bài (Quá khứ-Hiện tại-Tương lai, Tình yêu, Sự nghiệp, Thấu hiểu bản thân).
2. **Discord UI/UX:**
   - Embeds tông màu tím đen sang trọng, thumbnail lá bài Hiện tại.
   - Interactive Buttons: `[🃏 Chi Tiết Thẻ Bài]` và `[🔮 Xin Thêm Lời Khuyên]`.
   - Ghép ảnh các lá bài nằm ngang (Pillow), tự động xoay 180 độ chân thực với các lá bài Ngược (Reversed).
3. **Xử lý kỹ thuật:**
   - Deferred Responses (`defer(thinking=True)`) chống timeout 3s của Discord.
   - Rate Limiting / Cooldown 15 giây cho lệnh `/tarot` chống spam API.
   - Thuật toán bốc bài 100% ngẫu nhiên tại backend (không để LLM tự chọn).

---

## 2. Các bước đã thực hiện (Actions Taken)
- Cài đặt thư viện [`Pillow`](file:///d:/Project/BotDiscord/Tarot/requirements.txt) và cập nhật file `requirements.txt`.
- Tạo module ghép ảnh [`src/helpers/image_helper.py`](file:///d:/Project/BotDiscord/Tarot/src/helpers/image_helper.py):
  - Tải ảnh với cache RAM/ổ đĩa, xoay 180 độ đối với lá bài Ngược (`is_reversed`).
  - Ghép các lá bài nằm ngang trên nền canvas tím đen thành file ảnh `spread.png` sắc nét.
- Tạo module tương tác [`src/helpers/ui_views.py`](file:///d:/Project/BotDiscord/Tarot/src/helpers/ui_views.py):
  - Class `TarotActionView` với 2 nút: `[Chi Tiết Thẻ Bài]` và `[Xin Thêm Lời Khuyên]`.
  - Class `SpreadSelectMenu` & `SpreadMenuView` cung cấp Dropdown menu 4 chủ đề trải bài.
- Mở rộng [`src/services/tarot_service.py`](file:///d:/Project/BotDiscord/Tarot/src/services/tarot_service.py):
  - Bổ sung hàm `draw_cards(count, custom_positions)` hỗ trợ bốc linh hoạt 1, 3, 5 lá bài hoàn toàn tại backend.
- Cập nhật [`src/cogs/tarot_cog.py`](file:///d:/Project/BotDiscord/Tarot/src/cogs/tarot_cog.py):
  - Triển khai `/tarot`, `/draw`, `/spread`.
  - Thêm `@app_commands.checks.cooldown(1, 15.0)` và xử lý `CommandOnCooldown` thân thiện.
- Cập nhật [`bot.py`](file:///d:/Project/BotDiscord/Tarot/bot.py):
  - Thêm `setup_hook()` tự động nạp `src.cogs.tarot_cog` và đồng bộ app commands.

---

## 3. Phân tích thay đổi (Change Analysis)
- **Nguyên nhân & Giải pháp kỹ thuật:**
  - Việc ghép ảnh 3 lá ngang gắn vào `embed.set_image(url="attachment://spread.png")` giúp hiển thị trọn vẹn toàn bộ trải bài một cách trực quan, vượt trội hơn việc chỉ có 1 thumbnail nhỏ.
  - Các nút bấm `[Chi Tiết Thẻ Bài]` và `[Xin Thêm Lời Khuyên]` tăng tính tương tác hai chiều (interactive session) cho người dùng.
  - Dropdown Menu giúp mở rộng đa dạng chủ đề xem bói mà không làm rối danh sách lệnh Slash.
  - Cooldown 15 giây bảo vệ hạn mức quota API Google và ngăn chặn spam bot.
- **Ảnh hưởng đến các module liên quan:**
  - Kiến trúc module hóa sạch sẽ: `cogs` phụ trách giao diện, `services` phụ trách dữ liệu/AI, `helpers` phụ trách đồ họa/View.

---

## 4. Kiểm thử & Xác minh (Verification/Testing)
- Đã chạy kiểm thử tự động toàn diện:
  ```powershell
  python tests/test_tarot_flow.py
  ```
  -> **Kết quả:** 4/4 Tests Passed.
- Đã kiểm tra hàm ghép ảnh `create_spread_image()`: tạo ảnh PNG hợp lệ dung lượng ~477KB trong thời gian mili-giây.
- Đã nạp thành công module `bot.py` và `src.cogs.tarot_cog` mà không có bất kỳ xung đột nào.

---

## 5. Lưu ý / Việc cần làm tiếp (Notes & Follow-ups)
- Người dùng chỉ cần khởi động lại bot (`python bot.py`) để trải nghiệm toàn bộ các lệnh `/tarot`, `/draw`, `/spread` và các nút tương tác mới.
