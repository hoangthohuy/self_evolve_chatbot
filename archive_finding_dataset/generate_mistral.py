from openai import OpenAI
import time 
import ast
import json
import random
import os
from mistralai.client import Mistral
client = Mistral(api_key=os.environ["MISTRAL_API_KEY"])
system_prompt_fail = """Tạo cho tôi 1 đoạn hội thoại giữa người và salebot e-commerce tầm khoảng 2-15 câu bằng tiếng việt
    Yêu cầu :
    1. Giới tính,cảm xúc, background client tùy chọn và đa dạng
    2. Generate theo format json có indicate client và salebot (không được phép generate thừa gì thêm khác)
    3. Có thể có thương lượng giá tiền
    4. Sản phấm bất kì 
    5. Tầm 2-15 câu
    6. Thất bại bán hàng 

    format tôi cần:
    {
    "conversation": [
    {
    "speaker": "client",
    "text": "Chào bạn, mình đang xem tai nghe Sony WH-1000XM5 trên web, còn hàng không ạ?"
    },
    {
    "speaker": "salebot",
    "text": "Dạ còn ạ! Bản đen và bạc đều có sẵn, giao nhanh trong ngày nếu bạn ở nội thành."
    }
    ]
    }

    """
system_prompt_success = """Tạo cho tôi 1 đoạn hội thoại giữa người và salebot e-commerce tầm khoảng 2-15 câu bằng tiếng việt
    Yêu cầu :
    1. Giới tính,cảm xúc, background client tùy chọn và đa dạng
    2. Generate theo format json có indicate client và salebot (không được phép generate thừa gì thêm khác)
    3. Có thể có thương lượng giá tiền
    4. Sản phấm bất kì 
    5. Tầm 2-15 câu
    6. Thành công bán hàng 

    format tôi cần:
    {
    "conversation": [
    {
    "speaker": "client",
    "text": "Chào bạn, mình đang xem tai nghe Sony WH-1000XM5 trên web, còn hàng không ạ?"
    },
    {
    "speaker": "salebot",
    "text": "Dạ còn ạ! Bản đen và bạc đều có sẵn, giao nhanh trong ngày nếu bạn ở nội thành."
    }
    ]
    }

    """

def generate():
    fail_or_success = random.randint(1,2)
    system_prompt = ""
    result = ""
    if fail_or_success == 1 :
        system_prompt = system_prompt_fail
        result = "fail"
    else :
        system_prompt = system_prompt_success
        result = "successs"
    
    # start_time =time.time()
    
    response = client.chat.complete(
        model="mistral-small-latest",
        messages=[
            {
                "role": "user",
                "content": system_prompt,
            }
        ],
        temperature = 0.5,
        top_p=1
    )
    # end_time = time.time()
    # print(f"{end_time-start_time} seconds to generate" )
    # print(type(response.choices[0].message.content))
    answer = "\n".join(response.choices[0].message.content.splitlines()[1:-1])
    # print(answer)
    try:
        dict_to_add=(ast.literal_eval(answer))
        if type(dict_to_add) == dict : 
            dict_to_add["result"]=result
            return(dict_to_add)
    except Exception as e: 
        print ("error during convert the generated answer to dict")
        print (f'error {e}')
        return None

        
def run():
    start_time = time.time()
    id_counter = 0
    with open('dataset.json', 'a') as f:
        f.write("[")
        for i in range (1000):
             dict_to_write = generate()
             if dict_to_write is not None : 
                  dict_to_write["id_conversation"]=id_counter
                  id_counter+=1
                  f.write(json.dumps(dict_to_write))
                  f.write(",")
                  print(f"Successfully generate conversation {id_counter} ")
    #this block of code deletes the last comma and replace it with a close bracket to close the json list              
    with open('dataset.json',"r") as f :
        txt= f.read()
        new_txt = txt[:-1]
    with open('dataset.json',"w") as f:
        f.write(new_txt)
        f.write("]")
    end_time =time.time()    
    print(f"completed in{end_time-start_time} seconds")
run()
                


# return response.choices[0].message.content