import sqlite3

class User:
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password
    
    @classmethod
    def find_by_username(cls, username):  # without @classmethod here's self
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE username=?"
        result = cursor.execute(query, (username,))  # gotta use tuple and (username, ) is the way for one parameter

        row = result.fetchone() # fetch only the first row of the result set

        if row:  # == if row is not None
            user = cls(*row)  
            # equal user = cls(row[0], row[1], row[2])  # without @classmethod cls is User
        else:
            user = None

        connection.close()
        
        return user

    @classmethod
    def find_by_id(cls, _id):  # without @classmethod here's self
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE id=?"
        result = cursor.execute(query, (_id,))  # gotta use tuple and (username, ) is the way for one parameter

        row = result.fetchone() # fetch only the first row of the result set

        if row:  # == if row is not None
            user = cls(*row)  
            # equal user = cls(row[0], row[1], row[2])  # without @classmethod cls is User
        else:
            user = None

        connection.close()
        
        return user