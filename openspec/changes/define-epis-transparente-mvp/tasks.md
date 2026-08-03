## 1. Preparación y estructura del proyecto

- [x] 1.1 Crear repositorio con estructura de monorepo: `frontend/`, `backend/`, `database/`, `docker/`, `docs/`
- [x] 1.2 Inicializar proyecto backend con framework web (carpetas: `routes/`, `controllers/`, `services/`, `models/`, `middleware/`, `utils/`)
- [x] 1.3 Inicializar proyecto frontend con estructura de componentes (`components/`, `pages/`, `services/`, `styles/`)
- [x] 1.4 Configurar archivos de entorno (`.env.example`, `.env.development`, `.env.production`) con variables para BD, sesión, almacenamiento
- [x] 1.5 Configurar linters y formateadores (ESLint, Prettier para frontend; estilo equivalente para backend)
- [x] 1.6 Configurar gestor de dependencias (`package.json` con scripts dev, build, test, lint)
- [x] 1.7 Crear `README.md` con instrucciones de setup, variables de entorno y comandos disponibles

## 2. Infraestructura local y Docker

- [x] 2.1 Crear `docker-compose.yml` con servicios: app backend, base de datos PostgreSQL, adminer/pgadmin opcional
- [x] 2.2 Crear `Dockerfile` para backend (multi-stage: build + producción)
- [x] 2.3 Crear `Dockerfile` para frontend (servidor nginx para SPA en producción)
- [ ] 2.4 Crear script `docker/init-db.sql` con schema inicial de tablas
- [x] 2.5 Configurar volúmenes Docker para persistencia de datos y archivos de comprobantes
- [x] 2.6 Agregar script `scripts/setup-dev.sh` o `scripts/setup-dev.ps1` para entorno local sin Docker

## 3. Base de datos y migraciones

- [ ] 3.1 Crear migración inicial con tabla `users` (id, email, password_hash, nombres, apellidos, codigo_estudiante, rol, activo, created_at, updated_at) — FR-UA-01, FR-UA-03, BR-UA-01
- [ ] 3.2 Crear migración con tabla `financial_periods` (id, nombre, año, fecha_inicio, fecha_fin, estado, created_at, updated_at) — FR-FP-01, FR-FP-03
- [ ] 3.3 Crear migración con tabla `categories` (id, nombre, descripcion, activa, created_at, updated_at) — FR-CM-01, FR-CM-03
- [ ] 3.4 Crear migración con tabla `movements` (id, periodo_id, tipo [ingreso/gasto], categoria_id, descripcion, monto, proveedor, estado [borrador/publicado/anulado], fecha_movimiento, justificacion_anulacion, anulado_por, anulado_en, created_at, updated_at) — FR-IR-01, FR-ER-01, BR-MC-02
- [ ] 3.5 Crear migración con tabla `vouchers` (id, movement_id, nombre_archivo, ruta_archivo, tipo_mime, tamaño, visible, reemplazo_de, motivo_reemplazo, created_at) — FR-VA-01, FR-VA-03, BR-VA-01
- [ ] 3.6 Crear migración con tabla `correction_history` (id, movement_id, campo, valor_anterior, valor_nuevo, usuario_id, created_at) — FR-MC-01
- [ ] 3.7 Crear migración con tabla `audit_log` (id, usuario_id, tipo_operacion, entidad_tipo, entidad_id, detalle, direccion_ip, created_at) — FR-AL-01, BR-AL-01, BR-AL-02
- [ ] 3.8 Crear migración con tabla `sessions` (id, usuario_id, token, expires_at, created_at) — SEC-UA-01
- [ ] 3.9 Agregar índices en columnas de búsqueda frecuente: movements.periodo_id, movements.estado, movements.fecha_movimiento, audit_log.created_at, audit_log.tipo_operacion — NFR-SQ-01

## 4. Autenticación y control de acceso

