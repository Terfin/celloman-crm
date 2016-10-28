import logging

from flask import Flask, request, jsonify
from flask_cors import CORS
import customers
import lines
import customer_types
import requests as r

app = Flask(__name__)
CORS(app)
app.register_blueprint(customers.customers_app, url_prefix='/customers')
app.register_blueprint(lines.lines_app, url_prefix='/lines')
app.register_blueprint(customer_types.customer_types_app, url_prefix='/customer_types')
logging.getLogger('flask_cors').level = logging.DEBUG


@app.route('/', methods=['OPTIONS'], defaults={'path': ''})
@app.route('/<path:path>', methods=['OPTIONS'])
def options(path):
    return ''

@app.route('/login/', methods=['POST'])
def login():
    data = request.json
    print(data)
    req = r.post('http://127.0.0.1:8000/api-token-auth/', json=data)
    if req.status_code == 200:
        token = req.json()['token']
        req = r.get('http://127.0.0.1:8000/api/users/current/', headers={'Authorization': 'Token {}'.format(token)})
        print(req.headers)
        if req.status_code == 200:
            user = req.json()
            user['token'] = token
            return jsonify(user)
        else:
            print(req.json())
            return '', 500
    else:
        return '', 401

if __name__ == '__main__':
    app.run(debug=True, port=8001)