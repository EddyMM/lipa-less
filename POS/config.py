import os

import redis

from .constants import APP_NAME, DATABASE_URL, TESTING_DATABASE_URL, REDIS_URL_ENV_VAR, LOCAL_REDIS_URL


class BaseConfig(object):
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SECRET_KEY = os.environ.get(APP_NAME + "_SECRET_KEY")

    SESSION_TYPE = "redis"
    SESSION_REDIS = redis.from_url(os.environ.get(REDIS_URL_ENV_VAR, LOCAL_REDIS_URL))
    SESSION_PERMANENT = False


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    DEBUG = True


class ProductionConfig(BaseConfig):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False


class TestingConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = TESTING_DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False
