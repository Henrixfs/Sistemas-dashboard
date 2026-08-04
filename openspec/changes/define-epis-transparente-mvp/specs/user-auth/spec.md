# user-auth

Autenticación y control de acceso para administradores y alumnos.

## ADDED Requirements

### Requirement: FR-UA-01 — Iniciar sesión
El sistema SHALL permitir el inicio de sesión con contraseña usando el identificador correspondiente al rol: `codigo_estudiante` para alumnos y correo electrónico para administradores y superadministradores.

#### Scenario: Inicio de sesión exitoso como alumno
- **Given** un alumno importado y activo con código de estudiante y contraseña válida
- **When** ingresa su código de estudiante y contraseña correctos
- **Then** el sistema autentica al alumno y lo redirige al dashboard o al cambio obligatorio de contraseña cuando corresponda

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

### Requirement: FR-UA-03 — Importación administrativa de alumnos
El sistema SHALL crear cuentas de alumnos mediante importación desde un archivo Excel institucional. Cada alumno SHALL usar `codigo_estudiante` como identificador de acceso; el código será único y obligatorio para ese rol. No existirá autoregistro público de alumnos.

#### Scenario: Importación de alumnos con resumen
- **Given** un superadministrador con un archivo Excel institucional válido
- **When** inicia una importación de alumnos
- **Then** el sistema valida registros, evita códigos duplicados y alumnos existentes, crea las cuentas válidas y muestra los totales de creados, omitidos y errores sin exponer DNI ni contraseñas

### Requirement: BR-UA-01 — Roles de usuario
El sistema SHALL definir tres roles: alumno, administrador y superadministrador. Cada rol tiene permisos específicos sobre las funcionalidades del sistema.

#### Scenario: Verificación de permisos de administrador
- **Given** un administrador autenticado
- **When** accede al sistema
- **Then** el sistema muestra las opciones de gestión: periodos, ingresos, gastos, categorías, comprobantes, reportes y auditoría

#### Scenario: Verificación de permisos de alumno
- **Given** un alumno autenticado
- **When** accede al sistema
- **Then** el sistema muestra únicamente el dashboard financiero y la opción de descargar reportes; las opciones de gestión no están disponibles

### Requirement: SEC-UA-01 — Protección de sesión
La sesión del usuario SHALL protegerse mediante cookie HttpOnly y expirar después de un periodo de inactividad. El identificador real de sesión nunca SHALL almacenarse en texto plano; el almacenamiento persistente SHALL contener únicamente un hash del token y la metadata necesaria para revocación y control de inactividad.

#### Scenario: Expiración de sesión por inactividad
- **Given** un usuario autenticado
- **When** permanece inactivo por el tiempo máximo configurado
- **Then** el sistema cierra la sesión automáticamente y redirige al usuario a la pantalla de inicio de sesión

#### Scenario: Protección del identificador de sesión almacenado
- **Given** una sesión creada para un usuario autenticado
- **When** el sistema persiste la sesión
- **Then** almacena un hash del token, la fecha de última actividad, expiración y revocación, sin almacenar el token real en texto plano

#### Scenario: Intento de acceso a ruta protegida sin sesión
- **Given** un usuario no autenticado
- **When** intenta acceder a una ruta protegida del dashboard
- **Then** el sistema redirige al usuario a la pantalla de inicio de sesión

### Requirement: FR-UA-04 — Cambio obligatorio de contraseña inicial
Una cuenta de alumno importada SHALL iniciar con `must_change_password=true`. Después del primer inicio de sesión correcto, el sistema MUST exigir una contraseña nueva antes de permitir el acceso al resto de funcionalidades y, al completarse, SHALL establecer `must_change_password=false`.

#### Scenario: Alumno con contraseña temporal válida
- **Given** un alumno autenticado con `must_change_password=true`
- **When** intenta acceder al dashboard
- **Then** el sistema lo dirige al flujo de cambio obligatorio de contraseña

### Requirement: FR-UA-05 — Restablecimiento administrativo de acceso
El superadministrador SHALL poder restablecer el acceso de un alumno mediante un mecanismo temporal seguro. El restablecimiento SHALL establecer `must_change_password=true` y no persistirá una contraseña temporal en texto plano.

#### Scenario: Restablecimiento de un alumno
- **Given** un superadministrador y un alumno con problemas de acceso
- **When** el superadministrador restablece el acceso
- **Then** el sistema habilita un mecanismo temporal seguro, exige cambio de contraseña en el siguiente acceso y registra el evento sin secreto

### Requirement: FR-UA-06 — Bootstrap seguro de superadministrador
El sistema SHALL permitir crear la cuenta inicial de superadministrador mediante un mecanismo bootstrap seguro. Las credenciales MUST no estar hardcodeadas ni versionadas.

#### Scenario: Bootstrap inicial seguro
- **Given** un entorno sin superadministrador
- **When** el operador autorizado ejecuta el mecanismo bootstrap seguro
- **Then** el sistema crea la cuenta sin registrar ni exponer las credenciales en código, migraciones, Docker o archivos versionados

### Requirement: FR-UA-07 — Gestión privilegiada de administradores
El superadministrador SHALL poder crear, activar, desactivar y restablecer administradores. Un administrador ordinario MUST no crear superadministradores.

#### Scenario: Administrador intenta crear superadministrador
- **Given** un administrador autenticado sin rol superadministrador
- **When** intenta crear una cuenta superadministrador
- **Then** el sistema deniega la operación

### Requirement: BR-UA-02 — Identificadores por rol
Un alumno MUST tener `codigo_estudiante` único y obligatorio. Un administrador o superadministrador SHALL poder existir sin código estudiantil y utilizará un correo electrónico único normalizado como identificador administrativo.

#### Scenario: Administrador sin código estudiantil
- **Given** un superadministrador creando un administrador
- **When** registra un correo administrativo válido sin código estudiantil
- **Then** el sistema permite crear la cuenta administrativa
