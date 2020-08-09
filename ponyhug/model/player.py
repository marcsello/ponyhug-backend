#!/usr/bin/env python3
from flask_security import UserMixin
from sqlalchemy.sql import func
from .db import db
from .role import Role


roles_users = db.Table(
    "roles_users",
    db.Column("user_id", db.Integer(), db.ForeignKey("user.id")),
    db.Column("role_id", db.Integer(), db.ForeignKey("role.id")),
)


class Player(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, auto_increment=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    registered = db.Column(db.TIMESTAMP, nullable=False, server_default=func.now())

    email = db.Column(db.String(255), unique=True)
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship(
        Role, secondary=roles_users, backref=db.backref("users", lazy="dynamic")
    )



