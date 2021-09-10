#!/usr/bin/env python3
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from model import Timeframe


class TimeframeSchema(SQLAlchemyAutoSchema):

    class Meta:
        model = Timeframe
        include_relationships = True
        load_instance = True
        include_fk = False
