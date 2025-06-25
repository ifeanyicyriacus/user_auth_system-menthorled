import jwt
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

class UserService:
    def register_user(self, new_user_request):
        pass

    def login_user(self, login_request):
        pass

    def profile(self, user_id):
        pass


class JWTService:
    def __init__(self, Object):
        self.app = Object
        self.app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    def generate_token(self, user_id):
        payload = {
            'exp': datetime.utcnow() + timedelta(days=1),
            'iat': datetime.utcnow(),
            'sub': user_id
        }
        return jwt.encode(payload, self.app.config['SECRET_KEY'], algorithm='HS256')

    def verify_token(self, token):
        try:
            payload = jwt.decode(token, self.app.config['SECRET_KEY'], algorithms=['HS256'])
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
