import os

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from albums.config import Config, TestConfig


app = Flask(__name__)
if os.environ.get("ENV") == "test":
    app.config.from_object(TestConfig)
else:
    app.config.from_object(Config)

db = SQLAlchemy(app=app)

from .routes import albums, users

app.register_blueprint(albums.blueprint)
app.register_blueprint(users.blueprint)


@app.route("/health", methods=["GET"])
def health():
    if request.method == "GET":
        return jsonify("The Albums server is up and running. Awesome!"), 200
