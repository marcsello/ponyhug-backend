#!/usr/bin/env python3
from flask import abort, jsonify, request
from .api import api
from flask_restx import Resource
from marshmallow import ValidationError

from utils import ponytoken_required, this_player, anyadmin_required, json_required

from model import db, Faction
from schemas import FactionSchema

ns = api.namespace('factions', description="Operations related to factions")

_faction_schema = FactionSchema(many=False, exclude=["players"])
_factions_schema = FactionSchema(many=True, exclude=["players"])


@ns.route("")
class FactionsResource(Resource):
    @ponytoken_required
    def get(self):
        factions = Faction.query.all()
        return jsonify(_factions_schema.dump(factions)), 200

    @anyadmin_required
    @json_required
    def post(self):
        try:
            faction = _faction_schema.load(request.get_json(), session=db.session)
        except ValidationError as e:
            return abort(422, str(e))

        db.session.add(faction)
        db.session.commit()
        return jsonify(_faction_schema.dump(faction)), 201


@ns.route("/my")
class FactionMyResource(Resource):
    @ponytoken_required
    def get(self):
        return jsonify(_faction_schema.dump(this_player().faction))


@ns.route("/<int:id>")
class FactionResource(Resource):
    @ponytoken_required
    def get(self, id_: int):
        faction = Faction.query.filter_by(id=id_).first_or_404("No such faction")
        return jsonify(_faction_schema.dump(faction)), 200

    @anyadmin_required
    def delete(self, id_: int):
        Faction.query.filter_by(id=id_).delete()
        db.session.commit()
        return '', 204
