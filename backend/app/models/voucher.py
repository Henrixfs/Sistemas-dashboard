"""Voucher persistence model."""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    BigInteger,
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    LargeBinary,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.mixins import UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.movement import Movement
    from app.models.user import User


class Voucher(UUIDPrimaryKeyMixin, Base):
    __tablename__ = "vouchers"
    __table_args__ = (
        CheckConstraint("tamaño > 0", name="ck_vouchers_size_positive"),
        CheckConstraint(
            "tipo_mime IN ('application/pdf', 'image/jpeg', 'image/png')",
            name="ck_vouchers_tipo_mime",
        ),
        UniqueConstraint("ruta_logica", name="uq_vouchers_ruta_logica"),
        Index("ix_vouchers_movement", "movement_id"),
    )

    movement_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("movements.id", ondelete="RESTRICT"), nullable=False
    )
    nombre_archivo: Mapped[str] = mapped_column(String(255), nullable=False)
    ruta_logica: Mapped[str] = mapped_column(String(1024), nullable=False)
    tipo_mime: Mapped[str] = mapped_column(String(100), nullable=False)
    tamaño: Mapped[int] = mapped_column(BigInteger, nullable=False)
    visible: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    replaces_voucher_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("vouchers.id", ondelete="RESTRICT")
    )
    motivo_reemplazo: Mapped[str | None] = mapped_column(Text)
    uploaded_by: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"), nullable=False
    )
    replaced_by: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT")
    )
    replaced_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    sha256: Mapped[bytes | None] = mapped_column(LargeBinary(32))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    movement: Mapped[Movement] = relationship(back_populates="vouchers")
    comprobante_original: Mapped[Voucher | None] = relationship(
        remote_side="Voucher.id", back_populates="replacements"
    )
    replacements: Mapped[list[Voucher]] = relationship(back_populates="comprobante_original")
    subido_por: Mapped[User] = relationship(
        foreign_keys=[uploaded_by], back_populates="uploaded_vouchers"
    )
    reemplazado_por: Mapped[User | None] = relationship(
        foreign_keys=[replaced_by], back_populates="replaced_vouchers"
    )
