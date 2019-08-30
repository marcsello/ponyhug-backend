#!/usr/bin/env python3
import sys
sys.path.insert(0, '/opt/ponyhug/ponyhug') # <- This might need adjustment as well

from application import app as application

# configure
application.config['SQLALCHEMY_DATABASE_URI'] = "..."
application.config['PONYHUG_SECRET_KEY'] = "..."
