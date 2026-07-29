## Context

EPIS Transparente es un sistema web de transparencia financiera desde cero. No existe una aplicación previa ni legado técnico que condicione las decisiones. El MVP debe cubrir la gestión completa de periodos, ingresos, gastos, comprobantes y el flujo borrador/publicación, junto con un dashboard de consulta para alumnos autenticados. Las capacidades definidas en la propuesta abarcan 14 áreas funcionales que necesitan una arquitectura coherente, mantenible y que pueda crecer más allá del MVP.

## Goals / Non-Goals

**Goals:**
- Definir una arquitectura web moderna que separe frontend, backend y almacenamiento de archivos.
- Establecer un modelo de datos que soporte periodos, movimientos (ingresos/gastos), categorías, comprobantes, historial de correcciones y auditoría.
- Garantizar que los movimientos publicados no puedan eliminarse silenciosamente y que toda anulación quede registrada con justificación.
- Proveer autenticación diferenciada para administradores (gestión) y alumnos (consulta).
- Habilitar la consulta del saldo financiero calculado en tiempo real a partir de los movimientos publicados y vigentes.
- Asegurar que los comprobantes adjuntos sean accesibles solo para usuarios autenticados y con el rol adecuado.

**Non-Goals:**
- Definir el framework o lenguaje específico de implementación (se decide en la fase de codificación).
- Diseñar la UI en detalle (prototipos o mockups).
- Implementar integración con sistemas externos (bancos, SSO institucional).
- Definir la estrategia de despliegue o infraestructura en la nube.

## Decisions

| Decisión | Opción elegida | Alternativas consideradas | Razón |
|---|---|---|---|
| Arquitectura general | Frontend + API REST + Base de datos relacional + Almacenamiento de archivos | Monolito con plantillas SSR, GraphQL | Separación clara de concerns; REST es simple de implementar y consumir; la base relacional es natural para datos financieros con integridad transaccional. |
| Manejo de estado de movimientos | Patrón State con estados: borrador → publicado → anulado | Eliminación física, bandera activo/inactivo | El state pattern permite control explícito de transiciones válidas; un movimiento anulado conserva su registro histórico sin desaparecer. |
| Anulación vs corrección | Corrección permitida solo en campos no críticos (descripción, proveedor, categoría) con historial. Cambios en monto, tipo o periodo requieren anular + crear nuevo. | Corrección total con versionado | La regla de negocio es clara: si el movimiento cambia en sustancia, debe quedar trazabilidad del original y del nuevo. |
| Almacenamiento de comprobantes | Sistema de archivos con referencia en BD; acceso controlado por la aplicación | BD directa (BLOB), CDN externo | Almacenar binarios en BD escala mal; CDN es innecesario para el MVP. El sistema de archivos con ruta lógica permite migrar a CDN después. |
| Autenticación | Autenticación basada en sesión con correo y contraseña | JWT sin estado, SSO institucional | Sesión con cookie HttpOnly es simple y segura para MVP; SSO puede incorporarse después como alternativa. |
| Auditoría | Registro de auditoría en tabla separada (who, what, when, detail) | Logs de aplicación, triggers de BD | Tabla de auditoría explícita permite consultas y reportes; no depende de la retención de logs del servidor. |
| Cálculo de saldo | Sumatoria en tiempo real de ingresos - gastos (movimientos publicados y vigentes) | Saldo precálculado en tabla de periodos | Evita incoherencias por desincronización; BD relacional con índices adecuados lo hace eficiente para el volumen del MVP. |

## Risks / Trade-offs

- [Riesgo] La autenticación con correo/contraseña sin SSO puede ser un obstáculo si la institución exige integración con su sistema de cuentas. → Mitigación: diseñar la capa de autenticación como interfaz intercambiable desde el inicio.
- [Riesgo] El almacenamiento de comprobantes en el sistema de archivos del servidor no escala horizontalmente sin almacenamiento compartido. → Mitigación: usar rutas relativas y una abstracción de almacenamiento que permita migrar a S3/compatible después.
- [Riesgo] El cálculo de saldo en tiempo real puede volverse lento con muchos movimientos. → Mitigación: para el volumen esperado de una escuela (cientos, no miles de movimientos por periodo) no será un problema. Si lo fuera, puede cachearse o precálcularse.
- [Trade-off] El state pattern para movimientos agrega complejidad inicial pero evita bugs de consistencia difíciles de corregir después.

## Open Questions

- ¿Se usará un ORM o SQL directo para la capa de datos?
- ¿La sesión del alumno se crea con pre-registro (el administrador crea la cuenta) o con auto-registro más validación?
- ¿Los comprobantes deben tener algún procesamiento (generar thumbnail, sanitizar metadatos, ocultar información sensible) antes de almacenarse?
- ¿Se requiere paginación en el dashboard del alumno o es aceptable mostrar todos los movimientos del periodo seleccionado?
- ¿Hay algún lineamiento institucional sobre colores, logo o imagen de la escuela que deba reflejarse en la interfaz?
