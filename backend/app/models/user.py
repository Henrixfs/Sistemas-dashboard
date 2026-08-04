"""User persistence model."""

from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, CheckConstraint, ForeignKey, Index, String, Text, func, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.mixins import TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.audit_log import AuditLog
    from app.models.correction_history import CorrectionHistory
    from app.models.financial_period import FinancialPeriod
    from app.models.movement import Movement
    from app.models.session import SessionRecord
    from app.models.voucher import Voucher


class User(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "users"
    __table_args__ = (
        CheckConstraint(
            "rol IN ('alumno', 'administrador', 'superadministrador')", name="ck_users_rol"
        ),
        CheckConstraint(
            "rol <> 'alumno' OR codigo_estudiante IS NOT NULL",
            name="ck_users_alumno_codigo_estudiante",
        ),
        CheckConstraint(
            "rol NOT IN ('administrador', 'superadministrador') OR email IS NOT NULL",
            name="ck_users_administrativo_email",
        ),
        Index(
            "uq_users_codigo_estudiante_not_null",
            "codigo_estudiante",
            unique=True,
            postgresql_where=text("codigo_estudiante IS NOT NULL"),
        ),
    )

    email: Mapped[str | None] = mapped_column(String(320))
    password_hash: Mapped[str] = mapped_column(Text, nullable=False)
    nombres: Mapped[str] = mapped_column(String(150), nullable=False)
    apellidos: Mapped[str] = mapped_column(String(150), nullable=False)
    codigo_estudiante: Mapped[str | None] = mapped_column(String(50))
    rol: Mapped[str] = mapped_column(String(20), nullable=False)
    activo: Mapped[bool] = mapped_column(Boolean, nullable=False)
    must_change_password: Mapped[bool] = mapped_column(Boolean, nullable=False)
    created_by: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT")
    )

    sessions: Mapped[list[SessionRecord]] = relationship(back_populates="usuario")
    created_movements: Mapped[list[Movement]] = relationship(
        foreign_keys="Movement.created_by", back_populates="creado_por"
    )
    updated_movements: Mapped[list[Movement]] = relationship(
        foreign_keys="Movement.updated_by", back_populates="actualizado_por"
    )
    published_movements: Mapped[list[Movement]] = relationship(
        foreign_keys="Movement.published_by", back_populates="publicado_por"
    )
    annulled_movements: Mapped[list[Movement]] = relationship(
        foreign_keys="Movement.annulled_by", back_populates="anulado_por"
    )
    closed_periods: Mapped[list[FinancialPeriod]] = relationship(back_populates="cerrado_por")
    corrections: Mapped[list[CorrectionHistory]] = relationship(back_populates="usuario")
    audit_entries: Mapped[list[AuditLog]] = relationship(back_populates="usuario")
    uploaded_vouchers: Mapped[list[Voucher]] = relationship(
        foreign_keys="Voucher.uploaded_by", back_populates="subido_por"
    )
    replaced_vouchers: Mapped[list[Voucher]] = relationship(
        foreign_keys="Voucher.replaced_by", back_populates="reemplazado_por"
    )


Index(
    "uq_users_email_normalized",
    func.lower(User.email),
    unique=True,
    postgresql_where=User.email.is_not(None),
)
