from albums.models.users import Users
from werkzeug.security import check_password_hash

import base64
from albums.tests.integration.base_test_case import BaseTestCase


class UserRegisterTest(BaseTestCase):
    def test_register_success(self):
        # Register a new user with valid payload
        response = self.client.post(
            "/api/users/register",
            json={"username": "test_user_2", "password": "test_password_2"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["status"], "User successfully created")

        # Check if the new user was added to the database
        user = Users.query.filter_by(username="test_user_2").first()

        self.assertNotEqual(user, None)
        assert check_password_hash(user.password, "test_password_2") == True

        # Delete User
        response = self.client.delete(f"/api/users/{user.id}")
        self.assertEqual(response.status_code, 200)

    def test_register_fail(self):
        # Register a new User with invalid payload
        response = self.client.post(
            "/api/users/register",
            json={"_username": "test_user", "_password": "test_password"},
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.get_json(), "A Username and Password is required to register"
        )

        # Check if the new User was not added to the database
        user = Users.query.filter_by(username="test_user").first()
        self.assertEqual(user, None)


class UserLoginTest(BaseTestCase):
    def test_login_success(self):
        # Register a new user with valid payload
        response = self.client.post(
            "/api/users/register",
            json={"username": "test_user", "password": "test_password"},
        )

        # Login and receieve Token
        auth = {"username": "test_user", "password": "test_password"}
        response = self.client.post(
            "/api/users/login",
            headers={
                "Authorization": "Basic "
                + base64.b64encode(
                    f"{auth['username']}:{auth['password']}".encode("utf-8")
                ).decode("utf-8")
            },
        )

        # Check if Token is in response
        self.assertIn("Token", response.get_json())

        # Delete User
        user = Users.query.filter_by(username="test_user").first()
        response = self.client.delete(f"/api/users/{user.id}")
        self.assertEqual(response.status_code, 200)

    def test_login_fail(self):
        # Login with an invalid User
        auth = {"username": "_test_user", "password": "_test_password"}
        response = self.client.post(
            "/api/users/login",
            headers={
                "Authorization": "Basic "
                + base64.b64encode(
                    f"{auth['username']}:{auth['password']}".encode("utf-8")
                ).decode("utf-8")
            },
        )

        # Check if Token is not in response
        self.assertNotIn("Token", response.get_json())
