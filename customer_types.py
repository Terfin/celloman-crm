from flask import Blueprint, request, jsonify
import requests as r

customer_types_app = Blueprint('customer_types', __name__)
LIST_URL = 'http://127.0.0.1:8000/api/client_types/'
DETAIL_URL = LIST_URL + '{}/'

@customer_types_app.route('', methods=['GET'])
def list():
    req = r.get(LIST_URL, headers=request.headers)
    data = req.json()
    return jsonify(data)

# @client_types_app.route('/<int:client_type_id>/', methods=['GET'])
@customer_types_app.route('/<int:client_type_id>', methods=['GET'])
def detail(client_type_id):
    req = r.get(DETAIL_URL.format(client_type_id), headers={'authorization': request.headers['authorization']})
    data = req.json()
    return jsonify(data)