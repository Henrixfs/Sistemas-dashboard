"""Server-side session persistence model."""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Index, LargeBinary, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.mixins import UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.user import User


class SessionRecord(UUIDPrimaryKeyMixin, Base):
    __tablename__ = "sessions"
    __table_args__ = (
        Index("ix_sessions_user", "usuario_id"),
        Index("ix_sessions_expires", "expires_at"),
    )

    usuario_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"), nullable=False
    )
    token_hash: Mapped[bytes] = mapped_column(LargeBinary(32), nullable=False, unique=True)
    last_activity_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    usuario: Mapped[User] = relationship(back_populates="sessions")
