#!/usr/bin/env python3
from .db import db
from sqlalchemy.sql import func


class Hug(db.Model):
	id = db.Column(db.Integer, primary_key=True, auto_increment=True)
	timestamp = db.Column(db.TIMESTAMP, nullable=False, server_default=func.now())

	pony_id = db.Column(db.Integer, db.ForeignKey("pony.id"), nullable=False)
	pony = db.relationship("Pony", backref=db.backref("hugs", lazy=True))

	player_id = db.Column(db.Integer, db.ForeignKey("player.id"), nullable=False)
	player = db.relationship("Player", backref=db.backref("hugs", lazy=True))