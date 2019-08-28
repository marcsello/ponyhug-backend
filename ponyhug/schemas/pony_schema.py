#!/usr/bin/env python3
from marshmallow import fields
from marshmallow_sqlalchemy import ModelSchema
from model import Pony


class PonySchema(ModelSchema):

	first_hugger = fields.Method("get_first_hugged_by", dump_only=True)

	def get_first_hugged_by(self, pony):
		pass

	class Meta:
		exclude = ['key']
		model = Pony
