#!/usr/bin/env python3
from .db import db
from sqlalchemy.sql import func


class Timeframe(db.Model):
    id = db.Column(db.Integer, primary_key=True, auto_increment=True)
    begin_timestamp = db.Column(db.TIMESTAMP, nullable=False, server_default=func.now())
    end_timestamp = db.Column(db.TIMESTAMP, nullable=False)
