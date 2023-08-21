from application import create_app
from model import db

#
# Gunicron would run this once for each worker
# Since Flask deprecated before_first_request we need another way to run this only once (per pod at least)
#

if __name__ == '__main__':
    print("run db init")

    app = create_app()
    with app.app_context():
        db.create_all()

    print("db init complete")
