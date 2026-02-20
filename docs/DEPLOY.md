# Deploy

## Railway / Render
- Deploy `backend` service from `backend/Dockerfile`
- Deploy `frontend` service from `frontend/Dockerfile`
- Provision PostgreSQL + Redis
- Set env vars from `.env.example`
- Run post-deploy migration command:
  - `python -m app.db.init_db`

## Health check
- Backend: `/health`
- Frontend: `/`
