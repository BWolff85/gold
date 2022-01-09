from os import environ, path, pardir
from dotenv import load_dotenv

import os

# path = getcwd()
# parent = path.dirname(path)

# basedir = path.abspath(path.dirname(__file__) + "/../")
# load_dotenv(path.join(basedir, '.env'))
load_dotenv()


class Config(object):
    FLASK_ENV = 'development'
    TESTING = True

    # Database
    DB_NAME = environ.get("DB_NAME")
    DB_USER = environ.get("DB_USER")
    DB_PW = environ.get("DB_PW")
    DB_IP = environ.get("DB_IP")
    DB_PORT = environ.get("DB_PORT")
    SQLALCHEMY_DATABASE_URI = f'mysql+mysqlconnector://{DB_USER}:{DB_PW}@{DB_IP}:{DB_PORT}/{DB_NAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSONIFY_PRETTYPRINT_REGULAR = False

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True