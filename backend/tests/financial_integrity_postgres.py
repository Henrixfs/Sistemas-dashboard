"""Executable PostgreSQL integration checks for the financial integrity migration.

Run this module inside the backend container. It wraps all fixtures in one
transaction and rolls it back, so no test data remains in PostgreSQL.
"""

from __future__ import annotations

import os
import uuid
from datetime import date, datetime, timezone
from decimal import Decimal

from sqlalchemy import Connection, create_engine, text
from sqlalchemy.exc import DBAPIError


def _expect_failure(connection: Connection, statement: str, **params: object) -> None:
    savepoint = connection.begin_nested()
    try:
        connection.execute(text(statement), params)
    except DBAPIError:
        savepoint.rollback()
        return
    savepoint.rollback()
    raise AssertionError("The statement unexpectedly succeeded")


def _insert_movement(
    connection: Connection,
    *,
    movement_id: uuid.UUID,
    period_id: uuid.UUID,
    user_id: uuid.UUID,
    movement_type: str,
    state: str = "borrador",
    amount: Decimal = Decimal("10.00"),
    published_by: uuid.UUID | None = None,
    published_at: datetime | None = None,
    annulled_by: uuid.UUID | None = None,
    annulled_at: datetime | None = None,
    annulment_reason: str | None = None,
) -> None:
    connection.execute(
        text(
            """
            INSERT INTO movements (
                id, periodo_id, tipo, fuente, descripcion, monto, estado, fecha_movimiento,
                created_by, published_by, published_at, annulled_by, annulled_at,
                justificacion_anulacion
            ) VALUES (
                :id, :period_id, :movement_type, :source, 'integrity test', :amount, :state,
                :movement_date, :user_id, :published_by, :published_at, :annulled_by,
                :annulled_at, :annulment_reason
            )
            """
        ),
        {
            "id": movement_id,
            "period_id": period_id,
            "movement_type": movement_type,
            "source": "test source" if movement_type == "ingreso" else None,
            "amount": amount,
            "state": state,
            "movement_date": date(2026, 8, 3),
            "user_id": user_id,
            "published_by": published_by,
            "published_at": published_at,
            "annulled_by": annulled_by,
            "annulled_at": annulled_at,
            "annulment_reason": annulment_reason,
        },
    )


