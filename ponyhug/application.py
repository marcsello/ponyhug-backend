#!/usr/bin/env python3
from flask import Flask
from flask_cors import CORS

import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

# import stuff
from model import db
from utils import jwt, register_all_error_handlers

# import views
from views import PlayersView, HugsView, PoniesView, StatsView, AdminView, TimeframesView

from config import Config

if Config.SENTRY_DSN:
    sentry_sdk.init(
        dsn=Config.SENTRY_DSN,
        integrations=[FlaskIntegration()],
        traces_sample_rate=0.0,  # https://develop.sentry.dev/sdk/performance/#tracessamplerate
        send_default_pii=True,
        release=Config.SENTRY_RELEASE_ID,
        environment=Config.SENTRY_ENVIRONMENT,
        _experiments={"auto_enabling_integrations": True}
    )

# create flask app
app = Flask(__name__)
app.config.from_object(Config)

# initialize stuff
db.init_app(app)
jwt.init_app(app)
CORS(app)


@app.before_first_request
def initial_setup():
    db.create_all()


# register error handlers
register_all_error_handlers(app)

# register views
for view in [PlayersView, HugsView, PoniesView, StatsView, AdminView, TimeframesView]:
    view.register(app, trailing_slash=False)

# start debugging if needed
if __name__ == "__main__":
    app.run(debug=True)
