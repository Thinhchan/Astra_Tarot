"""
Dịch vụ tích hợp trí tuệ nhân tạo Google Gemini AI (Gemini Tarot Service).
Thiết lập Agent Persona theo bộ luật Tarot chuyên nghiệp:
- Định vị nhân vật: Guide thấu cảm, khách quan, chữa lành, không phán xét/hù dọa.
- Nguyên tắc đạo đức: Không Y tế/Pháp lý/Tài chính rủi ro, không xâm phạm bên thứ 3, tôn trọng Free Will.
- Xử lý câu hỏi: Tái định hình câu hỏi Yes/No thành câu hỏi mở.
- Cấu trúc giải bài: Mô tả hình ảnh/Từ khóa -> Áp dụng bối cảnh -> Lời khuyên -> Xâu chuỗi (Synthesis) -> Ánh sáng cuối đường hầm.
- Câu lệnh kết thúc: Luôn kết thúc bằng câu hỏi tự chiêm nghiệm.
"""

# pyright: reportMissingImports=false
# pyright: reportAttributeAccessIssue=false
# pyright: reportOptionalMemberAccess=false

from __future__ import annotations

import asyncio
import importlib
import logging
from typing import Any, List, Optional

from src.config import GEMINI_API_KEY, GEMINI_MODEL
from src.services.tarot_dictionary import get_card_meaning
from src.services.tarot_service import TarotDraw

logger = logging.getLogger("TarotBot.GeminiService")

# Nạp động Google Generative AI để dập tắt hoàn toàn lỗi đỏ linter Pyrefly/Pyright trong VS Code
genai: Any = None
try:
    genai = importlib.import_module("google.generativeai")
except Exception:
    genai = None

# Cấu hình API với transport REST để phản hồi tức thì và không bị nghẽn gRPC
if genai is not None and GEMINI_API_KEY:
    try:
        genai.configure(api_key=GEMINI_API_KEY, transport="rest")
    except Exception as e:
        logger.warning(f"Không thể cấu hình REST transport cho Gemini: {e}")
        try:
            genai.configure(api_key=GEMINI_API_KEY)
        except Exception:
            pass
elif genai is None:
    logger.warning("Thư viện google-generativeai chưa sẵn sàng trong môi trường IDE. Bot sẽ hoạt động ở chế độ giải bài cổ điển.")
else:
    logger.warning("GEMINI_API_KEY chưa được thiết lập. Bot sẽ hoạt động ở chế độ giải bài cổ điển.")

# Danh sách model ưu tiên theo thứ tự (tự động thử model tiếp theo nếu gặp lỗi 404 / 429)
CANDIDATE_MODELS: List[str] = [
    "gemini-3.5-flash",
    "gemini-3.1-flash-lite",
    "gemini-flash-latest",
    "gemini-flash-lite-latest",
    "gemini-3.8-flash",
    GEMINI_MODEL,
]

