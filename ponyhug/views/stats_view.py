#!/usr/bin/env python3
from sqlalchemy import func, desc
from flask import jsonify
from flask_classful import FlaskView

from utils import ponytoken_required

from model import db, Hug, Pony


class StatsView(FlaskView):

    @ponytoken_required
    def leader(self):
        leader_stat = db.session.query(
            func.count(Hug.player_id).label('cnt'), Hug.player_id
        ).group_by(Hug.player_id).order_by(desc('cnt')).first()

        count = 0
        if leader_stat:
            count = leader_stat.cnt

        return jsonify({"hug_counter": count}), 200

    @ponytoken_required
    def game(self):
        total_ponies = Pony.query.count()

        return jsonify({"total_ponies": total_ponies}), 200
