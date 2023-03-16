import base64
import json
import unittest

from unittest.mock import patch, ANY
from albums.models.users import Users
from albums import app
from sqlalchemy.exc import IntegrityError


class UserTestCase(unittest.TestCase):
    def setUp(self):
        self.app_context = app.app_context()
        self.app_context.push()

        # Create a test client for the app
        self.client = app.test_client()

    def tearDown(self):
        # Pop the Flask app context
        self.app_context.pop()

    @patch("albums.routes.users.db.session")
    def test_register_success(self, patch_db):
        patch_db.commit.return_value = None

        # create a test user
        user_data = {"username": "test_user", "password": "test_password"}
        response = self.client.post(
            "/api/users/register",
            data=json.dumps(user_data),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["status"], "User successfully created")

        patch_db.add.assert_called_once_with(
            Users(username="test_user", password=ANY, created_at=ANY, updated_at=ANY)
        )

    @patch("albums.routes.users.db.session")
    def test_register_fail(self, patch_db):
        patch_db.add.side_effect = IntegrityError(
            "IntegrityError", {}, "Duplicate Entry"
        )

        # create a test user
        user_data = {"username": "test_user", "password": "test_password"}
        response = self.client.post(
            "/api/users/register",
            data=json.dumps(user_data),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, "Username already exists")

    @patch("albums.routes.users.jwt.encode")
    @patch("albums.routes.users.check_password_hash")
    @patch("albums.routes.users.Users")
    def test_login_success(self, patch_users, patch_password_hash, patch_jwt_encode):
        patch_users.query.filter_by.return_value.first.return_value = Users(
            id=ANY, username="admin", password=ANY, created_at=ANY, updated_at=ANY
        )
        patch_password_hash.return_value = True
        patch_jwt_encode.return_value = "test_token"

        # log in with a test user
        auth = {"username": "admin", "password": "password"}
        response = self.client.post(
            "/api/users/login",
            headers={
                "Authorization": "Basic "
                + base64.b64encode(
                    f"{auth['username']}:{auth['password']}".encode("utf-8")
                ).decode("utf-8")
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"Token": "test_token"})

    @patch("albums.routes.users.check_password_hash")
    @patch("albums.routes.users.Users")
    def test_login_fail(self, patch_users, patch_password_hash):
        patch_users.query.filter_by.return_value.first.return_value = Users(
            id=ANY, username="admin", password=ANY, created_at=ANY, updated_at=ANY
        )
        patch_password_hash.return_value = False

        # log in with a test user
        auth = {"username": "admin", "password": "password"}
        response = self.client.post(
            "/api/users/login",
            headers={
                "Authorization": "Basic "
                + base64.b64encode(
                    f"{auth['username']}:{auth['password']}".encode("utf-8")
                ).decode("utf-8")
            },
        )

        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.json, "Could not authenticate the User with the given credentials"
        )

    @patch("albums.routes.users.db.session")
    @patch("albums.routes.users.Users")
    def test_delete_success(self, patch_users, patch_db):
        user_id = 1
        patch_users.query.filter_by.return_value.first.return_value = Users(
            id=user_id, username="admin", password=ANY, created_at=ANY, updated_at=ANY
        )
        patch_db.commit.return_value = None

        response = self.client.delete(f"/api/users/{user_id}")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, f"Successfully deleted User with ID {user_id}")

    @patch("albums.routes.users.db.session")
    @patch("albums.routes.users.Users")
    def test_delete_fail(self, patch_users, patch_db):
        user_id = 1
        patch_users.query.filter_by.return_value.first.return_value = None

        response = self.client.delete(f"/api/users/{user_id}")

        self.assertEqual(response.json, f"User with ID {user_id} not found")