- [ ] 4.1 Implementar endpoint `POST /api/auth/register` para registro de alumnos (nombres, apellidos, correo, código, contraseña) — FR-UA-03
- [ ] 4.2 Implementar endpoint `POST /api/auth/login` que valida credenciales, crea sesión y devuelve cookie HttpOnly — FR-UA-01, SEC-UA-01
- [ ] 4.3 Implementar endpoint `POST /api/auth/logout` que destruye la sesión activa — FR-UA-02
- [ ] 4.4 Implementar endpoint `GET /api/auth/me` que devuelve datos del usuario autenticado según su sesión — BR-UA-01
- [ ] 4.5 Implementar middleware `requireAuth` que verifica cookie de sesión válida en cada request protegido — SEC-UA-01
- [ ] 4.6 Implementar middleware `requireRole('admin')` que verifica que el usuario autenticado sea administrador — SEC-SP-02
- [ ] 4.7 Implementar expiración automática de sesión por inactividad (tiempo configurable vía env) — SEC-UA-01
- [ ] 4.8 Implementar hash de contraseñas con bcrypt antes de almacenar — SEC-SP-01
- [ ] 4.9 Implementar frontend: página de inicio de sesión con formulario y validación — FR-UA-01
- [ ] 4.10 Implementar frontend: página de registro de alumno con formulario y validación — FR-UA-03
- [ ] 4.11 Implementar frontend: navbar con información de usuario autenticado y botón de cerrar sesión — FR-UA-02
- [ ] 4.12 Implementar frontend: guardia de rutas que redirige a login si no hay sesión válida — SEC-UA-01
- [ ] 4.13 Implementar frontend: redirección por rol (admin a panel de gestión, alumno a dashboard) — BR-UA-01, SEC-SP-02

## 5. Periodos financieros

- [ ] 5.1 Implementar endpoint `POST /api/periods` para crear periodo (nombre, año, fecha_inicio, fecha_fin) — FR-FP-01
- [ ] 5.2 Implementar endpoint `GET /api/periods` para listar todos los periodos con estado (abierto/cerrado) — FR-FP-02
- [ ] 5.3 Implementar endpoint `PATCH /api/periods/:id/close` para cerrar periodo con validación de que no tenga borradores — FR-FP-03
- [ ] 5.4 Validar que la fecha de inicio sea anterior a la fecha de fin al crear periodo — FR-FP-01
- [ ] 5.5 Validar que no se puedan reabrir periodos cerrados — BR-FP-01
- [ ] 5.6 Restringir todos los endpoints de periodos al rol administrador — FR-FP-02
- [ ] 5.7 Implementar frontend: página de gestión de periodos con tabla y formulario de creación — FR-FP-01, FR-FP-02
- [ ] 5.8 Implementar frontend: acción de cerrar periodo con confirmación y feedback — FR-FP-03
- [ ] 5.9 Implementar frontend: selector de periodo reutilizable para usar en otras secciones — FR-FD-03

## 6. Categorías

- [ ] 6.1 Implementar endpoint `POST /api/categories` para crear categoría (nombre, descripción) — FR-CM-01
- [ ] 6.2 Implementar endpoint `GET /api/categories` para listar categorías activas e inactivas — FR-CM-04
- [ ] 6.3 Implementar endpoint `PATCH /api/categories/:id` para modificar nombre o descripción — FR-CM-02
- [ ] 6.4 Implementar endpoint `PATCH /api/categories/:id/deactivate` para desactivar categoría — FR-CM-03
- [ ] 6.5 Validar nombre único de categoría al crear y al modificar — FR-CM-01
- [ ] 6.6 Restringir todos los endpoints de categorías al rol administrador
- [ ] 6.7 Implementar frontend: página de gestión de categorías con tabla, formulario y acciones de editar/desactivar — FR-CM-01, FR-CM-02, FR-CM-03, FR-CM-04

## 7. Registro de ingresos

- [ ] 7.1 Implementar endpoint `POST /api/movements/income` para crear ingreso (periodo_id, descripcion, monto, fuente, opcional comprobante) en estado borrador — FR-IR-01
- [ ] 7.2 Implementar endpoint `PATCH /api/movements/:id` para editar campos de ingreso en estado borrador — FR-IR-02
- [ ] 7.3 Implementar endpoint `DELETE /api/movements/:id` para eliminar ingreso si está en estado borrador — FR-IR-03
- [ ] 7.4 Validar que no se pueda eliminar un ingreso en estado publicado — BR-IR-01
- [ ] 7.5 Validar que el monto del ingreso sea mayor a S/ 0.00 — FR-IR-01
- [ ] 7.6 Restringir endpoints de creación, edición y eliminación al rol administrador
- [ ] 7.7 Implementar frontend: formulario de registro de ingreso con campos y selector de periodo — FR-IR-01
- [ ] 7.8 Implementar frontend: acciones de editar y eliminar ingreso en tabla de movimientos (solo borradores) — FR-IR-02, FR-IR-03

