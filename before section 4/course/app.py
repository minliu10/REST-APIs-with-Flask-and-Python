from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

stores = [
    {
         'name':'My Wonderful Store',
         'items':[
             {
             'name':'My item',
             'price': 15.99
             }
        ]
    }
]

# json cannot be a list, but we wanna return not only a single stores
# but a dictionary with all our stores


# POST - used to recieve data
# GET - used to send data back only


@app.route('/')
def home2():
    return render_template('index.html')

# POST /store data: {name:}
@app.route('/store', methods=['POST'])
def create_store():
    request_data = request.get_json()
    new_store = {
        'name': request_data['name'],
        'items': []
        
    }
    stores.append(new_store)
    return jsonify(new_store)

# GET /store/<string:name>
@app.route('/store/<string:name>') # 'https://127.0.0.1:5000/store/some_name'
def get_store(name):
    # iterate over stores
    # If the store name matches, return it
    # If none match, return an error message
    for store in stores:
        if store['name'] == name:
            return jsonify(store) 
            # because store is a dict, so we can just return that store dict
    return jsonify({'message': 'store not found'})

# GET /store
@app.route('/store')
def get_stores():
    return jsonify({'stores':stores})
    # json cannot be a list, but we wanna return not only a single stores
    # but a dictionary with all our stores
    
# POST /store/<string:name>/item  {name:, price}
@app.route('/store/<string:name>/item', methods=['POST'])
def create_items_in_store(name):
    request_data = request.get_json()
    for store in stores:
        if store['name'] == name:
            new_item = {
                'name': request_data['name'],
                'price': request_data['price']
            }
            store['items'].append(new_item)
            return jsonify(new_item)
    return jsonify({'message':'store not found'})

# GET /store/<string:name>/item
@app.route('/store/<string:name>/item')
def get_items_in_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify({'items':store['items']})
    return jsonify({'message':'store not found'})










@app.route('/')  # 'https://google.com/'
def home():
    return "Hello world!"

app.run(port=5000)

