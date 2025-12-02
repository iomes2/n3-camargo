# Instala dependências e executa pipeline + treino + deploy
param(
    [string]$PythonExe = "python"
)

Write-Host "Instalando dependências..."
$req = Join-Path $PSScriptRoot "requirements.txt"
& $PythonExe -m pip install -r $req

Write-Host "Executando pipeline/treino/deploy..."
Push-Location $PSScriptRoot
& $PythonExe -m src.anon_n2
& $PythonExe -m src.main
Pop-Location