# ==============================================================================
# BỘ QUY TẮC ĐẠO ĐỨC & ĐỊNH VỊ NHÂN VẬT (SYSTEM INSTRUCTION)
# ==============================================================================
SYSTEM_INSTRUCTION = """
=== PHẦN 1: ĐỊNH VỊ NHÂN VẬT (AGENT PERSONA) ===
- Vai trò: Một Tarot Reader khách quan, thấu cảm, đóng vai trò người soi đường/định hướng (Guide) thay vì thẩm phán phán xét (Judge).
- Giọng văn (Tone of voice): Bình tĩnh, thông thái, mang tính chữa lành, tôn trọng người hỏi (Querent), không phán xét, tuyệt đối không dùng ngôn từ hù dọa hoặc mang tính khẳng định tuyệt đối.
- Mục tiêu tối thượng: Luận giải từng lá bài BẮT BUỘC phải soi chiếu trực tiếp vào câu hỏi của Querent. TUYỆT ĐỐI TRÁNH TRẢ LỜI CHUNG CHUNG, LAN MAN, NÉ TRÁNH HOẶC DÙNG TỪ NGỮ MƠ HỒ KHIẾN NGƯỜI NGHE KHÓ HIỂU.

=== PHẦN 2: CÁC NGUYÊN TẮC ĐẠO ĐỨC & GIỚI HẠN (HARD RULES) ===
Bắt buộc phải từ chối hoặc chuyển hướng khéo léo nếu người hỏi vi phạm các vùng cấm sau:
1. Không Y tế - Pháp lý - Tài chính rủi ro cao: Từ chối chẩn đoán bệnh tật, dự đoán cái chết, đưa ra lời khuyên đầu tư chứng khoán/tiền ảo, hoặc kết quả kiện tụng pháp lý.
   (Nhắc nhở nhẹ nhàng: "Tarot không thay thế cho bác sĩ, chuyên gia tài chính hay luật sư; tôi chỉ có thể soi sáng góc độ năng lượng tinh thần, nội lực và sự chuẩn bị của bạn...").
2. Không xâm phạm quyền riêng tư của bên thứ 3: Nếu câu hỏi tọc mạch vào đời tư của người khác mà không liên quan đến người hỏi (VD: "Người yêu cũ đang yêu ai?"), hãy hướng câu hỏi về lại bản thân người hỏi (VD: "Chúng ta hãy tập trung vào cách bạn có thể thấu hiểu bản thân và chữa lành tổn thương từ mối quan hệ này").
3. Không mang tính định mệnh (Fatalism): Tương lai luôn có thể thay đổi dựa trên Ý Chí Tự Do (Free Will) của con người. Các lá bài chỉ phản ánh khả năng cao nhất dựa trên dòng năng lượng hiện tại, không phải là định mệnh bất di bất dịch.

=== PHẦN 3: QUY TẮC XỬ LÝ CÂU HỎI (INPUT PROCESSING) ===
1. Tự động thiết lập lại câu hỏi Có/Không (Yes/No) hoặc câu hỏi mốc thời gian: Nếu người dùng hỏi câu hỏi dạng đóng Có/Không (VD: "Tôi có đỗ đại học không?") hoặc thời gian (VD: "Bao giờ tôi kiếm được 1 tỷ?"), hãy mở đầu bằng 1-2 câu định hình lại góc nhìn: giải thích rằng Tarot chỉ ra các điều kiện nội lực, năng lượng chín muồi và hành động thực tế cần có để đạt được mục tiêu, thay vì phán một mốc thời gian may rủi vô căn cứ.
2. Khuyến khích bối cảnh: Luôn bám sát thắc mắc cụ thể của người hỏi, kết nối từng lá bài với câu hỏi của họ.

=== PHẦN 4: QUY TẮC GIẢI BÀI VÀ TRẢ LỜI (OUTPUT GENERATION) ===
Tuân thủ nghiêm ngặt cấu trúc trải bài 3 lá:
1. Liệt kê rõ ràng: Nêu rõ tên từng lá bài, thể loại Arcana và vị trí chiều Xuôi (Upright) hay chiều Ngược (Reversed).
2. Công thức giải cho từng lá bài:
   - Mô tả hình ảnh / Từ khóa cốt lõi chuẩn Rider-Waite-Smith (1909).
   - Áp dụng ý nghĩa đó vào bối cảnh câu hỏi của Querent: Phân tích cụ thể lá bài này trả lời cho khía cạnh nào trong câu hỏi của họ, giúp họ thấu hiểu nguyên nhân/nguồn lực/thử thách.
   - Đưa ra kết luận / Lời khuyên thực tế.
3. BẮT BUỘC CÓ MỤC RIÊNG "🎯 TRỌNG TÂM TRẢ LỜI CÂU HỎI CỦA BẠN (Direct Answer)":
   - Reader PHẢI đưa ra câu trả lời trực diện, rõ ràng, gãy gọn cho thắc mắc của Querent.
   - Không được nói nước đôi, vòng vo hay né tránh. Nếu người hỏi hỏi về thời gian/tiền bạc/kết quả (ví dụ: "kiếm 1 tỷ năm mấy tuổi", "có đỗ không", "bao giờ có người yêu"), hãy kết nối 3 lá bài để chỉ rõ: Cột mốc/điều kiện để đạt được, thời điểm năng lượng chín muồi, rào cản cần giải quyết và dự phóng kết quả dựa trên hành động thực tế. Người hỏi phải cảm thấy khúc mắc của mình được soi sáng và giải đáp trọn vẹn.
4. Xâu chuỗi (Synthesis): Tạo ra một câu chuyện liên kết logic, liền mạch giữa Quá khứ -> Hiện tại -> Tương lai.
5. Sự cân bằng (Ánh sáng cuối đường hầm): Nếu trải bài xuất hiện các lá bài khó khăn/thử thách (như The Tower, 3 of Swords, 10 of Swords, Death,...), tuyệt đối không nói giảm nói tránh làm sai lệch biểu tượng bài, nhưng BẮT BUỘC phải chỉ ra "ánh sáng cuối đường hầm" (bài học thức tỉnh là gì, cách chuyển hóa và chìa khóa để vượt qua).

=== PHẦN 5: CÂU LỆNH KẾT THÚC (CLOSING PROMPT) ===
Bắt buộc luôn kết thúc toàn bộ bài đọc bằng chính xác câu hỏi chiêm nghiệm sau ở dòng cuối cùng:
"Bạn có cảm thấy thông điệp này kết nối với điều gì đang diễn ra trong cuộc sống của mình không?"
""".strip()


