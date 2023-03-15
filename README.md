# Albums API 

The Albums REST API is an application written in Python that allows you to perform basic CRUD operations on Album objects. 

## Features
- Unit testing with Python's unittest library, which allowed for Mocking/Patching
- PostgreSQL was used for storing Albums, Genres, and Artists data
- Sorting, Filtering, and Ordering have been implemented
- Data validation/serialization using Python's Marshmallow library
- Token-based authentication has been applied to the Create, Update and Delete Album endpoints
- The application has been dockerized with Docker v20.10.23 and Docker Compose v2.15.1. Feel free to try it on your machine, and hollar me if there are any questions 😊

## Requirements
- Docker v20.10.23
- Docker Compose v2.15.1

## Install
- `mkdir weecare`
- `cd weecare` 
- `git clone https://github.com/dppham1/albums.git`

## Run the app with docker-compose
- `docker-compose up -d`
- Verify that both the `albums` and `albums-postgres` containers are up and running with `docker ps -a`

## Running Unit tests
 - To run unit tests from inside the container, SSH into the albums container with `docker exec -it albums /bin/bash`
 - Once inside, from the `weecare` directory, run `sh albums/tests/unit/run_unit_tests.sh`

## Postman Collection
- The Albums API have been exported as a Postman Collection for your convenience 😬 The Collection also has docs on how the API works, but in case you don't use Postman, see the Endpoints section below.

## Endpoints

### Health Check
#### Request
`GET /health`
```
curl -i -H 'Accept: application/json' http://127.0.0.1:80/health
```
#### Response
```
HTTP/1.1 200 OK
Server: Werkzeug/2.2.3 Python/3.11.2
Date: Wed, 15 Mar 2023 03:59:59 GMT
Content-Type: application/json
Content-Length: 48
Connection: close

"The Albums server is up and running. Awesome!"
```
<br/>


### User Creation
#### Request
`POST /api/users/register`
```
curl --location --request POST 'http://127.0.0.1:80/api/users/register' --header 'Content-Type: application/json' --data-raw '{"username": "test_user", "password": "test_password"}'
```
#### Response
`User successfully created`
<br/>


### User Login
#### Request
`POST /api/users/login`
```
curl --location --request POST 'http://127.0.0.1:80/api/users/login' --header 'Authorization: Basic dGVzdF91c2VyOnRlc3RfcGFzc3dvcmQ='
```
#### Response
`{"Token":"ABCDEFGHIJKLMNOPQRSTUVWXYZ"}`
<br/>


### Get Albums
#### Request
`GET /api/albums/`
```
curl --location --request GET 'http://127.0.0.1:80/api/albums/?sort_by=album_id&order_by=asc'
```
#### Response
```
[
    {
        "artist_id": 20044,
        "created_at": "2023-03-15T03:08:34.425919",
        "genre_id": 14,
        "id": 952887,
        "images": [
            "https://is5-ssl.mzstatic.com/image/thumb/Music115/v4/dd/2b/8d/dd2b8d84-e032-94d2-473a-3f8efd18fe36/dj.rwfgroxa.jpg/55x55bb.png",
            "https://is2-ssl.mzstatic.com/image/thumb/Music115/v4/dd/2b/8d/dd2b8d84-e032-94d2-473a-3f8efd18fe36/dj.rwfgroxa.jpg/60x60bb.png",
            "https://is4-ssl.mzstatic.com/image/thumb/Music115/v4/dd/2b/8d/dd2b8d84-e032-94d2-473a-3f8efd18fe36/dj.rwfgroxa.jpg/170x170bb.png"
        ],
        "label_rights": "℗ 1998 Warner Records Inc.",
        "name": "Ray of Light",
        "price": {
            "amount": "4.99",
            "currency": "USD"
        },
        "release_date": "1998-02-22T00:00:00",
        "song_count": 13,
        "title": "Ray of Light - Madonna",
        "updated_at": "2023-03-15T03:08:34.425919",
        "url": "https://music.apple.com/us/album/ray-of-light/952887?uo=2"
    },
    ...
]
```
<br/>