## 8. Registro de gastos

- [ ] 8.1 Implementar endpoint `POST /api/movements/expense` para crear gasto (periodo_id, categoria_id, descripcion, monto, proveedor, opcional comprobante) en estado borrador — FR-ER-01
- [ ] 8.2 Implementar endpoint `PATCH /api/movements/:id` para editar campos de gasto en estado borrador — FR-ER-03
- [ ] 8.3 Implementar endpoint `DELETE /api/movements/:id` para eliminar gasto si está en estado borrador — FR-ER-04
- [ ] 8.4 Implementar endpoint `GET /api/movements?periodo_id=&estado=&tipo=` para listar movimientos con filtros — FR-ER-02, FR-DW-03
- [ ] 8.5 Validar que no se pueda eliminar un gasto en estado publicado — BR-ER-01
- [ ] 8.6 Validar que el monto del gasto sea mayor a S/ 0.00 — FR-ER-01
- [ ] 8.7 Restringir endpoints de creación, edición y eliminación al rol administrador
- [ ] 8.8 Implementar frontend: formulario de registro de gasto con selector de categoría y periodo — FR-ER-01
- [ ] 8.9 Implementar frontend: tabla de movimientos con filtros por periodo, estado y tipo — FR-ER-02, FR-DW-03
- [ ] 8.10 Implementar frontend: acciones de editar y eliminar gasto en tabla (solo borradores) — FR-ER-03, FR-ER-04

## 9. Comprobantes

- [ ] 9.1 Implementar endpoint `POST /api/movements/:id/vouchers` para adjuntar archivo a un movimiento — FR-VA-01
- [ ] 9.2 Implementar endpoint `GET /api/vouchers/:id` para servir archivo de comprobante (solo usuarios autenticados con permiso) — FR-VA-02, SEC-SP-03
- [ ] 9.3 Implementar endpoint `POST /api/vouchers/:id/replace` para reemplazar comprobante con motivo obligatorio — FR-VA-03
- [ ] 9.4 Validar formatos de archivo permitidos (PDF, JPG, PNG) al adjuntar — FR-VA-01
- [ ] 9.5 Validar que el motivo de reemplazo no esté vacío — FR-VA-03
- [ ] 9.6 Conservar el comprobante original al reemplazar, registrando la relación en BD — BR-VA-01
- [ ] 9.7 Restringir acceso a comprobantes de movimientos no publicados para alumnos — FR-VA-02
- [ ] 9.8 Almacenar archivos en sistema de archivos con ruta segura fuera del directorio público
- [ ] 9.9 Implementar frontend: componente de adjuntar archivo en formularios de movimiento — FR-VA-01
- [ ] 9.10 Implementar frontend: visualización de comprobante (vista previa o enlace de descarga) — FR-VA-02
- [ ] 9.11 Implementar frontend: diálogo de reemplazo de comprobante con campo de motivo — FR-VA-03

## 10. Flujo de borrador y publicación

- [ ] 10.1 Implementar endpoint `PATCH /api/movements/:id/publish` que cambia estado de borrador a publicado y registra fecha — FR-DW-02
- [ ] 10.2 Validar que solo el administrador pueda publicar movimientos — BR-DW-01
- [ ] 10.3 Validar que borradores puedan editarse (reutiliza 7.2 / 8.2) y eliminarse (reutiliza 7.3 / 8.3) sin restricciones — BR-DW-02
- [ ] 10.4 Implementar frontend: botón "Publicar" en tabla de movimientos con confirmación — FR-DW-02
- [ ] 10.5 Implementar frontend: indicador visual del estado de cada movimiento (borrador, publicado, anulado) — FR-DW-03

## 11. Correcciones y anulaciones

