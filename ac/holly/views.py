"""Holly's views.

This module is used as template for third exercise. The user needs to implement
logic of three endpoints.
"""

from flask import Blueprint, redirect, request, url_for
from werkzeug import Response

# Prepared Flask Blueprint, please don't touch this
bp = Blueprint("holly", __name__, url_prefix="/holly")


# Here is starting point of your exercise


class ValidationError(Exception):
    """Custom validation error for POST data."""


@bp.route("/greetings")
def greetings() -> str:
    """The function response with string 'Hello, my friend'
    to every request.

    Returns:
        str: Hello, my friend for every request
    """
    return "Hello, my friend"


@bp.route("/sum", methods=["POST"])
def sum_two_values() -> str:
    """This function gets two parameters (first_number and second_number) in
    request form object and the result is sum of these two values.

    Returns:
        str: Sum of values from request
    """
    first_number: str | None = request.form.get("first_number", None)
    second_number: str | None = request.form.get("second_number", None)

    if first_number is None or second_number is None:
        result =  "TODO: Handle missing value"
    else:
        try:
            result = f"{int(first_number) + int(second_number)}" # type: ignore
        except ValidationError as error:
            result = str(error) # code 400

    return result


@bp.route("/redirect")
def redirect_to_greetings() -> Response:
    """This function is used for redirecting incoming GET request to /greetings
    endpoint.

    To pass this test, implement redirection in proper Flask way.

    Returns:
        Response: redirect to /greetings endpoint
    """
    return redirect(url_for("holly.greetings"))
