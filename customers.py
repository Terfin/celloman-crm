from flask import Blueprint, request, jsonify
import requests as r


customers_app = Blueprint('customers', __name__)

@customers_app.route('/', methods=['GET'])
def list():
    req = r.get('http://127.0.0.1:8000/api/users')
    data = req.json()
    return jsonify(data)

@customers_app.route('/<int:user_id>', methods=['GET'])
def detail(user_id):
    req = r.get('http://127.0.0.1:8000/api/users/{}/'.format(user_id))
    data = req.json()
    return jsonify(data)

@customers_app.route('/', methods=['POST'])
def new_customer():
    data = request.data
    req = r.post('http://127.0.0.1:8000/api/users/', data=data)
    data = req.json()
    return jsonify(data)

@customers_app.route('/<int:user_id>', methods=['POST'])
def update_customer(user_id):
    data = request.data
    req = r.put('http://127.0.0.1:8000/api/users/{}/'.format(user_id), data=data)
    data = req.json()
    return jsonify(data)

@customers_app.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    r.delete('http://127.0.0.1:8000/api/users/{}/'.format(user_id))