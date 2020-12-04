import sqlite3

connection = sqlite3.connect('data.db') #create a file e as our database

cursor = connection.cursor()   #curoor is response for excuting the queries

create_table = "CREATE TABLE users (id int, username text, password text)"

cursor.execute(create_table)

user = (1, 'jose', 'asdf')
insert_query = "INSERT INTO users VALUES (?, ?, ?)"
cursor.execute(insert_query, user)


users = [
    (2, 'rolf', 'asdf'),
    (3, 'anne', 'xyz'),
]

cursor.executemany(insert_query, users)

select_query = "SELECT * FROM users"
# print(cursor.execute(select_query))
for row in cursor.execute(select_query):
    print(row)

connection.commit()   # save changes
 
connection.close()