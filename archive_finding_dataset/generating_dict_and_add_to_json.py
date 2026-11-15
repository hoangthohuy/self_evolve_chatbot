import json
import time 
import prompting_with_no_cache 
import ast

def generating_and_add_to_new_json(system_prompt,data_to_handle,path_json,continue_from_old_json,changing_function): 
    ds = data_to_handle
    #begin the json with an opening bracket to indicate the start of a list
    if continue_from_old_json == False :
        with open(path_json, 'a') as f:
            f.write("[")
    else : 
        with open(path_json,"r") as f :
            txt= f.read()
            new_txt = txt[:-1]
        with open(path_json,"w") as f:
            f.write(new_txt)
            f.write(",")   

    number_of_translations = len(ds)
    #save the indices of the translations that are not valid to be able to translate them again later
    list_index_invalid_translation = [] 
    start_time = time.time()
    with open(path_json, 'a') as f:
        for i in range(number_of_translations):
            print("start1")
            #translate the dialouge
            try : 
                result=((changing_function(ds[i],system_prompt)))
            except Exception as e:
                print(f"An error occurred: {e} at translation of index {i}, please try again from index {i}")
                f.write("]")  # Ensure the JSON list is properly closed even if an error occurs
                break
            #check if the result is a str and update the ds
            
            try :     
                if(ast.literal_eval(result))==dict:
                    print("The response is a list.")
                    ds[i]=ast.literal_eval(result)
                    print(f"Translation of index {i} is valid and updated in the ds.")
            except Exception as e:
                print(f"The response of index {i} has an error {e}, please check the response content: ")
                list_index_invalid_translation.append(i)
            f.write(json.dumps(ds[i]))
            f.write(",")
    end_time = time.time()
    #this block of code deletes the last comma and replace it with a close bracket to close the json list              
    with open(path_json,"r") as f :
        txt= f.read()
        new_txt = txt[:-1]
    with open(path_json,"w") as f:
        f.write(new_txt)
        f.write("]")                
                

    print(f"List of indices with invalid translations: {list_index_invalid_translation}")
    print(f"Time to translate the database : {end_time-start_time}")






