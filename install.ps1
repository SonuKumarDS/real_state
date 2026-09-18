Write-Host "Checking Docker..."
docker --version
if ($LASTEXITCODE -ne 0) { throw "Docker Desktop is required." }
if (!(Test-Path ".env")) { Copy-Item ".env.example" ".env" }
docker compose build
Write-Host "Installation complete. Run .\start.ps1"
