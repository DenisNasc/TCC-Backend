import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

BASEDIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    CORS_SUPPORTS_CREDENTIALS = True

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    JWT_TOKEN_LOCATION = ["cookies"]
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_COOKIE_SECURE = True
    JWT_COOKIE_DOMAIN = "127.0.0.1:3000"
    JWT_SESSION_COOKIE = False

    CSRF_ENABLED = True

    @staticmethod
    def init_app(app):
        pass


class DevConfig(Config):
    ENV = "development"
    SQLALCHEMY_DATABASE_URI = (
        f'sqlite:///{os.path.join(BASEDIR,"database","sqlite","dev.sqlite")}'
    )
    DEBUG = True
    SERVER_NAME = "127.0.0.1:5000"
    PORT = 5000
    CORS_ORIGINS = "*"


class TestConfig(Config):
    ENV = "testing"
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    DEBUG = True
    TESTING = True
    WTF_CSRF_ENABLED = False


class ProdConfig(Config):
    # "postgresql://postgres:postgres@localhost:5432/cars_api"
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    DEBUG = False
    SERVER_NAME = os.getenv("SERVER_NAME")
    PORT = os.getenv("PORT")
    CORS_ORIGINS = "*"


config = {
    "development": DevConfig,
    "testing": TestConfig,
    "production": ProdConfig,
    "default": DevConfig,
}