- [ ] 11.1 Implementar endpoint `PATCH /api/movements/:id/correct` para corregir descripción, proveedor o categoría de movimiento publicado, guardando valor anterior y nuevo en correction_history — FR-MC-01
- [ ] 11.2 Implementar endpoint `POST /api/movements/:id/void` para anular movimiento con justificación obligatoria, cambiando estado a "anulado" — FR-MC-02
- [ ] 11.3 Validar que la justificación de anulación no esté vacía — FR-MC-02
- [ ] 11.4 Validar que un movimiento anulado no se pueda modificar ni publicar nuevamente
- [ ] 11.5 Excluir movimientos anulados del cálculo de saldo en el dashboard — BR-MC-01
- [ ] 11.6 Registrar la anulación en el historial del movimiento (justificación, fecha, administrador) — BR-MC-02
- [ ] 11.7 Implementar flujo de "anular y crear nuevo" cuando cambia monto, tipo o periodo: endpoint que anula el original y redirige a formulario precargado — FR-MC-03
- [ ] 11.8 Implementar frontend: botón "Corregir" en detalle de movimiento publicado con formulario editable (solo campos permitidos) — FR-MC-01
- [ ] 11.9 Implementar frontend: diálogo de anulación con campo de justificación obligatorio — FR-MC-02
- [ ] 11.10 Implementar frontend: vista de historial de correcciones y anulaciones en detalle de movimiento — FR-MC-01, BR-MC-02

## 12. Auditoría

- [ ] 12.1 Implementar servicio de auditoría que registre automáticamente creación, publicación, corrección, anulación de movimientos y reemplazo de comprobantes — FR-AL-01
- [ ] 12.2 Incluir en cada registro: usuario, tipo de operación, entidad afectada, detalle de cambios, dirección IP y timestamp — BR-AL-02
- [ ] 12.3 Implementar endpoint `GET /api/audit-log` con filtros por fechas, tipo de operación, entidad y usuario — FR-AL-02
- [ ] 12.4 Garantizar que ninguna operación de BD permita modificar o eliminar registros de auditoría — BR-AL-01
- [ ] 12.5 Restringir acceso al log de auditoría al rol administrador
- [ ] 12.6 Implementar frontend: página de consulta de auditoría con filtros y tabla de resultados — FR-AL-02

## 13. Dashboard del alumno

- [ ] 13.1 Implementar endpoint `GET /api/dashboard/summary?periodo_id=` que devuelva resumen: total_ingresos, total_gastos, saldo, ultima_actualizacion — FR-FD-01, FR-FD-05
- [ ] 13.2 Implementar endpoint `GET /api/dashboard/movements?periodo_id=` que devuelva lista de movimientos publicados (no anulados) del periodo — FR-FD-02, BR-FD-01
- [ ] 13.3 Implementar endpoint `GET /api/dashboard/movements/:id` que devuelva detalle completo de un movimiento publicado — FR-FD-04
- [ ] 13.4 Calcular saldo como suma de ingresos menos suma de gastos (solo publicados y no anulados) — BR-MC-01, BR-FD-01
- [ ] 13.5 Implementar frontend: página de dashboard con tarjetas de total ingresos, total gastos, saldo — FR-FD-01
- [ ] 13.6 Implementar frontend: tabla de movimientos del periodo con orden por fecha descendente — FR-FD-02
- [ ] 13.7 Implementar frontend: selector de periodo que recarga los datos del dashboard — FR-FD-03
- [ ] 13.8 Implementar frontend: modal o vista de detalle de movimiento — FR-FD-04
- [ ] 13.9 Implementar frontend: indicador de última actualización del periodo — FR-FD-05
- [ ] 13.10 Verificar tiempo de carga del dashboard < 3 segundos con 500 movimientos de prueba — NFR-FD-01, NFR-SQ-01

## 14. Reportes

- [ ] 14.1 Implementar endpoint `GET /api/reports/movements?periodo_id=&tipo=&formato=pdf` para generar reporte PDF de movimientos (admin) — FR-RE-01
- [ ] 14.2 Implementar endpoint `GET /api/reports/movements?periodo_id=&tipo=&formato=csv` para generar reporte CSV de movimientos (admin) — FR-RE-01
- [ ] 14.3 Implementar endpoint `GET /api/reports/student?periodo_id=&formato=pdf` para generar reporte PDF de alumno (solo movimientos publicados) — FR-RE-02, BR-RE-01
- [ ] 14.4 Implementar filtro por tipo de movimiento (ingreso, gasto, todos) en reportes de admin — FR-RE-03
- [ ] 14.5 Implementar frontend: página de reportes con selector de periodo, tipo y formato (admin) — FR-RE-01
- [ ] 14.6 Implementar frontend: botón de descarga de reporte en dashboard del alumno — FR-RE-02

