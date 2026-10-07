# Task Log: Tối ưu Giao diện (Loại bỏ ảnh thừa) và Xoáy sâu Trọng tâm Luận giải Tarot

- **Thời gian thực hiện:** 2026-10-07 02:35 (GMT+7)
- **Tác vụ:** 
  1. Loại bỏ thumbnail thừa phía trên bên phải trong Discord Embed khi đã có ảnh ghép trải bài nằm ngang 3 lá (`spread.png` / `draw.png`).
  2. Nâng cấp toàn diện công cụ luận giải (Cả Gemini AI Prompt và Bộ luận giải Rider-Waite dự phòng) để giải quyết triệt để tình trạng trả lời lan man, nước đôi; luận giải thực chất từng lá bài và bổ sung mục trả lời trực diện vào câu hỏi của người hỏi.
  3. Khắc phục lỗi bất đồng bộ REST transport của thư viện Google Generative AI bằng `asyncio.to_thread` và cơ chế tự động chuyển đổi mô hình (Failover).

---

## 1. Tóm tắt yêu cầu (Request Overview)
- **Vấn đề 1 (Giao diện):** Người dùng phản ánh bị "thừa 1 ảnh ở trên". Cụ thể: Embed trải bài 3 lá vừa có Thumbnail góc trên bên phải (ảnh lá Hiện tại) vừa có ảnh ghép trải ngang 3 lá ở dưới cùng, dẫn đến việc lá bài trung tâm bị lặp lại 2 lần gây rối mắt.
- **Vấn đề 2 (Nội dung luận giải):** Người dùng phản ánh nội dung giải nghĩa bị "lan man quá", mang tính chung chung trừu tượng khiến người nghe khó hiểu. Yêu cầu:
  - Khi rút bài, phải **luận giải chi tiết từng lá bài** (nghĩa chuẩn, từ khóa, chiều xuôi/ngược, liên hệ bối cảnh).
  - Phải **xoáy thẳng vào trọng tâm câu hỏi của người hỏi** để họ cảm thấy được giải đáp khúc mắc thỏa đáng.
  - Vẫn giữ vững các quy tắc đạo đức cốt lõi (Không phán xét, không định mệnh áp đặt, tôn trọng Free Will, câu hỏi chiêm nghiệm kết thúc).

---

