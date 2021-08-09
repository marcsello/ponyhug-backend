#!/usr/bin/env python3
from datetime import datetime
import tzlocal

from flask import abort, jsonify, request
from flask_classful import FlaskView

from utils import json_required, ponytoken_required, this_player
from flask_jwt_simple import create_jwt

from model import db, Player, Timeframe
from schemas import PlayerSchema
import sqlalchemy.exc
import bleach


class PlayersView(FlaskView):
    player_schema = PlayerSchema(many=False)

    @ponytoken_required
    def me(self):
        return jsonify(self.player_schema.dump(this_player())), 200

    @json_required
    def post(self):

        now = datetime.now(tz=tzlocal.get_localzone())
        timeframe = Timeframe.query.filter(
            db.and_(Timeframe.begin_timestamp <= now, Timeframe.end_timestamp >= now)
        ).first()

        if not timeframe:
            return abort(423, "No active timeframe")

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

        return jsonify({
            "jwt": create_jwt(identity=player.id),
            "name": playername,
            "is_admin": player.is_admin
        }), 201
