#!/usr/bin/env python3
from marshmallow_sqlalchemy import ModelSchema
from model import Timeframe


class TimeframeSchema(ModelSchema):

    class Meta:
        model = Timeframe
