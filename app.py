from flask import Flask, jsonify, request, json

app = Flask(__name__)


stores: list[dict[
    str, list[dict[str, float]]
]] = [
    {
        'name': 'My Wonderful Store',
        'items': [
            {
                'name': 'My Item',
                'price': 15.99
            },
        ]
    }]


@app.route('/')
def home():
    return "Hello, world!"


@app.get('/store')
def get_stores():
    return jsonify({'stores': stores})


@app.post('/store')
def create_store():
    client_data = request.get_json()
    if not client_data:
        return jsonify({'message': 'No data provided'}), 400
    if 'name' not in client_data:
        return jsonify({'message': 'No name provided'}), 400
    if client_data['name'] in [store['name'] for store in stores]:
        return jsonify({'message': 'Store already exists'}), 400
    new_store = {
        'name': client_data['name']
    }
    stores.append(new_store)

    return jsonify(new_store), 201


@app.put('/store/<string:name>')
def update_store(name: str):
    data = request.get_json()
    store = next((store for store in stores if store['name'] == name), None)
    if not store:
        return jsonify({'message': 'Store not found'}), 404
    store.update(data)
    return jsonify(store), 200


@app.get('/store/<string:name>')
def get_specific_store(name) -> json:
    spec_store = next((store for store in stores if store['name'] == name), None)
    print(spec_store)
    if not spec_store:
        return jsonify({'message': 'Store not found'}), 404
    return jsonify({"store_info": spec_store}), 200


@app.get('/store/<string:name>/item')
def get_items_in_store(name: str) -> json:
    store = next((store for store in stores if store['name'] == name), None)
    if not store:
        return jsonify({'message': 'Store not found'}), 404
    return jsonify({'items': store['items']}), 200
