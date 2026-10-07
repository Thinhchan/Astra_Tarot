# Task Log: Thiết lập Bộ luật Agent Persona & Đạo đức Tarot 5 Phần

- **Thời gian thực hiện:** 2026-10-07 01:50 (GMT+7)
- **Tác vụ:** Cập nhật toàn diện `SYSTEM_INSTRUCTION`, cấu trúc prompt và động cơ giải bài trong [`src/services/gemini_service.py`](file:///d:/Project/BotDiscord/Tarot/src/services/gemini_service.py) theo đúng bộ luật 5 phần chuyên nghiệp do người dùng cung cấp.

---

## 1. Tóm tắt yêu cầu (Request Overview)
Tích hợp bộ khung quy tắc 5 phần chi tiết vào trí tuệ nhân tạo Gemini của bot:
1. **Phần 1 - Agent Persona:** Đóng vai trò Guide (người dẫn đường/định hướng) thấu cảm, khách quan, giọng văn chữa lành, bình tĩnh, không phán xét hay hù dọa.
2. **Phần 2 - Hard Rules:** Từ chối/chuyển hướng các câu hỏi thuộc vùng cấm (Y tế, Pháp lý, Đầu tư tài chính rủi ro cao), không xâm phạm đời tư bên thứ ba, tôn trọng tuyệt đối Ý chí tự do (Free Will), không định mệnh hóa (Anti-fatalism).
3. **Phần 3 - Input Processing:** Tự động tái định hình câu hỏi đóng Có/Không (Yes/No) thành câu hỏi mở mang tính xây dựng; liên hệ sâu sắc với bối cảnh Querent.
4. **Phần 4 - Output Generation:** Nêu rõ tên bài + trạng thái; công thức giải từng lá (Biểu tượng/Từ khóa -> Bối cảnh -> Bài học thực tế); bắt buộc có phần Xâu chuỗi (Synthesis) kết nối logic 3 lá thành một câu chuyện; luôn tìm ra "ánh sáng cuối đường hầm" cho các lá bài thử thách.
5. **Phần 5 - Closing Prompt:** Bắt buộc kết thúc bằng câu hỏi mở tự chiêm nghiệm: *"Bạn có cảm thấy thông điệp này kết nối với điều gì đang diễn ra trong cuộc sống của mình không?"*.

---

## 2. Các bước đã thực hiện (Actions Taken)
- Cập nhật [`src/services/gemini_service.py`](file:///d:/Project/BotDiscord/Tarot/src/services/gemini_service.py):
  - Viết lại toàn bộ hằng số `SYSTEM_INSTRUCTION` chi tiết theo đúng 5 phần quy tắc.
  - Tối ưu hóa hàm `build_tarot_prompt()`:
    - Bổ sung cấu trúc bố cục rõ ràng cho từng lá bài: Biểu tượng/Từ khóa -> Góc nhìn bối cảnh -> Bài học thực tế/Hành động đề xuất.
    - Bổ sung mục riêng `🔗 Bức Tranh Tổng Thể (Synthesis — Xâu chuỗi dòng chảy)` và `🔮 Lời khuyên từ Vũ Trụ (Actionable Guidance)`.
    - Gắn cứng câu hỏi chiêm nghiệm kết thúc ở dòng cuối cùng của prompt và hậu kiểm kết quả trả về của AI để bảo đảm luôn có câu hỏi này.
  - Cập nhật hàm `generate_classical_reading()`:
    - Nhận diện các từ khóa nhạy cảm (bệnh, chết, kiện, coin, yes/no) để tự động bổ sung câu mở đầu định hướng tinh tế (Reframing disclaimer).
    - Tạo câu chuyện xâu chuỗi (Synthesis) liền mạch kết nối 3 lá và câu hỏi đóng chuẩn xác theo Phần 5.

---

## 3. Phân tích thay đổi (Change Analysis)
- **Nguyên nhân & Giải pháp kỹ thuật:**
  - Nâng tầm bot từ một công cụ bốc bài ngẫu nhiên cơ bản trở thành một Chuyên gia Tarot / Life Coach tinh tế, chuẩn mực về đạo đức nghề nghiệp và thấu cảm tâm lý.
  - Việc cấu trúc rõ ràng cả trong `SYSTEM_INSTRUCTION`, `build_tarot_prompt()` và `generate_classical_reading()` đảm bảo chất lượng phản hồi luôn đồng nhất 100%, kể cả khi Gemini AI hoạt động trực tiếp lẫn khi chuyển sang cơ chế dự phòng.
- **Ảnh hưởng đến các module liên quan:**
  - Không làm thay đổi giao diện Embed của `bot.py` hay cấu trúc dữ liệu của `tarot_service.py`, tính tương thích hoàn hảo.

---

## 4. Kiểm thử & Xác minh (Verification/Testing)
- Chạy kiểm thử tự động toàn diện:
  ```powershell
  python tests/test_tarot_flow.py
  ```
  -> **Kết quả:** 4/4 Tests Passed.
- Chạy thử nghiệm kịch bản câu hỏi Yes/No (`"Tôi có đỗ đại học không?"`):
  -> **Kết quả:** Hệ thống tự động kích hoạt câu mở đầu chuyển hướng tinh tế: `> *Thay vì một câu trả lời Có/Không tuyệt đối, các lá bài sẽ soi sáng những yếu tố đang tác động đến hành trình của bạn để bạn làm chủ ý chí tự do (Free Will) của mình.*`, phân tích 3 lá bài theo đúng 3 tiêu chí, có phần Xâu chuỗi (Synthesis) và kết thúc chuẩn xác bằng câu hỏi chiêm nghiệm.

---

## 5. Lưu ý / Việc cần làm tiếp (Notes & Follow-ups)
- Người dùng chỉ cần khởi động lại bot (`python bot.py`) để các quy tắc mới có hiệu lực ngay lập tức.
