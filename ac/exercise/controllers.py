import functools
from collections.abc import Callable

import requests
from flask import flash, g, redirect, request, session, url_for
from werkzeug import Response

from ac.db import db
from ac.holly import constants as holly_constants
from ac.holly.structures import Holly

from . import messages, models

DEFAULT_TIMEOUT = 10


def check_passed_exercises(view: Callable[..., Response | str]) -> Callable[..., Response | str]:
    """Decorator for checking if user is allow to move the exercise.

    This function checks if the user is permitted to view the exercise
    description. The user is allow to see the description only if all previous
    exercises were successfully passed. Otherwise it is returned back to last
    unfinished exercise.

        Args:
            view (Callable): Flask view object, which is decorated.

        Returns:
            Union[Callable, Response]: Decorated callable object in case, when
              user is allowed to process to the next exercise. Redirect to the
              last unfinished exercise otherwise.
    """

    @functools.wraps(view)
    def wrapped_view(**kwargs: str | int) -> Response | str:
        # Determin which exercise is user allowed to see
        next_allowed_exercise = determine_next_allowed_exercise()

        # Get index of requested exercise
        requested_exercise = kwargs.get("exercise_id", 1)
        if not isinstance(requested_exercise, int):
            return redirect(url_for("exercise.index"))

        # Check if user is allow to see the requested exercise
        if next_allowed_exercise < requested_exercise:
            if requested_exercise != 1:
                flash(messages.SKIP_ATTEMPT)
            url = url_for("exercise.index", exercise_id=next_allowed_exercise)
            return redirect(url)
        return view(**kwargs)

    return wrapped_view


def determine_next_allowed_exercise() -> int:
    solved_exercises = g.get("solved_exercises", [])
    if not solved_exercises:
        return 1
    return max(solved_exercises) + 1


def move_to_next_exercise(exercise_id: int) -> Response:
    """Move challenger to next exercise.

    Args:
        exercise_id (int): index of last passed exercise

    Returns:
        Response: redirect to next exercise
    """
    # Determine next exercise number
    next_exercise = exercise_id + 1
    # Redirect to proper view
    return redirect(url_for("exercise.index", exercise_id=next_exercise))


def complete_exercise(exercise_id: int) -> None:
    """Mark exercise as complete.

    The completed exercises are stored into user session.

    Args:
        exercise_id (int): index of passed exercise.
    """
    solved_exercises: list[int] = g.get("solved_exercises", [])
    if exercise_id not in solved_exercises:
        solved_exercises.append(exercise_id)
        session["solved_exercises"] = solved_exercises
        solution = models.Solution(exercise_id=exercise_id)  # type: ignore  # noqa: PGH003
        db.session.add(solution)
        db.session.commit()


def check_holly_greetings() -> bool:
    """Helper function to check response of Holly's greetings endpoint.

    Returns:
        bool: true if the endpoint returns expected result, false otherwise
    """
    url = f"{request.url_root}holly/greetings"
    try:
        response = requests.get(url, timeout=DEFAULT_TIMEOUT)
    except (requests.exceptions.RequestException, requests.exceptions.JSONDecodeError, TypeError):
        return False
    else:
        return response.text == "Hello, my friend"


def check_holly_sum() -> bool:
    """Helper function to check response of Holly's sum endpoint.

    Returns:
        bool: true if the endpoint returns expected result, false otherwise
    """
    url = f"{request.url_root}holly/sum"
    data = {"first_number": 10, "second_number": 30}
    try:
        response = requests.post(url, data=data, timeout=DEFAULT_TIMEOUT)
    except (requests.exceptions.RequestException, requests.exceptions.JSONDecodeError, TypeError):
        return False
    else:
        return response.text == "40"


def check_holly_redirect() -> bool:
    """Helper function to check response of Holly's redirect endpoint.

    Returns:
        bool: true if the endpoint returns expected result, false otherwise
    """
    url = f"{request.url_root}holly/redirect"
    was_redirected = False
    try:
        response = requests.get(url, timeout=DEFAULT_TIMEOUT)
        if response.history and "/holly/greetings" in response.url:
            was_redirected = True
    except (requests.exceptions.RequestException, requests.exceptions.JSONDecodeError, TypeError):
        return False
    else:
        return was_redirected and response.text == "Hello, my friend"


def check_first_exercise() -> Response:
    """Check if first exercise was passed.

    Returns:
        Response: redirect to next exercise
    """
    exercise: models.Exercise | None = models.Exercise.query.get(1)
    if not exercise:
        return redirect(request.url)
    complete_exercise(exercise.id)
    return move_to_next_exercise(exercise.id)


def check_second_exercise() -> Response:
    """Check if second exercise was passed.

    In this case the user defined password from exercise is compared with the
    one stored in the internal database. If the match is occurred the user is
    able to move on to the next exercise

    Returns:
        Response: redirect to next exercise in case the password is correct,
            go back to exercise 2 otherwise
    """
    password = request.form.get("password", "")
    exercise: models.Exercise | None = models.Exercise.query.get(2)
    if not exercise or not exercise.check_password(password):
        flash(messages.EXERCISE_2_WRONG_PASSWORD)
        return redirect(request.url)

    complete_exercise(exercise.id)
    return move_to_next_exercise(exercise.id)


def check_third_exercise() -> Response:
    """Check if third exercise was passed.

    In this case, the three requests are resolved against Holly Blueprint and
    the results are compared to expected values. The user is allow to move on
    only if all three endpoints are implemented correctly.

    Returns:
        Response: redirect to next exercise in case that all three endpoints
            are implemented correctly, go back to exercise 3 otherwise
    """
    error_occurred = False
    exercise: models.Exercise | None = models.Exercise.query.get(3)
    if not exercise:
        return redirect(request.url)

    if not check_holly_greetings():
        error_occurred = True
        flash(messages.EXERCISE_3_GREETINGS_ERROR)

    if not check_holly_sum():
        error_occurred = True
        flash(messages.EXERCISE_3_SUM_ERROR)

    if not check_holly_redirect():
        error_occurred = True
        flash(messages.EXERCISE_3_REDIRECT_ERROR)

    if error_occurred:
        return redirect(request.url)

    complete_exercise(exercise.id)
    return move_to_next_exercise(exercise.id)


def check_fourth_exercise() -> Response:
    """Check if fourth exercise was passed.

    In this case, the function checks if the Holly instance response to magic
    methods, which will be implemented during exercise.

    Returns:
        Response: redirect to next exercise in case that all magic methods are
            properly implemented, go back to exercise 4 otherwise
    """
    error_occurred = False
    exercise: models.Exercise | None = models.Exercise.query.get(4)
    if not exercise:
        return redirect(request.url)
    holly = Holly()
    str_test = str(holly)
    repr_test = str(repr(holly))

    if str_test != holly_constants.HOLLY_STRING:
        error_occurred = True

    if repr_test != holly_constants.HOLLY_REPR:
        error_occurred = True

    if error_occurred:
        flash(messages.EXERCISE_4_ERROR)
        return redirect(request.url)

    complete_exercise(exercise.id)
    return move_to_next_exercise(exercise.id)