## 15. UI, UX y accesibilidad

- [ ] 15.1 Implementar layout responsive con CSS Grid/Flexbox que se adapte a móvil (375 px), tablet y escritorio — NFR-UX-01
- [ ] 15.2 Implementar indicador de carga (spinner/skeleton) en todas las vistas que hacen peticiones — NFR-UX-02
- [ ] 15.3 Implementar mensajes de error inline en formularios con resaltado visual del campo — NFR-UX-02
- [ ] 15.4 Implementar diálogos de confirmación antes de acciones destructivas (eliminar, anular, cerrar periodo) — NFR-UX-02
- [ ] 15.5 Implementar notificaciones toast para éxito/error de operaciones — NFR-UX-02
- [ ] 15.6 Implementar formato de montos en soles (S/ X XXX.XX) en todas las vistas — NFR-UX-03
- [ ] 15.7 Implementar navegación completa por teclado con orden de tabulación lógico y foco visible en todos los elementos interactivos — NFR-ACC-01
- [ ] 15.8 Agregar etiquetas `<label>` en todos los campos de formulario, asociadas correctamente mediante `for`/`id` — NFR-ACC-01
- [ ] 15.9 Agregar texto alternativo (`alt`) descriptivo en todos los iconos e imágenes decorativas — NFR-ACC-01
- [ ] 15.10 Verificar contraste de color mínimo 4.5:1 para texto normal y 3:1 para texto grande — NFR-ACC-01
- [ ] 15.11 Implementar roles ARIA y landmarks semánticos (`<nav>`, `<main>`, `<header>`, `<footer>`) — NFR-ACC-01
- [ ] 15.12 Probar navegación con lector de pantalla en flujos críticos (login, dashboard, listado de movimientos) — NFR-ACC-01

## 16. Seguridad y privacidad

- [ ] 16.1 Implementar token CSRF en todos los formularios de escritura y validarlo en backend — SEC-SP-04
- [ ] 16.2 Escapar toda salida de datos en frontend para prevenir XSS — SEC-SP-04
- [ ] 16.3 Usar consultas parametrizadas o ORM en todas las operaciones de BD para prevenir inyección SQL — SEC-SP-04
- [ ] 16.4 Configurar cookie de sesión con flags: HttpOnly, Secure (en producción), SameSite=Strict — SEC-UA-01
- [ ] 16.5 Implementar rate limiting en endpoints de autenticación (login, register) para prevenir fuerza bruta — SEC-SP-04
- [ ] 16.6 Almacenar comprobantes fuera del directorio público y servirlos solo mediante endpoint autenticado — SEC-SP-03
- [ ] 16.7 Verificar que los formularios de registro solo soliciten: nombres, apellidos, correo institucional y código de estudiante — SEC-SP-05
- [ ] 16.8 Implementar saneamiento de nombres de archivo al subir comprobantes (eliminar caracteres peligrosos, generar nombre único) — SEC-SP-03
- [ ] 16.9 Validar tamaño máximo de archivo de comprobante en backend
- [ ] 16.10 Verificar tiempo de respuesta de login < 2 segundos en condiciones normales — NFR-SP-01

## 17. Pruebas unitarias

- [ ] 17.1 Test: cálculo de saldo = total ingresos - total gastos (solo publicados y no anulados) — FR-FD-01, BR-MC-01, NFR-SQ-06
- [ ] 17.2 Test: movimiento anulado se excluye del saldo — BR-MC-01
- [ ] 17.3 Test: movimiento en borrador no aparece en dashboard de alumno — BR-FD-01
- [ ] 17.4 Test: no se puede eliminar movimiento publicado — BR-IR-01, BR-ER-01
- [ ] 17.5 Test: no se puede eliminar entrada de auditoría — BR-AL-01
- [ ] 17.6 Test: anulación sin justificación es rechazada — FR-MC-02
- [ ] 17.7 Test: corrección de descripción guarda historial con valor anterior y nuevo — FR-MC-01
- [ ] 17.8 Test: reemplazo de comprobante sin motivo es rechazado — FR-VA-03
- [ ] 17.9 Test: reemplazo de comprobante conserva el original — BR-VA-01
- [ ] 17.10 Test: no se puede cerrar periodo con borradores pendientes — FR-FP-03
- [ ] 17.11 Test: no se puede reabrir periodo cerrado — BR-FP-01
- [ ] 17.12 Test: registro con monto cero o negativo es rechazado — FR-IR-01, FR-ER-01
- [ ] 17.13 Test: hash de contraseña es diferente al texto original — SEC-SP-01
- [ ] 17.14 Test: periodo cerrado no acepta nuevos movimientos — FR-FP-03
- [ ] 17.15 Test: solo administrador puede publicar movimientos — BR-DW-01

