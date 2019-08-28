#!/usr/bin/env python3
from flask import request, abort, jsonify
from flask_classful import FlaskView
from utils import json_required, ponytoken_required, this_player

from model import db, Pony, Hug
from schemas import HugSchema


class HugsView(FlaskView):

	hug_schema = HugSchema(many=False)
	hugs_schema = HugSchema(many=True)

	@ponytoken_required
	def index(self):
		hugs = this_player().hugs

		return jsonify(self.hugs_schema.dump(hugs)), 200

	@ponytoken_required
	def get(self, id: int):

		hug = Hug.query.filter(db.and_(Hug.player == this_player(), Hug.id == id)).first()  # only hugs by the current player is allowed

		if not hug:
			abort(404)

		return jsonify(self.hug_schema.dump(hug)), 200

	@ponytoken_required
	@json_required
	def post(self):
		params = request.get_json()
		ponykey = params.get("key")

		pony = Pony.query.filter_by(key=ponykey).first()

		if not pony:
			abort(404)

		# check if pony already hugged by this player
		hug = Hug.query.filter(db.and_(Hug.player == this_player(), Hug.pony == pony)).first()

		if hug:
			abort(409, "Already hugged")

		# create new hug
		hug = Hug(pony=pony, player=this_player())

		db.session.add(hug)
		db.session.commit()

		return jsonify(self.hug_schema.dump(hug)), 201
