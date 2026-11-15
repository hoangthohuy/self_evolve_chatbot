from datasets import load_dataset
import datasets
import json

# ds = load_dataset("bitext/Bitext-customer-support-llm-chatbot-training-dataset")
# with open("bitext.parquet", "wb") as f:
#     ds["train"].to_parquet(f)

# import duckdb
# sql_query = "SELECT * FROM read_parquet('bitext.parquet') order by RANDOM() LIMIT 2687;"

# df = duckdb.sql(sql_query).df()

# print(df['intent'][100])
# print(len(df))
# df.to_parquet('bitext_training_set.parquet')

# import duckdb
# sql_query = "SELECT * FROM read_parquet('bitext_training_set.parquet') LIMIT 1 ;"

# df = duckdb.sql(sql_query).df()
# df.iloc[0,2]="lol"
# # print(((df['response'][0])))
# print(type(df.iloc[0]))

# "I'm truly sorry to hear that you are facing issues and need assistance in filing a customer complaint against our business. Your feedback is highly valuable to us, and we take complaints seriously as they help us improve our products and services. To ensure a smooth and efficient process, could you please provide mewith additional details about your complaint? This will enable me to understand the situation better and guide you through the necessary steps to file your complaint. Thank you for reaching out to us, and I'm here to support you throughout this process."

# import sys; import pandas as pd;

# pd.read_parquet("bitext_training_set.parquet").to_json("bitext_training_set.json", orient='records')


with open('bitext_training_set.json', 'r') as f:
    ds = json.load(f)

print(ds[0]["instruction"])