# Please install OpenAI SDK first: `pip3 install openai`
import ast
import json
import os
from openai import OpenAI
import time 


def translate_dialouge(dialouge):
    text_to_translate = str(dialouge)
    # print("Input text:", text_to_translate )
    system_prompt = """Translate the following sentence into natural-sounding Vietnamese, using conversational language typical of sales/price negotiation on e-commerce platforms.
    Requirements:
    1. Translate naturally, avoiding a rigid word-for-word translation.
    2. Change place names, brand names, and currencies to suit the Vietnamese context if necessary (e.g., USD -> VND, English store name -> Vietnamese store name).
    3. Retain the speaker's emotions and nuances (hesitation, anger, agreement, etc.).
    """ 
    prompt = system_prompt + text_to_translate

    base_url="https://api.deepseek.com"
    client = OpenAI(
        api_key='API_KEY',  # Replace with your actual API key  
        base_url=base_url)

    start_time = time.time()
    response = client.chat.completions.create(
        model="deepseek-v4-flash",
        messages=[
            {"role": "user", "content": prompt},
        ],
        stream=False,
        temperature=0.1,  # cân bằng giữa sáng tạo và chính xác (0-1)
        # reasoning_effort="low",
        extra_body={"thinking": {"type": "disabled"}},
        top_p=0.5,
    )
    end_time = time.time()

    print(f"Time taken for translation: {end_time - start_time} seconds")
    

    return response.choices[0].message.content


print(translate_dialouge("Firstly, I truly understand how important the reimbursement of {{Currency Symbol}}{{Refund Amount}} is for you. Every dollar counts, and we’re here to ensure your satisfaction. Let me promptly check the status of your refund. While I'm retrieving that information, may I ask if you have any additional details or documentation related to the reimbursement? Your insights will enhance our understanding and assist in resolving this matter efficiently. Thank you for your patience and trust in our commitment to resolving this matter swiftly."))