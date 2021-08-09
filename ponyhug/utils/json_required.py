#!/usr/bin/env python3
from flask import request, abort
from functools import wraps


def json_required(f):
    @wraps(f)
    def call(*args, **kwargs):

        if request.is_json:
            return f(*args, **kwargs)
        else:
            return abort(400, "JSON required")

    return call
