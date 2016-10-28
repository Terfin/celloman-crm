import json

from flask import Blueprint, request, jsonify
import requests as r

lines_app = Blueprint('lines', __name__)
LIST_URL = 'http://127.0.0.1:8000/api/lines/'
DETAIL_URL = LIST_URL + '{}/'

@lines_app.route('', methods=['GET'])
def list():
    req = r.get(LIST_URL, headers=request.headers)
    data = req.json()
    return jsonify(data)

# @lines_app.route('/<int:line_id>/', methods=['GET'])
@lines_app.route('/<int:line_id>', methods=['GET'])
def detail(line_id):
    req = r.get(DETAIL_URL.format(line_id), headers={'authorization': request.headers['authorization']})
    data = req.json()
    return jsonify(data)

@lines_app.route('/', methods=['POST'])
def new_line():
    data = request.json
    req = r.post(LIST_URL, data=json.dumps(data), headers={'content-type': 'application/json', 'authorization': request.headers['authorization']})
    data = req.json()
    return jsonify(data), 201

# @lines_app.route('/<int:line_id>/', methods=['PUT'])
@lines_app.route('/<int:line_id>', methods=['PUT'])
def update_line(line_id):
    data = request.json
    data.pop('id')
    data.pop('calls_to_center')
    data.pop('date_joined')
    req = r.get(DETAIL_URL.format(line_id), headers={'authorization': request.headers['authorization']})
    db_line = req.json()
    db_line.update(data)
    req = r.put(DETAIL_URL.format(line_id), data=json.dumps(db_line), headers={'content-type': 'application/json', 'authorization': request.headers['authorization']})
    data = req.json()
    return jsonify(data)

# @lines_app.route('/<int:line_id>/', methods=['DELETE'])
@lines_app.route('/<int:line_id>', methods=['DELETE'])
def delete_line(line_id):
    r.delete(DETAIL_URL.format(line_id), headers=request.headers)
    return '', 204