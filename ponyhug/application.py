#!/usr/bin/env python3
from flask import Flask
from flask_jwt_simple import JWTManager
from datetime import timedelta
import os

# import stuff
from model import db
from utils import jwt, register_all_error_handlers

# import views
from views import RegisterView, PlayersView, HugsView, PoniesView

# create flask app
app = Flask(__name__)

# configure flask app
app.config['JWT_EXPIRES'] = timedelta(days=14)  # yup, that long

# initialize stuff
db.init_app(app)
jwt.init_app(app)

with app.app_context():
	db.create_all()

# register error handlers
register_all_error_handlers(app)

# register views
for view in [RegisterView, PlayersView, HugsView, PoniesView]:
	view.register(app, trailing_slash=False)

# start debuggig if needed
if __name__ == "__main__":
	app.run(debug=True)
