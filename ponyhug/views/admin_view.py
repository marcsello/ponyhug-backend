#!/usr/bin/env python3
from flask import abort, current_app, request, jsonify
from flask_classful import FlaskView, route

from utils import ponytoken_required, this_player, json_required, anyadmin_required
from flask_jwt_extended import create_access_token

from model import db, Player
from schemas import PonySchema, PlayerSchema, LoginSuccessSchema
from sqlalchemy import func


class AdminView(FlaskView):
    pony_schema = PonySchema(many=False)
    ponies_schema = PonySchema(many=True)

    login_success_schema = LoginSuccessSchema(many=False)

    player_schema = PlayerSchema(many=False)

    @ponytoken_required
    @json_required
    @route('/promote', methods=['POST'])
    def promote(self):

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

    @anyadmin_required
    @route('/impersonate', methods=['POST'])
    def impersonate(self):
        params = request.get_json()
        playername = params.get("playername")

        player = Player.query.filter(name=playername).first_or_404("No such player")

        response = {
            "jwt": create_access_token(identity=player.id),
            "name": playername,
            "is_admin": player.is_admin,
            "faction": player.faction.id
        }

        return jsonify(self.login_success_schema.dump(response)), 200

    @anyadmin_required
    @route('/crashtest', methods=['POST'])
    def crashtest(self):
        a = 1 / 0
        return jsonify({"a": a}), 200

    @anyadmin_required
    def faction_members(self):
        counters = db.session.query(Player.faction_id, func.count(Player.faction_id)).group_by(Player.faction_id).all()
        return jsonify(dict(counters))
