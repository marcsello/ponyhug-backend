#!/usr/bin/env python3
from marshmallow import fields
from marshmallow_sqlalchemy import ModelSchema
from model import Player

from model import Hug


class PlayerSchema(ModelSchema):
    hug_counter = fields.Method("get_hug_count", dump_only=True)

    def get_hug_count(self, player):
        return Hug.query.filter_by(player=player).count()

    class Meta:
        exclude = ['id', 'hugs']
        model = Player
