import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

# int or Interger is the same in sqlite but if wanna autoincrement column , you have to use Integer
create_table = "CREATE TABLE IF NOT EXISTS users (id Integer PRIMARY KEY, username text, password text)"
cursor.execute(create_table)

create_table = "CREATE TABLE IF NOT EXISTS items (name text, price real)" # real is a number wuth a decimal point ex 10.99

cursor.execute(create_table)


connection.commit()

connection.close()