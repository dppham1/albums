import base64

from flask_testing import TestCase
from albums import app


class BaseTestCase(TestCase):
    def create_app(self):
        app.config["TESTING"] = True
        return app

    def register_and_login(self, client, username, password):
        """
        Helper function to register a User and login to receive the Token.
        Returns a tuple of (token, user_id).
        """
        response = client.post(
            "/api/users/register", json={"username": username, "password": password}
        )
        user_id = response.json.get("user_id")

        response = client.post(
            "/api/users/login",
            headers={
                "Authorization": "Basic "
                + base64.b64encode(f"{username}:{password}".encode("utf-8")).decode(
                    "utf-8"
                )
            },
        )
        return (response.json.get("Token"), user_id)
