import json
import time 
import archive_finding_dataset.translation as translation
import ast

with open('craigslist_bargains_test.json', 'r') as f:
    ds = json.load(f)
#begin the json with an opening bracket to indicate the start of a list
with open('test.json', 'a') as f:
    f.write("[")

number_of_translations = len(ds)
#save the indices of the translations that are not valid to be able to translate them again later
list_index_invalid_translation = [] 
with open('test.json', 'a') as f:
    for i in range(number_of_translations):
        
            #translate the dialouge
            try : 
                result=(ast.literal_eval(translation.translate_dialouge(ds[i]["utterance"])))
            except Exception as e:
                print(f"An error occurred: {e} at translation of index {i}, please try again from index {i}")
                f.write("]")  # Ensure the JSON list is properly closed even if an error occurs
                break
            #check if the result is a list and update the ds
            try :     
                if(type(result))==list:
                    # print("The response is a list.")
                    ds[i]["utterance"]=result
                    print(f"Translation of index {i} is valid and updated in the ds.")
            except Exception as e:
                print(f"The response of index {i} has an error {e}, please check the response content: ")
                list_index_invalid_translation.append(i)
            f.write(json.dumps(ds[i]))
            if i < number_of_translations - 1:  # Add a comma after each item except the last one
                f.write(",")
            else:
                #end the json with a closing bracket to indicate the end of a list
                f.write("]")
                break
            
            
    


print(f"List of indices with invalid translations: {list_index_invalid_translation}")







