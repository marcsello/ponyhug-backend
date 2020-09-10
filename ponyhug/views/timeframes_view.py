#!/usr/bin/env python3
from datetime import datetime
from flask import jsonify
from flask_classful import FlaskView

from model import db, Timeframe
from schemas import TimeframeSchema


class TimeframesView(FlaskView):
    timeframe_schema = TimeframeSchema(many=False, exclude=['id'])

    def current(self):
        now = datetime.now()
        timeframe = Timeframe.query.filter(
            db.and_(Timeframe.begin_timestamp <= now, Timeframe.end_timestamp >= now)
        ).first_or_404("No active timeframe")

        return jsonify(self.timeframe_schema.dump(timeframe)), 200