#!/usr/bin/env python3
from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from model import Faction, Player


class FactionSchema(SQLAlchemyAutoSchema):

    class Meta:
        dump_only = ['id']
        model = Faction
        include_relationships = True
        load_instance = True
        include_fk = False
