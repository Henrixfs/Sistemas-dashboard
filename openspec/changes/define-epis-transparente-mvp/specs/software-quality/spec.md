# software-quality

Requisitos medibles de rendimiento, confiabilidad, mantenibilidad, compatibilidad, capacidad de prueba y disponibilidad.

## ADDED Requirements

### Requirement: NFR-SQ-01 — Rendimiento
El sistema SHALL responder a las solicitudes de lectura del dashboard del alumno en menos de 3 segundos para periodos con hasta 500 movimientos.

#### Scenario: Verificación de rendimiento en consulta de dashboard
- **Given** un alumno autenticado y un periodo con 500 movimientos publicados
- **When** selecciona el periodo en el dashboard
- **Then** el sistema muestra la información completa en menos de 3 segundos

### Requirement: NFR-SQ-02 — Rendimiento en operaciones de escritura
Las operaciones de escritura (crear, publicar, corregir, anular) SHALL completarse en menos de 2 segundos.

#### Scenario: Verificación de rendimiento al publicar movimiento
- **Given** un administrador autenticado y un movimiento en borrador
- **When** hace clic en "Publicar"
- **Then** el sistema cambia el estado a publicado y muestra la confirmación en menos de 2 segundos

### Requirement: NFR-SQ-03 — Confiabilidad
El sistema SHALL manejar correctamente errores inesperados sin mostrar información técnica al usuario ni dejar datos en estado inconsistente.

#### Scenario: Error controlado sin datos inconsistentes
- **Given** un administrador creando un movimiento
- **When** ocurre un error del servidor durante el guardado
- **Then** el sistema muestra un mensaje genérico "Ocurrió un error. Intente nuevamente." y no se crea un registro parcial

### Requirement: NFR-SQ-04 — Mantenibilidad
El código fuente SHALL seguir una estructura de proyecto definida, con separación clara de capas y utilización de un estilo de código consistente.

#### Scenario: Verificación de estructura del proyecto
- **Given** el repositorio del proyecto
- **When** se revisa la estructura de directorios
- **Then** existe una separación clara entre capa de presentación, lógica de negocio, acceso a datos y utilidades

### Requirement: NFR-SQ-05 — Compatibilidad
El sistema SHALL ser funcional en las versiones más recientes de los navegadores Chrome, Firefox, Edge y Safari.

#### Scenario: Verificación de compatibilidad en Chrome
- **Given** un usuario con Google Chrome versión actual
- **When** accede al sistema y navega por todas las secciones
- **Then** todas las funcionalidades operan correctamente sin errores de visualización

#### Scenario: Verificación de compatibilidad en Firefox
- **Given** un usuario con Mozilla Firefox versión actual
- **When** accede al sistema y navega por todas las secciones
- **Then** todas las funcionalidades operan correctamente sin errores de visualización

### Requirement: NFR-SQ-06 — Capacidad de prueba
Las reglas de negocio y la lógica de cálculo financiero SHALL diseñarse de forma que puedan ser probadas unitariamente sin dependencia de la interfaz de usuario.

#### Scenario: Prueba unitaria de cálculo de saldo
- **Given** un conjunto de movimientos de prueba (ingresos y gastos)
- **When** se ejecuta la función de cálculo de saldo
- **Then** el resultado es la diferencia correcta entre el total de ingresos y gastos vigentes

### Requirement: NFR-SQ-07 — Disponibilidad
El sistema SHALL estar disponible durante el horario académico regular (lunes a viernes de 7:00 a 22:00, sábados de 8:00 a 14:00) con un tiempo de actividad mínimo del 99%.

#### Scenario: Verificación de disponibilidad en horario académico
- **Given** un alumno que intenta acceder al sistema un lunes a las 10:00
- **When** solicita la página del dashboard
- **Then** el sistema responde correctamente
