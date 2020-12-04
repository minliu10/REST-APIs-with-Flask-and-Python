from flask import Flask, request
from flask_restful import Resource, Api, reqparse # reqparse不是restful的一部分
from flask_jwt import JWT, jwt_required

from security import authenticate, identity
from user import UserRegister

app = Flask(__name__)
app.secret_key = 'joes'
api = Api(app)

# JWT() our app, and two functions
# create an new endpoint  /auth when we call /auth we send it a username and a password
# jwt send it to authenticate func. then generate jwt token, itself does nothing but we can
# send it to the next request we make(here is identity) jwt will call the identity func.
jwt = JWT(app, authenticate, identity)  

items = []


class Item(Resource):
    # parser is to make sure only price passes in, nothing else is allowed
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,  #price一定要有值
        help="This field cannot be left blank!"
    )
    # def get(self, name):
    #     # for item in items:
    #     #     if item['name'] == name:
    #     #         return item # dict
    #     return {'item': None}, 404  # 404, if you don't provide it, the status will be 200 OK

    # 簡化寫法
    @jwt_required()
    def get(self, name):
        #  過濾條件, 過濾的來源  回傳的是一個filter 包next 回傳遞一個符合過濾的item 
        item = next(filter(lambda x:x['name'] == name, items), None) # 沒有半個符合的東西會丟錯, 所以加None, 沒找到就給None 
        return {'item': item}, 200 if item else 404 # 404, if you don't provide it, the status will be 200 OK



    
    # data = request.get_json() this will give an error
    # 1) the request does not attach a JSON payload
    # 2) the request does not have the proper content-type header
    # two ways to deal the situation when you're not sure if your clients use json format
    # request.get_json(here) here can put those two below 
    # force=True means you do not need the content-type header
    # silent=True means it doesn't give an error but none

    def post(self, name):
        # data = request.get_json()
        

        if next(filter(lambda x:x['name'] == name, items), None):
            return {'message':"An item with name '{}' already exists.".format(name)}, 400
        data = Item.parser.parse_args()  # for parse  擺在if next 下 因為只要錯誤發生就不做任何事
        # data = request.get_json()  # error occur
        item = {'name':name, 'price': data['price']}
        items.append(item)
        return item, 201  # 201 for created
        
    def delete(self, name):
        global items
        items = list(filter(lambda x:x['name'] != name, items))
        return {'message':'Item deleted'}
    
    def put(self, name):
        # global items
        # data = request.get_json()
        data = Item.parser.parse_args()  # for parse
        item = next(filter(lambda x:x['name'] == name, items), None) 
        if item is None:
            item = {'name':name, 'price': data['price']}
            items.append(item)
        else:                 # if item exist
            item.update(data)
        return item

class ItemList(Resource):
    def get(self):
        return {'items': items}




# to tell api this resource we created(Student) now is accessible via our API
api.add_resource(Item, '/item/<string:name>')  # http://127.0.0.1:5000/item/Rolf
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
app.run(port=5000, debug=True)