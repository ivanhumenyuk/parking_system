import os

import click
from flask import Flask, Response, redirect, request
from flask.cli import with_appcontext
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy, BaseQuery
from flask_smorest import Api
from sqlalchemy.exc import SQLAlchemyError

from app.config import FLASK_DEV_CONFIG, DEV, FLASK_TEST_CONFIG

db = SQLAlchemy(query_class=BaseQuery)
app = Flask(__name__, instance_relative_config=True)
app.config.update(**FLASK_DEV_CONFIG)


def create_app(conf: str = None):

    db_url = os.environ.get("DATABASE_URL")
    ma = Marshmallow()
    migrate = Migrate()

    if db_url is None:
        db_path = os.path.join(app.instance_path, "db.sqlite3")
        db_url = f"sqlite:///{db_path}"
        os.makedirs(app.instance_path, exist_ok=True)

    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI=db_url,
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )

    @app.teardown_request
    def handle_db_error(exception):
        if isinstance(exception, SQLAlchemyError):
            db.session.rollback()
            db.session.remove()

    # if test_config is None:
    #     app.config.from_pyfile("config.py", silent=True)
    # else:
    #     app.config.update(test_config)

    api = Api(app)
    from app.api import blueprints

    for blp in blueprints:
        api.register_blueprint(blp)

    db.init_app(app)
    app.cli.add_command(init_db_command)

    ma.init_app(app)
    migrate.init_app(app, db)

    if conf != "test":
        # app.config.update(**FLASK_TEST_CONFIG)
        # tasks
        from app.tasks.prepare import init_app_tasks

        init_app_tasks(app)

    if conf == "test":
        app.config.update(**FLASK_TEST_CONFIG)

    with app.app_context():
        db.create_all()
        db.drop_all(app=app)
        db.create_all(app=app)

        return app


def init_db():
    db.drop_all()
    db.create_all()


@click.command("init-db")
@with_appcontext
def init_db_command():
    init_db()
    click.echo("Initialized the database.")



    #
    # with app.app_context():
    #     return app
