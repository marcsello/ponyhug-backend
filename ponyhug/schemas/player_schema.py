#!/usr/bin/env python3
from marshmallow_sqlalchemy import ModelSchema
from model import Player


class PlayerSchema(ModelSchema):

	class Meta:
		model = Player
