#!/usr/bin/env python3
from flask import Flask


# let's try using factory pattern (https://flask.palletsprojects.com/en/2.0.x/patterns/appfactories/)
def create_app(config_object=None) -> Flask:
    # IDK if this is the correct way of doing this
    if not config_object:
        from config import Config
        config_object = Config

    if config_object.SENTRY_DSN:
        import sentry_sdk
        from sentry_sdk.integrations.flask import FlaskIntegration

        sentry_sdk.init(
            dsn=config_object.SENTRY_DSN,
            integrations=[FlaskIntegration()],
            traces_sample_rate=0.0,  # https://develop.sentry.dev/sdk/performance/#tracessamplerate
            send_default_pii=True,
            release=config_object.SENTRY_RELEASE_ID,
            environment=config_object.SENTRY_ENVIRONMENT
        )

    app = Flask(__name__.split('.')[0])  # lol? https://spotofdata.com/flask-testing/
    app.config.from_object(config_object)

    # initialize stuff
    from model import db
    from utils import jwt, register_all_health_checks
    from flask_cors import CORS

    db.init_app(app)
    jwt.init_app(app)
    CORS(app, resources="*")

    # register health checks
    register_all_health_checks(app)

    # import views
    from views import api
    api.init_app(app)

    return app


# start debugging if needed
if __name__ == "__main__":
    create_app().run(debug=True)
