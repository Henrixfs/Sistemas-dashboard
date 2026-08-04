# audit-log

Registro de auditoría para todas las operaciones críticas sobre movimientos y comprobantes.

## ADDED Requirements

### Requirement: FR-AL-01 — Registrar operaciones críticas
El sistema SHALL registrar automáticamente en el log de auditoría toda operación crítica: creación, publicación, corrección, anulación de movimientos, reemplazo de comprobantes, importación de alumnos, restablecimiento de acceso y gestión de administradores. Los detalles MUST excluir DNI, contraseñas y credenciales temporales.

#### Scenario: Registro de auditoría al publicar un movimiento
- **Given** un administrador autenticado
- **When** publica un movimiento
- **Then** el sistema registra en el log: tipo de operación "publicación", ID del movimiento, fecha, hora y administrador que realizó la operación

#### Scenario: Registro de auditoría al anular un movimiento
- **Given** un administrador autenticado
- **When** anula un movimiento con justificación
- **Then** el sistema registra en el log: tipo de operación "anulación", ID del movimiento, justificación, fecha, hora y administrador

#### Scenario: Registro de restablecimiento sin secreto
- **Given** un superadministrador que restablece el acceso de un alumno
- **When** se completa el restablecimiento
- **Then** el sistema registra el actor, cuenta afectada, fecha y tipo de operación sin incluir DNI, contraseña ni mecanismo temporal

### Requirement: FR-AL-02 — Consultar log de auditoría
El administrador SHALL poder consultar el log de auditoría filtrado por fechas, tipo de operación, movimiento o administrador.

#### Scenario: Consulta de auditoría por rango de fechas
- **Given** un administrador autenticado y operaciones registradas en el log
- **When** selecciona un rango de fechas y hace clic en "Consultar"
- **Then** el sistema muestra todas las entradas de auditoría dentro del rango seleccionado

#### Scenario: Alumno intenta consultar el log de auditoría
- **Given** un alumno autenticado
- **When** intenta acceder a la sección de auditoría
- **Then** el sistema deniega el acceso

### Requirement: BR-AL-01 — Inmutabilidad del registro
El sistema MUST conservar de forma inmutable los registros de auditoría generados por las operaciones críticas y no permitirá que los usuarios los modifiquen o eliminen mediante la aplicación. La implementación SHALL incluir protección a nivel de base de datos para impedir operaciones UPDATE o DELETE sobre estos registros.

#### Scenario: Intento de eliminar entrada de auditoría
- **Given** un administrador autenticado
- **When** intenta eliminar una entrada del log de auditoría
- **Then** el sistema deniega la operación e indica que el registro de auditoría es inmutable

### Requirement: BR-AL-02 — Información mínima del registro
Cada entrada de auditoría SHALL contener: fecha y hora, tipo de operación, ID del registro afectado, usuario que realizó la operación, detalle de los cambios (valores anteriores si aplica) y dirección IP de origen.

#### Scenario: Verificación de contenido del registro
- **Given** una corrección de descripción realizada por un administrador
- **When** se consulta el registro de auditoría de esa corrección
- **Then** el sistema muestra: fecha, hora, administrador, ID del movimiento, valor anterior de la descripción, valor nuevo y dirección IP
