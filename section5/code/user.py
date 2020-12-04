import sqlite3
from flask_restful import Resource, reqparse
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

class UserRegister(Resource):


    parser = reqparse.RequestParser()
    parser.add_argument('username',
    type=str,
    required=True,
    help="This field canoot be blank."
    )
    parser.add_argument('password',
    type=str,
    required =True,
    help="This field connot be blank."
    )

    def post(self):
        data = UserRegister.parser.parse_args()
        
        if User.find_by_username(data['username']): # user exist
            return {'message': 'A user with that username already exists'}, 400


        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO users VALUES (NULL, ?, ?)"   # id is autoimcremented so set it Null
        cursor.execute(query, (data["username"], data['password']))

        connection.commit()
        connection.close()

        return {'message': 'User created sucessfully'}, 201