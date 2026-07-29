# reports

Generación y descarga de reportes financieros.

## ADDED Requirements

### Requirement: FR-RE-01 — Generar reporte de movimientos por periodo
El administrador SHALL poder generar un reporte en formato PDF o CSV con todos los movimientos (ingresos y gastos) de un periodo seleccionado.

#### Scenario: Generación exitosa de reporte de movimientos
- **Given** un administrador autenticado y un periodo con movimientos publicados
- **When** selecciona el periodo, elige formato PDF y hace clic en "Generar reporte"
- **Then** el sistema genera un archivo PDF con la lista de movimientos, montos, categorías y saldo final, y lo descarga

#### Scenario: Reporte de periodo sin movimientos
- **Given** un administrador autenticado y un periodo sin movimientos registrados
- **When** intenta generar un reporte de ese periodo
- **Then** el sistema genera un reporte indicando que no hay movimientos en el periodo seleccionado

### Requirement: FR-RE-02 — Descargar reporte para alumnos
El alumno SHALL poder descargar un reporte en formato PDF del periodo financiero actual, con los movimientos publicados.

#### Scenario: Alumno descarga reporte del periodo actual
- **Given** un alumno autenticado y un periodo abierto con movimientos publicados
- **When** selecciona "Descargar reporte" en el dashboard
- **Then** el sistema descarga un PDF con los ingresos, gastos, saldo y movimientos del periodo visible para el alumno

#### Scenario: Alumno intenta descargar reporte de administrador
- **Given** un alumno autenticado
- **When** intenta descargar un reporte con filtros o datos restringidos al rol administrador
- **Then** el sistema deniega la operación

### Requirement: FR-RE-03 — Filtrar reporte por tipo de movimiento
El administrador SHALL poder generar reportes filtrados solo por ingresos o solo por gastos dentro de un periodo.

#### Scenario: Reporte solo de ingresos
- **Given** un administrador autenticado y un periodo con ingresos y gastos registrados
- **When** selecciona el filtro "Solo ingresos" y genera el reporte
- **Then** el reporte contiene únicamente los ingresos del periodo

### Requirement: BR-RE-01 — El reporte de alumno solo incluye movimientos publicados
El reporte generado por un alumno SHALL incluir exclusivamente movimientos en estado publicado y vigente.

#### Scenario: Verificación de contenido del reporte de alumno
- **Given** un alumno autenticado y un periodo con movimientos en borrador, publicados y anulados
- **When** descarga el reporte del periodo
- **Then** el reporte incluye solo los movimientos publicados; los borradores y anulados no aparecen
