#!/usr/bin/env python3
from flask import request, abort, current_app
from .api import api
from flask_restx import Resource
from marshmallow import ValidationError

from utils import ponytoken_required, this_player, json_required, timeframe_required

from model import db, Pony, Hug
from schemas import HugSchema, PonykeySchema

ns = api.namespace('hugs', description="Operations related to hugs", decorators=[ponytoken_required])

_hug_schema = HugSchema(many=False)
_hugs_schema = HugSchema(many=True, only=['id', 'pony.id', 'pony.name', 'pony.image', 'pony.order'])

_ponykey_schema = PonykeySchema(many=False)


@ns.route("")
class HugsResource(Resource):

    def get(self):
        hugs = this_player().hugs
        return _hugs_schema.dump(hugs), 200

    @json_required
    @timeframe_required
    def post(self):

        if not this_player().is_approved:
            return abort(403, "player not approved")

        try:
            key = _ponykey_schema.load(request.get_json())
        except ValidationError as e:
            return abort(422, str(e))

        ponykey = key['key']

        pony = Pony.query.filter_by(key=ponykey).first_or_404("Unknown key")

        hug = Hug.query.filter_by(pony=pony, player=this_player()).first()
        if hug:
            new = False
            hug.count += 1
        else:
            # create new hug
            new = True
            hug = Hug(pony=pony, player=this_player())

        db.session.add(hug)
        db.session.commit()

        if new:
            current_app.logger.info(f"User {this_player().name} [{this_player().id}] hugged a new pony: {pony.name} [{pony.id}]")

        return _hug_schema.dump(hug), 201 if new else 200

@ns.route("/count")
class HugsCountResource(Resource):

    def get(self):
        hug_counter = Hug.query.filter_by(player=this_player()).count()
        return {"hug_counter": hug_counter}, 200


@ns.route("/<int:id_>")
class HugResource(Resource):

    def get(self, id_: int):
        # only hugs by the current player is allowed
        hug = Hug.query.filter(db.and_(Hug.player == this_player(), Hug.id == id_)).first_or_404()

        return _hug_schema.dump(hug), 200
