from flask import Blueprint, request, jsonify
import requests as r


customers_app = Blueprint('customers', __name__)
LIST_URL = 'http://127.0.0.1:8000/api/clients'
DETAIL_URL = LIST_URL + '/{}/'

@customers_app.route('', methods=['GET'])
def list():
    req = r.get(LIST_URL)
    data = req.json()
    return jsonify(data)

@customers_app.route('/<int:user_id>', methods=['GET'])
def detail(user_id):
    req = r.get(DETAIL_URL.format(user_id))
    data = req.json()
    return jsonify(data)

@customers_app.route('/', methods=['POST'])
def new_customer():
    data = request.data
    req = r.post(LIST_URL, data=data)
    data = req.json()
    return jsonify(data)

@customers_app.route('/<int:user_id>', methods=['POST'])
def update_customer(user_id):
    data = request.data
    req = r.put(DETAIL_URL.format(user_id), data=data)
    data = req.json()
    return jsonify(data)

@customers_app.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    r.delete(DETAIL_URL.format(user_id))