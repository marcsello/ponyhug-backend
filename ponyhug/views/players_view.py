#!/usr/bin/env python3
from flask import abort, jsonify, request
from flask_classful import FlaskView

from utils import json_required, ponytoken_required, this_player, timeframe_required, anyadmin_required
from flask_jwt_simple import create_jwt

from model import db, Player
from schemas import PlayerSchema, LoginSuccessSchema
import sqlalchemy.exc
import bleach


class PlayersView(FlaskView):
    player_schema = PlayerSchema(many=False)
    players_schema = PlayerSchema(many=True)

    login_success_schema = LoginSuccessSchema(many=False)

    @anyadmin_required
    def index(self):
        players = Player.query.all()
        return jsonify(self.players_schema.dump(players)), 200

    @anyadmin_required
    def get(self, name: str):
        player = Player.query.filter_by(name=name).first_or_404()
        return jsonify(self.player_schema.dump(player)), 200

    @ponytoken_required
    def me(self):
        return jsonify(self.player_schema.dump(this_player())), 200

    @json_required
    @timeframe_required
    def post(self):

        params = request.get_json()
        playername = params.get("playername")

        if not playername:
            return abort(422, "Missing field")

        # sanitize input
        playername_maxlen = Player.name.property.columns[0].type.length
        playername = bleach.clean(playername, tags=[])[:playername_maxlen]  # cut to approriate length
        # Length limiting is required here as SQLAlchemy does not validate the length of a field
        # If a database engine does not validate length (Like sqlite) that would lead to issues

        player = Player(name=playername)

        db.session.add(player)

        try:
            db.session.commit()
        except sqlalchemy.exc.IntegrityError:
            return abort(409, "Name already in use")

        response = {
            "jwt": create_jwt(identity=player.id),
            "name": playername,
            "is_admin": player.is_admin
        }

        return jsonify(self.login_success_schema.dump(response)), 201