## 2. Các bước đã thực hiện (Actions Taken)
1. **Khắc phục vấn đề hiển thị ảnh trùng lặp:**
   - Cập nhật [`src/cogs/tarot_cog.py`](file:///d:/Project/BotDiscord/Tarot/src/cogs/tarot_cog.py#L97-L103): Chuyển `embed.set_thumbnail()` thành cơ chế dự phòng (`elif`), chỉ hiển thị thumbnail khi hệ thống không tạo được file ảnh ghép `spread.png` (hoặc `draw.png`).
   - Cập nhật tương tự trong [`src/helpers/ui_views.py`](file:///d:/Project/BotDiscord/Tarot/src/helpers/ui_views.py#L172-L176) cho menu Dropdown trải bài `/spread`.
2. **Nâng cấp từ điển từ khóa 56 lá Ẩn phụ (Minor Arcana):**
   - Nâng cấp [`src/services/tarot_dictionary.py`](file:///d:/Project/BotDiscord/Tarot/src/services/tarot_dictionary.py#L260-L315): Thay thế các từ khóa tiếng Anh thô thành bộ từ khóa chuẩn tiếng Việt giàu hình tượng cho 4 bộ (Wands - Đam mê/Hành động, Cups - Cảm xúc/Gắn kết, Swords - Lý trí/Chiến lược, Pentacles - Tài chính/Thực tế) và các cấp bậc (Ace -> King).
3. **Đại tu Bộ luận giải Cổ điển dự phòng (Classical Interpretation Engine):**
   - Nâng cấp [`generate_classical_reading()`](file:///d:/Project/BotDiscord/Tarot/src/services/gemini_service.py#L140-L310):
     - Nhận diện phân loại chủ đề câu hỏi (Tài chính / Cột mốc thời gian / Công việc / Tình duyên / Lựa chọn...).
     - Phân tích chi tiết từng lá bài: Tên lá, chiều Xuôi/Ngược, từ khóa từ điển, ý nghĩa chuẩn và phân tích *Gắn vào câu hỏi của bạn*.
     - Bổ sung chuyên mục độc lập: **🎯 Trọng Tâm Trả Lời Câu Hỏi Của Bạn (Direct Answer)**: Tổng hợp 3 lá bài để trả lời trực tiếp băn khoăn của người hỏi (VD: giải thích cột mốc tài chính 1 tỷ VNĐ phụ thuộc vào điều kiện chín muồi nào, rào cản cần vượt qua và thời điểm năng lượng hội tụ).
4. **Nâng cấp System Instruction & Prompt cho Gemini AI:**
   - Cập nhật [`SYSTEM_INSTRUCTION`](file:///d:/Project/BotDiscord/Tarot/src/services/gemini_service.py#L60-L95) và [`build_tarot_prompt()`](file:///d:/Project/BotDiscord/Tarot/src/services/gemini_service.py#L96-L140):
     - Đặt yêu cầu bắt buộc: Tuyệt đối không trả lời né tránh, vòng vo hay mơ hồ; bắt buộc có mục `🎯 Trọng Tâm Trả Lời Câu Hỏi Của Bạn (Direct Answer)`.
5. **Khắc phục lỗi REST Transport & Thử nghiệm chuỗi Model AI:**
   - Thay thế `model.generate_content_async` bằng `asyncio.to_thread(model.generate_content, prompt)` để sửa lỗi nội tại của Google Generative AI REST transport (`object GenerateContentResponse can't be used in 'await' expression`).
   - Cập nhật danh sách ưu tiên `CANDIDATE_MODELS`: Tự động chuyển đổi mượt mà giữa các model (`gemini-3.5-flash` -> `gemini-3.1-flash-lite` -> ...) khi gặp lỗi 429 Quota Exceeded.

---

## 3. Phân tích thay đổi (Change Analysis)
- **Tính thẩm mỹ & Trực quan:**
  - Embed Discord giờ đây có bố cục sạch sẽ: Phía trên là thông tin quẻ bài và nội dung luận giải sâu sắc; phía dưới là dải banner ảnh ghép 3 lá nằm ngang nghệ thuật. Không còn bị lặp lại ảnh lá bài trung tâm ở góc trên.
- **Trải nghiệm giải đáp thực chất (User Satisfaction):**
  - Người dùng đặt câu hỏi cụ thể (ví dụ: *"tôi kiếm được 1 tỷ vnđ đầu tiên vào năm mấy tuổi"*) sẽ nhận được câu trả lời rõ ràng: Phân tích 3 lá Quá khứ - Hiện tại - Tương lai và kết luận trực diện vào câu hỏi: Cột mốc này gắn liền với giai đoạn chín muồi của năng lực làm chủ và kiểm soát sự nóng vội, thay vì chỉ nhận được các câu nói sáo rỗng "hạt mầm của lá bài".

---

## 4. Kết quả kiểm thử (Verification/Testing)
- Chạy kiểm thử tự động toàn diện:
  ```powershell
  python tests/test_tarot_flow.py
  ```
  - **Kết quả:** Đạt chuẩn **5/5 Tests Passed**:
    - Kho dữ liệu 78 lá bài nguyên vẹn 100%.
    - Bốc bài 3 lá Quá khứ - Hiện tại - Tương lai chính xác, không trùng lặp.
    - AI Model Failover hoạt động hoàn hảo: Khi `gemini-3.5-flash` chạm giới hạn RPM, hệ thống tự động chuyển tiếp sang `gemini-3.1-flash-lite` và nhận phản hồi thành công.
    - Bộ luận giải dự phòng bám sát 100% câu hỏi và trả lời sắc bén.
    - Tra cứu từ điển `/card` hoạt động chuẩn mực.

---

## 5. Ghi chú & Khởi động lại Bot (Next Steps)
- Khởi động lại bot trong terminal của bạn bằng lệnh:
  ```powershell
  python bot.py
  ```
- Tiến hành trải nghiệm lại lệnh `/tarot` trên Discord với câu hỏi cụ thể để kiểm tra giao diện không còn ảnh thừa và phần luận giải xoáy sâu vào trọng tâm.
