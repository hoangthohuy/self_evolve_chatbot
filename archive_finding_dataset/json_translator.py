import json
import time 
import prompting_with_no_cache as translation
import ast
system_prompt = """Translate the following sentence into natural-sounding Vietnamese, using conversational language typical of sales/price negotiation on e-commerce platforms.
    Requirements:
    1. Translate naturally, avoiding a rigid word-for-word translation.
    2. Change place names, brand names, and currencies to suit the Vietnamese context if necessary (e.g., USD -> VND, English store name -> Vietnamese store name).
    3. Retain the speaker's emotions and nuances (hesitation, anger, agreement, etc.).
    """ 

with open('bitext_training_set.json', 'r') as f:
    ds = json.load(f)
#begin the json with an opening bracket to indicate the start of a list
with open('bitext_training_set_translated.json', 'a') as f:
    f.write("[")

number_of_translations = len(ds)
#save the indices of the translations that are not valid to be able to translate them again later
list_index_invalid_translation = [] 
start_time = time.time()
with open('bitext_training_set_translated.json', 'a') as f:
    for i in range(number_of_translations):
        
            #translate the dialouge
            try : 
                result=((translation.response(ds[i]["instruction"],system_prompt)))
            except Exception as e:
                print(f"An error occurred: {e} at translation of index {i}, please try again from index {i}")
                f.write("]")  # Ensure the JSON list is properly closed even if an error occurs
                break
            #check if the result is a str and update the ds
            try :     
                if(type(result))==str:
                    # print("The response is a list.")
                    ds[i]["instruction"]=result
                    print(f"Translation of index {i} is valid and updated in the ds.")
            except Exception as e:
                print(f"The response of index {i} has an error {e}, please check the response content: ")
                list_index_invalid_translation.append(i)
            f.write(json.dumps(ds[i]))
            f.write(",")
end_time = time.time()
#this block of code deletes the last comma and replace it with a close bracket to close the json list              
with open('bitext_training_set_translated.json',"r") as f :
    txt= f.read()
    new_txt = txt[:-1]
with open('bitext_training_set_translated.json',"w") as f:
    f.write(new_txt)
    f.write("]")                
            

print(f"List of indices with invalid translations: {list_index_invalid_translation}")
print(f"Time to translate the database : {end_time-start_time}")






