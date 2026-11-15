from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification
import torch
list_label = [
	{"label":"false"},
	{"label":"true"},
]
id2label_label = {i:label['label'] for i, label in enumerate(list_label)}
label2id_label = {label['label']:i for i, label in enumerate(list_label)}

model_objection_detection = AutoModelForSequenceClassification.from_pretrained(
    "./models/objection_detection/checkpoint-24",
    num_labels=2,
    id2label=id2label_label,
    label2id=label2id_label,
)

list_type_objection = [
	{"type_objection":"Delivery concern"},
	{"type_objection":"Not ready"},
    {"type_objection":"Hard rejection"},
	{"type_objection":"Price objection"},
    {"type_objection":"Quality skepticism"},
	{"type_objection": "Trust deficit"}
]
id2label_type_objection = {i:type_objection['type_objection'] for i, type_objection in enumerate(list_type_objection)}
label2id_type_objection = {type_objection['type_objection']:i for i, type_objection in enumerate(list_type_objection)}

model_objection_classification = AutoModelForSequenceClassification.from_pretrained(
    "./models/objection_classification/checkpoint-84",
    num_labels=len(list_type_objection),
    id2label=id2label_type_objection,
    label2id=id2label_type_objection,
)


template_for_types_of_objections = {
  # Price objection - Khách hàng phản đối về giá
    "Price objection":
    [
      "Dạ vâng, em hiểu giá hơi cao so với dự định. Nhưng sản phẩm này có chất lượng rất tốt, em có thể hỗ trợ thêm ưu đãi nhỏ cho anh/chị nếu mua hôm nay ạ.",
      "Anh/chị thấy giá cao đúng không ạ? Thực ra sản phẩm này đi kèm bảo hành 2 năm và nhiều phụ kiện, nên tính ra rất hợp lý đó ạ. Em có thể giảm thêm 5% cho anh/chị.",
      "Giá này là giá tốt nhất rồi anh/chị ơi. Nhưng nếu anh/chị mua combo 2 sản phẩm thì em xin giảm thêm 10% ạ.",
      "Dạ em hiểu, ai cũng muốn giá tốt. Nhưng sản phẩm này em đảm bảo giá trị sử dụng lâu dài, không lo hỏng hóc. Em có thể hỗ trợ trả góp 0% cho anh/chị.",
      "Anh/chị thấy hơi đắt đúng không? Em xin phép so sánh với sản phẩm cùng phân khúc để anh/chị thấy đây là giá tốt nhất thị trường ạ."
    ],
  

  # Quality skepticism - Khách hàng nghi ngờ về chất lượng

    "Quality skepticism":
    [
      "Dạ anh/chị yên tâm, sản phẩm được làm từ nguyên liệu cao cấp, có giấy kiểm định chất lượng rõ ràng. Em có thể gửi ảnh thực tế và video review cho anh/chị xem ạ.",
      "Em hiểu lo lắng của anh/chị vì mua online không thấy hàng thật. Em xin cam kết hàng 100% giống mô tả, shop có chính sách đổi trả trong 7 ngày nếu không ưng ý ạ.",
      "Dạ sản phẩm này được rất nhiều khách hàng đánh giá tốt, anh/chị có thể xem review trên fanpage của shop. Em gửi link cho anh/chị tham khảo nhé.",
      "Anh/chị đừng lo về chất lượng ạ. Shop chúng em nhập hàng trực tiếp từ nhà sản xuất, có đầy đủ chứng từ. Nếu có vấn đề gì, shop chịu trách nhiệm hoàn toàn.",
      "Dạ em khuyên anh/chị dùng thử trước khi mua nếu có điều kiện. Hoặc em có thể gửi mẫu thử để anh/chị kiểm tra chất lượng thực tế ạ."
    ],


  # Trust deficit - Khách hàng thiếu niềm tin
    "Trust deficit":
    [
      "Dạ em hiểu anh/chị lo lắng về hàng giả hàng nhái. Shop em có giấy phép kinh doanh và là đại lý chính thức của thương hiệu, có hóa đơn VAT rõ ràng ạ.",
      "Anh/chị yên tâm, shop em đã hoạt động 5 năm, có giấy chứng nhận uy tín từ Sở Công Thương. Em gửi ảnh giấy tờ cho anh/chị kiểm tra nhé.",
      "Dạ shop có chính sách thanh toán COD để anh/chị kiểm tra hàng trước khi trả tiền. Nếu không ưng ý, anh/chị có thể từ chối nhận hàng ạ.",
      "Anh/chị có thể tham khảo đánh giá từ các khách hàng trước trên các trang mạng xã hội. Shop em có đánh giá 4.9/5 từ hơn 1000 khách hàng ạ.",
      "Dạ em xin cam kết bằng văn bản về nguồn gốc sản phẩm. Nếu phát hiện hàng giả, shop xin bồi thường gấp đôi số tiền ạ."
    ],


  # Delivery concern - Khách hàng lo lắng về giao hàng

    "Delivery concern":
    [
      "Dạ anh/chị yên tâm, shop hợp tác với đơn vị vận chuyển uy tín, hàng được đóng gói cẩn thận và giao đúng hẹn. Em sẽ gửi mã vận đơn để theo dõi ạ.",
      "Nếu anh/chị cần gấp, shop có thể hỗ trợ ship hỏa tốc trong ngày với chi phí hợp lý. Anh/chị cần nhận trước mấy giờ ạ?",
      "Dạ shop em giao hàng miễn phí nội thành, ngoại tỉnh mất 2-3 ngày tùy khoảng cách. Em sẽ cập nhật trạng thái đơn hàng liên tục cho anh/chị.",
      "Anh/chị đừng lo về việc hàng bị trầy xước. Shop đóng gói bằng túi chống sốc và thùng carton dày. Nếu hàng bị lỗi do vận chuyển, shop sẽ đổi mới 100% ạ.",
      "Dạ em xin hỗ trợ giao hàng tận tay với thời gian linh hoạt theo yêu cầu của anh/chị. Anh/chị có thể chọn khung giờ nhận hàng mong muốn ạ."
    ],


  # Not ready - Khách hàng chưa sẵn sàng quyết định

    "Not ready":
    [
      "Dạ anh/chị cứ suy nghĩ thêm, em không ép ạ. Em gửi thêm một số thông tin và hình ảnh chi tiết để anh/chị tham khảo, có gì liên hệ lại em nhé.",
      "Em hiểu ạ, mua sắm cũng cần cân nhắc. Anh/chị có thể tham khảo thêm, em sẽ giữ sản phẩm này lại 3 ngày cho anh/chị.",
      "Dạ không sao ạ, anh/chị cứ về hỏi ý kiến gia đình hoặc bạn bè. Em sẵn sàng hỗ trợ bất cứ lúc nào ạ.",
      "Anh/chị cần thêm thông tin gì về sản phẩm không? Em sẵn sàng giải đáp để anh/chị có cơ sở quyết định ạ.",
      "Dạ vâng, em xin gửi kèm bảng so sánh sản phẩm và các review để anh/chị tiện tham khảo. Khi nào anh/chị quyết định thì liên hệ em nhé."
    ],


  # Hard rejection - Khách hàng từ chối thẳng
    "Hard rejection":
    [
      "Dạ vâng, em xin cảm ơn anh/chị đã quan tâm đến sản phẩm của shop ạ. Chúc anh/chị tìm được sản phẩm ưng ý, nếu sau này cần gì cứ liên hệ em nhé.",
      "Không sao ạ, em tôn trọng quyết định của anh/chị. Shop em vẫn luôn sẵn sàng chào đón anh/chị quay lại bất cứ lúc nào ạ.",
      "Dạ em cảm ơn anh/chị đã dành thời gian. Hy vọng lần sau shop có sản phẩm phù hợp hơn với nhu cầu của anh/chị ạ.",
      "Vâng ạ, nếu anh/chị không ưng thì thôi ạ. Em xin cảm ơn và chúc anh/chị một ngày tốt lành ạ.",
      "Dạ không sao đâu ạ, mua bán là do duyên. Em vẫn sẵn sàng hỗ trợ anh/chị khi cần thông tin về sản phẩm nhé."
    ]
}


def objection_detection_classification(text,tokenizer):

    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding="max_length", max_length=256)
    with torch.no_grad():
        outputs = model_objection_detection(**inputs)

    logits = outputs.logits          # [1, num_labels]
    predicted_objection_or_not = logits.argmax(dim=-1).item()

    if(predicted_objection_or_not==1): 

        with torch.no_grad():
            outputs = model_objection_classification(**inputs)

        logits = outputs.logits          # [1, num_labels]
        predicted_type_of_objection = logits.argmax(dim=-1).item()
    else : 
        predicted_type_of_objection = -1



    # print(predicted_objection_or_not)
    # print(predicted_type_of_objection)

    return predicted_type_of_objection

