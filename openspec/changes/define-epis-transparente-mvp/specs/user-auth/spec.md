# user-auth

Autenticación y control de acceso para administradores y alumnos.

## ADDED Requirements

### Requirement: FR-UA-01 — Iniciar sesión
El sistema SHALL permitir a administradores y alumnos iniciar sesión con correo electrónico y contraseña.

#### Scenario: Inicio de sesión exitoso como administrador
- **Given** un administrador registrado con correo "admin@epis.edu.pe" y contraseña válida
- **When** ingresa sus credenciales correctas y hace clic en "Iniciar sesión"
- **Then** el sistema autentica al usuario, redirige al panel de administración y muestra su nombre en la interfaz

#### Scenario: Inicio de sesión con credenciales incorrectas
- **Given** un usuario registrado
- **When** ingresa una contraseña incorrecta
- **Then** el sistema muestra un mensaje "Correo o contraseña incorrectos" sin revelar cuál es el error

#### Scenario: Intento de inicio de sesión con cuenta inexistente
- **Given** un correo no registrado en el sistema
- **When** intenta iniciar sesión con ese correo
- **Then** el sistema muestra el mismo mensaje genérico "Correo o contraseña incorrectos"

### Requirement: FR-UA-02 — Cerrar sesión
El sistema SHALL permitir a cualquier usuario autenticado cerrar su sesión.

#### Scenario: Cierre de sesión exitoso
- **Given** un usuario autenticado
- **When** hace clic en "Cerrar sesión"
- **Then** el sistema finaliza la sesión, redirige a la pantalla de inicio de sesión y requiere autenticación para acceder nuevamente

### Requirement: FR-UA-03 — Registro de alumnos
El sistema SHALL permitir que los alumnos se registren proporcionando su correo institucional, nombres, apellidos y código de estudiante.

#### Scenario: Registro exitoso de alumno
- **Given** un alumno con correo institucional "juan.perez@epis.edu.pe"
- **When** completa el formulario de registro con sus datos y confirma
- **Then** el sistema crea la cuenta del alumno y muestra un mensaje indicando que la cuenta está pendiente de activación

### Requirement: BR-UA-01 — Roles de usuario
El sistema SHALL definir dos roles: administrador y alumno. Cada rol tiene permisos específicos sobre las funcionalidades del sistema.

#### Scenario: Verificación de permisos de administrador
- **Given** un administrador autenticado
- **When** accede al sistema
- **Then** el sistema muestra las opciones de gestión: periodos, ingresos, gastos, categorías, comprobantes, reportes y auditoría

#### Scenario: Verificación de permisos de alumno
- **Given** un alumno autenticado
- **When** accede al sistema
- **Then** el sistema muestra únicamente el dashboard financiero y la opción de descargar reportes; las opciones de gestión no están disponibles

### Requirement: SEC-UA-01 — Protección de sesión
La sesión del usuario SHALL protegerse mediante cookie HttpOnly y expirar después de un periodo de inactividad.

#### Scenario: Expiración de sesión por inactividad
- **Given** un usuario autenticado
- **When** permanece inactivo por el tiempo máximo configurado
- **Then** el sistema cierra la sesión automáticamente y redirige al usuario a la pantalla de inicio de sesión

#### Scenario: Intento de acceso a ruta protegida sin sesión
- **Given** un usuario no autenticado
- **When** intenta acceder a una ruta protegida del dashboard
- **Then** el sistema redirige al usuario a la pantalla de inicio de sesión
