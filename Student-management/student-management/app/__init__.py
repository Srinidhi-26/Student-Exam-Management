from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = "postgresql://postgres:user@localhost/studentdb"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        from app import student, models, marks
        from app.student import studentmanagement_api
        from app.marks import studentmarks_api

        app.register_blueprint(studentmanagement_api)
        app.register_blueprint(studentmarks_api)

    return app
