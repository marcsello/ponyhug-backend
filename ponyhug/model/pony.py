#!/usr/bin/env python3
from .db import db


class Pony(db.Model):

	id = db.Column(db.Integer, primary_key=True, auto_increment=True)
	key = db.Column(db.String(10), unique=True, nullable=False)
	title = db.Column(db.String(255), unique=True, nullable=False)
	source = db.Column(db.String(255), nullable=True)
	image = db.Column(db.String(255), unique=True)
