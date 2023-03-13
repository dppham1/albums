from flask import (
    Flask,
    jsonify,
    request
)
from flask_sqlalchemy import SQLAlchemy

from albums.config import DB_URL, JWT_SECRET_KEY


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY

db = SQLAlchemy(app)

from .resources import albums, users
app.register_blueprint(albums.blueprint)
app.register_blueprint(users.blueprint)

@app.route('/health', methods=['GET'])
def health():
    if request.method == 'GET':
        return jsonify('The Albums server is up and running. Awesome!'), 200