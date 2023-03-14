import json
import unittest

from datetime import datetime
from unittest.mock import patch, ANY
from albums.models.albums import Albums
from albums import app

class UserTestCase(unittest.TestCase):
    def setUp(self):
        self.app_context = app.app_context()
        self.app_context.push()

        # Create a test client for the app
        self.client = app.test_client()
        
    def tearDown(self):
        # Pop the Flask app context
        self.app_context.pop()


    @patch("albums.routes.albums.AlbumSchema.dump")
    @patch("albums.routes.albums.Albums")
    def test_get_albums(self, patch_albums, patch_album_schema):
        patch_albums.query.filter_by.return_value.order_by.return_value.all.return_value = [Albums(id=ANY, artist_id=ANY, genre_id=ANY, images=ANY, label_rights=ANY, name=ANY, price=ANY, release_date=ANY, song_count=ANY, title=ANY, url=ANY, updated_at=ANY, created_at=ANY)]
        patch_album_schema.return_value = {"album_data": True}

        # Get albums
        response = self.client.get('/api/albums/')

        self.assertEquals(response.status_code, 200)
        self.assertAlmostEquals(response.json, {'album_data': True})
    
    @patch("albums.auth.Users")
    @patch("albums.auth.jwt.decode")
    @patch("albums.routes.albums.db.session")
    @patch("albums.routes.albums.AlbumSchema.dump")
    @patch("albums.routes.albums.AlbumSchema.load")
    def test_create_album_success(self, patch_album_schema_load, patch_album_schema_dump, patch_db, patch_jwt_decode, patch_users):
        data = {'artist_id': 1, 'genre_id': 1, 'images': ['https:www.google.com'], 'label_rights': 'Sony Records', 'name': 'Album Name', 'price': {'amount': 5.99, 'currency': 'USD'}, 'release_date': '2020 11 05 14:00:00', 'song_count': 5, 'title': 'Title', 'url': 'https://www.url.com'}
        patch_album_schema_load.return_value = data
        patch_album_schema_dump.return_value = {"album_data": True}
        patch_db.commit.return_value = None
        patch_jwt_decode.return_value = {"id": "123"}
        patch_users.query.filter_by.return_value.first.return_value = True

        # Create album
        response = self.client.post('/api/albums/', data=json.dumps(data), headers={'Content-Type': 'application/json', 'Authorization': 'Bearer test_token'})
        
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.json, {'album_data': True})

    @patch("albums.auth.Users")
    @patch("albums.auth.jwt.decode")
    def test_create_album_fail(self, patch_jwt_decode, patch_users):
        patch_jwt_decode.return_value = {"id": "123"}
        patch_users.query.filter_by.return_value.first.return_value = True

        # Create album
        data_without_genre_id = {'artist_id': 1, 'images': ['https:www.google.com'], 'label_rights': 'Sony Records', 'name': 'Album Name', 'price': {'amount': 5.99, 'currency': 'USD'}, 'release_date': '2020 11 05 14:00:00', 'song_count': 5, 'title': 'Title', 'url': 'https://www.url.com'}
        response = self.client.post('/api/albums/', data=json.dumps(data_without_genre_id), headers={'Content-Type': 'application/json', 'Authorization': 'Bearer test_token'})

        self.assertEquals(response.status_code, 400)

    @patch("albums.routes.albums.db.session")
    @patch("albums.routes.albums.Albums")
    @patch("albums.auth.Users")
    @patch("albums.auth.jwt.decode")
    def test_update_album_success(self, patch_jwt_decode, patch_users, patch_album_schema, patch_db):
        patch_jwt_decode.return_value = {"id": "123"}
        patch_users.query.filter_by.return_value.first.return_value = True
        patch_album_schema.query.filter_by.return_value.first.return_value = Albums(id=18, name='Griff Album3', images=['https:www.google.com'], song_count=5, price={'amount': 5.99, 'currency': 'USD'}, label_rights='Sony Records', title='Title', url='https://www.url.com', artist_id=1, genre_id=1, release_date=datetime(1998, 2, 22, 0, 0), created_at=datetime(2023, 3, 14, 6, 53, 8), updated_at=datetime(2023, 3, 14, 6, 53, 8))
        patch_db.commit.return_value = None

        # Update album
        data = {'artist_id': 1, 'genre_id': 1, 'images': ['https:www.google.com'], 'label_rights': 'Sony Records', 'name': 'New Album Name', 'price': {'amount': 5.99, 'currency': 'USD'}, 'release_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'song_count': 5, 'title': 'Title', 'url': 'https://www.url.com'}
        response = self.client.put('/api/albums/1', data=json.dumps(data), headers={'Content-Type': 'application/json', 'Authorization': 'Bearer test_token'})

        self.assertEquals(response.status_code, 200)
        self.assertEqual(response.json.get('name'), 'New Album Name')

    @patch("albums.routes.albums.db.session")
    @patch("albums.routes.albums.Albums")
    @patch("albums.auth.Users")
    @patch("albums.auth.jwt.decode")
    def test_update_album_fail(self, patch_jwt_decode, patch_users, patch_album_schema, patch_db):
        patch_jwt_decode.return_value = {"id": "123"}
        patch_users.query.filter_by.return_value.first.return_value = True
        patch_album_schema.query.filter_by.return_value.first.return_value = {'artist_id': 1, 'genre_id': 1, 'images': ['https:www.google.com'], 'label_rights': 'Sony Records', 'name': 'Album Name', 'price': {'amount': 5.99, 'currency': 'USD'}, 'release_date': '2020 11 05 14:00:00', 'song_count': 5, 'title': 'Title', 'url': 'https://www.url.com'}
        patch_db.commit.return_value = None

        # Update album
        data_without_label_rights = {'artist_id': 1, 'genre_id': 1, 'images': ['https:www.google.com'], 'name': 'Album Name', 'price': {'amount': 5.99, 'currency': 'USD'}, 'release_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'song_count': 5, 'title': 'Title', 'url': 'https://www.url.com'}
        response = self.client.put('/api/albums/1', data=json.dumps(data_without_label_rights), headers={'Content-Type': 'application/json', 'Authorization': 'Bearer test_token'})

        self.assertEquals(response.status_code, 400)
        self.assertEqual(response.json.get('label_rights'),  ['Missing data for required field.'])

    @patch("albums.routes.albums.db.session")
    @patch("albums.routes.albums.Albums")
    @patch("albums.auth.Users")
    @patch("albums.auth.jwt.decode")
    def test_delete_album_success(self, patch_jwt_decode, patch_users, patch_albums, patch_db):
        patch_jwt_decode.return_value = {"id": "123"}
        patch_users.query.filter_by.return_value.first.return_value = True
        patch_albums.query.filter_by.return_value.first.return_value = {'artist_id': 1, 'genre_id': 1, 'images': ['https:www.google.com'], 'label_rights': 'Sony Records', 'name': 'Album Name', 'price': {'amount': 5.99, 'currency': 'USD'}, 'release_date': '2020 11 05 14:00:00', 'song_count': 5, 'title': 'Title', 'url': 'https://www.url.com'}
        patch_db.commit.return_value = True

        # Delete album
        response = self.client.delete('/api/albums/1', headers={'Content-Type': 'application/json', 'Authorization': 'Bearer test_token'})
        
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.json, 'Successfully deleted Album with ID 1')

    @patch("albums.routes.albums.Albums")
    @patch("albums.auth.Users")
    @patch("albums.auth.jwt.decode")
    def test_delete_album_fail(self, patch_jwt_decode, patch_users, patch_albums):
        patch_jwt_decode.return_value = {"id": "123"}
        patch_users.query.filter_by.return_value.first.return_value = True
        patch_albums.query.filter_by.return_value.first.return_value = None

        # Delete album
        response = self.client.delete('/api/albums/1', headers={'Content-Type': 'application/json', 'Authorization': 'Bearer test_token'})
        
        self.assertEquals(response.status_code, 404)
        self.assertEquals(response.json, 'Album with ID 1 not found')