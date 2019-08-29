#!/usr/bin/env python3
from flask import abort
from flask_jwt_simple import JWTManager, jwt_required, get_jwt_identity
from functools import wraps

from model import Player

try:
	from flask import _app_ctx_stack as ctx_stack
except ImportError:  # pragma: no cover
	from flask import _request_ctx_stack as ctx_stack

jwt = JWTManager()


def this_player() -> Player:

	return ctx_stack.top.current_player_object


def ponytoken_required(f):

	@jwt_required
	@wraps(f)
	def call(*args, **kwargs):

		playerid = get_jwt_identity()

		player = Player.query.get(playerid)

		if player:
			ctx_stack.top.current_player_object = player
			return f(*args, **kwargs)

		else:
			abort(500, "Player ID invalid")  # this really is a server error, since causing this error by the user should be caused by a forged requrest, which should not be possible because of the jwt

	return call

