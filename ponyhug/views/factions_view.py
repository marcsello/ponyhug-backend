#!/usr/bin/env python3
from flask import abort, jsonify, request
from flask_classful import FlaskView

from marshmallow import ValidationError

from utils import ponytoken_required, this_player, anyadmin_required, json_required

from model import db, Faction
from schemas import FactionSchema


class FactionsView(FlaskView):
    pass
