from flask import Flask, request, jsonify, Response
import customers
import requests as r

app = Flask(__name__)
app.register_blueprint(customers.customers_app, url_prefix='/customers')

@app.route('/login/', methods=['POST'])
def login():
    data = request.json
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
    app.run(debug=True)