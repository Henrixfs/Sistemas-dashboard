"""Financial period persistence model."""

from __future__ import annotations

import uuid
from datetime import date, datetime
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, Date, DateTime, ForeignKey, SmallInteger, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.mixins import TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.movement import Movement
    from app.models.user import User


class FinancialPeriod(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "financial_periods"
    __table_args__ = (
        CheckConstraint("fecha_inicio < fecha_fin", name="ck_financial_periods_date_range"),
        CheckConstraint("estado IN ('abierto', 'cerrado')", name="ck_financial_periods_estado"),
    )

    nombre: Mapped[str] = mapped_column(String(150), nullable=False)
    anio: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    fecha_inicio: Mapped[date] = mapped_column(Date, nullable=False)
    fecha_fin: Mapped[date] = mapped_column(Date, nullable=False)
    estado: Mapped[str] = mapped_column(String(20), nullable=False)
    closed_by: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"), nullable=True
    )
    closed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    cerrado_por: Mapped[User | None] = relationship(back_populates="closed_periods")
    movements: Mapped[list[Movement]] = relationship(back_populates="periodo")
