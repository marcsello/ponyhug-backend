#!/usr/bin/env python3
from flask import abort, request
from .api import api
from flask_restx import Resource
from marshmallow import ValidationError

from utils import ponytoken_required, this_player, anyadmin_required, json_required

from model import db, Pony, Hug
from schemas import PonySchema

ns = api.namespace("ponies", description="Ponies")

_pony_schema = PonySchema(many=False)
_ponies_schema = PonySchema(many=True)


@ns.route("")
class PoniesResource(Resource):

    @anyadmin_required
    def get(self):
        ponies = Pony.query.all()
        return _ponies_schema.dump(ponies), 200

    @anyadmin_required
    @json_required
    def post(self):
        try:
            pony = _pony_schema.load(request.get_json(), session=db.session)
        except ValidationError as e:
            return abort(422, str(e))

        db.session.add(pony)
        db.session.commit()
        return _pony_schema.dump(pony), 201


@ns.route("/count")
class PonyCountResource(Resource):
    @ponytoken_required
    def get(self):
        total_ponies = Pony.query.count()
        return {"total_ponies": total_ponies}, 200


@ns.route("/<int:id_>")
class PonyResource(Resource):
    @ponytoken_required
    def get(self, id_: int):  # TODO: this can be solved using a single query
        pony = Pony.query.get_or_404(id_, "Undiscovered or non-existent pony")

        # should replace to exists()
        Hug.query.filter(
            db.and_(Hug.player == this_player(), Hug.pony == pony)
        ).first_or_404("Undiscovered or non-existent pony")

        return _pony_schema.dump(pony), 200

    @anyadmin_required
    def delete(self, id_: int):
        Pony.query.filter_by(id=id_).delete()
        db.session.commit()
        return '', 204
