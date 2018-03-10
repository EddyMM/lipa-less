import os
from .constants import APP_NAME


class BaseConfig(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get(APP_NAME + "_DATABASE_URL")
    SECRET_KEY = os.environ.get(APP_NAME + "_SECRET_KEY")


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    DEBUG = True


class ProductionConfig(BaseConfig):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False
