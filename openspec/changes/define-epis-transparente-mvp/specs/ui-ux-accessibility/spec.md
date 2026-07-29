# ui-ux-accessibility

Diseño responsive, experiencia de usuario, estados de interfaz y accesibilidad conforme al objetivo WCAG 2.2 AA.

## ADDED Requirements

### Requirement: NFR-UX-01 — Diseño responsive
La interfaz SHALL adaptarse correctamente a dispositivos móviles, tablets y pantallas de escritorio sin pérdida de funcionalidad.

#### Scenario: Visualización en dispositivo móvil
- **Given** un usuario accediendo al dashboard desde un dispositivo con ancho de 375 px
- **When** carga la página
- **Then** los elementos se reorganizan en una sola columna, los botones y enlaces son táctiles (mínimo 44×44 px) y no hay desbordamiento horizontal

#### Scenario: Visualización en escritorio
- **Given** un usuario accediendo desde una pantalla de 1920×1080
- **When** carga la página
- **Then** los elementos se distribuyen en el espacio disponible aprovechando el ancho sin que el contenido se estire desproporcionadamente

### Requirement: NFR-UX-02 — Estados de interfaz
Toda acción del usuario SHALL tener retroalimentación visual inmediata: carga, éxito, error y confirmación.

#### Scenario: Indicador de carga
- **Given** un usuario en el dashboard
- **When** selecciona un periodo para cargar sus datos
- **Then** el sistema muestra un indicador de carga mientras obtiene la información

#### Scenario: Mensaje de error en formulario
- **Given** un administrador llenando un formulario de registro de gasto
- **When** intenta guardar con un campo obligatorio vacío
- **Then** el sistema resalta el campo en error y muestra un mensaje descriptivo debajo del campo

#### Scenario: Confirmación antes de acción destructiva
- **Given** un administrador que intenta eliminar un movimiento en borrador
- **When** hace clic en "Eliminar"
- **Then** el sistema muestra un diálogo de confirmación con el mensaje "¿Está seguro de eliminar este movimiento? Esta acción no se puede deshacer."

### Requirement: NFR-UX-03 — Claridad y facilidad de uso
La interfaz SHALL utilizar un lenguaje claro, evitar jerga técnica innecesaria y presentar la información financiera de forma comprensible.

#### Scenario: Visualización de montos con formato
- **Given** un usuario viendo el dashboard
- **When** observa los montos
- **Then** los valores monetarios se muestran en formato soles peruanos con separadores de miles y dos decimales (ej. S/ 10 500.00)

### Requirement: NFR-ACC-01 — Accesibilidad WCAG 2.2 AA
La interfaz SHALL cumplir con los criterios de accesibilidad WCAG 2.2 nivel AA, incluyendo contraste de colores, navegación por teclado, texto alternativo en imágenes y etiquetas en formularios.

#### Scenario: Navegación por teclado
- **Given** un usuario que navega solo con el teclado
- **When** presiona Tab para recorrer los elementos interactivos
- **Then** el orden de tabulación es lógico, el foco es visible en cada elemento y todas las funciones son accesibles sin ratón

#### Scenario: Contraste de colores
- **Given** un usuario con baja visión
- **When** visualiza el dashboard
- **Then** el texto tiene una relación de contraste mínima de 4.5:1 con el fondo (texto normal) y 3:1 (texto grande)

#### Scenario: Texto alternativo en imágenes
- **Given** un usuario que utiliza un lector de pantalla
- **When** el lector encuentra un icono o imagen en la interfaz
- **Then** el elemento tiene un atributo de texto alternativo descriptivo
