# Please install OpenAI SDK first: `pip3 install openai`
import ast
import json
import os
from openai import OpenAI
import time 



def response(dialouge,cache,system_prompt):
    text_to_translate = str(dialouge)
    # print("Input text:", text_to_translate )
    
    prompt = system_prompt + text_to_translate

    base_url="https://api.deepseek.com"
    client = OpenAI(
        api_key='API_KEY',  # Replace with your actual API key
        base_url=base_url)
    cache.append({"role": "user", "content": prompt})
    # start_time = time.time()
    response = client.chat.completions.create(
        model="deepseek-v4-flash",
        messages=cache,
        stream=False,
        temperature=0.1,  # cân bằng giữa sáng tạo và chính xác (0-1)
        # reasoning_effort="low",
        extra_body={"thinking": {"type": "disabled"}},
        top_p=0.5,
    )
    # end_time = time.time()
    cache.append({"role": "assistant", "content": response.choices[0].message.content})
    # print(f"Time taken for translation: {end_time - start_time} seconds")
    

    return response.choices[0].message.content


# print(translate_dialouge("Firstly, I truly understand how important the reimbursement of {{Currency Symbol}}{{Refund Amount}} is for you. Every dollar counts, and we’re here to ensure your satisfaction. Let me promptly check the status of your refund. While I'm retrieving that information, may I ask if you have any additional details or documentation related to the reimbursement? Your insights will enhance our understanding and assist in resolving this matter efficiently. Thank you for your patience and trust in our commitment to resolving this matter swiftly."))