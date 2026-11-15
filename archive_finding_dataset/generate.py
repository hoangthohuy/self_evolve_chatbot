from openai import OpenAI
import time 
import ast
# def generate_
system_prompt = """Tạo cho tôi 1 đoạn hội thoại giữa người và salebot e-commerce tầm khoảng 2-15 câu bằng tiếng việt
Yêu cầu :
1. Giới tính,cảm xúc , background client tùy chọn
2. Để theo format json có indicate client và salebot (không được phép generate thừa gì thêm khác)
3. Có thể có thương lượng giá tiền
4. Sản phấm bất kì 
5. tầm 2-15 câu
6. Thành công bán hàng 
7. Tùy chọn cảm xúc của người mua hàng (eg. rude, pleasant, indifferent)

ví dụ format tôi cần:
{
"conversation": [
{
"speaker": "client",
"text": "Chào bạn, mình đang xem tai nghe Sony WH-1000XM5 trên web, còn hàng không ạ?"
},
{
"speaker": "salebot",
"text": "Dạ còn ạ! Bản đen và bạc đều có sẵn, giao nhanh trong ngày nếu bạn ở nội thành."
},
{
"speaker": "client",
"text": "Nghe hấp dẫn đấy. Giá hiện tại là bao nhiêu vậy? Mình thấy web để 7.990.000đ."
},
{
"speaker": "salebot",
"text": "Đúng rồi ạ, nhưng tuần này tụi mình có khuyến mãi giảm 5%, còn 7.590.000đ, tặng kèm ốp chống sốc luôn ạ."
},
{
"speaker": "client",
"text": "Ốp thì cũng được nhưng giá vẫn hơi cao. Bạn giảm thêm được không? Mình lấy ngay."
},
{
"speaker": "salebot",
"text": "Dạ để mình xin phép – được 7.400.000đ, bao ship luôn, đó là giá tốt nhất mình có thể làm ạ."
},
{
"speaker": "client",
"text": "Ok, deal! Vậy mình chốt đơn, màu đen nhé. Thanh toán chuyển khoản được không?"
},
{
"speaker": "salebot",
"text": "Dạ được ạ, mình gửi link thanh toán và mã đơn hàng qua tin nhắn riêng. Cảm ơn bạn đã ủng hộ!"
}
]
}
"""
start_time = time.time()
base_url="https://api.deepseek.com"
client = OpenAI(
    api_key='API_KEY',  # Replace with your actual API key
    base_url=base_url)

# start_time = time.time()
response = client.chat.completions.create(
    model="deepseek-v4-flash",
    messages=[
        {"role": "user", "content": system_prompt},
    ],
    stream=False,
    temperature=0.1,  # cân bằng giữa sáng tạo và chính xác (0-1)
    # reasoning_effort="low",
    extra_body={"thinking": {"type": "disabled"}},
    top_p=0.5,
)
end_time = time.time()
print(f"{end_time-start_time} seconds to generate")
print(response.choices[0].message.content)
dict_to_add=(ast.literal_eval(response.choices[0].message.content))
print(type(dict_to_add))
# try:
#         dict_to_add=(ast.literal_eval(response.choices[0].message.content))
#         if type(dict_to_add) == dict : 
#             dict_to_add["result"]="success"
#             dict_to_add["id_conversation"]
#             print(dict_to_add)
# except Exception as e: 
#         print ("error during convert the generated answer to dict")
        

# return response.choices[0].message.content