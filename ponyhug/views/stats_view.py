#!/usr/bin/env python3
from sqlalchemy import func, desc
from flask import jsonify
from flask_classful import FlaskView

from utils import ponytoken_required, anyadmin_required

from model import db, Hug


class StatsView(FlaskView):

    @anyadmin_required
    def index(self):
        return 'TODO'

    @ponytoken_required
    def leader(self):
        asd = db.session.query(
            func.count(Hug.player_id).label('cnt'), Hug.player_id
        ).group_by(Hug.player_id).order_by(desc('cnt')).first()

        return jsonify({"hugs_of_leader": asd.cnt}), 200
