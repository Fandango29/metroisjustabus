# Deploy de um servico no ambiente de desenvolvimento, com smoke test e rollback automatico.
# Usado pela pipeline (job "Deploy em desenvolvimento"). Corre a partir da pasta deploy/dev.
# Cada servico e implantado sozinho, sem mexer nos outros (RNF-15).
# Nota: texto sem acentos, porque o Windows PowerShell 5.1 nao le bem UTF-8 sem BOM.

param(
    [Parameter(Mandatory = $true)] [ValidateSet("core", "bilhetes")] [string] $Servico,
    [Parameter(Mandatory = $true)] [int] $Porta,
    [Parameter(Mandatory = $true)] [string] $Imagem,
    [Parameter(Mandatory = $true)] [string] $Sha,
    [switch] $SimularFalha,
    [int] $Tentativas = 10,
    [int] $IntervaloSegundos = 3
)

$ErrorActionPreference = "Continue"
Set-Location $PSScriptRoot

$Contentor = "metroisjustabus-dev-$Servico-1"
$UrlBase = "http://localhost:$Porta"
$VariavelImagem = "$($Servico.ToUpper())_IMAGE"

# Corre um comando docker e falha o script se o comando falhar
function Invoke-Docker {
    & docker @args
    if ($LASTEXITCODE -ne 0) {
        throw "Falhou o comando: docker $($args -join ' ')"
    }
}

# Smoke test: /health responde ok e /version mostra o servico e o SHA esperados
function Test-Servico {
    param([string] $ShaEsperado, [string] $CaminhoHealth)
    for ($i = 1; $i -le $Tentativas; $i++) {
        try {
            $health = Invoke-RestMethod -Uri "$UrlBase$CaminhoHealth" -TimeoutSec 5
            $versao = Invoke-RestMethod -Uri "$UrlBase/version" -TimeoutSec 5
            $ok = $health.status -eq "ok" -and $versao.servico -eq $Servico -and $versao.commit -eq $ShaEsperado
            if ($ok) {
                Write-Host "Smoke test OK (tentativa $i): $Servico na versao $($versao.commit)"
                return $true
            }
            Write-Host "Tentativa ${i}: resposta inesperada ($($versao.servico), $($versao.commit))"
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
    Write-Host "Nao ha nenhuma versao de $Servico em execucao (primeiro deploy)."
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

# 3. Implantar so este servico, com a imagem publicada no GHCR (sem a reconstruir)
$ImagemNova = "${Imagem}:${Sha}"
Set-Item -Path "env:$VariavelImagem" -Value $ImagemNova
Write-Host "A implantar $ImagemNova"
Invoke-Docker compose pull $Servico
Invoke-Docker compose up -d --no-build $Servico

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

# 5. Rollback para a versao anterior deste servico
Write-Host "::error::O smoke test falhou para $ImagemNova"
if (-not $ImagemAnterior) {
    Write-Host "::error::Nao ha versao anterior de $Servico para repor."
    exit 1
}
Write-Host "A repor a versao anterior: $ImagemAnterior"
Set-Item -Path "env:$VariavelImagem" -Value $ImagemAnterior
Invoke-Docker compose up -d --no-build $Servico
Write-Host "::warning::Rollback concluido. Em execucao: $ImagemAnterior"
exit 1
