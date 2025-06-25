from flask import Flask, jsonify, request
from services import UserService, JWTService
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
        new_user:User = user_service.register_user(new_user_request)
        return jsonify(new_user.serialize), 201

    @staticmethod
    @app.route('/login', methods=['POST'])
    def login():
        login_request = {
            "email": request.json['email'],
            "password": request.json['password']
        }
        token = user_service.login_user(login_request)
        return jsonify({'token': token}), 200

    @staticmethod
    @app.route('/profile', methods=['GET'])
    def get_profile():
        token = request.headers.get('Authorization')

        if not token:
            return jsonify({"error": "Missing token"}), 401

        user_id = jwt_service.verify_token(token)
        if not user_id:
            return jsonify({"error": "Invalid token"}), 401

        return jsonify({"message": f"Hello, user {user_id}!"})

        return jsonify(
            {"name": "Civm", "email": "<EMAIL>"}
        )

if __name__ == '__main__':
    app.run()
