"""Financial movement persistence model."""

from __future__ import annotations

import uuid
from datetime import date, datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, Date, DateTime, ForeignKey, Index, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.mixins import TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.category import Category
    from app.models.correction_history import CorrectionHistory
    from app.models.financial_period import FinancialPeriod
    from app.models.user import User
    from app.models.voucher import Voucher


class Movement(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "movements"
    __table_args__ = (
        CheckConstraint("tipo IN ('ingreso', 'gasto')", name="ck_movements_tipo"),
        CheckConstraint(
            "estado IN ('borrador', 'publicado', 'anulado')", name="ck_movements_estado"
        ),
        CheckConstraint("monto > 0", name="ck_movements_monto_positive"),
        CheckConstraint(
            "tipo != 'ingreso' OR length(btrim(fuente)) > 0", name="ck_movements_ingreso_fuente"
        ),
        CheckConstraint(
            "estado = 'borrador' OR (published_by IS NOT NULL AND published_at IS NOT NULL)",
            name="ck_movements_publication_metadata",
        ),
        CheckConstraint(
            "estado != 'anulado' OR "
            "(length(btrim(justificacion_anulacion)) > 0 AND annulled_by IS NOT NULL "
            "AND annulled_at IS NOT NULL)",
            name="ck_movements_annulment_metadata",
        ),
        CheckConstraint(
            "reemplaza_movimiento_id IS NULL OR reemplaza_movimiento_id <> id",
            name="ck_movements_replacement_not_self",
        ),
        Index(
            "ix_movements_period_state_type_date",
            "periodo_id",
            "estado",
            "tipo",
            "fecha_movimiento",
        ),
        Index("ix_movements_category", "categoria_id"),
    )

    periodo_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("financial_periods.id", ondelete="RESTRICT"), nullable=False
    )
    tipo: Mapped[str] = mapped_column(String(20), nullable=False)
    categoria_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("categories.id", ondelete="RESTRICT")
    )
    fuente: Mapped[str | None] = mapped_column(String(255))
    descripcion: Mapped[str] = mapped_column(Text, nullable=False)
    monto: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False)
    proveedor: Mapped[str | None] = mapped_column(String(255))
    estado: Mapped[str] = mapped_column(String(20), nullable=False)
    fecha_movimiento: Mapped[date] = mapped_column(Date, nullable=False)
    created_by: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"), nullable=False
    )
    updated_by: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT")
    )
    published_by: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT")
    )
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    justificacion_anulacion: Mapped[str | None] = mapped_column(Text)
    annulled_by: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT")
    )
    annulled_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    reemplaza_movimiento_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("movements.id", ondelete="RESTRICT")
    )

    periodo: Mapped[FinancialPeriod] = relationship(back_populates="movements")
    categoria: Mapped[Category | None] = relationship(back_populates="movements")
    creado_por: Mapped[User] = relationship(
        foreign_keys=[created_by], back_populates="created_movements"
    )
    actualizado_por: Mapped[User | None] = relationship(
        foreign_keys=[updated_by], back_populates="updated_movements"
    )
    publicado_por: Mapped[User | None] = relationship(
        foreign_keys=[published_by], back_populates="published_movements"
    )
    anulado_por: Mapped[User | None] = relationship(
        foreign_keys=[annulled_by], back_populates="annulled_movements"
    )
    movimiento_original: Mapped[Movement | None] = relationship(
        remote_side="Movement.id", back_populates="movimientos_reemplazo"
    )
    movimientos_reemplazo: Mapped[list[Movement]] = relationship(
        back_populates="movimiento_original"
    )
    vouchers: Mapped[list[Voucher]] = relationship(back_populates="movement")
    corrections: Mapped[list[CorrectionHistory]] = relationship(back_populates="movement")
