#!/usr/bin/env python3
from .db import db
from .player import Player
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin


class OAuth(OAuthConsumerMixin, db.Model):
    provider_user_id = db.Column(db.String(256), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(Player.id), nullable=False)
    user = db.relationship(Player)
