# financial-periods

Gestión de periodos financieros (apertura, cierre, vigencia).

## ADDED Requirements

### Requirement: FR-FP-01 — Crear periodo financiero
El administrador SHALL poder crear un periodo financiero indicando nombre, año, fecha de inicio y fecha de fin.

#### Scenario: Creación exitosa de periodo
- **Given** un administrador autenticado en el sistema
- **When** completa el formulario con nombre "Periodo 2025-I", año 2025, inicio 01/03/2025 y fin 31/07/2025, y confirma la creación
- **Then** el sistema registra el periodo, lo muestra en la lista de periodos y confirma la operación

#### Scenario: Intento de crear periodo con fechas inválidas
- **Given** un administrador autenticado en el sistema
- **When** completa el formulario con fecha de inicio posterior a la fecha de fin
- **Then** el sistema rechaza la operación y muestra un mensaje indicando que la fecha de inicio debe ser anterior a la fecha de fin

### Requirement: FR-FP-02 — Listar periodos financieros
El sistema SHALL mostrar al administrador la lista de todos los periodos registrados con su estado (abierto/cerrado).

#### Scenario: Visualización de lista de periodos
- **Given** un administrador autenticado en el sistema y existen periodos registrados
- **When** accede a la sección de periodos financieros
- **Then** el sistema muestra una tabla con nombre, año, rango de fechas y estado de cada periodo

#### Scenario: Alumno intenta acceder a la lista de periodos
- **Given** un alumno autenticado en el sistema
- **When** intenta acceder a la gestión de periodos financieros
- **Then** el sistema deniega el acceso y muestra un mensaje de permiso insuficiente

### Requirement: FR-FP-03 — Cerrar periodo financiero
El administrador SHALL poder cerrar un periodo financiero. Un periodo cerrado no acepta nuevos movimientos.

#### Scenario: Cierre exitoso de periodo
- **Given** un administrador autenticado y un periodo abierto sin movimientos pendientes
- **When** selecciona cerrar el periodo y confirma la acción
- **Then** el sistema cambia el estado del periodo a "cerrado" y lo notifica al administrador

#### Scenario: Intento de cerrar periodo con movimientos en borrador
- **Given** un administrador autenticado y un periodo que contiene movimientos en estado borrador
- **When** intenta cerrar el periodo
- **Then** el sistema rechaza el cierre e indica que existen movimientos en borrador que deben publicarse o eliminarse primero

#### Scenario: Alumno intenta cerrar un periodo
- **Given** un alumno autenticado en el sistema
- **When** intenta cerrar un periodo financiero
- **Then** el sistema deniega la operación y muestra un mensaje de permiso insuficiente

### Requirement: BR-FP-01 — Un periodo cerrado no se puede reabrir
Un periodo financiero cerrado SHALL permanecer en estado cerrado y no podrá reabrirse.

#### Scenario: Intento de reabrir periodo cerrado
- **Given** un administrador autenticado y un periodo en estado cerrado
- **When** intenta reabrir el periodo
- **Then** el sistema deniega la operación e indica que los periodos cerrados no pueden reabrirse

### Requirement: BR-FP-02 — Periodo cerrado de solo lectura
Un periodo financiero cerrado SHALL ser de solo lectura respecto de sus datos financieros asociados. El sistema MUST impedir crear, modificar o eliminar movimientos, comprobantes y correcciones vinculados a dicho periodo.

#### Scenario: Intento de modificar un movimiento de periodo cerrado
- **Given** un administrador autenticado y un periodo cerrado con un movimiento asociado
- **When** intenta modificar, anular o adjuntar un comprobante al movimiento
- **Then** el sistema rechaza la operación e indica que el periodo está cerrado y es de solo lectura
