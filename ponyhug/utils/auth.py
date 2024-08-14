#!/usr/bin/env python3
from flask import abort, request, current_app

from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from functools import wraps

from model import Player

from flask import g  # request ctx got deprecated: https://flask.palletsprojects.com/en/2.3.x/changes/#version-2-2-0

jwt = JWTManager()


def this_player() -> Player:
    return g.ponyhug__current_player_object


def ponytoken_required(f):
    @jwt_required()
    @wraps(f)
    def call(*args, **kwargs):

        playerid = get_jwt_identity()

        player = Player.query.get(playerid)

        if player:
            g.ponyhug__current_player_object = player
            return f(*args, **kwargs)

        else:
            # this really is a server error, since causing this error by the user should be caused by a forged request,
            # which should not be possible because of the jwt
            current_app.logger.warning("A valid JWT token received but the Player ID is invalid!")
            return abort(500, "Player ID invalid")

    return call


def admintoken_required(f):
    @ponytoken_required
    @wraps(f)
    def call(*args, **kwargs):

        if this_player().is_admin:
            return f(*args, **kwargs)
        else:
            return abort(403, "Not admin")

    return call


def adminkey_required(f):
    @wraps(f)
    def call(*args, **kwargs):
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return abort(401, "Authorization header missing")

        try:
            auth_type, auth_key = auth_header.split(' ', 1)
        except ValueError:
            return abort(400, "Bad Authorization header. Expected value 'Key <KEY>'")

        if auth_type == 'Key' and auth_key == current_app.config['ADMIN_KEY']:
            current_app.logger.warning("Key auth used!")
            return f(*args, **kwargs)
        else:
            return abort(401, "Invalid key")

    return call


def anyadmin_required(f):
    @wraps(f)
    def call(*args, **kwargs):

        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return abort(401, "Authorization header missing")

        auth_type = auth_header.split(' ', 1)[0]

        if auth_type == 'Key':
            return adminkey_required(f)(*args, **kwargs)

        elif auth_type == 'Bearer':
            return admintoken_required(f)(*args, **kwargs)

        else:  # This would allow outsiders to enumerate admin endpoints to distinct them from regular endpoints
            return abort(400, "Bad Authorization header. Expected value '(Bearer/Key) <JWT>'")

    return call
