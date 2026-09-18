# Real Estate AI Platform

A local-first real-estate lead, investor matching, deal, commission and payment-tracking platform.

## What is included

- FastAPI backend
- SQLite by default (PostgreSQL-ready configuration)
- React/Vite frontend
- Property and investor CRM
- CSV imports
- Property-investor matching engine
- Lead/deal/commission tracking
- Dashboard analytics
- Audit log
- Docker Compose
- Windows PowerShell scripts
- Basic automated tests
- Source provenance and verification status
- Safe connector interface for future authorized APIs

## Important integration boundary

This project intentionally does not bypass CAPTCHAs, authentication, anti-bot systems, rate limits, privacy controls, or platform restrictions. Zillow/Facebook/Instagram/etc. connectors must use authorized APIs, licensed data, permitted public data, or user-assisted imports.

## Quick start (Windows)

Requirements: Docker Desktop.

```powershell
.\install.ps1
.\start.ps1
```

Open http://localhost:8000 for the API and http://localhost:5173 for the dashboard.

Without Docker:

```powershell
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Then:

```powershell
cd frontend
npm install
npm run dev
```

## Environment

Copy `.env.example` to `.env`. Secrets must never be committed.

## API

Swagger documentation: http://localhost:8000/docs

## Test

```powershell
cd backend
pytest
```

## Production notes

Before production use, replace the default development secret, enable HTTPS, use PostgreSQL, configure an external authentication provider or hardened auth, configure backups, and review applicable real-estate, privacy, advertising, referral-fee, licensing, and messaging requirements for each jurisdiction.
