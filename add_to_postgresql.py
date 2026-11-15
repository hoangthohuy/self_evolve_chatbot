# Source - https://stackoverflow.com/a/59860229
# Posted by Nikolay Baranenko
# Retrieved 2026-08-11, License - CC BY-SA 4.0

import psycopg2

connection = psycopg2.connect(database="mydatabase_chatbotsale", user='huy', password='123', host="172.18.0.2", port=5432)

cursor = connection.cursor()

def add_to_database(new_conversations_list) : 
    for c in new_conversations_list : 
        sql_context =f"""
        INSERT INTO formal_informal (text,label)
        VALUES ('{c["text"]}',{c["label"]});
        """


        cursor.execute(sql_context)
        connection.commit()







# for i in record :
#     print("Data from Database:- ", i)
#     print(type(i))

