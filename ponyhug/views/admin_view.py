#!/usr/bin/env python3
from flask import abort, current_app, request
from .api import api
from flask_restx import Resource
from utils import ponytoken_required, this_player, json_required, anyadmin_required
from flask_jwt_extended import create_access_token

from model import db, Player
from schemas import PonySchema, PlayerSchema, LoginSuccessSchema
from sqlalchemy import func

ns = api.namespace('admin', description="Administrative operations")

_login_success_schema = LoginSuccessSchema(many=False)


@ns.route("/promote")
class AdminPromoteResource(Resource):
    @ponytoken_required
    @json_required
    def post(self):

        player = this_player()

        if player.is_admin:
            return abort(409, "This player is already an admin")

        params = request.get_json()
        adminkey = params.get("key")

        if adminkey != current_app.config['ADMIN_KEY']:
            return abort(401, "Invalid key")

        player.is_admin = True
        db.session.add(player)
        db.session.commit()

        return '', 204


@ns.route("/impersonate")
class AdminImpersonateResource(Resource):
    @anyadmin_required
    def post(self):
        params = request.get_json()
        playername = params.get("playername")

        player = Player.query.filter(name=playername).first_or_404("No such player")

        response = {
            "jwt": create_access_token(identity=player.id),
            "name": playername,
            "is_admin": player.is_admin,
            "faction": player.faction.id
        }

        return _login_success_schema.dump(response), 200


@ns.route("/crashtest")
class AdminCrashTestResource(Resource):
    @anyadmin_required
    def post(self):
        a = 1 / 0
        return {"a": a}, 200


@ns.route("/faction_members")
class AdminFactionMembersResource(Resource):
    @anyadmin_required
    def get(self):
        counters = db.session.query(Player.faction_id, func.count(Player.faction_id)).group_by(Player.faction_id).all()
        return dict(counters)
