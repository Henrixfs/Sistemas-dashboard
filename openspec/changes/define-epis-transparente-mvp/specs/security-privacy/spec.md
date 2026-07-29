# security-privacy

Autenticación, autorización, protección de sesiones, archivos, comprobantes, datos personales y controles de seguridad.

## ADDED Requirements

### Requirement: SEC-SP-01 — Contraseña almacenada de forma segura
Las contraseñas SHALL almacenarse utilizando un algoritmo de hash seguro con sal (bcrypt o equivalente).

#### Scenario: Verificación de contraseña
- **Given** un usuario registrado con contraseña "MiClave123"
- **When** inicia sesión con la contraseña correcta
- **Then** el sistema verifica la contraseña contra el hash almacenado y autentica al usuario

### Requirement: SEC-SP-02 — Control de acceso por rol
El sistema SHALL verificar los permisos del rol del usuario antes de permitir cualquier operación de gestión o consulta.

#### Scenario: Acceso denegado a funcionalidad de administrador
- **Given** un alumno autenticado
- **When** intenta acceder directamente a la URL de creación de periodos
- **Then** el sistema deniega el acceso con código 403 y redirige al dashboard

#### Scenario: Acceso permitido a funcionalidad de administrador
- **Given** un administrador autenticado
- **When** accede a la URL de creación de periodos
- **Then** el sistema permite el acceso y muestra el formulario correspondiente

### Requirement: SEC-SP-03 — Protección de comprobantes
Los archivos de comprobantes SHALL ser accesibles solo para usuarios autenticados y el sistema SHALL verificar el permiso específico antes de servir el archivo.

#### Scenario: Alumno visualiza comprobante permitido
- **Given** un alumno autenticado y un comprobante marcado como visible adjunto a un movimiento publicado
- **When** solicita ver el comprobante
- **Then** el sistema verifica la sesión, el permiso y sirve el archivo

#### Scenario: Acceso directo a archivo de comprobante sin autenticación
- **Given** un usuario no autenticado
- **When** intenta acceder directamente a la URL de un archivo de comprobante
- **Then** el sistema deniega el acceso y redirige al inicio de sesión

### Requirement: SEC-SP-04 — Protección contra ataques comunes
El sistema SHALL implementar protección contra CSRF, XSS e inyección SQL.

#### Scenario: Protección CSRF en formulario de creación
- **Given** un administrador autenticado con una sesión activa
- **When** envía un formulario de creación de periodo sin el token CSRF válido
- **Then** el sistema rechaza la solicitud y muestra un error de validación

### Requirement: SEC-SP-05 — Datos personales mínimos
El sistema SHALL solicitar y almacenar únicamente los datos personales estrictamente necesarios para la operación: nombres, apellidos, correo electrónico y código de estudiante.

#### Scenario: Verificación de datos solicitados en registro
- **Given** un alumno en la página de registro
- **When** revisa los campos del formulario
- **Then** los únicos campos personales solicitados son: nombres, apellidos, correo electrónico institucional y código de estudiante

### Requirement: NFR-SP-01 — Tiempo de respuesta de autenticación
El proceso de inicio de sesión SHALL completarse en un tiempo máximo de 2 segundos en condiciones normales.

#### Scenario: Verificación de rendimiento de autenticación
- **Given** un usuario con credenciales válidas
- **When** hace clic en "Iniciar sesión"
- **Then** el sistema autentica y redirige al usuario en menos de 2 segundos
