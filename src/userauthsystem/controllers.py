from flask import Flask, jsonify, request
from src.userauthsystem.service.jwtservice import JWTService
from src.userauthsystem.service.userservice import UserService
from src.userauthsystem.model import User

app = Flask(__name__)

# POST /register – create new user (name, email, password)
user_service = UserService()
jwt_service = JWTService(app)

class UserController:
    @staticmethod
    @app.route('/register', methods=['POST'])
    def register():
        new_user_request = {
            "name": request.json['name'],
            "email": request.json['email'],
            "password": request.json['password']
        }
        new_user: User = user_service.register_user(new_user_request)
        return jsonify(new_user.serialize), 201

    @staticmethod
    @app.route('/login', methods=['POST'])
    def login():
        login_request = {
            "email": request.json['email'],
            "password": request.json['password']
        }
        token = user_service.login_user(login_request, jwt_service)
        if not token:
            return jsonify({'error': 'Invalid credentials'}), 401
        return jsonify({'token': token}), 200

    @staticmethod
    @app.route('/profile', methods=['GET'])
    def profile():
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'error': 'Authorization header is missing'}), 401
        parts = auth_header.split()
        if len(parts) != 2 or parts[0].lower() != 'bearer':
            return jsonify({"error": "Invalid Authorization header format"}), 401

        token = parts[1]

        user_profile = user_service.get_profile(token, jwt_service)
        return user_profile

if __name__ == '__main__':
    app.run()
    app.debug = True
