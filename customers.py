from flask import Blueprint, request, jsonify
import requests as r
import re
import json

customers_app = Blueprint('customers', __name__)
LIST_URL = 'http://127.0.0.1:8000/api/clients/'
DETAIL_URL = LIST_URL + '{}/'
alphanum = re.compile('[a-z0-9]')

def create_placeholder_username(first_name, last_name, suffix=None):
    if suffix is None:
        suffix = 0
    else:
        suffix += 1

    username = '{}{}{}'.format(first_name, last_name, suffix)
    username = username.lower()
    alphanum.sub('', username)
    data = {'username': username}
    req = r.get(LIST_URL, params=data, headers=request.headers)
    if len(req.json()) > 0:
        username = create_placeholder_username(first_name, last_name, suffix)
    return username


@customers_app.route('', methods=['GET'])
def list():
    req = r.get(LIST_URL, headers=request.headers)
    data = req.json()
    return jsonify(data)

# @customers_app.route('/<int:user_id>/', methods=['GET'])
@customers_app.route('/<int:user_id>', methods=['GET'])
def detail(user_id):
    req = r.get(DETAIL_URL.format(user_id), headers={'authorization': request.headers['authorization']})
    print(req.content)
    data = req.json()
    return jsonify(data)

@customers_app.route('/', methods=['POST'])
def new_customer():
    data = request.json
    if 'username' not in data:
        data['username'] = create_placeholder_username(data['first_name'], data['last_name'])
        data['password'] = data['username'][0] + '1234567'
    req = r.post(LIST_URL, data=json.dumps(data), headers={'content-type': 'application/json', 'authorization': request.headers['authorization']})
    data = req.json()
    return jsonify(data), 201

# @customers_app.route('/<int:user_id>/', methods=['PUT'])
@customers_app.route('/<int:user_id>', methods=['PUT'])
def update_customer(user_id):
    data = request.json
    data.pop('id')
    data.pop('calls_to_center')
    data.pop('date_joined')
    req = r.get(DETAIL_URL.format(user_id), headers={'authorization': request.headers['authorization']})
    db_customer = req.json()
    db_customer.update(data)
    req = r.put(DETAIL_URL.format(user_id), data=json.dumps(db_customer), headers={'content-type': 'application/json', 'authorization': request.headers['authorization']})
    data = req.json()
    return jsonify(data)

# @customers_app.route('/<int:user_id>/', methods=['DELETE'])
@customers_app.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    r.delete(DETAIL_URL.format(user_id), headers=request.headers)
    return '', 204