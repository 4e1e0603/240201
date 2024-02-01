from flask import Flask


def init_app(app: Flask) -> None:
    """Simple function which initialize holly
    application views.

    Args:
        app (Flask): Current instance of Flask application.
    """

    from . import views

    app.register_blueprint(views.bp)
