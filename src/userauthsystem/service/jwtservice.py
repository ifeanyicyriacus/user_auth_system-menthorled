from datetime import datetime, timedelta
import jwt
from flask import Flask
import os
from flask.cli import load_dotenv


load_dotenv()


class JWTError(Exception):
    # Base exception for JWT-related errors
    pass


class JWTService:
    TOKEN_EXPIRATION_DAYS = 1
    TOKEN_ALGORITHM = 'HS256'

    def __init__(self, app:Flask):
        self.app = app
        secret_key = os.getenv('SECRET_KEY')
        if not secret_key:
            raise JWTError("SECRET_KEY environment variable is not set")
        self.app.config['SECRET_KEY'] = secret_key

    def generate_token(self, user_data: dict):
        if not user_data:
            raise JWTError("User data cannot be empty")

        current_time = datetime.utcnow()
        payload = {
            'exp': current_time + timedelta(days=self.TOKEN_EXPIRATION_DAYS),
            'iat': current_time,
            'sub': user_data
        }
        try:
            return jwt.encode(
                payload,
                self.app.config['SECRET_KEY'],
                algorithm=self.TOKEN_ALGORITHM)
        except Exception as e:
            raise JWTError(f"Error generating token: {e}")

    def verify_token(self, token):
        if not token:
            return None

        try:
            payload = jwt.decode(
                token,
                self.app.config['SECRET_KEY'],
                algorithms=[self.TOKEN_ALGORITHM])
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
