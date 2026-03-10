from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token

app = Flask(__name__)

# Конфігурація JWT
app.config['JWT_SECRET_KEY'] = 'super-secret'
jwt = JWTManager(app)

# База автомобілів
cars_db = {
    1: {"brand": "BMW", "year": 2018, "engine_volume": 2.0, "price": 50000},
    2: {"brand": "Audi", "year": 2020, "engine_volume": 1.8, "price": 45000},
    3: {"brand": "Mercedes", "year": 2019, "engine_volume": 2.5, "price": 55000},
    4: {"brand": "Toyota", "year": 2017, "engine_volume": 2.4, "price": 35000},
    5: {"brand": "Honda", "year": 2016, "engine_volume": 1.6, "price": 30000},
    6: {"brand": "Nissan", "year": 2021, "engine_volume": 1.5, "price": 40000},
    7: {"brand": "Ford", "year": 2015, "engine_volume": 2.2, "price": 32000},
    8: {"brand": "Chevrolet", "year": 2018, "engine_volume": 1.8, "price": 28000},
    9: {"brand": "Volkswagen", "year": 2019, "engine_volume": 2.0, "price": 33000},
    10: {"brand": "Hyundai", "year": 2020, "engine_volume": 1.6, "price": 29000},
}

# користувачі
users = {
    "test_user": "test_pass"
}

# аутентифікація
def authenticate(username, password):
    if username in users and users[username] == password:
        return username


# endpoint авторизації
@app.route('/auth', methods=['POST'])
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return jsonify({"message": "Auth failed"}), 401

    username = authenticate(auth.username, auth.password)

    if not username:
        return jsonify({"message": "Wrong credentials"}), 401

    access_token = create_access_token(identity=username)

    return jsonify(access_token=access_token), 200


# endpoint пошуку авто
@app.route('/cars', methods=['GET'])
@jwt_required()
def get_cars():

    sort_by = request.args.get('sort_by')
    limit = request.args.get('limit')

    sorted_cars = sorted(
        cars_db.values(),
        key=lambda x: x.get(sort_by, 0) if sort_by else x["brand"]
    )

    if limit:
        sorted_cars = sorted_cars[:int(limit)]

    return jsonify(sorted_cars), 200


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)