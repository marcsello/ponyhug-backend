#!/usr/bin/env python3
from .db import db
from sqlalchemy.sql import func


class Player(db.Model):

	id = db.Column(db.Integer, primary_key=True, auto_increment=True)
	name = db.Column(db.String(50), unique=True, nullable=False)

	registered = db.Column(db.TIMESTAMP, nullable=False, server_default=func.now())
