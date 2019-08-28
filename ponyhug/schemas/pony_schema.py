#!/usr/bin/env python3
from marshmallow_sqlalchemy import ModelSchema
from model import Pony


class PonySchema(ModelSchema):

	class Meta:
		exclude = ['key']
		model = Pony
