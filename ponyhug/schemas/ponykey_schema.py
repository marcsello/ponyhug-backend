#!/usr/bin/env python3
from marshmallow import fields, Schema, RAISE
from marshmallow.validate import Length, Regexp


class PonykeySchema(Schema):
    key = fields.String(required=True, validate=[Length(equal=10), Regexp(r"^[0-9A-Z]$")])

    class Meta:
        load_only = ['key']
        unknown = RAISE
