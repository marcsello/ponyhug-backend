#!/usr/bin/env python3
from flask import request, abort
from flask_classful import FlaskView
from utils import json_required
from flask_jwt_simple import create_jwt
import bleach

from model import db, Player


class RegisterView(FlaskView):

	@json_required
	def post(self):

		params = request.get_json()
		playername = params.get("playername")

		if not playername:
			abort(422, "Missing field")

		# sanitize input
		playername = bleach.clean(playername)[:50] # <- this should not be hardcoded here

		player = Player.query.filter_by(name=playername).first()

		if player:
			abort(403, "Name already in use")

		player = Player(name=playername)

		db.session.add(player)
		db.session.commit()

		return {"jwt": create_jwt(identity=player.id), "playername" : playername}, 201
