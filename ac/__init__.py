import uuid
from pathlib import Path

from flask import Flask


def create_instance_dir(instance_path: Path) -> None:
    instance_path.mkdir(parents=True, exist_ok=True)


def resolve_db_uri(instance_path: Path) -> str:
    return f"sqlite:///{instance_path / 'ac.sqlite'}"


def create_secret(instance_path: Path) -> str:
    path_to_secret = instance_path / ".secret"
    if not path_to_secret.exists():
        secret = str(uuid.uuid4())
        path_to_secret.write_text(secret)
    else:
        secret = path_to_secret.read_text().strip()

    return secret


def create_app() -> Flask:
    # Create and configure the app
    from . import db, exercise, holly

    app = Flask(__name__)

    # Resolve necessary paths
    instance_path = Path(app.instance_path)
    create_instance_dir(instance_path)
    db_uri = resolve_db_uri(instance_path)

    # Define secret
    secret = create_secret(instance_path)

    app.config.from_mapping(
        FLASK_ENV="development",
        SECRET_KEY=secret,
        SQLALCHEMY_DATABASE_URI=db_uri,
        SQLALCHEMY_TRACK_MODIFICATIONS=True,
    )

    db.init_app(app)
    exercise.init_app(app)
    holly.init_app(app)
    return app
