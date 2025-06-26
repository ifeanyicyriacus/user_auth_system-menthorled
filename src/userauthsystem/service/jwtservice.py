from datetime import datetime, timedelta, UTC
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

    def __init__(self, app: Flask):
        self.app = app
        secret_key = os.getenv('SECRET_KEY')
        if not secret_key:
            raise JWTError("SECRET_KEY environment variable is not set")
        self.app.config['SECRET_KEY'] = secret_key

    def generate_token(self, user_data: dict):
        if not user_data:
            raise JWTError("User data cannot be empty")

        current_time = datetime.now(UTC)
        payload = {
            'exp': current_time + timedelta(days=self.TOKEN_EXPIRATION_DAYS),
            'iat': current_time,
            'sub': str(user_data.get('id', '')),  # Use user ID as subject
            'user_data': user_data  # Store full user data in separate claim
        }
        try:
            return jwt.encode(
                payload,
                self.app.config['SECRET_KEY'],
                algorithm=self.TOKEN_ALGORITHM)
        except Exception as e:
            raise JWTError(f"Error generating token: {e}")

    def verify_token(self, token) -> dict|None:
        if not token:
            return None

        try:
            payload = jwt.decode(
                jwt=token,
                key=self.app.config['SECRET_KEY'],
                algorithms=[self.TOKEN_ALGORITHM],
                options={
                    "verify_signature": True,
                    "verify_exp": True,
                    "verify_iat": True
                }
            )
            print(f"{payload}")
            return payload['user_data']
        except jwt.ExpiredSignatureError:
            raise JWTError("Token has expired")
        except jwt.InvalidTokenError as e:
            raise JWTError(f"Invalid token: {str(e)}")
