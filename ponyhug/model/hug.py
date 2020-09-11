#!/usr/bin/env python3
from .db import db
from sqlalchemy.sql import func


class Hug(db.Model):
    # The following makes sure that only one player-pony pair exists
    __table_args__ = (
        db.UniqueConstraint('pony_id', 'player_id', name='unique_pony_player'),
    )

    id = db.Column(db.Integer, primary_key=True, auto_increment=True)
    timestamp = db.Column(db.DateTime(timezone=True), nullable=False, server_default=func.now())

    pony_id = db.Column(db.Integer, db.ForeignKey("pony.id", ondelete="CASCADE"), nullable=False)
    pony = db.relationship("Pony", backref=db.backref("hugs", lazy=True))

    player_id = db.Column(db.Integer, db.ForeignKey("player.id", ondelete="CASCADE"), nullable=False)
    player = db.relationship("Player", backref=db.backref("hugs", lazy=True))
