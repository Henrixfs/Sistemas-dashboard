[CmdletBinding()]
param(
    [switch]$InstallDependencies
)

$ErrorActionPreference = 'Stop'

function Assert-Command {
    param([Parameter(Mandatory = $true)][string]$Name)

    if (-not (Get-Command $Name -ErrorAction SilentlyContinue)) {
        throw "No se encontro '$Name'. Instale la version requerida antes de continuar."
    }
}

Assert-Command -Name 'python'
Assert-Command -Name 'npm.cmd'

if (-not (Test-Path '.env.development')) {
    Copy-Item '.env.example' '.env.development'
    Write-Host 'Se creo .env.development desde .env.example. Reemplace los valores de ejemplo antes de ejecutar la aplicacion.'
}

New-Item -ItemType Directory -Force -Path 'storage/vouchers' | Out-Null

if ($InstallDependencies) {
    python -m pip install -e '.\backend[dev]'
    npm.cmd ci
}

Write-Host 'Entorno local preparado. Ejecute npm.cmd run dev para iniciar frontend y backend.'
