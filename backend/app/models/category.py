"""Expense category persistence model."""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.mixins import TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.movement import Movement


class Category(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "categories"
    __table_args__ = (UniqueConstraint("nombre", name="uq_categories_nombre"),)

    nombre: Mapped[str] = mapped_column(String(150), nullable=False)
    descripcion: Mapped[str | None] = mapped_column(Text)
    activa: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    movements: Mapped[list[Movement]] = relationship(back_populates="categoria")
