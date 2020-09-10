#!/usr/bin/env python3
from flask import abort, jsonify, current_app, request
from flask_classful import FlaskView, route

from utils import ponytoken_required, this_player, json_required, admin_required
from flask_jwt_simple import create_jwt

from model import db, Player


class AdminView(FlaskView):

    @ponytoken_required
    @json_required
    @route('/promote', methods=['POST'])
    def promote(self):

        player = this_player()

        if player.is_admin:
            abort(409, "This player is already an admin")

        params = request.get_json()
        adminkey = params.get("key")

        if adminkey != current_app.config['ADMIN_KEY']:
            abort(401, "Invalid key")

        player.is_admin = True
        db.session.add(player)
        db.session.commit()

        return '', 204

    @json_required
    @route('/impersonate', methods=['POST'])
    def impersonate(self):

        params = request.get_json()
        adminkey = params.get("key")
        playername = params.get("playername")

        if adminkey != current_app.config['ADMIN_KEY']:
            abort(401, "Invalid key")

        player = Player.query.filter(name=playername).first()

        if not player:
            abort(404, "No such player")

        return {"jwt": create_jwt(identity=player.id), "playername": playername, "is_admin": False}, 200