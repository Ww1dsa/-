$ErrorActionPreference = 'Stop'
Set-Location -Path $PSScriptRoot

python -m pip install -r requirements.txt -t .\.python_packages\lib\site-packages

Write-Host 'FC dependency packaging completed.' -ForegroundColor Green