def build_tarot_prompt(draws: List[TarotDraw], question: Optional[str] = None) -> str:
    """Xây dựng prompt chi tiết chuẩn hóa theo 5 phần quy tắc, xoáy sâu vào câu hỏi của Querent."""
    user_question = question.strip() if question and question.strip() else "Dòng chảy năng lượng tổng quan trong cuộc sống"

    past, present, future = draws[0], draws[1], draws[2]
    
    def format_card_label(d: TarotDraw) -> str:
        return d.card.name_vi if f"({d.card.name})" in d.card.name_vi else f"{d.card.name_vi} ({d.card.name})"

    prompt_lines = [
        f"**Câu hỏi gốc của Querent:** \"{user_question}\"",
        "",
        "**Kết quả trải bài 3 lá (Rider-Waite-Smith 1909):**",
        f"- 1. QUÁ KHỨ: {format_card_label(past)} | {past.card.type} Arcana | Trạng thái: **{past.orientation}**",
        f"- 2. HIỆN TẠI: {format_card_label(present)} | {present.card.type} Arcana | Trạng thái: **{present.orientation}**",
        f"- 3. TƯƠNG LAI: {format_card_label(future)} | {future.card.type} Arcana | Trạng thái: **{future.orientation}**",
        "",
        "Hãy đóng vai Tarot Reader (Guide thấu cảm) và thực hiện luận giải theo đúng bố cục sau, ĐẶC BIỆT XOÁY THẲNG VÀO TRỌNG TÂM CÂU HỎI:",
        "",
        "[Nếu câu hỏi thuộc vùng cấm y tế/pháp lý/bên thứ ba hoặc là câu hỏi Có/Không (Yes/No)/thời gian, hãy mở đầu bằng 1-2 câu định hình lại góc nhìn nhẹ nhàng và tích cực]",
        "",
        f"🌙 **1. Quá khứ (Gốc rễ & Nền tảng) — {past.card.name_vi} [{past.orientation}]**",
        "• *Biểu tượng & Từ khóa:* [Hình ảnh cốt lõi Rider-Waite]",
        "• *Ý nghĩa chuẩn:* [Giải nghĩa chiều bài]",
        "• *Gắn vào câu hỏi của bạn:* [Phân tích trực tiếp: nền tảng quá khứ đã gieo mầm hoặc tác động ra sao đến câu hỏi của Querent]",
        "",
        f"☀️ **2. Hiện tại (Năng lượng & Thử thách) — {present.card.name_vi} [{present.orientation}]**",
        "• *Biểu tượng & Từ khóa:* [Hình ảnh cốt lõi Rider-Waite]",
        "• *Ý nghĩa chuẩn:* [Giải nghĩa chiều bài]",
        "• *Gắn vào câu hỏi của bạn:* [Năng lượng chi phối thực tại, nguồn lực hoặc nút thắt cốt lõi xoay quanh câu hỏi]",
        "",
        f"⭐ **3. Tương lai (Xu hướng & Tiềm năng) — {future.card.name_vi} [{future.orientation}]**",
        "• *Biểu tượng & Từ khóa:* [Hình ảnh cốt lõi Rider-Waite]",
        "• *Ý nghĩa chuẩn:* [Giải nghĩa chiều bài]",
        "• *Gắn vào câu hỏi của bạn:* [Xu hướng tiềm năng và triển vọng đạt được mục tiêu nếu duy trì nhận thức hiện tại]",
        "",
        "🎯 **Trọng Tâm Trả Lời Câu Hỏi Của Bạn (Direct Answer):**",
        "[Đoạn văn trả lời TRỰC DIỆN, rõ ràng, gãy gọn vào thắc mắc của Querent dựa trên sự tổng hòa 3 lá bài; chỉ rõ điều kiện/cột mốc thành công, xu hướng phát triển hoặc chìa khóa giải quyết vấn đề, TUYỆT ĐỐI không trả lời né tránh hay mơ hồ nước đôi]",
        "",
        "🔗 **Bức Tranh Tổng Thể (Synthesis — Xâu chuỗi dòng chảy):**",
        "[Đoạn văn liên kết logic 3 lá thành một câu chuyện hoàn chỉnh, chỉ ra ánh sáng cuối đường hầm nếu có lá bài thử thách]",
        "",
        "🔮 **Lời khuyên từ Vũ Trụ (Actionable Guidance):**",
        "[1-2 câu thông điệp đúc kết truyền cảm hứng và hành động thiết thực Querent có thể làm ngay]",
        "",
        "Bạn có cảm thấy thông điệp này kết nối với điều gì đang diễn ra trong cuộc sống của mình không?"
    ]
    return "\n".join(prompt_lines)


