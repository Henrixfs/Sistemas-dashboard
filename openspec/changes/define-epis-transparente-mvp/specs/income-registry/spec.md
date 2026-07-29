# income-registry

Registro de ingresos y aportes con sus datos asociados.

## ADDED Requirements

### Requirement: FR-IR-01 — Registrar ingreso
El administrador SHALL poder registrar un ingreso económico indicando periodo, descripción, monto en soles, fecha, fuente del ingreso y opcionalmente un comprobante.

#### Scenario: Registro exitoso de ingreso en borrador
- **Given** un administrador autenticado y un periodo abierto
- **When** completa los datos del ingreso (descripción "Aporte ordinario 2025-I", monto S/ 5000.00, fuente "Ministerio de Educación") y guarda como borrador
- **Then** el sistema crea el movimiento en estado borrador, lo asocia al periodo y lo muestra en la lista de movimientos del periodo

#### Scenario: Registro de ingreso con monto inválido
- **Given** un administrador autenticado y un periodo abierto
- **When** intenta registrar un ingreso con monto igual a S/ 0.00 o negativo
- **Then** el sistema rechaza el registro y muestra un mensaje indicando que el monto debe ser mayor a S/ 0.00

#### Scenario: Alumno intenta registrar un ingreso
- **Given** un alumno autenticado en el sistema
- **When** intenta acceder al formulario de registro de ingresos
- **Then** el sistema deniega el acceso y muestra un mensaje de permiso insuficiente

### Requirement: FR-IR-02 — Editar ingreso en borrador
El administrador SHALL poder modificar cualquier campo de un ingreso que se encuentre en estado borrador.

#### Scenario: Edición exitosa de ingreso en borrador
- **Given** un administrador autenticado y un ingreso en estado borrador
- **When** modifica el monto de S/ 5000.00 a S/ 5500.00 y guarda los cambios
- **Then** el sistema actualiza el monto del ingreso y mantiene el estado borrador

### Requirement: FR-IR-03 — Eliminar ingreso en borrador
El administrador SHALL poder eliminar un ingreso que se encuentre en estado borrador.

#### Scenario: Eliminación exitosa de ingreso en borrador
- **Given** un administrador autenticado y un ingreso en estado borrador
- **When** selecciona eliminar el ingreso y confirma la operación
- **Then** el sistema elimina el movimiento de forma permanente y lo notifica

### Requirement: BR-IR-01 — Ingreso publicado no se elimina
El sistema MUST impedir la eliminación física de un ingreso publicado. Cuando sea necesario invalidarlo, el administrador deberá anularlo con una justificación y el movimiento deberá permanecer visible en el historial correspondiente.

#### Scenario: Intento de eliminar ingreso publicado
- **Given** un administrador autenticado y un ingreso en estado publicado
- **When** intenta eliminar el ingreso
- **Then** el sistema deniega la operación e indica que los movimientos publicados no pueden eliminarse, solo anularse
