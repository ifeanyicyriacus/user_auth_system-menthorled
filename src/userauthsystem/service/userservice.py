import os

from flask import jsonify, Response

from src.userauthsystem.model import User
from src.userauthsystem.repositories import MongoDBRepository, Repository, UserFileRepository
from src.userauthsystem.service.jwtservice import JWTService


class UserService:
    # user_repository:Repository = MongoDBRepository(
    #     connection_string=os.getenv('MONGODB_CONNECTION_STRING'),
    #     database_name=os.getenv('MONGODB_DATABASE_NAME'),
    #     collection_name=os.getenv('MONGODB_COLLECTION_NAME')
    # )
    user_repository:Repository = UserFileRepository()


    def register_user(self, new_user_request) -> User:
        new_user:User = User(**new_user_request)
        assert new_user.id is None
        self.user_repository.save(new_user)
        assert new_user.id is not None
        return new_user

    def login_user(self, login_request, jwt_service:JWTService) -> str | None:
        user:User = self.user_repository.get_user_by_email(login_request['email'])
        if not user:
            return None
        is_user_valid = user.verify_password(login_request['password'])
        if not is_user_valid:
            return None
        return jwt_service.generate_token(user.serialize)


    @staticmethod
    def get_profile(token:str, jwt_service:JWTService) -> tuple[Response, int]:
        if not token:
            return jsonify({"error": "Missing token"}), 401
        print(jwt_service.verify_token(token))
        user_profile = jwt_service.verify_token(token)
        if not user_profile:
            return jsonify({"error": "Invalid token"}), 401

        return jsonify(user_profile), 200
