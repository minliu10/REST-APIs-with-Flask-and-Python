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
        item = self.find_by_name(name)
        if item:
            return item
        return {'message': 'Item not found'}, 404




    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        if row:
            return {'item': {'name': row[0], 'price': row[1]}}
        

    def post(self, name):
        if self.find_by_name(name):  # or Item.find_by_name(name)
            return {'message':"An item with name '{}' already exists.".format(name)}, 400
        
        data = Item.parser.parse_args()  

        item = {'name':name, 'price': data['price']}

        try:
            self.insert(item)
        except:
            return {"message": "An error occurred inserting the item."}, 500 #Internal server Error


        return item, 201  # 201 for created

    @classmethod
    def insert(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO items VALUES (?, ?)"
        cursor.execute(query, (item['name'], item['price']))

        connection.commit()
        connection.close()
    
    
    def delete(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query, (name,))
        connection.commit()
        connection.close()
        return {'message':'Item deleted'}
    
    def put(self, name):
        data = Item.parser.parse_args()  # for parse
        
        item = self.find_by_name(name)
        updated_item = {'name':name, 'price': data['price']}
        
        if item is None:
            try:
                self.insert(updated_item)
            except:
                return {"message": "An error occurred inserting the item."}, 500 # 500 Internal server Error
        else:                 # if item exist
            try:
                self.update(updated_item)
            except:
                return {"message": "An error occurred updating the item."}, 500
        return updated_item

    @classmethod
    def update(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(query, (item['price'], item['name']))
        
        connection.commit() # commit is used for saving changes in the database
        connection.close()

class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items"
        result = cursor.execute(query)
        items = []
        for row in result:
            items.append({'name': row[0], 'price': row[1]})
        # connection.commit() # no need bc commit is used for saving, fetch file doesn't change anything
        connection.close()

        return {'items': items}
