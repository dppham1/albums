import jwt

from datetime import datetime, timedelta
from sqlalchemy.exc import IntegrityError


from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from werkzeug.security import generate_password_hash, check_password_hash

from albums import db
from albums.config import JWT_SECRET_KEY
from albums.models.users import Users, UserSchema

blueprint = Blueprint("users", __name__, url_prefix="/api/users")


@blueprint.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return (
            jsonify({"status": "A Username and Password is required to register"}),
            400,
        )

    username = username.lower()
    hashed_password = generate_password_hash(password, method="sha256")

    try:
        user_schema = UserSchema()
        user_schema.load(data)
    except ValidationError as e:
        return jsonify(e.messages), 400

    new_user = Users(username=username, password=hashed_password)
    new_user.created_at = datetime.utcnow().replace(microsecond=0)
    new_user.updated_at = datetime.utcnow().replace(microsecond=0)

    try:
        db.session.add(new_user)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"status": "Username already exists"}), 400

    return jsonify({"status": "User successfully created", "user_id": new_user.id}), 200


@blueprint.route("/login", methods=["POST"])
def login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return jsonify("A Username and Password is required to login"), 401

    user = Users.query.filter_by(username=auth.username.lower()).first()
    if not user:
        return jsonify({"status": "User does not exist"}), 400

    if check_password_hash(user.password, auth.password):
        payload = {"id": user.id, "exp": datetime.utcnow() + timedelta(minutes=120)}
        token = jwt.encode(payload, JWT_SECRET_KEY, algorithm="HS256")
        return jsonify({"Token": token}), 200

    return (
        jsonify(
            {"status": "Could not authenticate the User with the given credentials"}
        ),
        401,
    )


@blueprint.route("/<int:user_id>", methods=["DELETE"])
def delete(user_id):
    if request.method == "DELETE":
        user_record = Users.query.filter_by(id=user_id).first()
        if user_record:
            try:
                db.session.delete(user_record)
                db.session.commit()
            except Exception as e:
                return jsonify(e.messages), 400

            return (
                jsonify({"status": f"Successfully deleted User with ID {user_id}"}),
                200,
            )
        else:
            return jsonify({"status": f"User with ID {user_id} not found"}), 404
