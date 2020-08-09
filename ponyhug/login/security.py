#!/usr/bin/env python3
from flask_security import SQLAlchemyUserDatastore, Security
from model import db, Player, Role

user_datastore = SQLAlchemyUserDatastore(db, Player, Role)
security = Security(datastore=user_datastore)
