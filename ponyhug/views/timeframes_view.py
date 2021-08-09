#!/usr/bin/env python3
from datetime import datetime
import tzlocal
from flask import jsonify, abort, request
from flask_classful import FlaskView
from marshmallow import ValidationError

from utils import anyadmin_required, json_required

from model import db, Timeframe
from schemas import TimeframeSchema


class TimeframesView(FlaskView):
    timeframe_schema_noid = TimeframeSchema(many=False, exclude=['id'])
    timeframe_schema = TimeframeSchema(many=False)
    timeframes_schema = TimeframeSchema(many=True)

    def current(self):
        now = datetime.now(tz=tzlocal.get_localzone())
        timeframe = Timeframe.query.filter(
            db.and_(Timeframe.begin_timestamp <= now, Timeframe.end_timestamp >= now)
        ).first_or_404("No active timeframe")

        return jsonify(self.timeframe_schema_noid.dump(timeframe)), 200

    @anyadmin_required
    def index(self):
        timeframes = Timeframe.query.all()
        return jsonify(self.timeframes_schema.dump(timeframes)), 200

    @anyadmin_required
    @json_required
    def post(self):
        try:
            timeframe = self.timeframe_schema.load(request.get_json(), session=db.session)
        except ValidationError as e:
            return abort(422, str(e))

        db.session.add(timeframe)
        db.session.commit()
        return jsonify(self.timeframe_schema.dump(timeframe)), 201

    @anyadmin_required
    def delete(self, timeframeid: int):
        Timeframe.query.filter_by(id=timeframeid).delete()
        db.session.commit()
        return '', 204
