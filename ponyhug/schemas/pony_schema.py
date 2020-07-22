#!/usr/bin/env python3
from typing import Optional
from marshmallow import fields
from marshmallow_sqlalchemy import ModelSchema
from sqlalchemy import asc

from model import Hug, Player, Pony


class PonySchema(ModelSchema):
    first_hugger = fields.Method("get_first_hugged_by", dump_only=True)
    hugs = fields.Pluck('HugSchema', 'player', many=True)

    def get_first_hugged_by(self, pony) -> Optional[Player]:
        first_hug_for_this_pony = Hug.query.filter_by(pony=pony).order_by(asc('timestamp')).first()

        if not first_hug_for_this_pony:
            return None

        return first_hug_for_this_pony.player.name

    class Meta:
        exclude = ['key']
        model = Pony
