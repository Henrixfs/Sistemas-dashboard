"""Audit-log persistence model."""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Any

from sqlalchemy import DateTime, ForeignKey, Index, String, Uuid, func
from sqlalchemy.dialects.postgresql import INET, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.mixins import UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.user import User


class AuditLog(UUIDPrimaryKeyMixin, Base):
    __tablename__ = "audit_log"
    __table_args__ = (
        Index("ix_audit_log_user_created", "usuario_id", "created_at"),
        Index("ix_audit_log_operation_created", "tipo_operacion", "created_at"),
        Index("ix_audit_log_entity_created", "entidad_tipo", "entidad_id", "created_at"),
    )

    usuario_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"), nullable=False
    )
    tipo_operacion: Mapped[str] = mapped_column(String(100), nullable=False)
    entidad_tipo: Mapped[str] = mapped_column(String(100), nullable=False)
    entidad_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    detalle: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False)
    direccion_ip: Mapped[str | None] = mapped_column(INET)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    usuario: Mapped[User] = relationship(back_populates="audit_entries")
