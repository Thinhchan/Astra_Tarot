# Task Log: Core Services (Tarot Deck Logic & Gemini AI Integration)

- **Thời gian thực hiện:** 2026-10-07 01:06 (GMT+7)
- **Tác vụ:** Xây dựng tầng xử lý nghiệp vụ bộ bài Tarot (`tarot_service.py`) và kết nối Gemini AI (`gemini_service.py`).

---

## 1. Tóm tắt yêu cầu (Request Overview)
- Nạp bộ dữ liệu 78 lá bài Tarot vào bộ nhớ RAM khi bot khởi động.
- Xây dựng cơ chế bốc ngẫu nhiên 3 lá không trùng lặp (Past - Present - Future) kèm xác suất 50/50 trạng thái Xuôi (Upright) / Ngược (Reversed).
- Tích hợp thư viện `google-generativeai` để luận giải trải bài:
  - Thiết kế System Instruction và Prompt chuyên sâu theo lý thuyết chuẩn biểu tượng học Rider-Waite-Smith (1909).
  - Giọng văn huyền bí, chiêm nghiệm, phân tích Ẩn chính/Ẩn phụ, sự tắc nghẽn năng lượng ở lá ngược và lời khuyên hành động.
  - Hỗ trợ gọi API bất đồng bộ (`generate_content_async`) để không gây chặn Discord event loop.

---

## 2. Các bước đã thực hiện (Actions Taken)
- Tạo module [`src/services/tarot_service.py`](file:///d:/Project/BotDiscord/Tarot/src/services/tarot_service.py):
  - Định nghĩa data models: `TarotCard`, `TarotDraw`.
  - Triển khai class `TarotDeck` quản lý nạp dữ liệu từ `data/tarot_data.json` và hàm `draw_three_cards()` sử dụng `random.sample()` đảm bảo không trùng lặp.
  - Khởi tạo instance singleton `tarot_deck` sẵn sàng phục vụ toàn hệ thống.
- Tạo module [`src/services/gemini_service.py`](file:///d:/Project/BotDiscord/Tarot/src/services/gemini_service.py):
  - Cấu hình Gemini Client (`google.generativeai`) với `GEMINI_API_KEY` và `GEMINI_MODEL`.
  - Thiết lập `SYSTEM_INSTRUCTION` đóng vai Tarot Reader kinh nghiệm, am hiểu biểu tượng học 1909.
  - Xây dựng hàm `build_tarot_prompt()` ghép nối câu hỏi của người dùng và thông tin chi tiết của 3 lá bài.
  - Hàm `interpret_tarot_spread()` gọi API bất đồng bộ, xử lý ngoại lệ và fallback an toàn khi chưa có API key.

---

## 3. Phân tích thay đổi (Change Analysis)
- **Nguyên nhân & Giải pháp kỹ thuật:**
  - `TarotDeck` được load 1 lần duy nhất khi khởi động ứng dụng giúp tối ưu tốc độ đọc đĩa (I/O) về 0 trong suốt vòng đời bot.
  - Việc dùng `random.sample()` loại trừ khả năng rút trùng bài trong cùng một lượt trải 3 lá.
  - Sử dụng phương thức `generate_content_async` của Gemini API để giữ cho Discord Bot luôn phản hồi mượt mà (`heartbeat latency` không bị lag).
  - Cơ chế fallback thông minh: Khi thiếu API key hoặc lỗi mạng, hệ thống vẫn trả về giao diện hướng dẫn hữu ích thay vì throw exception làm treo Slash Command.
- **Ảnh hưởng đến các module liên quan:**
  - Cung cấp toàn bộ hàm nghiệp vụ cho Cog giao diện Discord (`src/cogs/tarot_cog.py`) ở Task 4 tiếp theo.

---

## 4. Kiểm thử & Xác minh (Verification/Testing)
- Đã chạy kiểm tra logic bốc bài và format prompt:
  ```powershell
  python -c "import sys; sys.stdout.reconfigure(encoding='utf-8'); from src.services.tarot_service import tarot_deck; from src.services.gemini_service import build_tarot_prompt; draws = tarot_deck.draw_three_cards(); print(build_tarot_prompt(draws, 'Liệu công việc mới có thuận lợi không?'))"
  ```
- **Kết quả:**
  - Nạp 78 lá bài thành công.
  - Bốc đúng 3 lá phân bổ đều cho 3 vị trí `QUÁ KHỨ`, `HIỆN TẠI`, `TƯƠNG LAI` kèm trạng thái ngẫu nhiên `Xuôi (Upright)` / `Ngược (Reversed)`.
  - Prompt tạo ra đạt chuẩn cấu trúc, đầy đủ đề mục và không bị lặp tên bài.

---

## 5. Lưu ý / Việc cần làm tiếp (Notes & Follow-ups)
- **Task 4 tiếp theo:** Viết `src/cogs/tarot_cog.py` và `main.py` để hiện thực hóa Slash Command `/tarot [question]`, hiển thị Embed tông Dark Purple, ảnh Thumbnail của lá bài Hiện tại và thông báo deferring "Đang kết nối với vũ trụ và xào bài...".
