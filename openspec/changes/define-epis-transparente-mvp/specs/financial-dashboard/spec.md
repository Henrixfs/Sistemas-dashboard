# financial-dashboard

Panel financiero interactivo para consulta de ingresos, gastos, saldo y movimientos.

## ADDED Requirements

### Requirement: FR-FD-01 — Visualizar saldo del periodo
El dashboard SHALL mostrar el saldo actual del periodo financiero seleccionado, calculado como la diferencia entre el total de ingresos y el total de gastos publicados y vigentes.

#### Scenario: Visualización de saldo con datos positivos
- **Given** un alumno autenticado y un periodo con ingresos publicados por S/ 10 000.00 y gastos publicados por S/ 4000.00
- **When** accede al dashboard
- **Then** el sistema muestra saldo de S/ 6000.00, total ingresos S/ 10 000.00 y total gastos S/ 4000.00

#### Scenario: Visualización de saldo en periodo sin movimientos
- **Given** un alumno autenticado y un periodo sin movimientos publicados
- **When** selecciona ese periodo en el dashboard
- **Then** el sistema muestra saldo S/ 0.00, total ingresos S/ 0.00 y total gastos S/ 0.00

### Requirement: FR-FD-02 — Consultar movimientos del periodo
El dashboard SHALL mostrar la lista de movimientos (ingresos y gastos) del periodo seleccionado, indicando tipo, descripción, monto, categoría, fecha y estado.

#### Scenario: Visualización de movimientos publicados
- **Given** un alumno autenticado y un periodo con movimientos publicados
- **When** accede al dashboard y selecciona el periodo
- **Then** el sistema muestra una lista con todos los movimientos publicados del periodo, ordenados por fecha (más reciente primero)

### Requirement: FR-FD-03 — Seleccionar periodo
El dashboard SHALL permitir al alumno seleccionar qué periodo financiero desea consultar mediante un selector.

#### Scenario: Cambio de periodo en el dashboard
- **Given** un alumno autenticado y múltiples periodos registrados
- **When** selecciona un periodo diferente en el selector
- **Then** el dashboard se actualiza para mostrar los datos del periodo seleccionado

### Requirement: FR-FD-04 — Ver detalle de movimiento
El dashboard SHALL permitir al alumno hacer clic en un movimiento para ver su detalle: descripción completa, monto, categoría, proveedor (si aplica), fecha, comprobante adjunto (si visible) y estado.

#### Scenario: Consulta de detalle de gasto
- **Given** un alumno autenticado y un gasto publicado
- **When** hace clic en el gasto de la lista
- **Then** el sistema muestra una vista detallada con todos los campos del movimiento

### Requirement: FR-FD-05 — Ver fecha de última actualización
El dashboard SHALL mostrar la fecha y hora de la última actualización de la información financiera del periodo.

#### Scenario: Visualización de última actualización
- **Given** un alumno autenticado en el dashboard
- **When** consulta un periodo
- **Then** el sistema muestra la fecha y hora del último movimiento publicado o corrección realizada en ese periodo

### Requirement: BR-FD-01 — Solo movimientos publicados y vigentes afectan el dashboard
El dashboard SHALL considerar exclusivamente los movimientos en estado "publicado" y que no hayan sido anulados.

#### Scenario: Movimiento anulado no aparece en dashboard
- **Given** un alumno autenticado y un periodo donde un gasto de S/ 1000.00 fue anulado
- **When** consulta el dashboard
- **Then** el gasto anulado no aparece en la lista de movimientos y no afecta el saldo calculado

### Requirement: NFR-FD-01 — Tiempo de carga del dashboard
El dashboard SHALL cargar los datos del periodo seleccionado en un tiempo máximo de 3 segundos en condiciones normales de operación.

#### Scenario: Verificación de rendimiento del dashboard
- **Given** un alumno autenticado y un periodo con hasta 500 movimientos
- **When** selecciona el periodo
- **Then** el dashboard se renderiza completamente en menos de 3 segundos
