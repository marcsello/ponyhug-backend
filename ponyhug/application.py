#!/usr/bin/env python3
import os
from datetime import timedelta
from flask import Flask
from flask_cors import CORS

import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

# import stuff
from model import db
from utils import jwt, register_all_error_handlers

# import views
from views import PlayersView, HugsView, PoniesView, StatsView, AdminView, TimeframesView

SENTRY_DSN = os.environ.get('SENTRY_DSN')

if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[FlaskIntegration()],
        traces_sample_rate=1.0,
        send_default_pii=True,
        release=os.environ.get('RELEASE_ID', "dev"),
        environment=os.environ.get('RELEASEMODE', "DEV"),
        _experiments={"auto_enabling_integrations": True}
    )


# create flask app
app = Flask(__name__)

# configure flask app
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI', "sqlite://")
app.config['JWT_SECRET_KEY'] = os.environ['JWT_SECRET_KEY']
app.config['JWT_EXPIRES'] = timedelta(days=14)  # yup, that long
app.config['ADMIN_KEY'] = os.environ.get('ADMIN_KEY')  # None would not match anything
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.secret_key = os.environ.get("FLASK_SECRET_KEY", os.urandom(16))

# initialize stuff
db.init_app(app)
jwt.init_app(app)
CORS(app, origins=os.environ.get('ALLOWED_ORIGINS', '*'))


@app.before_first_request
def initial_setup():
    db.create_all()


# register error handlers
register_all_error_handlers(app)

# register views
for view in [PlayersView, HugsView, PoniesView, StatsView, AdminView, TimeframesView]:
    view.register(app, trailing_slash=False)

# start debuggig if needed
if __name__ == "__main__":
    app.run(debug=True)
