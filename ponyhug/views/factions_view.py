#!/usr/bin/env python3
from flask import abort, jsonify, request
from flask_classful import FlaskView

from marshmallow import ValidationError

from utils import ponytoken_required, this_player, anyadmin_required, json_required

from model import db, Faction
from schemas import FactionSchema


class FactionsView(FlaskView):
    faction_schema = FactionSchema(many=False, exclude=["players"])
    factions_schema = FactionSchema(many=True, exclude=["players"])

    @ponytoken_required
    def index(self):
        factions = Faction.query.all()
        return jsonify(self.factions_schema.dump(factions)), 200

    @ponytoken_required
    def get(self, id_: int):
        faction = Faction.query.filter_by(id=id_).first_or_404("No such faction")
        return jsonify(self.faction_schema.dump(faction)), 200

    @ponytoken_required
    def my(self):
        return jsonify(self.faction_schema.dump(this_player().faction))

    @anyadmin_required
    @json_required
    def post(self):
        try:
            faction = self.faction_schema.load(request.get_json(), session=db.session)
        except ValidationError as e:
            return abort(422, str(e))

        db.session.add(faction)
        db.session.commit()
        return jsonify(self.faction_schema.dump(faction)), 201

    @anyadmin_required
    def delete(self, id_: int):
        Faction.query.filter_by(id=id_).delete()
        db.session.commit()
        return '', 204
