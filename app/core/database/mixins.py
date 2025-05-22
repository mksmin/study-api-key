from datetime import datetime

from sqlalchemy import func, Integer
from sqlalchemy.orm import Mapped, mapped_column


class IntIdMixin:
    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(default=datetime.now, server_default=func.now(), nullable=False)
    deleted_at: Mapped[datetime] = mapped_column(default=None, server_default=None, nullable=True)
