from dataclasses import dataclass
from datetime import datetime
from marshmallow import Schema, fields

from albums import db


@dataclass
class Users(db.Model):
    id: int
    username: str
    password: str
    created_at: datetime
    updated_at: datetime

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(50))
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True, allow_none=False)
    password = fields.Str(required=True, allow_none=False)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
