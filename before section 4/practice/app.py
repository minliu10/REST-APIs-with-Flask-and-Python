from flask import Flask,jsonify,request, render_template

app = Flask(__name__)

companies = [
    {
        'name':'Uni-President',
        'subsidiary': [
            {
                'name': '7-11',
                'head': 'Taipei'
            },
            {
                'name': 'Starbucks',
                'head': 'Taipei'
            }
        ]
    },
    {
        'name':'ASUS',
        'subsidiary':[
            {
                'name':'Pegatron',
                'head':'Taipei'
            }
        ]
    }
]



@app.route('/')
def home3():
    return render_template('index.html')


# Companies GET

@app.route('/companies')
def get_companies():
    return jsonify({'companies':companies})

@app.route('/companies/<string:name>')
def get_company(name):
    for company in companies:
        if company['name'] == name:
            return jsonify(company) 
    return jsonify({'message':'company not found'})

@app.route('/companies/<string:name>/subsidiary')
def get_subsidiary_in_company(name):
    for company in companies:
        if company['name'] == name:
            return jsonify(company['subsidiary'])
    return jsonify({'message':'company not found'})

@app.route('/companies', methods=['POST'])
def create_company():
    request_data = request.get_json()
    new_company = {
        'name':request_data['name'],
        'subsidiary': []
    }
    companies.append(new_company)
    return jsonify(new_company)
@app.route('/companies/<string:name>/subsidiary', methods=['POST'])
def create_subsidiary_in_company(name):
    request_data = request.get_json()
    for company in companies:
        if company['name'] == name:
            new_subsidiary = {
                'name': request_data['name'],
                'head': request_data['head']
            }
            company['subsidiary'].append(new_subsidiary)
            return jsonify(new_subsidiary)
    return jsonify({'message':'company not found'})


app.run(port=5000)
