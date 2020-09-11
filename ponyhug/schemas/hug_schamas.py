#!/usr/bin/env python3
from marshmallow import fields
from marshmallow_sqlalchemy import ModelSchema
from model import Hug


class HugSchema(ModelSchema):
    player = fields.Pluck('PlayerSchema', 'name', many=False)
    pony = fields.Nested('PonySchema', many=False, only=['id', 'name', 'image'])

    class Meta:
        model = Hug
