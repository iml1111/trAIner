'''
Application Config Setting
'''
import os
from logging.config import dictConfig
from dotenv import load_dotenv

load_dotenv(verbose=True)

APP_NAME = "TRAINER"
BASEDIR = os.path.abspath(os.path.dirname(__file__))
FLASK_CONFIG = os.getenv('FLASK_CONFIG') or 'development'


class Config:
    '''General Config'''
    SLOW_API_TIME = 0.5
    API_LOGGING = False
    JSON_AS_ASCII = False
    SECRET_KEY = "top-secret"
    MONGODB_URI = "mongodb://localhost:27017"
    MONGODB_NAME = "Trainer"
    # API 타이머 출력 경로 (response, log, none)
    TIMER_OUTPUT = 'response'

    # Model Paths
    CTR_MODEL_PATH = os.environ['CTR_MODEL_PATH']
    DEEP_MODEL_PATH = os.environ['DEEP_MODEL_PATH']

    @staticmethod
    def init_app(app):
        pass

if FLASK_CONFIG == 'development':
    class AppConfig(Config):
        DEBUG = True
        TESTING = False
        MONGODB_URI = os.environ[APP_NAME + "_MONGODB_URI"]

elif FLASK_CONFIG == 'production':
    class AppConfig(Config):
        DEBUG = False
        TESTING = False
        TIMER_OUTPUT = 'log'
        SECRET_KEY = os.environ["SECRET_KEY"]
        MONGODB_URI = os.environ[APP_NAME + "_MONGODB_URI"]
else:
    raise Exception("Flask Config not Selected.")

config = AppConfig

class TestConfig(Config):
    DEBUG = True
    TESTING = True
    MONGODB_URI = os.environ[APP_NAME + "_MONGODB_URI"]

if __name__ == '__main__':
    pass