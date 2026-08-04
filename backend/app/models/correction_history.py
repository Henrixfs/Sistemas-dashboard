"""Immutable correction-history persistence model."""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Any

from sqlalchemy import DateTime, ForeignKey, Index, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.mixins import UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.movement import Movement
    from app.models.user import User


class CorrectionHistory(UUIDPrimaryKeyMixin, Base):
    __tablename__ = "correction_history"
    __table_args__ = (Index("ix_correction_history_movement_created", "movement_id", "created_at"),)

    movement_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("movements.id", ondelete="RESTRICT"), nullable=False
    )
    campo: Mapped[str] = mapped_column(String(100), nullable=False)
    valor_anterior: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False)
    valor_nuevo: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False)
    usuario_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"), nullable=False
    )
    motivo: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    movement: Mapped[Movement] = relationship(back_populates="corrections")
    usuario: Mapped[User] = relationship(back_populates="corrections")
