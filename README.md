# StrikeGenius.ai

StrikeGenius.ai is a deployable SaaS platform for automated F&O options scanning and backtesting using Angel One data, a rule-AST engine, subscription billing, and a responsive web application.

## Monorepo Layout
- `backend/` FastAPI, SQLAlchemy async, PostgreSQL, Redis, Stripe, Angel One integration
- `frontend/` Next.js App Router, TypeScript, TailwindCSS, Zustand state
- `docs/` Setup, API, deployment, legal docs

## Quick Start
```bash
cp .env.example .env
docker compose up --build
```

Open `http://localhost:3000`.
