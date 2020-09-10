#!/usr/bin/env python3
import os
from datetime import timedelta
from flask import Flask

# import stuff
from model import db
from utils import jwt, register_all_error_handlers

# import views
from views import PlayersView, HugsView, PoniesView

# create flask app
app = Flask(__name__)

# configure flask app
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI', "sqlite://")
app.config['JWT_SECRET_KEY'] = os.environ['JWT_SECRET_KEY']
app.config['JWT_EXPIRES'] = timedelta(days=14)  # yup, that long

app.secret_key = os.environ.get("FLASK_SECRET_KEY", os.urandom(16))

# initialize stuff
db.init_app(app)
jwt.init_app(app)


@app.before_first_request
def initial_setup():
    db.create_all()


# register error handlers
register_all_error_handlers(app)

# register views
for view in [PlayersView, HugsView, PoniesView]:
    view.register(app, trailing_slash=False)

# start debuggig if needed
if __name__ == "__main__":
    app.run(debug=True)
