from abc import ABC
from pymongo import MongoClient
from src.userauthsystem.model import User

class Repository(ABC):
    def save(self, new_user) -> any:pass
    def get_user_by_email(self, email:str) -> User:pass

class UserFileRepository(Repository):
    count: int = 1
    user_list:list[User] = []

    def save(self, new_user):
        new_user.id = self.count
        self.count += 1
        self.user_list.append(new_user)

    def get_user_by_email(self, email:str) -> User:

        for user in self.user_list:
            if user.email == email:
                return user
        raise ValueError

class MongoDBRepository(Repository):
    def __init__(self, connection_string:str, database_name:str, collection_name:str):
        self.client = MongoClient(connection_string)
        print(self.client)
        self.database = self.client[database_name]
        print(self.database)
        self.collection = self.database[collection_name]
        print(self.collection)

    def save(self, document):
        result = self.collection.insert_one(document)
        return result.inserted_id
    def get_user_by_email(self, email:str) -> User:
        user = self.collection.find_one({"email": email})
        return User(**user) if user else None
    def delete_all(self):
        self.collection.delete_many({})

