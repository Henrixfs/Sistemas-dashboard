"""add financial integrity triggers

Revision ID: 8b53d93b4fc1
Revises: 2e6e98d8c631
Create Date: 2026-08-03 23:59:00.000000
"""

from typing import Sequence, Union

from alembic import op

revision: str = "8b53d93b4fc1"
down_revision: Union[str, Sequence[str], None] = "2e6e98d8c631"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add database protections for financial history and audit records."""
    op.execute(
        """
        CREATE FUNCTION enforce_movement_state_and_financial_immutability()
        RETURNS trigger
        LANGUAGE plpgsql
        AS $$
        BEGIN
            IF TG_OP = 'UPDATE' THEN
                IF OLD.estado = 'anulado' THEN
                    RAISE EXCEPTION 'voided movements are read-only' USING ERRCODE = '55000';
                END IF;

                IF OLD.estado = 'borrador' AND NEW.estado NOT IN ('borrador', 'publicado') THEN
                    RAISE EXCEPTION 'a draft movement can only remain draft or be published'
                        USING ERRCODE = '23514';
                END IF;

                IF OLD.estado = 'publicado' AND NEW.estado NOT IN ('publicado', 'anulado') THEN
                    RAISE EXCEPTION 'a published movement can only remain published or be voided'
                        USING ERRCODE = '23514';
                END IF;

                IF OLD.estado = 'publicado' AND (
                    NEW.monto IS DISTINCT FROM OLD.monto
                    OR NEW.tipo IS DISTINCT FROM OLD.tipo
                    OR NEW.periodo_id IS DISTINCT FROM OLD.periodo_id
                    OR NEW.fecha_movimiento IS DISTINCT FROM OLD.fecha_movimiento
                ) THEN
                    RAISE EXCEPTION 'financial fields of a published movement are immutable'
                        USING ERRCODE = '55000';
                END IF;
            END IF;
            RETURN NEW;
        END;
        $$;
        """
    )
    op.execute(
        """
        CREATE TRIGGER trg_enforce_movement_state_and_financial_immutability
        BEFORE UPDATE ON movements
        FOR EACH ROW
        EXECUTE FUNCTION enforce_movement_state_and_financial_immutability();
        """
    )
    op.execute(
        """
        CREATE FUNCTION require_voucher_for_expense_publication()
        RETURNS trigger
        LANGUAGE plpgsql
        AS $$
        BEGIN
            IF NEW.tipo = 'gasto'
                AND NEW.estado = 'publicado'
                AND (TG_OP = 'INSERT' OR OLD.estado = 'borrador')
                AND NOT EXISTS (
                    SELECT 1
                    FROM vouchers
                    WHERE movement_id = NEW.id
                ) THEN
                RAISE EXCEPTION 'an expense requires a valid voucher before publication'
                    USING ERRCODE = '23514';
            END IF;
            RETURN NEW;
        END;
        $$;
        """
    )
    op.execute(
        """
        CREATE TRIGGER trg_require_voucher_for_expense_publication
        BEFORE INSERT OR UPDATE OF estado ON movements
        FOR EACH ROW
        EXECUTE FUNCTION require_voucher_for_expense_publication();
        """
    )
    op.execute(
        """
        CREATE FUNCTION prevent_historical_movement_deletion()
        RETURNS trigger
        LANGUAGE plpgsql
        AS $$
        BEGIN
            IF OLD.estado IN ('publicado', 'anulado') THEN
                RAISE EXCEPTION 'published or voided movements cannot be deleted'
                    USING ERRCODE = '55000';
            END IF;
            RETURN OLD;
        END;
        $$;
        """
    )
    op.execute(
        """
        CREATE TRIGGER trg_prevent_historical_movement_deletion
        BEFORE DELETE ON movements
        FOR EACH ROW
        EXECUTE FUNCTION prevent_historical_movement_deletion();
        """
    )
    op.execute(
        """
        CREATE FUNCTION prevent_closed_period_movement_mutation()
        RETURNS trigger
        LANGUAGE plpgsql
        AS $$
        DECLARE
            target_period_id uuid;
        BEGIN
            IF TG_OP = 'DELETE' THEN
                target_period_id := OLD.periodo_id;
            ELSE
                target_period_id := NEW.periodo_id;
            END IF;

            IF EXISTS (
                SELECT 1
                FROM financial_periods
                WHERE id = target_period_id AND estado = 'cerrado'
            ) THEN
                IF TG_OP IN ('INSERT', 'DELETE') THEN
                    RAISE EXCEPTION 'financial data in a closed period is read-only'
                        USING ERRCODE = '55000';
                ELSIF (
                    NEW.periodo_id IS DISTINCT FROM OLD.periodo_id
                    OR NEW.tipo IS DISTINCT FROM OLD.tipo
                    OR NEW.monto IS DISTINCT FROM OLD.monto
                    OR NEW.estado IS DISTINCT FROM OLD.estado
                    OR NEW.fecha_movimiento IS DISTINCT FROM OLD.fecha_movimiento
                    OR NEW.published_by IS DISTINCT FROM OLD.published_by
                    OR NEW.published_at IS DISTINCT FROM OLD.published_at
                    OR NEW.annulled_by IS DISTINCT FROM OLD.annulled_by
                    OR NEW.annulled_at IS DISTINCT FROM OLD.annulled_at
                    OR NEW.justificacion_anulacion IS DISTINCT FROM OLD.justificacion_anulacion
                    OR NEW.reemplaza_movimiento_id IS DISTINCT FROM OLD.reemplaza_movimiento_id
                ) THEN
                    RAISE EXCEPTION 'financial data in a closed period is read-only'
                        USING ERRCODE = '55000';
                END IF;
            END IF;

            IF TG_OP = 'DELETE' THEN
                RETURN OLD;
            END IF;
            RETURN NEW;
        END;
        $$;
        """
    )
    op.execute(
        """
        CREATE TRIGGER trg_prevent_closed_period_movement_mutation
        BEFORE INSERT OR UPDATE OR DELETE ON movements
        FOR EACH ROW
        EXECUTE FUNCTION prevent_closed_period_movement_mutation();
        """
    )
    op.execute(
        """
        CREATE FUNCTION prevent_audit_log_mutation()
        RETURNS trigger
        LANGUAGE plpgsql
        AS $$
        BEGIN
            RAISE EXCEPTION 'audit log records are immutable' USING ERRCODE = '55000';
        END;
        $$;
        """
    )
    op.execute(
        """
        CREATE TRIGGER trg_prevent_audit_log_mutation
        BEFORE UPDATE OR DELETE ON audit_log
        FOR EACH ROW
        EXECUTE FUNCTION prevent_audit_log_mutation();
        """
    )


def downgrade() -> None:
    """Remove database protections introduced by this revision."""
    op.execute("DROP TRIGGER IF EXISTS trg_require_voucher_for_expense_publication ON movements")
    op.execute("DROP FUNCTION IF EXISTS require_voucher_for_expense_publication()")
    op.execute(
        "DROP TRIGGER IF EXISTS trg_enforce_movement_state_and_financial_immutability ON movements"
    )
    op.execute("DROP FUNCTION IF EXISTS enforce_movement_state_and_financial_immutability()")
    op.execute("DROP TRIGGER IF EXISTS trg_prevent_audit_log_mutation ON audit_log")
    op.execute("DROP FUNCTION IF EXISTS prevent_audit_log_mutation()")
    op.execute("DROP TRIGGER IF EXISTS trg_prevent_closed_period_movement_mutation ON movements")
    op.execute("DROP FUNCTION IF EXISTS prevent_closed_period_movement_mutation()")
    op.execute("DROP TRIGGER IF EXISTS trg_prevent_historical_movement_deletion ON movements")
    op.execute("DROP FUNCTION IF EXISTS prevent_historical_movement_deletion()")
