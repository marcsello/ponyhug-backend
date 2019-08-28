#!/usr/bin/env python3
from model import db
from flask import Flask
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('PONYHUG_SQL_URI', 'sqlite:///:memory:')
db.init_app(app)

with app.app_context():
	db.create_all()

if __name__ == "__main__":
	app.run(debug=True)


