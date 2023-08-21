#!/usr/bin/env python3
from sqlalchemy import func, desc
from .api import api
from flask_restx import Resource

from utils import ponytoken_required

from model import db, Hug, Player

ns = api.namespace("stats", description="Various statistics")


@ns.route('')
class StatsResource(Resource):

    @ponytoken_required
    def get(self):
        leader_stat = db.session.query(
            func.count(Hug.player_id).label('cnt'), Hug.player_id
        ).group_by(Hug.player_id).order_by(desc('cnt')).first()

        leader_hug_count = 0
        if leader_stat:
            leader_hug_count = leader_stat.cnt

        sum_hugs = db.session.query(Hug.id).count()

        return {
            "leader_hug_count": leader_hug_count,
            "sum_hugs": sum_hugs
        }, 200
