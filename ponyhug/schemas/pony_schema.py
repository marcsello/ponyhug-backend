#!/usr/bin/env python3
from typing import Optional, Dict
from marshmallow import fields
from marshmallow_sqlalchemy import ModelSchema
from sqlalchemy import asc

from model import Hug, Pony


class PonySchema(ModelSchema):
    first_hug = fields.Method("get_first_hug", dump_only=True)
    hugs = fields.Pluck('HugSchema', 'player', many=True, dump_only=True)

    def get_first_hug(self, pony) -> Optional[Dict[str, str]]:
        first_hug_for_this_pony = Hug.query.filter_by(pony=pony).order_by(asc('timestamp')).first()

        if not first_hug_for_this_pony:
            return None

        return {
            "playername": first_hug_for_this_pony.player.name,
            "timestamp": first_hug_for_this_pony.timestamp
        }

    class Meta:
        load_only = ['key']
        model = Pony
