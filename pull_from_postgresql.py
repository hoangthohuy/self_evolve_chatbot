# Source - https://stackoverflow.com/a/59860229
# Posted by Nikolay Baranenko
# Retrieved 2026-08-11, License - CC BY-SA 4.0

import psycopg2

connection = psycopg2.connect(database="mydatabase_chatbotsale", user='huy', password='123', host="172.18.0.2", port=5432)

cursor = connection.cursor()

def choose_random_from_database(num_of_row):
    sql_context =f"""
    SELECT * FROM formal_informal ORDER BY RANDOM()
    LIMIT {num_of_row}
    """


    cursor.execute(sql_context)

    # Fetch all rows from database
    record = cursor.fetchall()

    return((record))

# print(choose_random_from_database(10)) 



# for i in record :
#     print("Data from Database:- ", i)
#     print(type(i))

