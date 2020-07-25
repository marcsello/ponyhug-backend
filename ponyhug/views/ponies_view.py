#!/usr/bin/env python3
from flask import abort, jsonify
from flask_classful import FlaskView
from utils import ponytoken_required, this_player

from model import db, Pony, Hug
from schemas import PonySchema


class PoniesView(FlaskView):
    pony_schema = PonySchema(many=False)
    ponies_schema = PonySchema(many=True, only=['id', 'name', 'image'])

    @ponytoken_required
    def index(self):

        this_players_hugs = this_player().hugs

        # yup... we solve this from code... pretty shitty method

        ponies_hugged_by_this_player = [hug.pony for hug in this_players_hugs]

        return jsonify(self.ponies_schema.dump(ponies_hugged_by_this_player)), 200

    @ponytoken_required
    def get(self, id: int):

        pony = Pony.query.get(id)

        if not pony:
            abort(404, "Undiscovered or non-existent pony")

        # should replace to exists()
        if not Hug.query.filter(db.and_(Hug.player == this_player(), Hug.pony == pony)).first():
            abort(404, "Undiscovered or non-existent pony")  # only hugged ponies should be visible

        return jsonify(self.pony_schema.dump(pony)), 200
