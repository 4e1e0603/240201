import click
from flask import Flask
from flask.cli import with_appcontext  # type: ignore  # noqa: PGH003
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import insert
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


exercises: list[dict[str, str | int | None]] = [
    {"id": 1, "pwd": None},
    {
        "id": 2,
        "pwd": "pbkdf2:sha256:150000$0YsVYjvq$ded149398b1bc6b919d745d2dc361ed9b6463bb8e9de16fb993c3bdbb91b6fee",
    },
    {"id": 3, "pwd": None},
    {"id": 4, "pwd": None},
]


def insert_initial_data(db_instance: SQLAlchemy) -> None:
    """Inserting initial data for exercises.

    Args:
        db_instance (SQLAlchemy): Initialized DB instance.
    """
    from ac.exercise.models import Exercise

    with db_instance.engine.connect() as con, con.begin():
        for exercise in exercises:
            stmt = insert(Exercise).values(**exercise)
            con.execute(stmt)


@click.command("init-db", short_help="Create database, with initial values")
@with_appcontext
def init_db_command() -> None:
    """Custom Flask command to initializing database structure."""
    db.create_all()
    insert_initial_data(db)
    click.echo("Initialised the database")


def init_app(app: Flask) -> None:
    """Function for initializing database.

    Args:
        app (Flask): Flask application instance.
    """
    db.init_app(app)
    app.cli.add_command(init_db_command)
