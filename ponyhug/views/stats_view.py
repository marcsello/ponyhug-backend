#!/usr/bin/env python3
from sqlalchemy import func, desc
from .api import api
from flask_restx import Resource

from utils import ponytoken_required

from model import db, Hug, Player

ns = api.namespace("stats", description="Various statistics")


@ns.route('/leader')
class LeaderResource(Resource):

    @ponytoken_required
    def get(self):
        leader_stat = db.session.query(
            func.count(Hug.player_id).label('cnt'), Hug.player_id
        ).group_by(Hug.player_id).order_by(desc('cnt')).first()

        count = 0
        if leader_stat:
            count = leader_stat.cnt

        return {"hug_counter": count}, 200
