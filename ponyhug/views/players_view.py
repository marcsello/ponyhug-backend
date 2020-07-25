#!/usr/bin/env python3
from flask import abort, jsonify, request
from flask_classful import FlaskView
from utils import ponytoken_required, json_required
from flask_jwt_simple import create_jwt

from model import db, Player
from schemas import PlayerSchema
import bleach


class PlayersView(FlaskView):
    player_schema = PlayerSchema(many=False)
    players_schema = PlayerSchema(many=True)

    @ponytoken_required
    def index(self):
        players = Player.query.all()

        return jsonify(self.players_schema.dump(players)), 200

    @ponytoken_required
    def get(self, name: str):
        player = Player.query.filter_by(name=name).first()

        if not player:
            abort(404)

        return jsonify(self.player_schema.dump(player)), 200

    @json_required
    def post(self):

        params = request.get_json()
        playername = params.get("playername")

        if not playername:
            abort(422, "Missing field")

        # sanitize input
        playername_maxlen = Player.name.property.columns[0].type.length
        playername = bleach.clean(playername, tags=[])[:playername_maxlen]  # cut to approriate length
        # Length limiting is required here as SQLAlchemy does not validate the length of a field
        # If a database engine does not validate length (Like sqlite) that would lead to issues

        player = Player.query.filter_by(name=playername).first()

        if player:
            abort(409, "Name already in use")

        player = Player(name=playername)

        db.session.add(player)
        db.session.commit()

        return {"jwt": create_jwt(identity=player.id), "playername": playername}, 201
