#!/usr/bin/env python3
from typing import Optional, Dict
from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from sqlalchemy import asc
from marshmallow.validate import Length, Regexp, Range

from model import Hug, Pony


class PonySchema(SQLAlchemyAutoSchema):
    first_hug = fields.Method("get_first_hug", dump_only=True)
    hugs = fields.Pluck('HugSchema', 'player', many=True, dump_only=True)
    key = fields.String(required=True, validate=[Length(equal=10), Regexp(r"^[0-9A-Z]*$")])
    order = fields.Integer(required=True, validate=Range(min=1))

    def get_first_hug(self, pony) -> Optional[Dict[str, str]]:
        first_hug_for_this_pony = Hug.query.filter_by(pony=pony).order_by(asc('timestamp')).first()

        if not first_hug_for_this_pony:
            return None

        return {
            "playername": first_hug_for_this_pony.player.name,
            "timestamp": first_hug_for_this_pony.timestamp.isoformat()  # need string
        }

    class Meta:
        load_only = ['key']
        dump_only = ['id']
        model = Pony
        include_relationships = True
        load_instance = True
        include_fk = True