## 18. Pruebas de integración

- [ ] 18.1 Test: flujo completo crear ingreso → publicar → aparece en dashboard de alumno — FR-IR-01, FR-DW-02, FR-FD-02
- [ ] 18.2 Test: flujo completo crear gasto → publicar → anular → saldo se recalcula — FR-ER-01, FR-MC-02, BR-MC-01
- [ ] 18.3 Test: flujo de corrección de descripción → historial registra cambio — FR-MC-01
- [ ] 18.4 Test: flujo de adjuntar → reemplazar comprobante con motivo → original se conserva — FR-VA-01, FR-VA-03, BR-VA-01
- [ ] 18.5 Test: registro de auditoría se crea al publicar, corregir y anular — FR-AL-01
- [ ] 18.6 Test: alumno no puede acceder a rutas de administración (gestión de periodos, categorías, movimientos) — SEC-SP-02
- [ ] 18.7 Test: sesión expira después del tiempo de inactividad configurado — SEC-UA-01
- [ ] 18.8 Test: endpoint público no sirve archivos de comprobante sin autenticación — SEC-SP-03
- [ ] 18.9 Test: reporte de alumno solo incluye movimientos publicados — BR-RE-01
- [ ] 18.10 Test: flujo de anulación + creación de nuevo movimiento por cambio de monto — FR-MC-03

## 19. Pruebas end-to-end

- [ ] 19.1 E2E: registro de alumno → login → consulta dashboard → descarga reporte
- [ ] 19.2 E2E: login admin → crear periodo → crear categoría → registrar ingreso → publicar → verificar saldo
- [ ] 19.3 E2E: login admin → registrar gasto → adjuntar comprobante → publicar → reemplazar comprobante
- [ ] 19.4 E2E: login admin → anular movimiento → verificar que no aparece en dashboard de alumno
- [ ] 19.5 E2E: login admin → corregir descripción de movimiento → verificar historial
- [ ] 19.6 E2E: login admin → cerrar periodo → verificar que no permite nuevos movimientos
- [ ] 19.7 E2E: verificar diseño responsive en 3 tamaños de pantalla (375 px, 768 px, 1920 px) — NFR-UX-01
- [ ] 19.8 E2E: verificar navegación completa con solo teclado en flujo dashboard — NFR-ACC-01
- [ ] 19.9 E2E: intentar acceso a ruta protegida sin sesión → redirige a login — SEC-UA-01
- [ ] 19.10 E2E: login con credenciales incorrectas → mensaje genérico de error — FR-UA-01

## 20. CI/CD y documentación

- [ ] 20.1 Configurar pipeline CI (GitHub Actions) que ejecute linter, pruebas unitarias y de integración en cada push
- [ ] 20.2 Configurar pipeline CI que ejecute pruebas E2E en pull requests
- [ ] 20.3 Configurar build automático de imágenes Docker en CI
- [ ] 20.4 Agregar script `docker/seed.sql` con datos de prueba para desarrollo (periodo, categorías, movimientos de ejemplo)
- [ ] 20.5 Documentar en `docs/architecture.md` la arquitectura, decisiones técnicas y justificaciones del diseño
- [ ] 20.6 Documentar en `docs/api.md` los endpoints REST con ejemplos de request/response
- [ ] 20.7 Documentar en `docs/deploy.md` el proceso de despliegue en producción
- [ ] 20.8 Documentar en `docs/testing.md` cómo ejecutar cada nivel de prueba y los datos necesarios
- [ ] 20.9 Verificar que el proyecto cumple NFR-SQ-07: disponibilidad en horario académico (lunes a viernes 7:00-22:00, sábados 8:00-14:00, uptime 99%)
