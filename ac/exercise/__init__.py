from flask import Flask


def init_app(app: Flask) -> None:
    """Simple function which initialize exercise
    application models and views.

    Args:
        app (Flask): Current instance of Flask application.
    """

    from . import views

    app.register_blueprint(views.bp)
