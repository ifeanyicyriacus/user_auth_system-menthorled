from abc import ABC
from pymongo import MongoClient
from pymongo.server_api import ServerApi

from src.userauthsystem.model import User

class Repository(ABC):
    def save(self, new_user) -> any:pass
    def get_user_by_email(self, email:str) -> User:pass

class MongoDBRepository(Repository):
    def __init__(self, connection_string:str, database_name:str, collection_name:str):
        self._client = MongoClient(connection_string, server_api=ServerApi('1'))
        self._database = self._client[database_name]
        self.collection = self._database[collection_name]

    def save(self, user: User):
        user_dict = {
            "name": user.name,
            "email": user.email,
            "password": user._hashed_password
        }
        result = self.collection.insert_one(user_dict)
        user.id = str(result.inserted_id)
        return user.id

    def get_user_by_email(self, email:str) -> User:
        user_doc = self.collection.find_one({"email": email})
        if user_doc:
            user = User(
                name=user_doc["name"],
                email=user_doc["email"],
                password=user_doc["password"]
            )
            user.id = str(user_doc["_id"])
            user._hashed_password = user_doc["password"]
            return user
        return None


    def delete_all(self):
        self.collection.delete_many({})
#
