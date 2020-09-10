#!/usr/bin/env python3
from flask import abort, jsonify, current_app, request
from flask_classful import FlaskView, route

from marshmallow import ValidationError

from utils import ponytoken_required, this_player, json_required, anyadmin_required, adminkey_required, admintoken_required
from flask_jwt_simple import create_jwt

from model import db, Player, Pony
from schemas import PonySchema


class AdminView(FlaskView):
    pony_schema = PonySchema(many=False)
    ponies_schema = PonySchema(many=True)

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

    @anyadmin_required
    @route('/impersonate', methods=['POST'])
    def impersonate(self):
        params = request.get_json()
        playername = params.get("playername")

        player = Player.query.filter(name=playername).first()

        if not player:
            abort(404, "No such player")

        return {"jwt": create_jwt(identity=player.id), "playername": playername, "is_admin": player.is_admin}, 200

    @anyadmin_required
    @json_required
    @route('/ponies', methods=['POST'])
    def createpony(self):
        params = request.get_json()
        try:
            pony = self.pony_schema.load(params, session=db.session)
        except ValidationError as e:
            abort(400, str(e))

        db.session.add(pony)
        db.session.commit()
        return jsonify(self.pony_schema.dump(pony)), 201

    @anyadmin_required
    @route('/ponies/<ponyid>', methods=['DELETE'])
    def deletepony(self, ponyid: int):
        Pony.query.filter_by(id=ponyid).delete()
        db.session.commit()
        return '', 204

    @anyadmin_required
    @route('/ponies', methods=['GET'])
    def listponies(self):
        ponies = Pony.query.all()
        return jsonify(self.ponies_schema.dump(ponies)), 201
