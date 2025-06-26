import jwt
import unittest
from datetime import datetime, timedelta
from flask import Flask
from src.userauthsystem.service.jwtservice import JWTService, JWTError


class TestJWTService(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.testing = True
        self.app.config['SECRET_KEY'] = "test_secret_key"
        self.jwt_service = JWTService(self.app)

    def test_generate_token_with_valid_data(self):
        user_data = {'id': 1, 'email': 'test@example.com'}
        token = self.jwt_service.generate_token(user_data)
        self.assertIsInstance(token, str)
        decoded = jwt.decode(token, self.app.config['SECRET_KEY'], algorithms=[JWTService.TOKEN_ALGORITHM])
        self.assertEqual(decoded['user_data'], user_data)

    def test_generate_token_with_empty_data(self):
        with self.assertRaises(JWTError):
            self.jwt_service.generate_token({})

    def test_verify_valid_token(self):
        user_data = {'id': 1, 'email': 'test@example.com'}
        token = self.jwt_service.generate_token(user_data)
        result = self.jwt_service.verify_token(token)
        self.assertEqual(result, user_data)

    def test_verify_expired_token(self):
        user_data = {'id': 1, 'email': 'test@example.com'}
        current_time = datetime.utcnow() - timedelta(days=2)
        payload = {
            'exp': current_time,
            'iat': current_time - timedelta(minutes=5),
            'sub': str(user_data.get('id', '')),  # Use user ID as subject
            'user_data': user_data
        }
        expired_token = jwt.encode(payload, self.app.config['SECRET_KEY'], algorithm=JWTService.TOKEN_ALGORITHM)
        with self.assertRaises(JWTError):
            self.jwt_service.verify_token(expired_token)

    def test_verify_invalid_token(self):
        invalid_token = "invalid.token.value"
        with self.assertRaises(JWTError):
            self.jwt_service.verify_token(invalid_token)

    def test_verify_token_with_empty_value(self):
        result = self.jwt_service.verify_token(None)
        self.assertIsNone(result)
