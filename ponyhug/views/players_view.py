#!/usr/bin/env python3
from flask import abort, request, current_app
from .api import api
from flask_restx import Resource

from utils import json_required, ponytoken_required, this_player, timeframe_required, anyadmin_required
from flask_jwt_extended import create_access_token

from model import db, Player
from schemas import PlayerSchema, LoginSuccessSchema
from sqlalchemy import func
import sqlalchemy.exc
import bleach

_player_schema = PlayerSchema(many=False)
_players_schema = PlayerSchema(many=True)

_login_success_schema = LoginSuccessSchema(many=False)

ns = api.namespace("players", description="Players")


@ns.route("")
class PlayersResource(Resource):

    @anyadmin_required
    def get(self):
        players = Player.query.all()
        return _players_schema.dump(players), 200

    @json_required
    @timeframe_required
    def post(self):

        # It seems like that validating, cleaning etc. isn't really solvable using marshmallow

        params = request.get_json()
        playername = params.get("name")

        if not playername:
            return abort(422, "Missing field")

        # sanitize input
        playername_maxlen = Player.name.property.columns[0].type.length
        # cut to appropriate length
        playername = bleach.clean(playername, tags=[], attributes={}).strip()[:playername_maxlen]
        # Length limiting is required here as SQLAlchemy does not validate the length of a field
        # If a database engine does not validate length (Like sqlite) that would lead to issues

        player = Player(name=playername)

        db.session.add(player)

        try:
            db.session.commit()
        except sqlalchemy.exc.IntegrityError:
            return abort(409, "Name already in use")

        current_app.logger.info(f"User {playername} registered.")

        response = {
            "jwt": create_access_token(identity=player.id),
            "name": player.name,
            "is_admin": player.is_admin
        }

        return _login_success_schema.dump(response), 201


@ns.route("/<int:id_>")
class PlayerResource(Resource):
    @anyadmin_required
    def get(self, id_: int):  # Using names would have caused problems with the /me endpoint
        player = Player.query.get_or_404(id_)
        return _player_schema.dump(player), 200


@ns.route("/me")
class PlayerMeResource(Resource):
    @ponytoken_required
    def get(self):
        return _player_schema.dump(this_player()), 200
