# movement-correction

Corrección de datos permitidos con historial y anulación de movimientos con justificación.

## ADDED Requirements

### Requirement: FR-MC-01 — Corregir datos documentales de movimiento publicado
El administrador SHALL poder corregir la descripción, el proveedor o la categoría de un movimiento publicado. Cada corrección SHALL registrarse en el historial del movimiento.

#### Scenario: Corrección exitosa de descripción
- **Given** un administrador autenticado y un movimiento publicado con descripción "Compra de proyector"
- **When** cambia la descripción a "Adquisición de proyector multimedia" y guarda
- **Then** el sistema actualiza la descripción, registra en el historial: valor anterior, valor nuevo, fecha, hora y administrador que realizó la corrección

#### Scenario: Corrección de descripción sin cambios
- **Given** un administrador autenticado y un movimiento publicado
- **When** intenta guardar la misma descripción sin modificaciones
- **Then** el sistema notifica que no hay cambios para guardar

### Requirement: FR-MC-02 — Anular movimiento publicado
El administrador SHALL poder anular un movimiento publicado. La anulación SHALL requerir una justificación obligatoria. Un movimiento anulado no afecta el saldo.

#### Scenario: Anulación exitosa de movimiento
- **Given** un administrador autenticado y un movimiento publicado
- **When** selecciona anular el movimiento, ingresa la justificación "El gasto fue registrado en el periodo incorrecto" y confirma
- **Then** el sistema cambia el estado del movimiento a "anulado", registra la justificación, fecha, hora y administrador, y el movimiento deja de afectar el saldo del dashboard

#### Scenario: Anulación sin justificación
- **Given** un administrador autenticado y un movimiento publicado
- **When** intenta anular el movimiento sin proporcionar justificación
- **Then** el sistema rechaza la anulación e indica que la justificación es obligatoria

### Requirement: FR-MC-03 — Reemplazar movimiento por cambio de monto, tipo o periodo
Si el administrador necesita cambiar el monto, el tipo de movimiento (ingreso ↔ gasto) o el periodo, SHALL anular el movimiento original y crear uno nuevo.

#### Scenario: Cambio de monto mediante anulación y nuevo registro
- **Given** un administrador autenticado y un gasto publicado por S/ 2500.00
- **When** anula el gasto con justificación "El monto correcto es S/ 2750.00", crea un nuevo gasto por S/ 2750.00 y lo publica
- **Then** el movimiento original queda anulado con su justificación, el nuevo movimiento se crea con estado publicado, y el saldo refleja solo el nuevo movimiento

### Requirement: BR-MC-01 — Los movimientos anulados no afectan el saldo
Un movimiento en estado anulado SHALL excluirse del cálculo de saldo en el dashboard financiero.

#### Scenario: Verificación de saldo tras anulación
- **Given** un periodo con un ingreso de S/ 5000.00 y un gasto de S/ 2000.00 (saldo S/ 3000.00)
- **When** el administrador anula el gasto de S/ 2000.00
- **Then** el saldo del periodo se recalcula a S/ 5000.00 (solo considera el ingreso vigente)

### Requirement: BR-MC-02 — Toda anulación queda registrada en el historial
Cada anulación SHALL incluir en el historial: movimiento original, justificación, fecha, hora, administrador que anuló y el movimiento de reemplazo si existe.

#### Scenario: Consulta de historial de anulación
- **Given** un administrador que anuló un movimiento con justificación
- **When** consulta el historial del movimiento anulado
- **Then** el sistema muestra los datos completos de la anulación
