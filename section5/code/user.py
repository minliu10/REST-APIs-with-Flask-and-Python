import sqlite3

class User:
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password
    
   
    def find_by_username(self, username): 
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE username=?"
        result = cursor.execute(query, (username,))  # gotta use tuple and (username, ) is the way for one parameter

        row = result.fetchone() # fetch only the first row of the result set

        if row:  # == if row is not None
            user = User(row[0], row[1], row[2])  
        else:
            user = None

        connection.close()
        
        return user