#!/usr/bin/env python3
from marshmallow import fields, Schema, RAISE


class LoginSuccessSchema(Schema):
    jwt = fields.String(required=True)
    name = fields.String(required=True)
    is_admin = fields.Boolean(required=True)

    class Meta:
        dump_only = ['jwt', 'name', 'is_admin']
        unknown = RAISE
