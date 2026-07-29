# voucher-attachment

Adjunto, visualización y reemplazo de comprobantes digitales (PDF/imagen).

## ADDED Requirements

### Requirement: FR-VA-01 — Adjuntar comprobante a un movimiento
El administrador SHALL poder adjuntar uno o varios archivos de comprobante a un movimiento (ingreso o gasto) en cualquier estado.

#### Scenario: Adjunto exitoso de comprobante
- **Given** un administrador autenticado y un movimiento en estado borrador
- **When** selecciona un archivo PDF válido y lo adjunta al movimiento
- **Then** el sistema asocia el archivo al movimiento, lo almacena y muestra el nombre del comprobante en los detalles del movimiento

#### Scenario: Adjunto de archivo con formato no soportado
- **Given** un administrador autenticado y un movimiento en estado borrador
- **When** intenta adjuntar un archivo con extensión .exe
- **Then** el sistema rechaza el archivo e indica que solo se permiten formatos PDF, JPG y PNG

### Requirement: FR-VA-02 — Visualizar comprobante
El alumno SHALL poder visualizar los comprobantes adjuntos a movimientos publicados, siempre que el administrador no haya restringido su visibilidad.

#### Scenario: Alumno visualiza comprobante permitido
- **Given** un alumno autenticado y un movimiento publicado con un comprobante visible adjunto
- **When** hace clic en el nombre del comprobante
- **Then** el sistema muestra una vista previa o descarga del archivo

#### Scenario: Alumno intenta ver comprobante de movimiento en borrador
- **Given** un alumno autenticado y un movimiento en estado borrador con comprobante adjunto
- **When** intenta acceder al comprobante
- **Then** el sistema deniega el acceso porque el movimiento aún no está publicado

### Requirement: FR-VA-03 — Reemplazar comprobante
El administrador SHALL poder reemplazar un comprobante adjunto, registrando el motivo del reemplazo.

#### Scenario: Reemplazo exitoso de comprobante
- **Given** un administrador autenticado y un movimiento publicado con un comprobante adjunto
- **When** selecciona reemplazar el comprobante, adjunta un nuevo archivo, indica el motivo "El comprobante anterior tenía un error de tipeo en el RUC" y confirma
- **Then** el sistema reemplaza el archivo, registra el motivo en el historial y notifica al administrador

#### Scenario: Reemplazo de comprobante sin motivo
- **Given** un administrador autenticado y un movimiento con comprobante adjunto
- **When** intenta reemplazar el comprobante sin proporcionar un motivo
- **Then** el sistema rechaza la operación e indica que el motivo es obligatorio

### Requirement: BR-VA-01 — El comprobante original se conserva
Al reemplazar un comprobante, el archivo original SHALL conservarse en el sistema con una referencia al motivo de reemplazo.

#### Scenario: Verificación de conservación del original
- **Given** un administrador que reemplazó un comprobante con motivo registrado
- **When** se consulta el historial de comprobantes del movimiento
- **Then** el sistema muestra tanto el comprobante original como el reemplazo, cada uno con su fecha y motivo asociado
