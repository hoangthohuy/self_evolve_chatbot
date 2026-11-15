import json
import prompting_with_no_cache
import random
from archive_finding_dataset.generating_dict_and_add_to_json import *
# with open('datasets/dataset_for_adding_lable_for_intent_classification.json', 'r') as f:
#     ds = json.load(f)


# unique_labels = set()    
# groups_of_sentences_with_same_label = {}


# for sentence in ds : 
#     unique_labels.add(sentence['label'])
#     if sentence['label'] not in groups_of_sentences_with_same_label :
#         groups_of_sentences_with_same_label[sentence['label']] = []
#     groups_of_sentences_with_same_label[sentence["label"]].append(sentence)


# # print(groups_of_sentences_with_same_label["refuse_to_buy"])


# # print(prompting_with_no_cache.response(sentence,system_prompt))

# print(106-len(groups_of_sentences_with_same_label["place_order"]))

# for label in unique_labels : 
#     data_to_handle = [] 
#     for i in range(106-len(groups_of_sentences_with_same_label[label])):
#         sentence = random.choice(groups_of_sentences_with_same_label[label])
#         data_to_handle.append(sentence)
#     system_prompt = f"""
#     Viết {106-len(groups_of_sentences_with_same_label[label])} câu MỚI khác nhau, cùng nhãn với câu gốc bên dưới. 
#     {106-len(groups_of_sentences_with_same_label[label])} câu này phải khác nhau rõ rệt về cấu trúc, độ dài, văn phong — 
#     không câu nào được giống câu khác về cách diễn đạt.

#     Trả về JSON list gồm {106-len(groups_of_sentences_with_same_label[label])} dict, mỗi dict cùng format với câu gốc."""

#     print(data_to_handle)
#     result = prompting_with_no_cache.response(system_prompt,str(data_to_handle))
#     print(result)
#     with open(f'{label}.json','w') as f :
#         f.write(str(result))



# random.shuffle(data_to_handle)

# print("start0")

# generating_and_add_to_new_json(system_prompt=system_prompt,data_to_handle=data_to_handle,
#                                path_json="datasets/dataset_for_adding_lable_for_intent_classification.json",
#                                continue_from_old_json=True,changing_function=prompting_with_no_cache.response)


with open("ask_for_sale.json","r") as f:
    ds1 = json.load(f)

with open("ask_info.json","r") as f:
    ds2 = json.load(f)

with open("place_order.json","r") as f:
    ds3 = json.load(f)

with open("refuse_to_buy.json","r") as f:
    ds4 = json.load(f)      

with open('datasets/dataset_for_adding_lable_for_intent_classification.json', 'r') as f:
    ds5 = json.load(f)

ds = ds1+ds2+ds3+ds4+ds5

random.shuffle(ds)

with open('test.json', 'w') as f:
    f.write(str(ds))

    

