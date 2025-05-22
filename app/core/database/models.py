from datetime import datetime
from sqlalchemy import Integer, String, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from .mixins import IntIdMixin, TimestampMixin


class APIKey(TimestampMixin, IntIdMixin, Base):
    __tablename__ = "api_keys"

    key_hash: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    username: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    revoked: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
