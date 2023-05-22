from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql+psycopg2://hello_flask:hello_flask@localhost/student"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
app.app_context().push()
db.create_all()

try:
    from app import models, student, marks

    app.register_blueprint(student.studentmanagement_api)
    app.register_blueprint(marks.studentmarks_api)
    models.db.configure_mappers()
    if app.config["FLASK_ENV_EDITABLE"] == "local":
        models.db.create_all()
    models.db.session.commit()

except Exception as e:
    import traceback

    traceback.print_exc()
    app.logger.error(e)

if __name__ == "__main__":
    with app.app_context():
        app.run(debug=True)
