#!/usr/bin/env python3
from sqlalchemy import sql
from model import db
from healthcheck import HealthCheck


def database_available():
    try:
        db.session.execute(sql.text('SELECT 1'))
        return True, 'db is ok'
    except Exception as e:
        return False, str(e)


health = HealthCheck()
health.add_check(database_available)


def register_all_health_checks(app):
    app.add_url_rule("/healthz", "healthcheck", view_func=lambda: health.run())
