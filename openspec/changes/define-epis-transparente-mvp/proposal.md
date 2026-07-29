## Why

Los alumnos de la Escuela Profesional de Ingeniería de Sistemas no disponen de un medio accesible, transparente y confiable para conocer el estado financiero de su escuela. Actualmente la información está dispersa, no hay trazabilidad de ingresos y gastos, y los comprobantes no son visibles para la comunidad estudiantil. EPIS Transparente resuelve esta necesidad ofreciendo un sistema web
donde los alumnos autorizados de la Escuela Profesional de Ingeniería
de Sistemas puedan consultar la información financiera publicada,
conocer cuánto dinero ingresó, en qué se gastó, cuánto saldo queda,
qué comprobantes respaldan cada movimiento y cuándo se realizó la
última actualización.

## What Changes

- Sistema web de transparencia financiera para la Escuela Profesional de Ingeniería de Sistemas.
- Registro y publicación de periodos financieros, ingresos, gastos y categorías.
- Adjunto y visualización de comprobantes digitales que respalden los gastos.
- Flujo de trabajo de borrador → publicación para control de calidad de la información.
- Corrección y anulación controlada de movimientos publicados, con justificación e historial.
- Dashboard financiero con saldos, ingresos, gastos e indicadores claros.
- Autenticación para alumnos (consulta) y administradores (gestión).
- Reportes descargables para ambos roles.
- Registro de auditoría mínima de todas las operaciones críticas.
- Cálculo del saldo financiero a partir de los ingresos y gastos publicados y vigentes del periodo seleccionado.

## Capabilities

### New Capabilities

- `financial-periods`: Gestión de periodos financieros (apertura, cierre, vigencia).
- `income-registry`: Registro de ingresos y aportes con sus datos asociados.
- `expense-registry`: Registro de gastos con categorización y datos del proveedor.
- `voucher-attachment`: Adjunto, visualización y reemplazo de comprobantes digitales (PDF/imagen).
- `draft-workflow`: Flujo de borrador y publicación de movimientos financieros.
- `movement-correction`: Corrección de datos permitidos con historial y anulación de movimientos con justificación.
- `reports`: Generación y descarga de reportes financieros.
- `user-auth`: Autenticación y control de acceso para administradores y alumnos.
- `financial-dashboard`: Panel financiero interactivo para consulta de ingresos, gastos, saldo y movimientos.
- `audit-log`: Registro de auditoría para todas las operaciones críticas sobre movimientos y comprobantes.
- `category-management`: Creación, modificación, desactivación y consulta de categorías utilizadas para clasificar los gastos.
- `ui-ux-accessibility`: Diseño responsive, experiencia de usuario, estados de interfaz y accesibilidad conforme al objetivo WCAG 2.2 AA.
- `security-privacy`: Autenticación, autorización, protección de sesiones, archivos, comprobantes, datos personales y controles de seguridad.
- `software-quality`: Requisitos medibles de rendimiento, confiabilidad, mantenibilidad, compatibilidad, capacidad de prueba y disponibilidad.

### Modified Capabilities

- Ninguna. No existen especificaciones previas en este proyecto.

## Impact

**Usuarios:**
- Administradores de la escuela (docentes o personal designado) que registrarán y publicarán la información financiera.
- Alumnos de la Escuela Profesional de Ingeniería de Sistemas que consultarán el dashboard y descargarán reportes.

**Procesos:**
- Se introduce un flujo formal de publicación financiera con control de calidad (borrador → publicación).
- Se establece un proceso de corrección y anulación con justificación y auditoría.
- La información financiera pasa de estar dispersa a centralizada y trazable.

**Información:**
- Periodos financieros, ingresos, gastos, categorías, comprobantes, saldos y movimientos.
- Historial de correcciones y registro de auditoría.

## Alcance del MVP

- Funcionalidades completas para administradores: gestión de periodos, ingresos, gastos, comprobantes, flujo borrador/publicación, correcciones y anulaciones.
- Dashboard de consulta para alumnos con autenticación obligatoria.
- Visualización de comprobantes permitidos.
- Reportes descargables básicos.
- Auditoría mínima de operaciones críticas.
- Interfaz responsive, atractiva, clara y fácil de usar.
- Consideraciones de accesibilidad y seguridad básicas.
- Control de acceso y protección de la información sensible contenida en los comprobantes publicados.

## Fuera del MVP

- Pagos o transacciones en línea (el sistema no ejecuta pagos reales).
- Integración con bancos u otras instituciones externas.
- Notificaciones push o por correo electrónico.
- Roles adicionales (superadmin, revisor, etc.).
- Módulo de presupuestos o planificación financiera.
- Aplicación móvil nativa.
- Internacionalización (i18n).

## Riesgos Principales

- **Adopción**: Que los administradores no utilicen el sistema de forma consistente, dejando la información desactualizada.
- **Calidad de datos**: Que la información financiera ingresada contenga errores y el proceso de corrección no se use adecuadamente.
- **Seguridad**: Exposición de información financiera sensible si la autenticación o el control de acceso no son robustos.
- **Alcance**: Presión por incluir funcionalidades fuera del MVP que retrasen la entrega.
- **Privacidad**: Publicación accidental de datos personales o sensibles contenidos en los comprobantes financieros.

## Decisiones Pendientes

- Tipo de autenticación (correo/contraseña, SSO institucional, o ambos).
- Política de retención de comprobantes y límites de tamaño/formatos aceptados.
- Definición de "alumno válido" para el acceso al dashboard (todos los matriculados, solo los de la EPIS, etc.).
- Periodicidad recomendada de actualización de la información financiera.
- Plataforma de despliegue y requisitos de infraestructura.
- Mecanismo para crear, habilitar o importar las cuentas de los alumnos.
- Información sensible que deberá ocultarse antes de publicar un comprobante.
- Quién estará autorizado para crear cuentas de administrador.
- Tiempo durante el cual se conservarán los comprobantes y movimientos.
