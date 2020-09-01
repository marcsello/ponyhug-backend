#!/usr/bin/env python3
from flask import request, abort, jsonify
from flask_classful import FlaskView
from flask_login import login_required
from flask_security import roles_required

from utils import json_required, ponytoken_required, this_player
import sqlalchemy.exc

from model import db, Pony, Hug
from schemas import HugSchema


class HugsView(FlaskView):
    hug_schema = HugSchema(many=False)
    hugs_schema = HugSchema(many=True)

    @ponytoken_required
    @roles_required('admin')
    def index(self):
        hugs = this_player().hugs

        return jsonify(self.hugs_schema.dump(hugs)), 200

    @ponytoken_required
    @roles_required('admin')
    def get(self, hugid: int):
        # only hugs by the current player is allowed
        hug = Hug.query.filter(db.and_(Hug.player == this_player(), Hug.id == hugid)).first()

        if not hug:
            abort(404)

        return jsonify(self.hug_schema.dump(hug)), 200

    @ponytoken_required
    @login_required
    def post(self):
        params = request.get_json()
        ponykey = params.get("key")

        pony = Pony.query.filter_by(key=ponykey).first()

        if not pony:
            abort(404, "Unknown key")

        # create new hug
        hug = Hug(pony=pony, player=this_player())

        db.session.add(hug)
        try:
            db.session.commit()
        except sqlalchemy.exc.IntegrityError:
            abort(409, "Already hugged")
        return jsonify(self.hug_schema.dump(hug)), 201
