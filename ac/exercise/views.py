from flask import Blueprint, g, render_template, request, session
from werkzeug import Response

from . import controllers

bp = Blueprint("exercise", __name__, url_prefix="/exercise", template_folder="templates")


@bp.route("/<int:exercise_id>", methods=("GET", "POST"))
@controllers.check_passed_exercises
def index(exercise_id: int = 1) -> Response | str:
    """Manage exercises

    This function is responsible for rendering exercises to user.
    Also it contains logic for checking answers which user send to
    application.

    Args:
        exercise_id (int, optional): Requested exercise. Defaults to 1.

    Returns:
        Union[Response, str]: If the request method is GET, it returns
            the rendered template. If the request method is POST, the
            function chose the proper validation function and checks,
            if the user's answer is correct.
    """
    if request.method == "POST":
        checker = None
        if exercise_id == 1:
            checker = controllers.check_first_exercise
        if exercise_id == 2:
            checker = controllers.check_second_exercise
        if exercise_id == 3:
            checker = controllers.check_third_exercise
        if exercise_id == 4:
            checker = controllers.check_fourth_exercise

        if checker is not None:
            return checker()

    template_file = f"exercise/exercise_{exercise_id}.html"
    allowed_exercises = controllers.determine_next_allowed_exercise()
    return render_template(
        template_file,
        exercise_id=exercise_id,
        allowed_exercises=allowed_exercises,
    )


@bp.before_app_request
def get_solved_exercises() -> None:
    """Function for getting list of solved exercises from user session."""
    g.solved_exercises = session.get("solved_exercises", [])
