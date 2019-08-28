#!/usr/bin/env python3
from marshmallow_sqlalchemy import ModelSchema, fields
from model import Hug


class HugSchema(ModelSchema):

	player = fields.Pluck('PlayerSchema', 'name', many=False)
	pony = fields.Nested('PonySchema', many=False, only=['id', 'name', 'image'])

	class Meta:
		model = Hug
