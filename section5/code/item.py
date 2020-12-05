import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required


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
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        if row:
            return {'item': {'name': row[0], 'price': row[1]}}
        
        return {'message': 'Item not found'}, 404

    
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
