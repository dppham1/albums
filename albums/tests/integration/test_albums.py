import json

from albums.models.albums import Albums
from albums.tests.integration.base_test_case import BaseTestCase
from datetime import datetime


class CreateAlbumTest(BaseTestCase):
    def test_create_album_success(self):
        # Register and Login to receive Token
        token, user_id = self.register_and_login(
            self.client, "test_user", "test_password"
        )

        # Create Album
        data = {
            "artist_id": 1,
            "genre_id": 14,
            "images": ["https:www.google.com"],
            "label_rights": "Sony Records",
            "name": "Test Album Name",
            "price": {"amount": 5.99, "currency": "USD"},
            "release_date": "2023-02-14 00:00:00",
            "song_count": 5,
            "title": "Title",
            "url": "https://www.url.com",
        }
        response = self.client.post(
            "/api/albums/",
            data=json.dumps(data),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}",
            },
        )
        album_id = response.json.get("id")

        # Check that the request was successful
        self.assertEqual(response.status_code, 200)

        # Check if the new Album was added to the database
        album = Albums.query.filter_by(name="Test Album Name").first()
        assert album is not None

        # Cleanup
        response = self.client.delete(
            f"/api/albums/{album_id}",
            data=json.dumps(data),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}",
            },
        )
        self.client.delete(f"/api/users/{user_id}")

    def test_create_album_fail(self):
        # Create album with no token
        album_data = {
            "artist_id": 1,
            "genre_id": 14,
            "images": ["https:www.google.com"],
            "label_rights": "Sony Records",
            "name": "Album Name",
            "price": {"amount": 5.99, "currency": "USD"},
            "release_date": "2020 11 05 14:00:00",
            "song_count": 5,
            "title": "Title",
            "url": "https://www.url.com",
        }
        response = self.client.post(
            "/api/albums/",
            data=json.dumps(album_data),
            headers={"Content-Type": "application/json"},
        )

        # Check that the Request failed due to a missing Token
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"status": "A valid Token is required"})


class GetAlbumsTest(BaseTestCase):
    def test_get_all_albums(self):
        # Register and Login to receive Token
        token, user_id = self.register_and_login(
            self.client, "test_user", "test_password"
        )

        # Create Album
        data = {
            "artist_id": 1,
            "genre_id": 14,
            "images": ["https:www.google.com"],
            "label_rights": "Sony Records",
            "name": "Test Album Name",
            "price": {"amount": 5.99, "currency": "USD"},
            "release_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "song_count": 5,
            "title": "Title",
            "url": "https://www.url.com",
        }
        response = self.client.post(
            "/api/albums/",
            data=json.dumps(data),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}",
            },
        )
        album_id = response.json.get("id")

        # Get Album
        response = self.client.get(f"/api/albums/?name=Test Album Name&page=1")

        # Check that the Album's name is what we expect it to be
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json[0]["name"], data["name"])

        # Cleanup
        response = self.client.delete(
            f"/api/albums/{album_id}",
            data=json.dumps(data),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}",
            },
        )
        self.client.delete(f"/api/users/{user_id}")


class UpdateAlbumTest(BaseTestCase):
    def test_update_album_success(self):
        # Register and Login to receive Token
        token, user_id = self.register_and_login(
            self.client, "test_user", "test_password"
        )

        # Create Album
        data = {
            "artist_id": 1,
            "genre_id": 14,
            "images": ["https:www.google.com"],
            "label_rights": "Sony Records",
            "name": "Test Album Name",
            "price": {"amount": 5.99, "currency": "USD"},
            "release_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "song_count": 5,
            "title": "Title",
            "url": "https://www.url.com",
        }
        response = self.client.post(
            "/api/albums/",
            data=json.dumps(data),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}",
            },
        )
        album_id = response.json.get("id")

        # Update album's song_count field
        data = {
            "artist_id": 1,
            "genre_id": 14,
            "images": ["https:www.google.com"],
            "label_rights": "Sony Records",
            "name": "New Album Name",
            "price": {"amount": 5.99, "currency": "USD"},
            "release_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "song_count": 6,
            "title": "Title",
            "url": "https://www.url.com",
        }
        response = self.client.put(
            f"/api/albums/{album_id}",
            data=json.dumps(data),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}",
            },
        )

        self.assertEqual(response.status_code, 200)  # WHY????
        self.assertEqual(response.json["song_count"], 6)

        # Cleanup
        response = self.client.delete(
            f"/api/albums/{album_id}",
            data=json.dumps(data),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}",
            },
        )
        self.client.delete(f"/api/users/{user_id}")

    def test_update_album_fail(self):
        # Register and Login to receive Token
        token, user_id = self.register_and_login(
            self.client, "test_user", "test_password"
        )

        # Update an Album that does not exist
        invalid_album_id = 1000000
        data = {
            "artist_id": 1,
            "genre_id": 14,
            "images": ["https:www.google.com"],
            "label_rights": "Sony Records",
            "name": "New Album Name",
            "price": {"amount": 5.99, "currency": "USD"},
            "release_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "song_count": 6,
            "title": "Title",
            "url": "https://www.url.com",
        }
        response = self.client.put(
            "/api/albums/1000000",
            data=json.dumps(data),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}",
            },
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json, {"status": f"Album with ID {invalid_album_id} not found"}
        )

        # Cleanup
        self.client.delete(f"/api/users/{user_id}")


class DeleteAlbumTest(BaseTestCase):
    def test_delete_album_success(self):
        # Register and Login to receive Token
        token, user_id = self.register_and_login(
            self.client, "test_user", "test_password"
        )

        # Create Album
        data = {
            "artist_id": 1,
            "genre_id": 14,
            "images": ["https:www.google.com"],
            "label_rights": "Sony Records",
            "name": "Test Album Name",
            "price": {"amount": 5.99, "currency": "USD"},
            "release_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "song_count": 5,
            "title": "Title",
            "url": "https://www.url.com",
        }
        response = self.client.post(
            "/api/albums/",
            data=json.dumps(data),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}",
            },
        )
        album_id = response.json.get("id")

        # Delete Album
        response = self.client.delete(
            f"/api/albums/{album_id}",
            data=json.dumps(data),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}",
            },
        )

        # Cleanup
        self.client.delete(f"/api/users/{user_id}")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json, {"status": f"Successfully deleted Album with ID {album_id}"}
        )

    def test_delete_album_fail(self):
        # Register and Login to receive Token
        token, user_id = self.register_and_login(
            self.client, "test_user", "test_password"
        )

        # Delete an Album that does not exist
        invalid_album_id = 1000000
        response = self.client.delete(
            f"/api/albums/{invalid_album_id}",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}",
            },
        )

        # Cleanup
        self.client.delete(f"/api/users/{user_id}")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json, {"status": f"Album with ID {invalid_album_id} not found"}
        )
