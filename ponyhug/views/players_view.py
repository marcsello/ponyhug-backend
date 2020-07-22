#!/usr/bin/env python3
from flask import abort, jsonify
from flask_classful import FlaskView
from utils import ponytoken_required

from model import Player
from schemas import PlayerSchema


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