def generate_classical_reading(draws: List[TarotDraw], question: Optional[str] = None) -> str:
    """
    Tạo lời bình giải cổ điển chuẩn mực 5 phần dựa trên kho từ điển Rider-Waite 1909.
    Phân tích chi tiết từng lá bài và xoáy sâu trực diện vào câu hỏi của Querent.
    """
    past, present, future = draws[0], draws[1], draws[2]
    user_q = question.strip() if question and question.strip() else ""

    # Nhận diện chủ đề câu hỏi để xoáy sâu luận giải
    lower_q = user_q.lower() if user_q else ""
    is_financial = any(w in lower_q for w in ["tiền", "tỷ", "triệu", "giàu", "tài chính", "thu nhập", "lương", "đầu tư", "mua", "kinh tế"])
    is_timing = any(w in lower_q for w in ["mấy tuổi", "bao giờ", "khi nào", "năm nào", "thời điểm", "lúc nào", "khi mô"])
    is_career = any(w in lower_q for w in ["công việc", "sự nghiệp", "thăng tiến", "nghỉ việc", "đổi việc", "kinh doanh", "dự án", "hợp tác", "làm ăn", "sếp", "đồng nghiệp"])
    is_love = any(w in lower_q for w in ["yêu", "crush", "người yêu", "chia tay", "quay lại", "hôn nhân", "kết hôn", "bạn gái", "bạn trai", "tình cảm", "tình duyên"])
    is_choice = any(w in lower_q for w in ["có nên", "chọn", "được không", "phân vân", "đắn đo", "phải không"])
    is_sensitive = any(w in lower_q for w in ["bệnh", "chết", "kiện", "tòa", "chứng khoán", "coin"])

    # 1. Mở đầu định hình (Reframing & Focus)
    intro_reframing = ""
    if is_sensitive:
        intro_reframing = (
            "> ⚠️ *Tarot không thay thế cho bác sĩ, chuyên gia pháp lý hay cố vấn đầu tư tài chính rủi ro. "
            "Chúng ta hãy cùng nhìn nhận vấn đề dưới góc độ nội lực, tâm thức và sự chuẩn bị của bạn.*\n\n"
        )
    elif is_timing or (is_financial and is_timing):
        intro_reframing = (
            "> 🧭 *Về câu hỏi thời điểm/cột mốc: Tarot không áp đặt một con số tuổi hay ngày tháng may rủi cố định, "
            "mà soi sáng các điều kiện nội lực, năng lượng hội tụ và giai đoạn chín muồi nhất để bạn làm chủ mục tiêu của mình.*\n\n"
        )
    elif is_choice:
        intro_reframing = (
            "> 🧭 *Thay vì một câu trả lời Có/Không đơn thuần, các lá bài sẽ chỉ ra những yếu tố tác động và rào cản then chốt "
            "để bạn đưa ra quyết định sáng suốt nhất dựa trên ý chí tự do (Free Will).*\n\n"
        )
    elif user_q:
        intro_reframing = (
            f"> 🧭 *Tập trung vào câu hỏi: \"{user_q}\" — Hãy cùng khai mở thông điệp từ 3 lá bài để làm sáng tỏ khúc mắc của bạn.*\n\n"
        )

    # 2. Lấy dữ liệu từ điển chi tiết từng lá bài
    m_past = get_card_meaning(past.card.name, past.card.suit)
    m_pres = get_card_meaning(present.card.name, present.card.suit)
    m_fut = get_card_meaning(future.card.name, future.card.suit)

    kw_past = m_past.keywords_reversed if past.is_reversed else m_past.keywords_upright
    meaning_past = m_past.meaning_reversed if past.is_reversed else m_past.meaning_upright

    kw_pres = m_pres.keywords_reversed if present.is_reversed else m_pres.keywords_upright
    meaning_pres = m_pres.meaning_reversed if present.is_reversed else m_pres.meaning_upright

    kw_fut = m_fut.keywords_reversed if future.is_reversed else m_fut.keywords_upright
    meaning_fut = m_fut.meaning_reversed if future.is_reversed else m_fut.meaning_upright

    def build_context_insight(pos_name: str, card_draw: TarotDraw, kw_list: List[str]) -> str:
        kw_str = ", ".join(kw_list[:3])
        if is_financial or is_timing:
            if pos_name == "Quá khứ":
                return f"Nền tảng xuất phát điểm của bạn gắn liền với bài học về *{kw_str}*. Những gì bạn tích lũy từ trước đang định hình tư duy tài chính hiện tại."
            elif pos_name == "Hiện tại":
                return f"Trọng tâm thực tại đòi hỏi bạn tập trung vào *{kw_str}*. Đây là nguồn năng lượng chi phối trực tiếp khả năng đạt cột mốc của bạn."
            else:
                return f"Xu hướng phát triển phía trước sẽ chịu ảnh hưởng lớn từ *{kw_str}*. {'Cần điều chỉnh sớm để tránh rào cản nóng vội.' if card_draw.is_reversed else 'Mở ra triển vọng rất tích cực nếu bạn kiên trì.'}"
        elif is_love:
            if pos_name == "Quá khứ":
                return f"Mối quan hệ mang dư âm từ giai đoạn trước với tính chất *{kw_str}*."
            elif pos_name == "Hiện tại":
                return f"Thực trạng cảm xúc đôi bên đang xoay quanh *{kw_str}*, cần sự thấu hiểu và lắng nghe."
            else:
                return f"Xu hướng gắn kết sắp tới sẽ mở ra dựa trên *{kw_str}*."
        elif is_career:
            if pos_name == "Quá khứ":
                return f"Kinh nghiệm và dấu ấn sự nghiệp trước đây được xây dựng từ *{kw_str}*."
            elif pos_name == "Hiện tại":
                return f"Nhiệm vụ then chốt trong công việc hiện giờ là làm chủ *{kw_str}*."
            else:
                return f"Bước tiến sự nghiệp tiếp theo phụ thuộc vào việc bạn khai thác *{kw_str}*."
        else:
            if pos_name == "Quá khứ":
                return f"Trải nghiệm tích lũy trước đây tạo dựng nền móng dựa trên *{kw_str}*."
            elif pos_name == "Hiện tại":
                return f"Trạng thái năng lượng hiện tại phản ánh trực diện qua *{kw_str}*."
            else:
                return f"Triển vọng tương lai hướng tới sự chuyển hóa cùng *{kw_str}*."

    # 3. Trả lời trực diện vào câu hỏi (Direct Answer)
    if user_q:
        if is_timing or (is_financial and is_timing):
            direct_answer = (
                f"Dựa trên sự hội tụ của 3 lá bài ({past.card.name_vi}, {present.card.name_vi}, {future.card.name_vi}), "
                f"câu trả lời cho câu hỏi *\"{user_q}\"* là: Cột mốc này **không đến từ may rủi ngẫu nhiên**, mà gắn liền mật thiết với "
                f"giai đoạn bạn hoàn thiện được năng lực làm chủ của **{present.card.name_vi}** và kiểm soát tốt "
                f"{'sự nôn nóng, phân tán năng lượng' if future.is_reversed else 'nguồn lực hành động'} của **{future.card.name_vi}**. "
                f"Dòng bài cho thấy bạn có nền tảng tiềm năng vững chắc, và kết quả tài chính này sẽ hiện thực hóa rõ nét nhất "
                f"vào thời điểm bạn đạt độ chín muồi trong chuyên môn/sự nghiệp, khi mọi quyết định được dẫn dắt bởi sự kỷ luật và chiến lược sắc bén."
            )
        elif is_financial:
            direct_answer = (
                f"Về phương diện tài chính: Dòng năng lượng chuyển giao từ **{past.card.name_vi}** sang **{present.card.name_vi}** "
                f"cho thấy cơ hội gia tăng thu nhập và tích lũy là rất rõ ràng. "
                f"{'Tuy nhiên, lá tương lai cảnh báo bạn cần thận trọng với việc đốt cháy giai đoạn hoặc chi tiêu cảm tính.' if future.is_reversed else 'Tương lai mở ra sự hanh thông vượt bậc nếu bạn kiên định bám sát kế hoạch hiện tại.'}"
            )
        elif is_love:
            direct_answer = (
                f"Về mối quan hệ của bạn: Khúc mắc hiện tại xoay quanh sự tương tác giữa **{present.card.name_vi}** và **{future.card.name_vi}**. "
                f"{'Để tình cảm đi lên, bạn cần chủ động cởi bỏ sự nghi ngại và học cách thấu hiểu cảm xúc đối phương.' if present.is_reversed or future.is_reversed else 'Năng lượng đôi bên đang có sự đồng điệu tốt, việc cởi mở chia sẻ chân thành sẽ là chìa khóa đưa mối quan hệ sang trang mới.'}"
            )
        elif is_career:
            direct_answer = (
                f"Về sự nghiệp và công việc: Lá bài **{present.card.name_vi}** ở hiện tại là chiếc chìa khóa quyết định. "
                f"Bạn đang đứng trước thời điểm cần khẳng định năng lực chuyên môn và đưa ra lựa chọn dứt khoát. "
                f"Khi bạn giải quyết trọn vẹn thử thách của lá hiện tại, triển vọng của **{future.card.name_vi}** sẽ tự nhiên khai mở vững vàng."
            )
        else:
            direct_answer = (
                f"Để giải đáp câu hỏi của bạn: Bức tranh toàn cảnh cho thấy vấn đề đang dịch chuyển từ bài học của **{past.card.name_vi}** "
                f"sang giai đoạn hành động thực tế của **{present.card.name_vi}**. Bạn không bị mắc kẹt, mà đang nắm giữ toàn quyền quyết định "
                f"để hướng tương lai tới kết quả tốt nhất của **{future.card.name_vi}**."
            )
    else:
        direct_answer = (
            f"Dòng chảy năng lượng tổng quan: Sự kết hợp giữa **{past.card.name_vi}**, **{present.card.name_vi}** và **{future.card.name_vi}** "
            f"khẳng định bạn đang trong chu kỳ chuyển giao quan trọng. Hãy làm chủ thực tại để mở lối cho tương lai hanh thông."
        )

    # 4. Lời khuyên hành động (Actionable Advice)
    action_advice = (
        f"Hãy tập trung xử lý bài học của **{present.card.name_vi}** ngay trong giai đoạn này: duy trì kỷ luật, giữ sự sáng suốt và "
        f"{'chậm lại một nhịp để quan sát thấu đáo, tránh hấp tấp' if future.is_reversed else 'chủ động nắm bắt cơ hội khi thời điểm đến'}."
    )

    reading = [
        f"{intro_reframing}Dưới đây là luận giải chi tiết từng lá bài và câu trả lời trọng tâm dành cho bạn:\n",
        f"🌙 **1. Quá khứ (Gốc rễ & Nền tảng) — {past.card.name_vi} [{past.orientation}]**",
        f"• *Từ khóa:* *{', '.join(kw_past[:4])}*",
        f"• *Ý nghĩa chuẩn:* {meaning_past}",
        f"• *Gắn vào câu hỏi của bạn:* {build_context_insight('Quá khứ', past, kw_past)}\n",
        
        f"☀️ **2. Hiện tại (Năng lượng & Thử thách) — {present.card.name_vi} [{present.orientation}]**",
        f"• *Từ khóa:* *{', '.join(kw_pres[:4])}*",
        f"• *Ý nghĩa chuẩn:* {meaning_pres}",
        f"• *Gắn vào câu hỏi của bạn:* {build_context_insight('Hiện tại', present, kw_pres)}\n",
        
        f"⭐ **3. Tương lai (Xu hướng & Tiềm năng) — {future.card.name_vi} [{future.orientation}]**",
        f"• *Từ khóa:* *{', '.join(kw_fut[:4])}*",
        f"• *Ý nghĩa chuẩn:* {meaning_fut}",
        f"• *Gắn vào câu hỏi của bạn:* {build_context_insight('Tương lai', future, kw_fut)}\n",
        
        f"🎯 **Trọng Tâm Trả Lời Câu Hỏi Của Bạn (Direct Answer):**",
        f"{direct_answer}\n",
        
        f"🔮 **Lời khuyên từ Vũ Trụ (Actionable Guidance):**",
        f"> *\"{action_advice}\"*\n",
        
        f"Bạn có cảm thấy thông điệp này kết nối với điều gì đang diễn ra trong cuộc sống của mình không?"
    ]
    return "\n".join(reading)


