from dataclasses import dataclass
from datetime import datetime
from marshmallow import Schema, fields

from albums import db

@dataclass
class Genres(db.Model):
    id: int
    name: str
    created_at: datetime
    updated_at: datetime

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False) 
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

class GenreSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, allow_none=False)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)