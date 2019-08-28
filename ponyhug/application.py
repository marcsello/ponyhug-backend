#!/usr/bin/env python3
from flask import Flask
from flask_jwt_simple import JWTManager
from datetime import timedelta
import os

# import stuff
from model import db
from utils import jwt, register_all_error_handlers

# import views
from views import RegisterView

# create flask app
app = Flask(__name__)

# configure flask app
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('PONYHUG_SQL_URI', 'sqlite:///:memory:')
app.config['JWT_SECRET_KEY'] = os.environ["PONYHUG_SECRET_KEY"]  # Tokes will least very-very long... so we need a constant key
app.config['JWT_EXPIRES'] = timedelta(days=14)  # yup, that long

# initialize stuff
db.init_app(app)
jwt.init_app(app)

with app.app_context():
	db.create_all()

# register error handlers
register_all_error_handlers(app)

# register views
for view in [RegisterView]:
	view.register(app, trailing_slash=False)

# start debuggig if needed
if __name__ == "__main__":
	app.run(debug=True)
