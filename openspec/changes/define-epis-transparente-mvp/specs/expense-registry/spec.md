# expense-registry

Registro de gastos con categorización y datos del proveedor.

## ADDED Requirements

### Requirement: FR-ER-01 — Registrar gasto
El administrador SHALL poder registrar un gasto indicando periodo, categoría, descripción, monto en soles, proveedor y opcionalmente un comprobante.

#### Scenario: Registro exitoso de gasto en borrador
- **Given** un administrador autenticado y un periodo abierto
- **When** completa los datos del gasto (categoría "Material didáctico", descripción "Adquisición de proyector", monto S/ 2500.00, proveedor "TecnoSoluciones EIRL") y guarda como borrador
- **Then** el sistema crea el movimiento en estado borrador, lo asocia al periodo y lo muestra en la lista de movimientos

#### Scenario: Registro de gasto con monto mayor al saldo disponible
- **Given** un administrador autenticado, un periodo abierto con saldo de S/ 1000.00
- **When** intenta registrar un gasto de S/ 1500.00
- **Then** el sistema permite el registro (el gasto se registra igualmente; el saldo negativo es informativo)

### Requirement: FR-ER-02 — Listar gastos por periodo
El sistema SHALL mostrar al administrador la lista de gastos filtrados por periodo, con opción de ver solo borradores, solo publicados o todos.

#### Scenario: Visualización de gastos filtrados
- **Given** un administrador autenticado y un periodo con gastos en diversos estados
- **When** selecciona el periodo y el filtro "publicados"
- **Then** el sistema muestra únicamente los gastos en estado publicado de ese periodo

### Requirement: FR-ER-03 — Editar gasto en borrador
El administrador SHALL poder modificar cualquier campo de un gasto en estado borrador.

#### Scenario: Edición exitosa de gasto en borrador
- **Given** un administrador autenticado y un gasto en estado borrador
- **When** modifica el proveedor de "TecnoSoluciones EIRL" a "InnovaTech Perú" y guarda
- **Then** el sistema actualiza el proveedor y mantiene el estado borrador

### Requirement: FR-ER-04 — Eliminar gasto en borrador
El administrador SHALL poder eliminar un gasto en estado borrador.

#### Scenario: Eliminación exitosa de gasto en borrador
- **Given** un administrador autenticado y un gasto en estado borrador
- **When** selecciona eliminar el gasto y confirma la operación
- **Then** el sistema elimina el movimiento de forma permanente

### Requirement: BR-ER-01 — Gasto publicado no se elimina
El sistema MUST impedir la eliminación física de un gasto publicado. Cuando sea necesario invalidarlo, el administrador deberá anularlo con una justificación y el movimiento deberá permanecer visible en el historial correspondiente.

#### Scenario: Intento de eliminar gasto publicado
- **Given** un administrador autenticado y un gasto en estado publicado
- **When** intenta eliminar el gasto
- **Then** el sistema deniega la operación e indica que los movimientos publicados no pueden eliminarse, solo anularse

### Requirement: BR-ER-02 — Gasto publicado requiere comprobante válido
Un gasto en estado borrador SHALL poder existir sin comprobante. El sistema MUST impedir que un gasto pase a estado publicado si no tiene al menos un comprobante válido asociado conforme a FR-VA-01; la validación SHALL ejecutarse al intentar publicarlo.

#### Scenario: Guardar gasto sin comprobante como borrador
- **Given** un administrador autenticado y un periodo abierto
- **When** registra un gasto sin adjuntar comprobante y lo guarda como borrador
- **Then** el sistema crea el gasto en estado borrador

#### Scenario: Publicar gasto con comprobante válido
- **Given** un administrador autenticado y un gasto en estado borrador con al menos un comprobante válido asociado
- **When** intenta publicar el movimiento
- **Then** el sistema publica el gasto
