$ErrorActionPreference = 'Stop'
Set-Location -Path $PSScriptRoot

$target = '.\.python_packages\lib\site-packages'
if (Test-Path $target) {
	Remove-Item -Recurse -Force $target
}
New-Item -ItemType Directory -Path $target -Force | Out-Null

python -m pip install --upgrade `
	--platform manylinux2014_x86_64 `
	--python-version 37 `
	--implementation cp `
	--abi cp37m `
	--only-binary=:all: `
	-r requirements.txt `
	-t $target

Write-Host 'FC dependency packaging completed.' -ForegroundColor Green
