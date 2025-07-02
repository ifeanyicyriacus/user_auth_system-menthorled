from abc import ABC
from pymongo import MongoClient
from pymongo.server_api import ServerApi

import sqlite3

from src.userauthsystem.model import User

class Repository(ABC):
    def save(self, new_user) -> any:pass
    def get_user_by_email(self, email:str) -> User:pass


#
# class SQLiteRepository(Repository):
#     def __init__(self, db_path='user_db.sqlite'):
#         self.db_path = db_path
#         self._create_table()
#
#     def _create_table(self):
#         conn = sqlite3.connect(self.db_path)
#         cursor = conn.cursor()
#         cursor.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, email TEXT, password TEXT)''')
#         conn.commit()
#         conn.close()
#
#     def save(self, user):
#         conn = sqlite3.connect(self.db_path)
#         cursor = conn.cursor()
#         try:
#             cursor.execute(
#                 'INSERT INTO users (name, email, password) VALUES (?, ?, ?)',
#                 (user.name, user.email, user.password)
#             )
#             user.id = cursor.lastrowid
#             conn.commit()
#             return user.id
#         finally:
#             conn.close()
#
#     def get_user_by_email(self, email: str) -> User:
#         conn = sqlite3.connect(self.db_path)
#         cursor = conn.cursor()
#         try:
#             cursor.execute('SELECT id, name, email, password FROM users WHERE email = ?', (email,))
#             row = cursor.fetchone()
#             if row:
#                 return User(name=row[1], email=row[2], password=row[3])
#             return None
#         finally:
#             conn.close()
#
#     def delete_all(self):
#         conn = sqlite3.connect(self.db_path)
#         cursor = conn.cursor()
#         try:
#             cursor.execute('DELETE FROM users')
#             conn.commit()
#         finally:
#             conn.close()
#
#
# class UserInMemoryRepository(Repository):
#     count: int = 1
#     user_list:list[User] = []
#
#     def save(self, new_user):
#         new_user.id = self.count
#         self.count += 1
#         self.user_list.append(new_user)
#
#     def get_user_by_email(self, email:str) -> User:
#
#         for user in self.user_list:
#             if user.email == email:
#                 return user
#         raise ValueError
#

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

    # def save(self, document):
    #     result = self.collection.insert_one(document)
    #     return result.inserted_id

    # def get_user_by_email(self, email:str) -> User:
    #     user = self.collection.find_one({"email": email})
    #     return User(**user) if user else None

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