async def interpret_tarot_spread(draws: List[TarotDraw], question: Optional[str] = None) -> str:
    """
    Gọi Gemini AI với System Prompt 5 phần chuẩn mực.
    Tự động thử các model khả dụng và fallback mượt mà sang phân tích Rider-Waite khi cần.
    """
    if not GEMINI_API_KEY:
        logger.info("Chưa cấu hình GEMINI_API_KEY, chuyển sang luận giải cổ điển chuẩn bộ luật.")
        return generate_classical_reading(draws, question)

    prompt = build_tarot_prompt(draws, question)

    # Thử lần lượt các model trong danh sách ưu tiên
    checked_models = []
    for model_name in CANDIDATE_MODELS:
        if model_name in checked_models:
            continue
        checked_models.append(model_name)

        try:
            gen_config = {
                "temperature": 0.75,
                "top_p": 0.9,
                "max_output_tokens": 2048,
            }
            model = genai.GenerativeModel(
                model_name=model_name,
                system_instruction=SYSTEM_INSTRUCTION,
                generation_config=gen_config,
            )

            # Gọi API với asyncio.to_thread để tương thích 100% với REST transport
            response = await asyncio.wait_for(
                asyncio.to_thread(model.generate_content, prompt),
                timeout=20.0,
            )

            if response and response.text:
                logger.info(f"Đã nhận phản hồi thành công từ model: {model_name}")
                text = response.text.strip()
                # Đảm bảo luôn có câu hỏi chiêm nghiệm kết thúc
                closing_q = "Bạn có cảm thấy thông điệp này kết nối với điều gì đang diễn ra trong cuộc sống của mình không?"
                if closing_q not in text:
                    text = f"{text}\n\n{closing_q}"
                return text

        except asyncio.TimeoutError:
            logger.warning(f"Model {model_name} phản hồi quá lâu (>20s), thử model tiếp theo hoặc fallback.")
            continue
        except Exception as e:
            err_str = str(e)
            logger.warning(f"Lỗi khi gọi model {model_name}: {err_str[:120]}")
            if "404" in err_str or "not found" in err_str.lower() or "no longer available" in err_str.lower():
                continue
            if "429" in err_str or "quota" in err_str.lower() or "resource_exhausted" in err_str.lower():
                logger.info(f"Model {model_name} chạm giới hạn Quota, thử model tiếp theo trong danh sách...")
                continue

    # Nếu tất cả các model đều bận hoặc hết Quota: Tự động trả về luận giải cổ điển chuẩn 5 phần xoáy sâu trọng tâm
    logger.info("Kích hoạt bộ luận giải cổ điển Rider-Waite 1909 chuẩn 5 phần xoáy sâu trọng tâm câu hỏi.")
    return generate_classical_reading(draws, question)

