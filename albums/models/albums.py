from datetime import datetime
from dataclasses import dataclass
from marshmallow import Schema, fields, ValidationError

from albums import db


@dataclass
class Albums(db.Model):
    id: int
    name: str
    images: list
    song_count: int
    price: dict
    label_rights: str
    title: str
    url: str
    artist_id: int
    genre_id: int
    release_date: datetime
    created_at: datetime
    updated_at: datetime

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False) 
    images = db.Column(db.Text)
    song_count = db.Column(db.Integer)
    price = db.Column(db.JSON)
    label_rights = db.Column(db.String(100))
    title = db.Column(db.String(50))
    url = db.Column(db.String(50))
    artist_id = db.Column(db.Integer)
    genre_id = db.Column(db.Integer)
    release_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

class PriceField(fields.Field):
    """
    Custom Validator for "price" field of Albums object
    """
    def _deserialize(self, value, attr, data, **kwargs):
        if isinstance(value.get('amount'), int) or isinstance(value.get('amount'), float) and isinstance(value.get('currency'), str):
            return value
        else:
            raise ValidationError("Price object's 'amount' field should be an int or double and 'currency' field should be a str")

class AlbumSchema(Schema):  
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, allow_none=False)
    images = fields.List(fields.String(), required=True, allow_none=False)
    song_count = fields.Int(required=True, allow_none=False)
    price = PriceField(required=True, allow_none=False)
    label_rights = fields.Str(required=True, allow_none=False)
    title = fields.Str(required=True, allow_none=False)
    url = fields.Str(required=True, allow_none=False)
    artist_id = fields.Int(required=True, allow_none=False)
    genre_id = fields.Int(required=True, allow_none=False)
    release_date = fields.DateTime(required=True, allow_none=False)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)