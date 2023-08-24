#!/usr/bin/env python3
from sqlalchemy import asc, desc
from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from model import Player

from model import Hug


class PlayerSchema(SQLAlchemyAutoSchema):
    hug_counter = fields.Method("get_hug_count", dump_only=True)
    playtime = fields.Method("get_playtime", dump_only=True)

    def get_hug_count(self, player) -> int:
        return Hug.query.filter_by(player=player).count()

    def get_playtime(self, player):
        first_hug = Hug.query.filter_by(player=player).order_by(asc('timestamp')).first()
        last_hug = Hug.query.filter_by(player=player).order_by(desc('timestamp')).first()

        if not (first_hug and last_hug):
            return None

        return (last_hug.timestamp - first_hug.timestamp).total_seconds()

    class Meta:
        # Regular players won't be able to access other player's schema, so we can safely dump the is_admin
        exclude = [
            'hugs'
        ]
        model = Player
        include_relationships = True
        load_instance = True
        include_fk = False
