#!/usr/bin/env python3
from flask import abort, jsonify, request
from flask_classful import FlaskView

from marshmallow import ValidationError

from utils import ponytoken_required, this_player, anyadmin_required, json_required

from model import db, Pony, Hug
from schemas import PonySchema


class PoniesView(FlaskView):
    pony_schema = PonySchema(many=False)
    ponies_schema = PonySchema(many=True, only=['id', 'name', 'image', 'order'])

    @anyadmin_required
    def index(self):
        ponies = Pony.query.all()
        return jsonify(self.ponies_schema.dump(ponies)), 200

    @ponytoken_required
    def get(self, ponyid: int): # TODO: this can be solved using a single query
        pony = Pony.query.get_or_404(ponyid, "Undiscovered or non-existent pony")

        # should replace to exists()
        Hug.query.filter(
            db.and_(Hug.player == this_player(), Hug.pony == pony)
        ).first_or_404("Undiscovered or non-existent pony")

        return jsonify(self.pony_schema.dump(pony)), 200

    @ponytoken_required
    def count(self):
        total_ponies = Pony.query.count()
        return jsonify({"total_ponies": total_ponies}), 200

    @anyadmin_required
    @json_required
    def post(self):
        try:
            pony = self.pony_schema.load(request.get_json(), session=db.session)
        except ValidationError as e:
            return abort(422, str(e))

        db.session.add(pony)
        db.session.commit()
        return jsonify(self.pony_schema.dump(pony)), 201

    @anyadmin_required
    def delete(self, ponyid: int):
        Pony.query.filter_by(id=ponyid).delete()
        db.session.commit()
        return '', 204

