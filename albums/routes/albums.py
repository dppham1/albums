from datetime import datetime

from flask import Blueprint, jsonify, request
from marshmallow import ValidationError

from albums import db
from albums.models.albums import Albums, AlbumSchema
from albums.auth import token_required


blueprint = Blueprint("albums", __name__, url_prefix="/api/albums")


@blueprint.route("/", methods=["GET"])
def get_albums():
    if request.method == "GET":
        # filter
        filters = {}
        filter_params = {"name", "artist_id", "genre_id"}
        for param in filter_params:
            if request.args.get(param):
                filters[param] = request.args.get(param)

        # sort
        sort_by = request.args.get("sort_by")
        if sort_by and hasattr(Albums, sort_by):
            sort_column = getattr(Albums, sort_by)
        else:
            sort_column = Albums.id

        # order
        if request.args.get("order_by") == "desc":
            sort_column = sort_column.desc()
        else:
            sort_column = sort_column.asc()
        
        # pagination
        page = int(request.args.get("page")) if (request.args.get("page") and request.args.get("page").isdigit()) else 1
        per_page = 5

        # find records
        albums = Albums.query.filter_by(**filters).order_by(sort_column).paginate(page=page, per_page=per_page, error_out=False)
        response_data = AlbumSchema(many=True).dump(albums)

        return jsonify(response_data), 200


@blueprint.route("/<int:album_id>", methods=["PUT"])
@token_required
def update_album(album_id):
    if request.method == "PUT":
        album_record = Albums.query.filter_by(id=album_id).first()
        if album_record:
            try:
                album_schema = AlbumSchema()
                album_data = album_schema.load(request.json)
            except ValidationError as e:
                return jsonify(e.messages), 400

            for attr, value in album_data.items():
                setattr(album_record, attr, value)

            db.session.commit()

            response_data = album_schema.dump(album_record)
            return jsonify(response_data), 200
        else:
            return jsonify(f"Album with ID {album_id} not found"), 404


@blueprint.route("/", methods=["POST"])
@token_required
def create_album():
    if request.method == "POST":
        try:
            album_schema = AlbumSchema()
            album_data = album_schema.load(request.json)
        except ValidationError as e:
            return jsonify(e.messages), 400

        new_album = Albums(**album_data)
        new_album.created_at = datetime.utcnow().replace(microsecond=0)
        new_album.updated_at = datetime.utcnow().replace(microsecond=0)

        try:
            db.session.add(new_album)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 400

        response_data = album_schema.dump(new_album)

        return jsonify(response_data)


@blueprint.route("/<int:album_id>", methods=["DELETE"])
@token_required
def delete_album(album_id):
    if request.method == "DELETE":
        album_record = Albums.query.filter_by(id=album_id).first()
        if album_record:
            try:
                db.session.delete(album_record)
                db.session.commit()
            except Exception as e:
                return jsonify(e.messages), 400

            return jsonify(f"Successfully deleted Album with ID {album_id}"), 200
        else:
            return jsonify(f"Album with ID {album_id} not found"), 404
