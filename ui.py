from tkinter import *
from prompting_with_cache import * 
from objection_detection_classification import * 
from style_detection import * 
from result_of_conversation_classification import * 
from improve_model import * 

tokenizer = AutoTokenizer.from_pretrained("Qualcomm-AI-Research/BamiBERT")
# GUI
root = Tk()
root.title("Chatbot")

BG_GRAY = "#ABB2B9"
BG_COLOR = "#17202A"
TEXT_COLOR = "#EAECEE"

FONT = "Helvetica 14"
FONT_BOLD = "Helvetica 13 bold"

cache_for_ongoing_conversation = []
cache_for_improve_model = []
system_prompt = """Imagine you're a vietnamese guitar salebot, response to what the client said : """ 

list_conversation_for_improve_model = []

number_of_conversations_added = 0 


# Send message to the chatbot function
def send():
    
    type_of_objection=objection_detection_classification(e.get(),tokenizer) 
    type_of_communication_style = informal_or_not(e.get(),tokenizer)
    cache_for_improve_model.append({"speaker": "client", "text" : e.get(),"label": type_of_communication_style})
    if(type_of_objection==-1):
        system_prompt = f"""Imagine you're a vietnamese guitar salesbot, response to what the client said, 
                            while adapting to the client's {id2label_style[type_of_communication_style]} 
                            communication style and the fact that the client message is {len(e.get().split())} words long : \n""" 
    else :
        system_prompt = f"""Imagine you're a vietnamese guitar salesbot and just got this type of of objection :{id2label_type_objection[type_of_objection]},
                            using this template as reference : {str(template_for_types_of_objections[id2label_type_objection[type_of_objection]])}
                            response to what the client said, while adapting to the client's {id2label_style[type_of_communication_style]} 
                            communication style and the fact that the client message is {len(e.get().split())} words long : \n"""
    
    print(system_prompt + e.get())
    send = "You -> " + e.get()
    txt.insert(END, "\n" + send)

    bot_response = response(e.get(),cache_for_ongoing_conversation,system_prompt)

    txt.insert(END, "\n" + f"Bot -> {bot_response}")

    e.delete(0, END)

    if(type_of_objection==2):
        txt.insert(END, "\n" + f"Bot -> Hard rejection")
        e.delete(0, END)
        print("Hard rejection") 
    else : 
        cache_for_improve_model.append({"speaker": "salebot", "text" : bot_response})

#end conversation function (when user wants to end the conversation, the conversation will be added to the dataset and the formal-informal classifier will be improved after n conversations)
def end_conversation() :
    global cache_for_ongoing_conversation
    global cache_for_improve_model
    global list_conversation_for_improve_model
    global number_of_conversations_added
    txt.delete(1.0, END)
    txt.insert(END, "\n" + """Bot -> Xin chào anh/chị! Em là trợ lý ảo của [Shop]. Em có thể hỗ trợ tư vấn sản phẩm và đặt hàng. Mọi thông tin em cung cấp đều được kiểm tra với kho hàng thực tế""")
    list_conversation_for_improve_model.append({"conversation":cache_for_improve_model, "label": outcome(str(cache_for_improve_model),tokenizer)})
    cache_for_ongoing_conversation = []
    cache_for_improve_model = []
    number_of_conversations_added+=1
    #after n conversations, the model will be improved with the new data
    if (number_of_conversations_added==1): #n=1 for testing purpose, can be changed to any number
        improve_model(list_conversation_for_improve_model)
        list_conversation_for_improve_model = []
        number_of_conversations_added = 0

    # print(f"list conversation : {list_conversation_for_improve_model}")
    
    # print(f"cache_for_ongoing_conversation : {cache_for_ongoing_conversation}")
    # print(f"cache_for_improve_model : {cache_for_improve_model}")
    

lable1 = Label(root, bg=BG_COLOR, fg=TEXT_COLOR, text="Welcome", font=FONT_BOLD, pady=10, width=20, height=1).grid(
    row=0)

txt = Text(root, bg=BG_COLOR, fg=TEXT_COLOR, font=FONT, width=80)
txt.grid(row=1, column=0, columnspan=3)

scrollbar = Scrollbar(txt)
scrollbar.place(relheight=1, relx=0.974)
txt.insert(END, "\n" + """Bot -> Xin chào anh/chị! Em là trợ lý ảo của [Shop]. Em có thể hỗ trợ tư vấn sản phẩm và đặt hàng. Mọi thông tin em cung cấp đều được kiểm tra với kho hàng thực tế""")
e = Entry(root, bg="#2C3E50", fg=TEXT_COLOR, font=FONT, width=55)
e.grid(row=2, column=0)


#to send the message, the user click the "Send" button 
send = Button(root, text="Send", font=FONT_BOLD, bg=BG_GRAY,
              command=send).grid(row=2, column=1)

#to end the conversation, the user click the "End conversation" button
end_conversation = Button(root, text="End conversation", font=FONT_BOLD, bg=BG_GRAY,
              command=end_conversation).grid(row=2, column=2)


root.mainloop()

