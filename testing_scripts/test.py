import random
import json


# with open('dataset.json',"r") as f :
#     txt= f.read()
#     new_txt = txt[:-1]
# with open('dataset.json',"w") as f:
#     f.write(new_txt)
#     f.write(",")

# with open('dataset1.json',"r") as f:
#     new_txt1= f.read()
# with open('dataset.json',"a") as f:
#     f.write(new_txt1)
      


# random.shuffle(ds)

# with open('list_of_conversation.json', 'w') as f:
#     f.write(str(ds))


with open('list_of_conversation.json', 'r') as f:
    ds  = json.load(f)
print(ds[1999]["id_conversation"])
for i in range(len(ds)):
    if ds [i]["id_conversation"] == 0:
        print(i)

for i in range(1141,len(ds)):
    ds [i]["id_conversation"] += 1141

print(ds[1999]["id_conversation"])

with open("list_of_conversation1.json" , "w") as f : 
    json.dump((ds),f)
