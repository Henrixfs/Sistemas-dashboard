# draft-workflow

Flujo de borrador y publicación de movimientos financieros.

## ADDED Requirements

### Requirement: FR-DW-01 — Guardar movimiento como borrador
El administrador SHALL poder guardar un movimiento (ingreso o gasto) como borrador sin publicarlo. Los borradores solo son visibles para el administrador.

#### Scenario: Guardar movimiento como borrador
- **Given** un administrador autenticado completando los datos de un nuevo gasto
- **When** hace clic en "Guardar como borrador"
- **Then** el sistema crea el movimiento en estado borrador y no es visible para los alumnos

### Requirement: FR-DW-02 — Publicar movimiento
El administrador SHALL poder publicar un movimiento en estado borrador. Al publicarse, el movimiento se vuelve visible para los alumnos en el dashboard. Un ingreso puede publicarse sin comprobante. Un gasto SHALL tener al menos un comprobante válido asociado conforme a FR-VA-01 antes de pasar a publicado; esta validación ocurre al intentar publicar, no al guardar el borrador.

#### Scenario: Publicación exitosa de movimiento
- **Given** un administrador autenticado y un movimiento en estado borrador con todos los campos obligatorios completos
- **When** selecciona publicar el movimiento y confirma la acción
- **Then** el sistema cambia el estado del movimiento a "publicado", registra la fecha y hora de publicación, y el movimiento aparece en el dashboard del alumno

#### Scenario: Publicación de ingreso sin comprobante
- **Given** un administrador autenticado y un ingreso en estado borrador sin comprobante adjunto
- **When** intenta publicar el movimiento
- **Then** el sistema permite la publicación

#### Scenario: Publicación de gasto sin comprobante válido
- **Given** un administrador autenticado y un gasto en estado borrador sin comprobante válido asociado
- **When** intenta publicar el movimiento
- **Then** el sistema rechaza la publicación e indica que el gasto requiere al menos un comprobante válido

### Requirement: FR-DW-03 — Listar movimientos por estado
El administrador SHALL poder filtrar los movimientos por estado (borrador, publicado, anulado) dentro de un periodo seleccionado.

#### Scenario: Filtro por estado borrador
- **Given** un administrador autenticado y un periodo con movimientos en diversos estados
- **When** selecciona el filtro "Borrador"
- **Then** el sistema muestra únicamente los movimientos en estado borrador de ese periodo

### Requirement: BR-DW-01 — Solo el administrador puede publicar
La acción de publicar un movimiento SHALL estar restringida exclusivamente al rol de administrador.

#### Scenario: Alumno intenta publicar un movimiento
- **Given** un alumno autenticado en el sistema
- **When** intenta acceder a la funcionalidad de publicación
- **Then** el sistema deniega el acceso

### Requirement: BR-DW-02 — Los borradores pueden editarse y eliminarse
Un movimiento en estado borrador SHALL poder ser editado o eliminado por el administrador sin restricciones.

#### Scenario: Editar borrador
- **Given** un administrador autenticado y un movimiento en estado borrador
- **When** modifica la descripción y guarda
- **Then** el sistema actualiza el movimiento sin crear historial de cambios

#### Scenario: Eliminar borrador
- **Given** un administrador autenticado y un movimiento en estado borrador
- **When** elimina el movimiento y confirma
- **Then** el sistema elimina el movimiento de forma permanente
