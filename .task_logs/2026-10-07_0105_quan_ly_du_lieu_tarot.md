# Task Log: Quản lý Dữ liệu Tarot (Dataset Generation)

- **Thời gian thực hiện:** 2026-10-07 01:05 (GMT+7)
- **Tác vụ:** Viết script tạo dataset 78 lá bài Rider-Waite chuẩn và xuất ra file `data/tarot_data.json`.

---

## 1. Tóm tắt yêu cầu (Request Overview)
- Xây dựng kho dữ liệu 78 lá bài Tarot Rider-Waite (22 lá Ẩn chính Major Arcana + 56 lá Ẩn phụ Minor Arcana gồm 4 bộ: Gậy, Ly, Kiếm, Tiền).
- Dữ liệu tinh gọn: chỉ lưu trữ `id`, `name`, `name_vi`, `type`, `suit` và đường dẫn ảnh `image_url` trực tiếp phân giải cao.
- Không chứa phần giải nghĩa cố định trong JSON để phục vụ việc giải nghĩa động theo thời gian thực từ Gemini AI.

---

## 2. Các bước đã thực hiện (Actions Taken)
- Tạo script [`scripts/generate_tarot_data.py`](file:///d:/Project/BotDiscord/Tarot/scripts/generate_tarot_data.py):
  - Tải dữ liệu metadata 78 lá bài chuẩn 1909 Pamela Colman Smith / Arthur Edward Waite từ nguồn mở ổn định.
  - Ánh xạ tên tiếng Anh và Việt ngữ chuẩn thuật ngữ Tarot Rider-Waite.
  - Ghép nối link ảnh trực tiếp phân giải cao (`https://raw.githubusercontent.com/metabismuth/tarot-json/master/cards/...`).
  - Hỗ trợ mã hóa UTF-8 tránh xung đột ký tự trên môi trường console Windows.
- Thực thi script và sinh ra tệp dữ liệu [`data/tarot_data.json`](file:///d:/Project/BotDiscord/Tarot/data/tarot_data.json).

---

## 3. Phân tích thay đổi (Change Analysis)
- **Nguyên nhân & Giải pháp kỹ thuật:**
  - Thay vì hardcode thủ công 78 đối tượng trong mã nguồn bot, việc sử dụng script sinh dữ liệu và lưu thành JSON tĩnh giúp bot khởi động cực nhanh (nạp 1 lần vào bộ nhớ RAM) và dễ dàng cập nhật CDN/link ảnh khi cần.
  - Bổ sung trường `name_vi` giúp giao diện Discord hiển thị gần gũi với người dùng Việt Nam đồng thời giữ nguyên thuật ngữ tiếng Anh gốc cho Gemini AI tham chiếu chính xác.
- **Ảnh hưởng đến các module liên quan:**
  - Cung cấp nguồn dữ liệu chuẩn mực cho `src/services/tarot_service.py` thực hiện logic xào bài và bốc ngẫu nhiên 3 lá.

---

## 4. Kiểm thử & Xác minh (Verification/Testing)
- Lệnh kiểm tra cấu trúc dữ liệu JSON:
  ```powershell
  python -c "import json, sys; sys.stdout.reconfigure(encoding='utf-8'); cards = json.load(open('data/tarot_data.json', encoding='utf-8')); print('Total:', len(cards), '| Sample:', cards[0]['name_vi'], '| Img:', cards[0]['image_url'])"
  ```
- **Kết quả:**
  - File JSON chứa đúng 78 phần tử lá bài (`Total: 78`).
  - Lá 0: `The Fool` | `Chàng Khờ (The Fool)` | URL ảnh hợp lệ trả về HTTP 200 JPEG.
  - Lá 78: `King of Pentacles` | `Vua Tiền (King of Pentacles)`.

---

## 5. Lưu ý / Việc cần làm tiếp (Notes & Follow-ups)
- **Task 3 tiếp theo:** Xây dựng module `src/services/tarot_service.py` để nạp dữ liệu vào RAM, bốc ngẫu nhiên 3 lá (Quá khứ - Hiện tại - Tương lai kèm trạng thái Xuôi/Ngược), và module `src/services/gemini_service.py` kết nối Gemini API để giải nghĩa.
