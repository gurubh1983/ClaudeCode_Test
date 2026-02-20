# Setup

1. Copy environment file:
```bash
cp .env.example .env
```
2. Fill Angel One and Stripe secrets.
3. Start stack:
```bash
docker compose up --build
```
4. Initialize DB schema:
```bash
docker compose exec backend python -m app.db.init_db
```
