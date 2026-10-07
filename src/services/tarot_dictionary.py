"""
Từ điển tra cứu ý nghĩa chuẩn 78 lá bài Tarot Rider-Waite-Smith (1909).
Cung cấp từ khóa, ý nghĩa chiều xuôi (Upright), chiều ngược (Reversed), nguyên tố và biểu tượng học.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass(frozen=True)
class CardMeaning:
    """Cấu trúc dữ liệu ý nghĩa từ điển của một lá bài."""
    keywords_upright: List[str]
    keywords_reversed: List[str]
    meaning_upright: str
    meaning_reversed: str
    symbolism: str
    element: str


# ==============================================================================
# BẢNG TỪ ĐIỂN 22 LÁ ẨN CHÍNH (MAJOR ARCANA)
# ==============================================================================
MAJOR_MEANINGS: Dict[str, CardMeaning] = {
    "The Fool": CardMeaning(
        keywords_upright=["Khởi đầu mới", "Ngây thơ", "Tự do", "Can đảm", "Tiềm năng vô hạn"],
        keywords_reversed=["Liều lĩnh", "Bất cẩn", "Sợ hãi rủi ro", "Thiếu suy nghĩ"],
        meaning_upright="The Fool đại diện cho bước nhảy niềm tin vào một hành trình mới toanh. Bạn đang đứng trước cơ hội với tâm hồn rộng mở, không bị ràng buộc bởi định kiến hay nỗi sợ quá khứ.",
        meaning_reversed="Nhắc nhở về sự ngây thơ quá mức dẫn đến hành động dại dột hoặc ngược lại, nỗi sợ hãi đang khiến bạn ngập ngừng không dám bước ra khỏi vùng an toàn.",
        symbolism="Chàng trai trẻ đứng mép vực với chú chó trắng cảnh báo và nhành hồng trắng biểu trưng cho sự thuần khiết.",
        element="Khí (Air) • Sao Thiên Vương (Uranus)",
    ),
    "The Magician": CardMeaning(
        keywords_upright=["Ý chí", "Kỹ năng", "Hiện thực hóa", "Hành động chủ động", "Sáng tạo"],
        keywords_reversed=["Thao túng", "Lãng phí tài năng", "Ảo tưởng", "Kế hoạch kém"],
        meaning_upright="Bạn nắm giữ đủ mọi nguồn lực và công cụ cần thiết để biến ý tưởng thành hiện thực. Đây là thời điểm vàng để tập trung năng lượng và hành động dứt khoát.",
        meaning_reversed="Cảnh báo sự lạm dụng quyền lực, thao túng người khác hoặc tài năng đang bị phân tán, chôn vùi do thiếu định hướng rõ ràng.",
        symbolism="Bàn đá bày đủ 4 biểu tượng (Gậy, Ly, Kiếm, Tiền), tay chỉ trời tay chỉ đất (Như trên sao, dưới vậy).",
        element="Khí (Air) • Sao Thủy (Mercury)",
    ),
    "The High Priestess": CardMeaning(
        keywords_upright=["Trực giác", "Bí mật", "Tiềm thức", "Tĩnh lặng", "Trí tuệ tâm linh"],
        keywords_reversed=["Bí mật bị che giấu", "Bỏ qua trực giác", "Hời hợt", "Kìm nén cảm xúc"],
        meaning_upright="Lời kêu gọi lắng nghe tiếng nói tĩnh lặng bên trong bạn. Mọi câu trả lời bạn đang tìm kiếm đều đã hiện hữu trong tiềm thức; hãy kiên nhẫn quan sát thay vì vội vã hành động.",
        meaning_reversed="Bạn đang phớt lờ trực giác của mình hoặc bị cuốn vào những tin đồn, bí mật khuất tất. Cần dành thời gian lắng đọng tâm trí.",
        symbolism="Ngồi giữa hai cột trụ B (Boaz - bóng tối) và J (Jachin - ánh sáng), cuộn giấy Torah trên tay và vương miện mặt trăng.",
        element="Nước (Water) • Mặt Trăng (Moon)",
    ),
    "The Empress": CardMeaning(
        keywords_upright=["Sinh sôi", "Nuôi dưỡng", "Trù phú", "Thiên nhiên", "Tình mẫu tử"],
        keywords_reversed=["Phụ thuộc cảm xúc", "Bế tắc sáng tạo", "Bỏ bê bản thân", "Kiểm soát"],
        meaning_upright="Biểu tượng của sự dồi dào, sinh sôi nảy nở và sáng tạo tràn đầy. Thời điểm lý tưởng để chăm sóc các dự án, tình cảm và tận hưởng vẻ đẹp cuộc sống.",
        meaning_reversed="Dấu hiệu bạn đang cho đi quá nhiều mà quên chăm sóc bản thân, hoặc sự sáng tạo đang bị nghẽn lại bởi sự gò bó.",
        symbolism="Nữ hoàng ngồi giữa cánh đồng lúa mì vàng óng và dòng thác nước, vương miện 12 ngôi sao.",
        element="Đất (Earth) • Sao Kim (Venus)",
    ),
    "The Emperor": CardMeaning(
        keywords_upright=["Kỷ luật", "Cấu trúc", "Quyền lực", "Vững chãi", "Lãnh đạo"],
        keywords_reversed=["Độc tài", "Cứng nhắc", "Mất kiểm soát", "Thiếu kỷ luật"],
        meaning_upright="Đại diện cho trật tự, lý trí và khả năng làm chủ tình thế. Bạn cần thiết lập ranh giới rõ ràng, lên kế hoạch bài bản và kiên định với mục tiêu.",
        meaning_reversed="Cảnh báo sự bảo thủ, áp đặt ý chí lên người khác hoặc ngược lại, sự thiếu kỷ luật đang làm đổ vỡ các dự định của bạn.",
        symbolism="Vị vua ngồi trên ngai vàng khắc đầu cừu đực, mặc giáp sắt và cầm quyền trượng Ankh.",
        element="Lửa (Fire) • Cung Bạch Dương (Aries)",
    ),
    "The Hierophant": CardMeaning(
        keywords_upright=["Truyền thống", "Niềm tin", "Đạo đức", "Học tập", "Người hướng dẫn"],
        keywords_reversed=["Phá vỡ quy tắc", "Bất tuân", "Giáo điều hẹp hòi", "Tự do tư tưởng"],
        meaning_upright="Đại diện cho tri thức truyền thống, tổ chức xã hội và các giá trị đạo đức bền vững. Thời điểm phù hợp để học hỏi từ người đi trước hoặc tuân theo quy chuẩn đã được kiểm chứng.",
        meaning_reversed="Khuyến khích bạn dám bước ra khỏi các quy chuẩn lỗi thời, lắng nghe la bàn đạo đức của chính mình thay vì mù quáng theo đám đông.",
        symbolism="Vị giáo hoàng ngồi trước hai tín đồ, cầm cây thánh giá ba tầng và hai chìa khóa vàng bạc bắt chéo.",
        element="Đất (Earth) • Cung Kim Ngưu (Taurus)",
    ),
    "The Lovers": CardMeaning(
        keywords_upright=["Tình yêu", "Hòa hợp", "Lựa chọn giá trị", "Gắn kết", "Đồng điệu"],
        keywords_reversed=["Mâu thuẫn", "Lựa chọn sai lầm", "Mất cân bằng", "Xung đột giá trị"],
        meaning_upright="Không chỉ là tình yêu lứa đôi nồng nàn mà còn là phép thử về sự lựa chọn đạo đức và giá trị sống. Thể hiện sự hòa hợp sâu sắc giữa hai tâm hồn.",
        meaning_reversed="Mâu thuẫn nội tâm hoặc sự bất hòa trong mối quan hệ. Cần tự hỏi liệu bạn có đang thỏa hiệp giá trị cốt lõi của mình hay không.",
        symbolism="Adam và Eva trong vườn địa đàng dưới sự chúc phúc của thiên thần Raphael, phía sau là cây tri thức và cây sự sống.",
        element="Khí (Air) • Cung Song Tử (Gemini)",
    ),
    "The Chariot": CardMeaning(
        keywords_upright=["Chiến thắng", "Ý chí sắt đá", "Tập trung", "Vượt chướng ngại", "Kiểm soát"],
        keywords_reversed=["Mất phương hướng", "Hung hăng", "Bất lực", "Áp lực đè nặng"],
        meaning_upright="Chiến thắng đạt được thông qua kỷ luật và sự làm chủ những nguồn năng lượng đối nghịch. Hãy kiên định bám sát mục tiêu, bạn sẽ về đích thành công.",
        meaning_reversed="Cảnh báo bạn đang để cảm xúc lấn át lý trí, hoặc cố gắng kiểm soát những thứ nằm ngoài tầm tay dẫn đến kiệt sức.",
        symbolism="Chiến binh trên cỗ xe được kéo bởi hai nhân sư đen và trắng kéo về hai hướng khác nhau.",
        element="Nước (Water) • Cung Cự Giải (Cancer)",
    ),
    "Strength": CardMeaning(
        keywords_upright=["Dũng cảm", "Dịu dàng", "Kiên nhẫn", "Làm chủ bản năng", "Sức mạnh nội tâm"],
        keywords_reversed=["Tự ti", "Mất kiên nhẫn", "Bản năng lấn át", "Yếu đuối"],
        meaning_upright="Sức mạnh đích thực không đến từ vũ lực bạo tàn mà đến từ sự dịu dàng, kiên định và thấu cảm. Bạn có đủ năng lượng để thuần hóa mọi 'con sư tử' thử thách.",
        meaning_reversed="Cảm giác nghi ngờ bản thân, nản lòng trước khó khăn hoặc để cơn giận dữ, bản năng chi phối hành vi.",
        symbolism="Người phụ nữ đội biểu tượng vô cực nhẹ nhàng khép hàm con sư tử hung dữ bằng vòng hoa.",
        element="Lửa (Fire) • Cung Sư Tử (Leo)",
    ),
    "The Hermit": CardMeaning(
        keywords_upright=["Chiêm nghiệm", "Tìm kiếm chân lý", "Nội tâm", "Tĩnh tại", "Khai sáng"],
        keywords_reversed=["Cô lập", "Lập dị", "Từ chối lời khuyên", "Lạc lối"],
        meaning_upright="Thời điểm cần tạm lui về không gian riêng để suy ngẫm, tự soi sáng con đường của chính mình. Sự tĩnh lặng sẽ mang lại câu trả lời sáng tỏ nhất.",
        meaning_reversed="Cảnh báo việc tự cô lập mình quá mức biến thành sự trốn tránh thực tại hoặc khép kín trái tim với thế giới bên ngoài.",
        symbolism="Vị ẩn sĩ già đứng trên đỉnh núi tuyết cầm chiếc đèn lồng chứa ngôi sao 6 cánh soi đường.",
        element="Đất (Earth) • Cung Xử Nữ (Virgo)",
    ),
    "Wheel of Fortune": CardMeaning(
        keywords_upright=["Vận may", "Chu kỳ", "Định mệnh", "Bước ngoặt", "Thay đổi tất yếu"],
        keywords_reversed=["Vận xui", "Kháng cự thay đổi", "Chu kỳ tiêu cực lặp lại"],
        meaning_upright="Bánh xe số phận đang quay, mang lại những bước ngoặt bất ngờ. Mọi thăng trầm đều là một phần tự nhiên của dòng đời; hãy linh hoạt thuận theo thời thế.",
        meaning_reversed="Thời điểm thử thách khi vận may chưa mỉm cười. Đừng cố chống lại bánh xe, hãy bình tĩnh học bài học từ nghịch cảnh để chuẩn bị cho chu kỳ mới.",
        symbolism="Bánh xe định mệnh khắc chữ TORA cùng 4 sinh vật bốn góc đại diện cho 4 chòm sao kiên định.",
        element="Lửa (Fire) • Sao Mộc (Jupiter)",
    ),
    "Justice": CardMeaning(
        keywords_upright=["Công lý", "Nhân quả", "Trung thực", "Quyết định sáng suốt", "Cân bằng"],
        keywords_reversed=["Bất công", "Thiếu trung thực", "Thiên vị", "Trốn tránh trách nhiệm"],
        meaning_upright="Mọi hành động đều mang theo hệ quả nhân quả tương xứng. Đòi hỏi bạn phải nhìn nhận sự thật khách quan, minh bạch và chịu trách nhiệm với lựa chọn của mình.",
        meaning_reversed="Cảm giác bị đối xử bất công hoặc chính bạn đang không thành thật với bản thân và người khác. Sự thật rồi sẽ phải phơi bày.",
        symbolism="Nữ thần cầm thanh kiếm công lý hướng lên trời và cán cân thăng bằng tuyệt đối.",
        element="Khí (Air) • Cung Thiên Bình (Libra)",
    ),
    "The Hanged Man": CardMeaning(
        keywords_upright=["Buông bỏ", "Góc nhìn mới", "Tạm dừng", "Hy sinh có ý nghĩa", "Giác ngộ"],
        keywords_reversed=["Bế tắc vô ích", "Kháng cự", "Trì hoãn", "Hy sinh mù quáng"],
        meaning_upright="Đôi khi lùi một bước là để tiến ba bước. Việc tạm dừng và nhìn nhận vấn đề từ một góc độ hoàn toàn ngược lại sẽ giúp bạn tìm thấy lối thoát sáng suốt.",
        meaning_reversed="Bạn đang bế tắc vì cố chấp không chịu buông bỏ điều đã không còn phù hợp, hoặc đang đóng vai nạn nhân một cách vô ích.",
        symbolism="Người đàn ông treo ngược chân vào cây chữ T sống động, đầu tỏa vầng hào quang bình thản.",
        element="Nước (Water) • Sao Hải Vương (Neptune)",
    ),
    "Death": CardMeaning(
        keywords_upright=["Kết thúc", "Tái sinh", "Chuyển hóa", "Khép lại quá khứ", "Cánh cửa mới"],
        keywords_reversed=["Sợ thay đổi", "Bám víu quá khứ", "Chậm trễ chuyển hóa", "Trì trệ"],
        meaning_upright="Không mang nghĩa đen về thể xác! Đây là sự khép lại tự nhiên của một giai đoạn cũ để mở đường cho một khởi đầu mới mẻ, tái sinh mạnh mẽ hơn.",
        meaning_reversed="Nỗi sợ hãi thay đổi đang khiến bạn bám víu vào những mối quan hệ hay công việc đã mục ruỗng. Hãy học cách buông tay.",
        symbolism="Kỵ sĩ xương trên lưng ngựa trắng mang lá cờ hoa hồng thần bí, phía chân trời mặt trời đang mọc.",
        element="Nước (Water) • Cung Bọ Cạp (Scorpio)",
    ),
    "Temperance": CardMeaning(
        keywords_upright=["Cân bằng", "Hòa hợp", "Kiên nhẫn", "Điều độ", "Chữa lành"],
        keywords_reversed=["Mất cân bằng", "Thái quá", "Nóng vội", "Xung đột nội tâm"],
        meaning_upright="Nghệ thuật dung hòa các mặt đối lập để tìm thấy điểm cân bằng hoàn hảo. Kiên nhẫn và điều độ sẽ giúp bạn chữa lành mọi vết thương và hóa giải mâu thuẫn.",
        meaning_reversed="Bạn đang đi đến những thái cực cực đoan trong cảm xúc hoặc lối sống, dẫn đến sự bất an và mệt mỏi thể chất lẫn tinh thần.",
        symbolism="Thiên thần một chân dưới nước một chân trên bờ, rót nước qua lại nhịp nhàng giữa hai chiếc cốc vàng.",
        element="Lửa (Fire) • Cung Nhân Mã (Sagittarius)",
    ),
    "The Devil": CardMeaning(
        keywords_upright=["Ràng buộc", "Nghiện ngập", "Ảo tưởng vật chất", "Cám dỗ", "Bóng tối nội tâm"],
        keywords_reversed=["Tự do", "Nhận thức tỉnh thức", "Phá vỡ xiềng xích", "Lấy lại quyền kiểm soát"],
        meaning_upright="Cảnh báo về những thói quen xấu, sự lệ thuộc độc hại hoặc nỗi sợ hãi đang giam cầm bạn. Hãy nhớ rằng sợi dây xích đeo trên cổ thực chất rất lỏng lẻo.",
        meaning_reversed="Tin vui về sự thức tỉnh! Bạn đã nhìn thấu những ảo tưởng và bắt đầu từng bước bẻ gãy xiềng xích để lấy lại tự do cho tâm hồn.",
        symbolism="Ác quỷ Baphomet ngồi trên bệ đá với hai người đàn ông và đàn bà bị xích lỏng quanh cổ.",
        element="Đất (Earth) • Cung Ma Kết (Capricorn)",
    ),
    "The Tower": CardMeaning(
        keywords_upright=["Sụp đổ bất ngờ", "Thức tỉnh đột ngột", "Giải phóng", "Đập tan ảo tưởng"],
        keywords_reversed=["Tránh được tai họa", "Nỗi sợ sụp đổ", "Trì hoãn điều tất yếu"],
        meaning_upright="Cơn bão giải phóng cần thiết! Cấu trúc giả tạo hay niềm tin sai lầm bấy lâu nay bị sụp đổ bất ngờ để bạn xây dựng lại nền móng vững chắc và chân thật hơn.",
        meaning_reversed="Bạn đang linh cảm thấy cơn khủng hoảng nhưng cố né tránh, hoặc đang chậm rãi vượt qua dư chấn của một biến cố lớn.",
        symbolism="Tòa tháp trên đỉnh núi bị sét đánh gãy vương miện, bốc cháy và hất tung hai người xuống vực.",
        element="Lửa (Fire) • Sao Hỏa (Mars)",
    ),
    "The Star": CardMeaning(
        keywords_upright=["Hy vọng", "Niềm tin", "Cảm hứng", "Bình yên", "Chữa lành sau giông bão"],
        keywords_reversed=["Mất niềm tin", "Thất vọng", "Thiếu cảm hứng", "Bế tắc tinh thần"],
        meaning_upright="Ánh sáng dịu dàng sau cơn bão! The Star mang đến niềm hy vọng tràn trề, sự tĩnh lặng và phước lành của vũ trụ. Hãy tin vào ước mơ của bạn.",
        meaning_reversed="Cảm giác bi quan tạm thời khiến bạn không nhìn thấy những phước lành đang hiện diện xung quanh. Hãy nhen nhóm lại ngọn lửa niềm tin.",
        symbolism="Thiên thần khỏa thân rót hai bình nước sự sống xuống đất và hồ nước dưới bầu trời đêm 8 ngôi sao rực rỡ.",
        element="Khí (Air) • Cung Bảo Bình (Aquarius)",
    ),
    "The Moon": CardMeaning(
        keywords_upright=["Ảo ảnh", "Bất an", "Tiềm thức", "Trực giác mông lung", "Nỗi sợ mơ hồ"],
        keywords_reversed=["Giải tỏa nỗi sợ", "Sự thật sáng tỏ", "Vượt qua hoang mang"],
        meaning_upright="Bạn đang đi trong màn sương mờ ảo của sự bất an và hoài nghi. Những bóng ma tâm lý đang phóng đại nỗi sợ; đừng đưa ra quyết định vội vàng khi chưa nhìn rõ sự thật.",
        meaning_reversed="Màn sương đang dần tan biến, ánh sáng bình minh sắp trở lại giúp bạn nhìn rõ bản chất vấn đề và giải thoát khỏi những nỗi sợ vô căn cứ.",
        symbolism="Vầng trăng nhỏ giọt sương với chó sói và chó nhà cùng sủa, con tôm từ dưới đầm lầy sâu thẳm bò lên bờ.",
        element="Nước (Water) • Cung Song Ngư (Pisces)",
    ),
    "The Sun": CardMeaning(
        keywords_upright=["Thành công", "Hân hoan", "Rạng rỡ", "Sức sống", "Chân lý sáng tỏ"],
        keywords_reversed=["Niềm vui tạm hoãn", "Lạc quan thái quá", "Mây mờ che khuất"],
        meaning_upright="Lá bài tích cực bậc nhất trong bộ Tarot! Ánh sáng mặt trời xua tan mọi tăm tối, mang đến niềm vui, sức khỏe dồi dào, thành công rực rỡ và sự tự tin trọn vẹn.",
        meaning_reversed="Ánh mặt trời vẫn ở đó nhưng bị mây mờ che phủ. Niềm vui có thể bị trì hoãn một chút nhưng năng lượng tích cực vẫn luôn đồng hành cùng bạn.",
        symbolism="Đứa trẻ trần truồng rạng rỡ cưỡi ngựa trắng dưới vầng thái dương chói lọi và cánh đồng hoa hướng dương.",
        element="Lửa (Fire) • Mặt Trời (Sun)",
    ),
    "Judgement": CardMeaning(
        keywords_upright=["Phán xét", "Tiếng gọi định mệnh", "Thức tỉnh", "Tái sinh", "Ân xá"],
        keywords_reversed=["Tự trách móc", "Nghi ngờ bản thân", "Trốn tránh tiếng gọi", "Hối hận"],
        meaning_upright="Thời khắc thức tỉnh thiêng liêng! Tiếng kèn vũ trụ vang lên gọi bạn bước sang một chương mới của cuộc đời. Đã đến lúc khép lại quá khứ và sống đúng với sứ mệnh.",
        meaning_reversed="Bạn đang chìm trong sự phán xét khắt khe với chính mình hoặc chần chừ không dám đón nhận lời mời gọi bước lên nấc thang mới.",
        symbolism="Thiên thần Gabriel thổi chiếc kèn trumpet trên mây, những người bên dưới đứng dậy khỏi quan tài với lòng tôn kính.",
        element="Lửa (Fire) • Sao Diêm Vương (Pluto)",
    ),
    "The World": CardMeaning(
        keywords_upright=["Viên mãn", "Hoàn thành", "Thành tựu lớn", "Hòa nhập", "Hành trình trọn vẹn"],
        keywords_reversed=["Chưa hoàn thành", "Dang dở", "Thiếu sót bước cuối", "Trì trệ"],
        meaning_upright="Đích đến vinh quang của chuyến hành trình chàng khờ! Bạn đã hoàn thành xuất sắc một chu kỳ lớn, đạt được sự trọn vẹn, thấu hiểu và tự do tuyệt đối.",
        meaning_reversed="Bạn đã đi rất gần đến đích nhưng vẫn còn thiếu một mảnh ghép nhỏ cuối cùng. Đừng bỏ cuộc ngay trước cánh cửa thành công.",
        symbolism="Người phụ nữ khiêu vũ trong vòng nguyệt quế xanh tươi, bốn góc là bốn tạo vật thần thánh canh giữ vũ trụ.",
        element="Đất (Earth) • Sao Thổ (Saturn)",
    ),
}


# ==============================================================================
# HÀM TRA CỨU VÀ TẠO Ý NGHĨA CHO TOÀN BỘ 78 LÁ (BAO GỒM ẨN PHỤ)
# ==============================================================================
SUIT_GENERAL: Dict[str, Dict[str, str]] = {
    "Wands": {
        "element": "Lửa (Fire) • Năng lượng, đam mê, hành động, sự nghiệp",
        "upright": "Năng lượng sáng tạo, nhiệt huyết bùng nổ, sự quyết đoán và tinh thần tiên phong.",
        "reversed": "Nóng vội, cạn kiệt năng lượng, thiếu kiên nhẫn, trì trệ hoặc bùng nổ xung đột.",
    },
    "Cups": {
        "element": "Nước (Water) • Cảm xúc, tình yêu, trực giác, mối quan hệ",
        "upright": "Tình cảm dạt dào, sự gắn kết yêu thương, trực giác sâu sắc và bình an nội tâm.",
        "reversed": "Tổn thương tình cảm, đóng kín trái tim, ảo tưởng hão huyền hoặc cảm xúc mất kiểm soát.",
    },
    "Swords": {
        "element": "Khí (Air) • Lý trí, tư duy, sự thật, thử thách tâm lý",
        "upright": "Trí tuệ sắc bén, chân lý minh bạch, quyết định dứt khoát và vượt qua thử thách lý trí.",
        "reversed": "Bất an, dằn vặt suy nghĩ, xung đột lời nói, lo âu thái quá hoặc nhìn nhận lệch lạc.",
    },
    "Pentacles": {
        "element": "Đất (Earth) • Vật chất, tiền tài, sức khỏe, sự ổn định thực tế",
        "upright": "Thịnh vượng bền vững, cơ hội tài chính, nỗ lực có kết quả và nền tảng thực tế vững chắc.",
        "reversed": "Bất ổn tài chính, tham lam, lãng phí tài nguyên hoặc thiếu tầm nhìn thực tế dài hạn.",
    },
}

MINOR_NUMBERS: Dict[str, Dict[str, str]] = {
    "Ace": {"title": "Khởi nguyên", "upright": "Hạt mầm cơ hội mới tinh khôi, tiềm năng thuần khiết mở ra.", "reversed": "Cơ hội bị bỏ lỡ, khởi đầu trắc trở hoặc thiếu động lực thực hiện."},
    "Two": {"title": "Lựa chọn & Cân bằng", "upright": "Sự cân bằng, kết hợp đối tác và định hướng lựa chọn.", "reversed": "Mất thăng bằng, xung đột ưu tiên hoặc chần chừ không dứt khoát."},
    "Three": {"title": "Phát triển & Kết nối", "upright": "Sự mở rộng, hợp tác nhóm và bước đầu gặt hái kết quả.", "reversed": "Thiếu đồng thuận, trì hoãn tiến độ hoặc kỳ vọng chưa thành."},
    "Four": {"title": "Ổn định & Nền móng", "upright": "Sự an toàn, củng cố ranh giới và trật tự vững chãi.", "reversed": "Cứng nhắc, bế tắc, đóng khung trong vùng an toàn quá mức."},
    "Five": {"title": "Thử thách & Xung đột", "upright": "Bài học từ khó khăn, xung đột và va chạm thực tế.", "reversed": "Vượt qua giông bão, hòa giải bất đồng hoặc chấp nhận buông bỏ."},
    "Six": {"title": "Hài hòa & Chuyển giao", "upright": "Sự chữa lành, chia sẻ hỗ trợ và tiến tới bến bờ bình yên.", "reversed": "Khó khăn trong thích nghi, bám víu chuyện cũ hoặc bất công."},
    "Seven": {"title": "Đánh giá & Chiêm nghiệm", "upright": "Tự suy xét, kiên nhẫn chiến lược và bảo vệ thành quả.", "reversed": "Nghi ngờ bản thân, thiếu tập trung hoặc chiến lược sai hướng."},
    "Eight": {"title": "Nỗ lực & Chuyển động", "upright": "Sự tập trung rèn luyện, tốc độ tiến triển nhanh chóng.", "reversed": "Hối hả sai lầm, kiệt sức hoặc thiếu kiên định."},
    "Nine": {"title": "Thành tựu & Đỉnh cao", "upright": "Sự tự chủ, thu hoạch viên mãn và kiên cường vượt ải cuối.", "reversed": "Mệt mỏi kiệt sức, lo âu trước đích đến hoặc tự mãn."},
    "Ten": {"title": "Hoàn tất & Chuyển biến", "upright": "Đỉnh điểm của chu kỳ, kết quả trọn vẹn của hành trình.", "reversed": "Gánh nặng quá tải, cố chấp kéo dài điều đã đến lúc kết thúc."},
    "Page": {"title": "Tiểu đồng (Người học việc)", "upright": "Tâm thế người học, tin tức mới mẻ, lòng hiếu kỳ khám phá.", "reversed": "Nông nổi, tin tức thất thiệt, thiếu chín chắn hoặc nhút nhát."},
    "Knight": {"title": "Hiệp sĩ (Hành động)", "upright": "Năng lượng tiến công, lòng quả cảm theo đuổi lý tưởng.", "reversed": "Hấp tấp, liều lĩnh, thiếu kiên nhẫn hoặc thoái lui."},
    "Queen": {"title": "Hoàng hậu (Nuôi dưỡng)", "upright": "Sự thấu hiểu nội tâm, làm chủ cảm xúc và nuôi dưỡng bền bỉ.", "reversed": "Phụ thuộc, kiểm soát cảm xúc hoặc ghen tuông, lạnh nhạt."},
    "King": {"title": "Vua (Lãnh đạo)", "upright": "Quyền lực tối cao, tầm nhìn chiến lược và sự kiểm soát trưởng thành.", "reversed": "Độc đoán, lạm quyền, bất ổn hoặc thiếu trách nhiệm."},
}


def get_card_meaning(card_name: str, suit: Optional[str] = None) -> CardMeaning:
    """Truy xuất ý nghĩa từ điển chi tiết cho bất kỳ lá bài nào trong 78 lá."""
    if card_name in MAJOR_MEANINGS:
        return MAJOR_MEANINGS[card_name]

    # Xử lý cho 56 lá Ẩn phụ (Minor Arcana)
    suit_info = SUIT_GENERAL.get(suit or "Wands", SUIT_GENERAL["Wands"])
    element_text = suit_info["element"]

    # Tách rank (Ace, Two, Three, ..., King)
    rank = card_name.split(" of ")[0] if " of " in card_name else "Ace"
    num_info = MINOR_NUMBERS.get(rank, MINOR_NUMBERS["Ace"])

    upright_text = f"{num_info['upright']} Trong lĩnh vực của bộ {suit}: {suit_info['upright']}"
    reversed_text = f"{num_info['reversed']} Cảnh báo về năng lượng bộ {suit}: {suit_info['reversed']}"

    suit_keywords = {
        "Wands": ("Hành động", "Đam mê", "Nhiệt huyết", "Ý chí"),
        "Cups": ("Cảm xúc", "Tình yêu", "Trực giác", "Gắn kết"),
        "Swords": ("Lý trí", "Trí tuệ", "Quyết đoán", "Chiến lược"),
        "Pentacles": ("Tài chính", "Thực tế", "Thịnh vượng", "Nền tảng"),
    }
    rank_keywords_upright = {
        "Ace": ("Khởi đầu mới", "Cơ hội vàng"),
        "Two": ("Cân bằng", "Lựa chọn"),
        "Three": ("Hợp tác", "Mở rộng"),
        "Four": ("Ổn định", "Nền móng"),
        "Five": ("Thử thách", "Vượt khó"),
        "Six": ("Hài hòa", "Thuận lợi"),
        "Seven": ("Chiêm nghiệm", "Kiên nhẫn"),
        "Eight": ("Rèn luyện", "Tập trung"),
        "Nine": ("Thành tựu", "Bền bỉ"),
        "Ten": ("Viên mãn", "Đỉnh cao"),
        "Page": ("Học hỏi", "Cơ hội mới"),
        "Knight": ("Tiến công", "Quyết liệt"),
        "Queen": ("Làm chủ cảm xúc", "Nuôi dưỡng"),
        "King": ("Lãnh đạo", "Tầm nhìn chiến lược"),
    }
    rank_keywords_reversed = {
        "Ace": ("Trì hoãn", "Bỏ lỡ cơ hội"),
        "Two": ("Mất thăng bằng", "Do dự"),
        "Three": ("Bất đồng", "Chậm tiến độ"),
        "Four": ("Bế tắc", "Cố chấp"),
        "Five": ("Xung đột", "Tổn thất"),
        "Six": ("Trở ngại", "Khó thích nghi"),
        "Seven": ("Nghi ngờ", "Thiếu tập trung"),
        "Eight": ("Hấp tấp", "Kiệt sức"),
        "Nine": ("Lo âu", "Mệt mỏi"),
        "Ten": ("Quá tải", "Cần buông bỏ"),
        "Page": ("Nông nổi", "Thiếu chín chắn"),
        "Knight": ("Nóng vội", "Liều lĩnh"),
        "Queen": ("Nôn nóng", "Thiếu kiên nhẫn"),
        "King": ("Cứng nhắc", "Áp lực kiểm soát"),
    }

    s_kw = suit_keywords.get(suit or "Wands", ("Năng lượng", "Thực tại", "Hành động", "Chuyển hóa"))
    r_up = rank_keywords_upright.get(rank, ("Khởi sắc", "Thuận dòng"))
    r_rev = rank_keywords_reversed.get(rank, ("Nút thắt", "Cần điều chỉnh"))

    kw_upright = [r_up[0], s_kw[0], r_up[1], s_kw[2]]
    kw_reversed = [r_rev[0], f"{s_kw[0]} bế tắc", r_rev[1], "Cần cân bằng"]

    return CardMeaning(
        keywords_upright=kw_upright,
        keywords_reversed=kw_reversed,
        meaning_upright=upright_text,
        meaning_reversed=reversed_text,
        symbolism=f"Thuộc bộ {suit} ({element_text.split(' • ')[0]}), mang phẩm chất của {num_info['title']}.",
        element=element_text,
    )
