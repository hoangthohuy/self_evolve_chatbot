# from datasets import load_dataset
import json

# ds = load_dataset("stanfordnlp/craigslist_bargains", revision="refs/convert/parquet")
# with open("craigslist_bargains_train.parquet", "wb") as f:
#     ds["train"].to_parquet(f)
# with open("craigslist_bargains_validation.parquet", "wb") as f:
#     ds["validation"].to_parquet(f)
# with open("craigslist_bargains_test.parquet", "wb") as f:
#     ds["test"].to_parquet(f)

# train_ds = load_dataset("parquet", data_files="craigslist_bargains_train.parquet")

# with open("craigslist_bargains_train.json", "w") as f:
#     f.write(str(train_ds))
# import sys; import pandas as pd;

# pd.read_parquet("craigslist_bargains_test.parquet").to_json("craigslist_bargains_test.json", orient='records')

# with open('test.json', 'a') as f:
#     f.write("]")  # Initialize the file with an empty list

# length_not_ok =[]
# with open('test.json', 'r') as f:
#     ds = json.load(f)
#     i=0
#     for data in ds:
#         length_ok = (len(data["utterance"]) == len(data["agent_turn"]))
#         length_not_ok.append(i)
#         i+=1
# print(f"List of indices with invalid translations: {length_not_ok}")
        


# with open("test.json","r") as f :
#     txt= f.read()
#     new_txt = txt[:-1]
# with open("test.json","w") as f:
#     f.write(new_txt)
#     f.write("]")
import random
print(random.randint(1,2))
