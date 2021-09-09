#!/usr/bin/env python3
from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from model import Hug


class HugSchema(SQLAlchemyAutoSchema):
    player = fields.Pluck('PlayerSchema', 'name', many=False)
    pony = fields.Nested('PonySchema', many=False)

    class Meta:
        model = Hug
        include_relationships = True
        load_instance = True
        include_fk = False
