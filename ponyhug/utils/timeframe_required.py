#!/usr/bin/env python3
from flask import abort
from functools import wraps
from datetime import datetime
import tzlocal

from model import db, Timeframe


def timeframe_required(f):
    @wraps(f)
    def call(*args, **kwargs):
        now = datetime.now(tz=tzlocal.get_localzone())
        timeframe = Timeframe.query.filter(
            db.and_(Timeframe.begin_timestamp <= now, Timeframe.end_timestamp >= now)
        ).first()

        if timeframe:
            return f(*args, **kwargs)
        else:
            return abort(423, "No active timeframe")

    return call
