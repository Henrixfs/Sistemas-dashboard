"""Schema metadata checks for the initial financial migration."""

from __future__ import annotations

from decimal import Decimal
from pathlib import Path

from alembic.config import Config
from alembic.script import ScriptDirectory
from sqlalchemy import Numeric

from app.models import Base
from app.models.movement import Movement

EXPECTED_TABLES = {
    "audit_log",
    "categories",
    "correction_history",
    "financial_periods",
    "movements",
    "sessions",
    "users",
    "vouchers",
}

EXPECTED_INDEXES = {
    "uq_users_email_normalized",
    "uq_users_codigo_estudiante_not_null",
    "ix_movements_period_state_type_date",
    "ix_movements_category",
    "ix_vouchers_movement",
    "ix_correction_history_movement_created",
    "ix_audit_log_user_created",
    "ix_audit_log_operation_created",
    "ix_audit_log_entity_created",
    "ix_sessions_user",
    "ix_sessions_expires",
}


def test_financial_metadata_defines_all_business_tables() -> None:
    assert EXPECTED_TABLES <= set(Base.metadata.tables)


def test_movement_amount_uses_decimal_numeric_14_2() -> None:
    amount_type = Movement.__table__.c.monto.type

    assert isinstance(amount_type, Numeric)
    assert (amount_type.precision, amount_type.scale, amount_type.asdecimal) == (14, 2, True)
    assert amount_type.python_type is Decimal


def test_metadata_defines_only_required_financial_indexes() -> None:
    index_names = {index.name for table in Base.metadata.tables.values() for index in table.indexes}

    assert EXPECTED_INDEXES <= index_names


def test_sessions_metadata_never_declares_a_plaintext_token() -> None:
    session_columns = Base.metadata.tables["sessions"].columns

    assert "token_hash" in session_columns
    assert "token" not in session_columns


def test_initial_alembic_revision_is_the_only_head() -> None:
    backend_dir = Path(__file__).resolve().parents[1]
    config = Config(str(backend_dir / "alembic.ini"))
    script = ScriptDirectory.from_config(config)

    assert script.get_heads() == ["8b53d93b4fc1"]
    assert script.get_revision("8b53d93b4fc1").down_revision == "2e6e98d8c631"
