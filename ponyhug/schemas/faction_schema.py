#!/usr/bin/env python3
from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from model import Faction, Hug, Player


class FactionSchema(SQLAlchemyAutoSchema):
    hug_count = fields.Method("get_hug_count", dump_only=True)
    member_count = fields.Method("get_member_count", dump_only=True)

    def get_hug_count(self, faction) -> int:
        return Hug.query.filter_by(faction=faction).count()

    def get_member_count(self, faction) -> int:
        return Player.query.filter_by(faction=faction).count()

    class Meta:
        dump_only = ['id']
        model = Faction
        include_relationships = True
        load_instance = True
        include_fk = True
