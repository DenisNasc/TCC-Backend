from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


def initialize_db(app):
    db = SQLAlchemy()
    migrate = Migrate()

    db.init_app(app)
    migrate.init_app(app, db)

    return db
