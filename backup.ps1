$stamp = Get-Date -Format "yyyyMMdd-HHmmss"
New-Item -ItemType Directory -Force -Path ".\backups" | Out-Null
docker compose cp backend:/app/data/realestate.db ".\backups\realestate-$stamp.db"
Write-Host "Backup created."
