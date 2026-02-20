# API

Base URL: `/api/v1`

## Auth
- `POST /auth/register`
- `POST /auth/login`
- `POST /auth/password-reset/request`
- `POST /auth/password-reset/confirm`

## User
- `GET /users/me`

## Scanner
- `POST /scanner/run`
- `POST /scanner/backtest`

## Billing
- `GET /billing/plan`
- `POST /billing/checkout`
- `GET /billing/invoices`
- `POST /billing/webhook`
