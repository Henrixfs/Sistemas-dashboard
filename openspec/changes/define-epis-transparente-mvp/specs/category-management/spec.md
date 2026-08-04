# category-management

Creación, modificación, desactivación y consulta de categorías utilizadas para clasificar los gastos.

## ADDED Requirements

### Requirement: FR-CM-01 — Crear categoría de gasto
El administrador SHALL poder crear una categoría de gasto indicando nombre y descripción opcional.

#### Scenario: Creación exitosa de categoría
- **Given** un administrador autenticado
- **When** completa el formulario con nombre "Material didáctico", descripción "Recursos educativos y materiales de enseñanza" y confirma
- **Then** el sistema crea la categoría, la muestra en la lista de categorías activas y notifica al administrador

#### Scenario: Creación de categoría con nombre duplicado
- **Given** un administrador autenticado y una categoría existente "Material didáctico"
- **When** intenta crear otra categoría con el mismo nombre
- **Then** el sistema rechaza la operación e indica que el nombre de categoría ya existe

### Requirement: FR-CM-02 — Modificar categoría
El administrador SHALL poder modificar el nombre o la descripción de una categoría existente.

#### Scenario: Modificación exitosa de categoría
- **Given** un administrador autenticado y una categoría "Material didáctico"
- **When** cambia el nombre a "Recursos didácticos" y guarda
- **Then** el sistema actualiza el nombre de la categoría y los gastos existentes mantienen la referencia actualizada

### Requirement: FR-CM-03 — Desactivar categoría
El administrador SHALL poder desactivar una categoría. Las categorías desactivadas no aparecen en el selector de nuevas transacciones pero los gastos existentes la conservan.

#### Scenario: Desactivación de categoría sin movimientos asociados
- **Given** un administrador autenticado y una categoría sin gastos asociados
- **When** selecciona desactivar la categoría y confirma
- **Then** el sistema desactiva la categoría y ya no aparece en el selector de nuevos gastos

#### Scenario: Desactivación de categoría con movimientos asociados
- **Given** un administrador autenticado y una categoría con gastos registrados
- **When** selecciona desactivar la categoría y confirma
- **Then** el sistema desactiva la categoría, los gastos existentes conservan la categoría, pero no está disponible para nuevos gastos

### Requirement: FR-CM-04 — Listar categorías
El sistema SHALL mostrar al administrador la lista de categorías activas e inactivas.

#### Scenario: Visualización de categorías
- **Given** un administrador autenticado y categorías activas e inactivas
- **When** accede a la sección de categorías
- **Then** el sistema muestra todas las categorías, indicando cuáles están activas y cuáles inactivas

### Requirement: BR-CM-01 — Conservación de categorías con historial
El sistema MUST impedir la eliminación destructiva de una categoría con movimientos financieros asociados. La categoría SHALL desactivarse para impedir su selección en nuevos gastos y conservará las referencias históricas existentes.

#### Scenario: Intento de eliminar una categoría con historial
- **Given** un administrador autenticado y una categoría asociada a gastos existentes
- **When** intenta eliminar la categoría
- **Then** el sistema rechaza la eliminación destructiva y permite únicamente su desactivación