def run_integrity_checks() -> None:
    """Exercise every database rule required by tasks 3.10 through 3.14."""
    engine = create_engine(os.environ["DATABASE_URL"])
    now = datetime.now(timezone.utc)
    user_id, open_period_id = (uuid.uuid4() for _ in range(2))

    with engine.connect() as connection:
        transaction = connection.begin()
        try:
            connection.execute(
                text(
                    """
                    INSERT INTO users (id, email, password_hash, nombres, apellidos, rol, activo,
                                       must_change_password)
                    VALUES (:id, :email, 'not-a-secret', 'Integration', 'Tester', 'administrador',
                            true, false)
                    """
                ),
                {"id": user_id, "email": f"integrity-{user_id}@example.test"},
            )
            for period_id, state in ((open_period_id, "abierto"),):
                connection.execute(
                    text(
                        """
                        INSERT INTO financial_periods (
                            id, nombre, anio, fecha_inicio, fecha_fin, estado,
                            created_at, updated_at
                        ) VALUES (:id, :name, 2026, '2026-01-01', '2026-12-31', :state, :now, :now)
                        """
                    ),
                    {
                        "id": period_id,
                        "name": f"Integrity {state} {period_id}",
                        "state": state,
                        "now": now,
                    },
                )

            draft_id = uuid.uuid4()
            _insert_movement(
                connection,
                movement_id=draft_id,
                period_id=open_period_id,
                user_id=user_id,
                movement_type="ingreso",
            )
            connection.execute(text("DELETE FROM movements WHERE id = :id"), {"id": draft_id})

            published_income_id = uuid.uuid4()
            _insert_movement(
                connection,
                movement_id=published_income_id,
                period_id=open_period_id,
                user_id=user_id,
                movement_type="ingreso",
            )
            connection.execute(
                text(
                    """
                    UPDATE movements
                    SET estado = 'publicado', published_by = :user_id, published_at = :now
                    WHERE id = :id
                    """
                ),
                {"id": published_income_id, "user_id": user_id, "now": now},
            )
            _expect_failure(
                connection, "DELETE FROM movements WHERE id = :id", id=published_income_id
            )
            _expect_failure(
                connection,
                "UPDATE movements SET monto = 99.00 WHERE id = :id",
                id=published_income_id,
            )
            _expect_failure(
                connection,
                "UPDATE movements SET estado = 'borrador' WHERE id = :id",
                id=published_income_id,
            )
            _expect_failure(
                connection,
                "UPDATE movements SET estado = 'anulado' WHERE id = :id",
                id=published_income_id,
            )

            voided_id = uuid.uuid4()
            _insert_movement(
                connection,
                movement_id=voided_id,
                period_id=open_period_id,
                user_id=user_id,
                movement_type="ingreso",
                state="publicado",
                published_by=user_id,
                published_at=now,
            )
            connection.execute(
                text(
                    """
                    UPDATE movements
                    SET estado = 'anulado', annulled_by = :user_id, annulled_at = :now,
                        justificacion_anulacion = 'integration test void'
                    WHERE id = :id
                    """
                ),
                {"id": voided_id, "user_id": user_id, "now": now},
            )
            _expect_failure(connection, "DELETE FROM movements WHERE id = :id", id=voided_id)

            expense_without_voucher_id = uuid.uuid4()
            _insert_movement(
                connection,
                movement_id=expense_without_voucher_id,
                period_id=open_period_id,
                user_id=user_id,
                movement_type="gasto",
            )
            _expect_failure(
                connection,
                """
                UPDATE movements
                SET estado = 'publicado', published_by = :user_id, published_at = :now
                WHERE id = :id
                """,
                id=expense_without_voucher_id,
                user_id=user_id,
                now=now,
            )

            expense_with_voucher_id = uuid.uuid4()
            _insert_movement(
                connection,
                movement_id=expense_with_voucher_id,
                period_id=open_period_id,
                user_id=user_id,
                movement_type="gasto",
            )
            connection.execute(
                text(
                    """
                    INSERT INTO vouchers (
                        id, movement_id, nombre_archivo, ruta_logica, tipo_mime, tamaño, visible,
                        uploaded_by
                    ) VALUES (
                        :id, :movement_id, 'valid.pdf', :path, 'application/pdf', 1, true, :user_id
                    )
                    """
                ),
                {
                    "id": uuid.uuid4(),
                    "movement_id": expense_with_voucher_id,
                    "path": f"integrity/{expense_with_voucher_id}.pdf",
                    "user_id": user_id,
                },
            )
            connection.execute(
                text(
                    """
                    UPDATE movements
                    SET estado = 'publicado', published_by = :user_id, published_at = :now
                    WHERE id = :id
                    """
                ),
                {"id": expense_with_voucher_id, "user_id": user_id, "now": now},
            )

            locked_period_id = uuid.uuid4()
            locked_movement_id = uuid.uuid4()
            connection.execute(
                text(
                    """
                    INSERT INTO financial_periods (
                        id, nombre, anio, fecha_inicio, fecha_fin, estado, created_at, updated_at
                    ) VALUES (:id, :name, 2026, '2026-01-01', '2026-12-31', 'abierto', :now, :now)
                    """
                ),
                {
                    "id": locked_period_id,
                    "name": f"Integrity locked {locked_period_id}",
                    "now": now,
                },
            )
            _insert_movement(
                connection,
                movement_id=locked_movement_id,
                period_id=locked_period_id,
                user_id=user_id,
                movement_type="ingreso",
            )
            connection.execute(
                text("UPDATE financial_periods SET estado = 'cerrado' WHERE id = :id"),
                {"id": locked_period_id},
            )
            _expect_failure(
                connection,
                "UPDATE movements SET monto = 99.00 WHERE id = :id",
                id=locked_movement_id,
            )

            _expect_failure(
                connection,
                """
                INSERT INTO movements (
                    id, periodo_id, tipo, fuente, descripcion, monto, estado, fecha_movimiento,
                    created_by
                ) VALUES (
                    :id, :period_id, 'ingreso', 'test source', 'invalid amount', 0.00, 'borrador',
                    '2026-08-03', :user_id
                )
                """,
                id=uuid.uuid4(),
                period_id=open_period_id,
                user_id=user_id,
            )

            audit_id = uuid.uuid4()
            connection.execute(
                text(
                    """
                    INSERT INTO audit_log (
                        id, usuario_id, tipo_operacion, entidad_tipo, entidad_id,
                        detalle, created_at
                    ) VALUES (
                        :id, :user_id, 'integration_test', 'movement', :entity_id, '{}'::jsonb, :now
                    )
                    """
                ),
                {"id": audit_id, "user_id": user_id, "entity_id": published_income_id, "now": now},
            )
            _expect_failure(
                connection,
                "UPDATE audit_log SET tipo_operacion = 'changed' WHERE id = :id",
                id=audit_id,
            )
            _expect_failure(connection, "DELETE FROM audit_log WHERE id = :id", id=audit_id)
        finally:
            transaction.rollback()


def test_postgresql_financial_integrity_rules() -> None:
    """Run the PostgreSQL checks when an integration database is explicitly enabled."""
    if os.environ.get("RUN_POSTGRES_INTEGRATION") != "1":
        import pytest

        pytest.skip("requires RUN_POSTGRES_INTEGRATION=1 and a PostgreSQL integration database")
    run_integrity_checks()


if __name__ == "__main__":
    run_integrity_checks()
