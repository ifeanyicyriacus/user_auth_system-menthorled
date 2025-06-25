import bcrypt


def hash_password(password:str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
def verify_password(password:str, hashed_password:str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

class User:
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self._hashed_password = None
        self.set_password(password)

    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, name):
        self._name = name

    @property
    def email(self):
        return self._email
    @email.setter
    def email(self, email):
        self._email = email

    def set_password(self, password):
        self._hashed_password = hash_password(password)
    def verify_password(self, password) -> bool:
        return verify_password(password, self._hashed_password)

    @property
    def serialize(self) -> dict:
        return {
            'name': self.name,
            'email': self.email,
        }