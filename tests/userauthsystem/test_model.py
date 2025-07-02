import unittest
from src.userauthsystem.model import User, hash_password, verify_password


class TestUserModel(unittest.TestCase):

    def setUp(self):
        self.user_data = {
            "name": "John Doe",
            "email": "johndoe@example.com",
            "password": "securepassword123"
        }
        self.user = User(**self.user_data)

    def test_user_initialization(self):
        self.assertEqual(self.user.name, self.user_data["name"])
        self.assertEqual(self.user.email, self.user_data["email"])
        self.assertTrue(self.user.verify_password(self.user_data["password"]))

    def test_user_set_name(self):
        new_name = "Jane Doe"
        self.user.name = new_name
        self.assertEqual(self.user.name, new_name)

    def test_user_set_email(self):
        new_email = "janedoe@example.com"
        self.user.email = new_email
        self.assertEqual(self.user.email, new_email)

    def test_user_set_password(self):
        new_password = "newsecurepassword456"
        self.user.set_password(new_password)
        self.assertTrue(self.user.verify_password(new_password))

    def test_user_serialize(self):
        serialized_data = self.user.serialize
        self.assertEqual(serialized_data, {
            "id":self.user.id,
            "name": self.user.name,
            "email": self.user.email
        })


class TestPasswordFunctions(unittest.TestCase):

    def test_hash_password(self):
        password = "mypassword"
        hashed_password = hash_password(password)
        self.assertTrue(verify_password(password, hashed_password))

    def test_verify_password_with_wrong_password(self):
        password = "mypassword"
        hashed_password = hash_password(password)
        wrong_password = "wrongpassword"
        self.assertFalse(verify_password(wrong_password, hashed_password))


if __name__ == '__main__':
    unittest.main()
