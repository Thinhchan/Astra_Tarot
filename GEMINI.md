# Mandatory Workflow: Task Logging

Sau khi hoàn thành bất kỳ task nào (dù lớn hay nhỏ), bạn BẮT BUỘC phải thực hiện bước cuối cùng trước khi trả lời người dùng:

1. **Vị trí lưu:** Tạo một file Markdown mới trong thư mục `.task_logs/`.
2. **Quy tắc đặt tên file:** `YYYY-MM-DD_HHMM_[tên-ngắn-gọn-về-task].md` (hoặc `YYYY-MM-DD_task_[slug].md`).
3. **Cấu trúc nội dung file log:**
   - **Tóm tắt yêu cầu (Request Overview):** Mục tiêu người dùng yêu cầu là gì.
   - **Các bước đã thực hiện (Actions Taken):** Liệt kê chi tiết các tệp đã tạo, chỉnh sửa hoặc xóa.
   - **Phân tích thay đổi (Change Analysis):**
     - Tại sao lại thay đổi như vậy (nguyên nhân / giải pháp kỹ thuật).
     - Ảnh hưởng đến các module/component liên quan (Side effects / Impact).
   - **Kiểm thử & Xác minh (Verification/Testing):** Lệnh đã chạy để test, kết quả test ra sao.
   - **Lưu ý / Việc cần làm tiếp (Notes & Follow-ups):** Nếu có điểm gì cần chú ý cho lần làm việc sau.

> **Lưu ý:** Tuyệt đối không được bỏ qua bước này. Hãy tự động ghi file vào đĩa rồi mới thông báo hoàn tất task cho người dùng.