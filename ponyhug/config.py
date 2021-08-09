import os
from datetime import timedelta


class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI', "sqlite://")

    JWT_SECRET_KEY = os.environ['JWT_SECRET_KEY']
    JWT_EXPIRES = timedelta(days=int(os.environ.get("JWT_EXPIRES_DAYS", 14)))  # yup, that long
    ADMIN_KEY = os.environ.get('ADMIN_KEY')  # None would not match anything
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get("FLASK_SECRET_KEY", os.urandom(16))

    SENTRY_DSN = os.environ.get('SENTRY_DSN')
    SENTRY_RELEASE_ID = os.environ.get('SENTRY_RELEASE_ID', 'dev')
    SENTRY_ENVIRONMENT = os.environ.get('SENTRY_ENVIRONMENT', 'dev')

    CORS_ORIGINS = os.environ.get('ALLOWED_ORIGINS', "*")
