#!/usr/bin/env python3
from datetime import datetime
import tzlocal

from flask import request, abort, jsonify
from flask_classful import FlaskView

from utils import ponytoken_required, this_player, json_required
import sqlalchemy.exc

from model import db, Pony, Hug, Timeframe
from schemas import HugSchema


class HugsView(FlaskView):
    hug_schema = HugSchema(many=False)
    hugs_schema = HugSchema(many=True)

    @ponytoken_required
    def index(self):
        hugs = this_player().hugs

        return jsonify(self.hugs_schema.dump(hugs)), 200

    @ponytoken_required
    def get(self, hugid: int):
        # only hugs by the current player is allowed
        hug = Hug.query.filter(db.and_(Hug.player == this_player(), Hug.id == hugid)).first_or_404()

        return jsonify(self.hug_schema.dump(hug)), 200

    @ponytoken_required
    @json_required
    def post(self):

        now = datetime.now(tz=tzlocal.get_localzone())
        timeframe = Timeframe.query.filter(
            db.and_(Timeframe.begin_timestamp <= now, Timeframe.end_timestamp >= now)
        ).first()

        if not timeframe:
            return abort(423, "No active timeframe")

        params = request.get_json()
        ponykey = params.get("key")

        pony = Pony.query.filter_by(key=ponykey).first_or_404("Unknown key")

        # create new hug
        hug = Hug(pony=pony, player=this_player())

        db.session.add(hug)
        try:
            db.session.commit()
        except sqlalchemy.exc.IntegrityError:
            return abort(409, "Already hugged")
        return jsonify(self.hug_schema.dump(hug)), 201
