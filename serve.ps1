# Servidor HTTP simples para visualizar o front
param(
  [int]$Port = 8000,
  [string]$PythonExe = "python"
)

Write-Host "Servindo na porta $Port (http://localhost:$Port/front/)"
Push-Location $PSScriptRoot
& $PythonExe -m http.server $Port
Pop-Location
