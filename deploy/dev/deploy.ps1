# Deploy do ambiente de desenvolvimento, com smoke test e rollback automatico.
# Usado pela pipeline (job "Deploy em desenvolvimento"). Corre a partir da pasta deploy/dev.
# Nota: texto sem acentos, porque o Windows PowerShell 5.1 nao le bem UTF-8 sem BOM.

param(
    [Parameter(Mandatory = $true)] [string] $Imagem,
    [Parameter(Mandatory = $true)] [string] $Sha,
    [switch] $SimularFalha,
    [int] $Tentativas = 10,
    [int] $IntervaloSegundos = 3
)

$ErrorActionPreference = "Continue"
Set-Location $PSScriptRoot

$Contentor = "metroisjustabus-dev-core-1"
$UrlBase = "http://localhost:8000"

# Corre um comando docker e falha o script se o comando falhar
function Invoke-Docker {
    & docker @args
    if ($LASTEXITCODE -ne 0) {
        throw "Falhou o comando: docker $($args -join ' ')"
    }
}

# Smoke test: /health responde ok e /version mostra o SHA esperado
function Test-Servico {
    param([string] $ShaEsperado, [string] $CaminhoHealth)
    for ($i = 1; $i -le $Tentativas; $i++) {
        try {
            $health = Invoke-RestMethod -Uri "$UrlBase$CaminhoHealth" -TimeoutSec 5
            $versao = Invoke-RestMethod -Uri "$UrlBase/version" -TimeoutSec 5
            if ($health.status -eq "ok" -and $versao.commit -eq $ShaEsperado) {
                Write-Host "Smoke test OK (tentativa $i): versao $($versao.commit)"
                return $true
            }
            Write-Host "Tentativa ${i}: resposta inesperada (commit $($versao.commit))"
        } catch {
            Write-Host "Tentativa ${i}: o servico ainda nao responde ($($_.Exception.Message))"
        }
        Start-Sleep -Seconds $IntervaloSegundos
    }
    return $false
}

# 1. Guardar a versao que esta a correr agora, para o rollback
$ImagemAnterior = docker ps -a --filter "name=^$Contentor$" --format "{{.Image}}"
if ($ImagemAnterior) {
    Write-Host "Versao atualmente em execucao: $ImagemAnterior"
} else {
    Write-Host "Nao ha nenhuma versao em execucao (primeiro deploy)."
}

# 2. Criar o .env a partir do segredo da pipeline (nunca vem do repositorio)
if (-not $env:POSTGRES_PASSWORD) {
    throw "O segredo POSTGRES_PASSWORD nao esta definido."
}
Set-Content -Path ".env" -Encoding Ascii -Value @(
    "POSTGRES_USER=core",
    "POSTGRES_PASSWORD=$env:POSTGRES_PASSWORD",
    "POSTGRES_DB=core"
)

# 3. Implantar a nova versao (a imagem publicada no GHCR, sem a reconstruir)
$ImagemNova = "${Imagem}:${Sha}"
$env:CORE_IMAGE = $ImagemNova
Write-Host "A implantar $ImagemNova"
Invoke-Docker compose pull core
Invoke-Docker compose up -d --no-build

# 4. Smoke test
$CaminhoHealth = "/health"
if ($SimularFalha) {
    Write-Host "ATENCAO: falha do smoke test simulada (demonstracao do rollback)"
    $CaminhoHealth = "/health-simulacao-de-falha"
}

if (Test-Servico -ShaEsperado $Sha -CaminhoHealth $CaminhoHealth) {
    Write-Host "Deploy concluido: $ImagemNova"
    exit 0
}

# 5. Rollback para a versao anterior
Write-Host "::error::O smoke test falhou para $ImagemNova"
if (-not $ImagemAnterior) {
    Write-Host "::error::Nao ha versao anterior para repor."
    exit 1
}
Write-Host "A repor a versao anterior: $ImagemAnterior"
$env:CORE_IMAGE = $ImagemAnterior
Invoke-Docker compose up -d --no-build core
Write-Host "::warning::Rollback concluido. Em execucao: $ImagemAnterior"
exit 1