### Create Album
#### Request
`POST /api/albums`
```
curl --location --request POST 'http://127.0.0.1:80/api/albums/' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MiwiZXhwIjoxNjc4ODU3MDA1fQ.iFvwGGg79rjFqUlkIvMDEwwXVxm67uSaq-62hCK6r1Y' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name": "David'\''s Album",
    "images": [
        "https://images.saymedia-content.com/.image/t_share/MTc0NDkxNzgyMzYzNDg5NjQw/vinyl-to-paper-how-to-write-an-album-review.jpg"
    ],
    "song_count": 10,
    "price": {
        "amount": 10.99,
        "currency": "USD"
    },
    "label_rights": "David Music Entertainment",
    "title": "Album Title",
    "url": "https://music.apple.com/us/album/red-taylors-version-a-message-from-taylor/1590368448",
    "artist_id": 159260351,
    "genre_id": 14,
    "release_date": "2023-02-14 00:00:00"
}'
```
#### Response
```
{
    "artist_id": 159260351,
    "created_at": "2023-03-15T04:06:47",
    "genre_id": 14,
    "id": 2,
    "images": [
        "https://images.saymedia-content.com/.image/t_share/MTc0NDkxNzgyMzYzNDg5NjQw/vinyl-to-paper-how-to-write-an-album-review.jpg"
    ],
    "label_rights": "David Music Entertainment",
    "name": "David's Album",
    "price": {
        "amount": 10.99,
        "currency": "USD"
    },
    "release_date": "2023-02-14T00:00:00",
    "song_count": 10,
    "title": "Album Title",
    "updated_at": "2023-03-15T04:06:47",
    "url": "https://music.apple.com/us/album/red-taylors-version-a-message-from-taylor/1590368448"
}
```
<br/>


### Update Album
#### Request
`PUT /api/albums/{album_id}`
```
curl --location --request PUT 'http://127.0.0.1:80/api/albums/1' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MiwiZXhwIjoxNjc4ODU3MDA1fQ.iFvwGGg79rjFqUlkIvMDEwwXVxm67uSaq-62hCK6r1Y' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name": "Test Album2",
    "images": [
        "https://images.saymedia-content.com/.image/t_share/MTc0NDkxNzgyMzYzNDg5NjQw/vinyl-to-paper-how-to-write-an-album-review.jpg"
    ],
    "song_count": 5,
    "price": {
        "amount": 5.99,
        "currency": "USD"
    },
    "label_rights": "Sony Music Entertainment",
    "title": "Album Title",
    "url": "https://music.apple.com/us/album/red-taylors-version-a-message-from-taylor/1590368448",
    "artist_id": 159260351,
    "genre_id": 14,
    "release_date": "2023-02-14 00:00:00"
}'
```
#### Response
```
{
    "artist_id": 159260351,
    "created_at": "2023-03-15T04:06:47",
    "genre_id": 14,
    "id": 2,
    "images": [
        "https://images.saymedia-content.com/.image/t_share/MTc0NDkxNzgyMzYzNDg5NjQw/vinyl-to-paper-how-to-write-an-album-review.jpg"
    ],
    "label_rights": "Sony Music Entertainment",
    "name": "Test Album2",
    "price": {
        "amount": 5.99,
        "currency": "USD"
    },
    "release_date": "2023-02-14T00:00:00",
    "song_count": 5,
    "title": "Album Title",
    "updated_at": "2023-03-15T04:06:47",
    "url": "https://music.apple.com/us/album/red-taylors-version-a-message-from-taylor/1590368448"
}
```
<br/>


### Delete Album
#### Request
`DELETE /api/albums{album_id}`
```
curl --location --request DELETE 'http://127.0.0.1:80/api/albums/2' --header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MiwiZXhwIjoxNjc4ODU3MDA1fQ.iFvwGGg79rjFqUlkIvMDEwwXVxm67uSaq-62hCK6r1Y'
```
### Response
`"Successfully deleted Album with ID 2"`
<br/>