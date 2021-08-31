#!/usr/bin/env python3
from .db import db


class Faction(db.Model):
    id = db.Column(db.Integer, primary_key=True, auto_increment=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    accent = db.Column(db.String(7), nullable=False)
    variant = db.Column(db.String(10), nullable=False)  # yes, bootstrap variant :/

    icon_lg = db.Column(db.String(50), nullable=False)
    icon_sm = db.Column(db.String(50), nullable=False)
