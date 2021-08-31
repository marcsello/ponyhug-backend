#!/usr/bin/env python3
from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from model import Faction, Player


class FactionSchema(SQLAlchemyAutoSchema):
    member_count = fields.Method("get_member_count", dump_only=True)

    def get_member_count(self, faction) -> int:
        return Player.query.filter_by(faction=faction).count()

    class Meta:
        dump_only = ['id']
        model = Faction
        include_relationships = True
        load_instance = True
        include_fk = True
