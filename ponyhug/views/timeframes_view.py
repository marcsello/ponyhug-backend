#!/usr/bin/env python3
from datetime import datetime
import tzlocal
from flask import abort, request
from .api import api
from flask_restx import Resource
from marshmallow import ValidationError

from utils import anyadmin_required, json_required

from model import db, Timeframe
from schemas import TimeframeSchema

ns = api.namespace("timeframes", description="Timeframes")

_timeframe_schema_noid = TimeframeSchema(many=False, exclude=['id'])
_timeframe_schema = TimeframeSchema(many=False)
_timeframes_schema = TimeframeSchema(many=True)


@ns.route('/current')
class CurrentTimeframeResource(Resource):

    def get(self):
        now = datetime.now(tz=tzlocal.get_localzone())
        timeframe = Timeframe.query.filter(
            db.and_(Timeframe.begin_timestamp <= now, Timeframe.end_timestamp >= now)
        ).first_or_404("No active timeframe")

        return _timeframe_schema_noid.dump(timeframe), 200


@ns.route('')
class TimeframesResource(Resource):
    @anyadmin_required
    def get(self):
        timeframes = Timeframe.query.all()
        return _timeframes_schema.dump(timeframes), 200

    @anyadmin_required
    @json_required
    def post(self):
        try:
            timeframe = _timeframe_schema.load(request.get_json(), session=db.session)
        except ValidationError as e:
            return abort(422, str(e))

        db.session.add(timeframe)
        db.session.commit()
        return _timeframe_schema.dump(timeframe), 201


@ns.route('/<int:id_>')
class TimeframeResource(Resource):

    @anyadmin_required
    def delete(self, id_: int):
        Timeframe.query.filter_by(id=id_).delete()
        db.session.commit()
        return '', 204
