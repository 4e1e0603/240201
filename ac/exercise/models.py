from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from werkzeug.security import check_password_hash

from ac.db import db


class Exercise(db.Model):  # type:ignore  # noqa: PGH003
    """Database model for exercise object.

    It represents exercises which user needs to solve.
    """

    id: Mapped[int] = mapped_column(primary_key=True)
    pwd: Mapped[str] = mapped_column(String(94), nullable=True)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.pwd, password)


class Solution(db.Model):  # type:ignore  # noqa: PGH003
    """Database model for solution object.

    It represents the time, when the solution of
    exercise was created.
    """

    id: Mapped[int] = mapped_column(primary_key=True)
    time_stamp: Mapped[datetime] = mapped_column(DateTime(), nullable=False, default=datetime.utcnow)
    exercise_id: Mapped[int] = mapped_column(Integer, ForeignKey("exercise.id"), nullable=False)
