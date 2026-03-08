param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]] $Args
)

$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $root

if (-not (Test-Path ".\venv\Scripts\Activate.ps1")) {
    Write-Host "Creating venv at .\venv ..."
    python -m venv venv
}

Write-Host "Activating venv..."
. .\venv\Scripts\Activate.ps1

Set-Location ".\env"
python llm_env.py @Args

