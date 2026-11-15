# Please install OpenAI SDK first: `pip3 install openai`
import ast
import os
from openai import OpenAI
import time 
user_prompt = """Translate the following dialogue into natural-sounding Vietnamese, using conversational language typical of sales/price negotiation on e-commerce platforms.
Requirements:
1. Translate naturally, avoiding a rigid word-for-word translation.
2. Change place names, brand names, and currencies to suit the Vietnamese context if necessary (e.g., USD -> VND, English store name -> Vietnamese store name).
3. Retain the speaker's emotions and nuances (hesitation, anger, agreement, etc.).
4. Maintain the correct sentence number, format (like a python list), and order of the dialogue (even if a sentence is have the length of 0).
[ "hi I am intereste din the bike", "Awesome! Please hold for a moment while I complete a sale.", "I have a limited budget and not a lot of time... I wanted to make an offer of 850", "I understand - I am ready to work with you on this. As you know, this is a quality bike and well worth the asking price, however there is some room for negotiation.", "so what do you think of 850", "I can come down some - I would take $1000.", "what about 900?", "Meet in the middle? 950?", "okay , a bit more than I WANTED TO PAY BUT SEEMS REASONABLE. sorry for the caps, lol.", "", … ]"""

base_url="https://api.deepseek.com"
client = OpenAI(
    api_key='API_KEY',  # Replace with your actual API key
    base_url=base_url)

start_time = time.time()
response = client.chat.completions.create(
    model="deepseek-v4-flash",
    messages=[
        {"role": "user", "content": user_prompt},
    ],
    stream=False,
    temperature=0.1,  # cân bằng giữa sáng tạo và chính xác (0-1)
    # reasoning_effort="low",
    extra_body={"thinking": {"type": "disabled"}},
    top_p=0.5,
)
end_time = time.time()
print(f"Time taken for translation: {end_time - start_time} seconds")
try :     
    if(type((ast.literal_eval(response.choices[0].message.content))))==list:
        print("The response is a list.")
except Exception as e:
    print(f"The response has an error {e}, please check the response content: ")

print(response.choices[0].message.content)

