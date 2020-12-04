import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

# int or Interger is the same in sqlite but if wanna autoincrement column , you have to use Integer
create_table = "CREATE TABLE IF NOT EXISTS users (id Integer PRIMARY KEY, username text, password text)"
cursor.execute(create_table)

connection.commit()

connection.close()