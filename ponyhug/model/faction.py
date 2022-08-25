#!/usr/bin/env python3
from .db import db


class Faction(db.Model):
    id = db.Column(db.Integer, primary_key=True, auto_increment=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    # Must use values that are defined on the frontend
    color_scheme = db.Column(db.String(15), nullable=False)
    icon_set = db.Column(db.String(15), nullable=False)
