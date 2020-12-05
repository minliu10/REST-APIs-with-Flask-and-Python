from flask import Flask
from flask_restful import Apicd
from flask_jwt import JWT, jwt_required

from security import authenticate, identity
from user import UserRegister
from item import Item, ItemList

app = Flask(__name__)
app.secret_key = 'joes'
api = Api(app)

# JWT() our app, and two functions
# create an new endpoint  /auth when we call /auth we send it a username and a password
# jwt send it to authenticate func. then generate jwt token, itself does nothing but we can
# send it to the next request we make(here is identity) jwt will call the identity func.
jwt = JWT(app, authenticate, identity)  

# to tell api this resource we created(Student) now is accessible via our API
api.add_resource(Item, '/item/<string:name>')  # http://127.0.0.1:5000/item/Rolf
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')


if __name__ == '__main__':                 # the .py file you run will be __main__
    app.run(port=5000, debug=True)