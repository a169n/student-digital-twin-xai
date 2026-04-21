.PHONY: bootstrap check lint format up down api web ml

bootstrap:
	pnpm install
	cd apps/api && uv sync
	cd services/ml && uv sync

check:
	pnpm -r lint || true
	cd apps/api && uv run ruff check src
	cd services/ml && uv run ruff check src

lint:
	pnpm -r lint
	cd apps/api && uv run ruff check src
	cd services/ml && uv run ruff check src

format:
	pnpm -r format
	cd apps/api && uv run ruff format src
	cd services/ml && uv run ruff format src

up:
	docker compose up --build

down:
	docker compose down

api:
	cd apps/api && uv run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

web:
	cd apps/web && pnpm dev

ml:
	cd services/ml && uv run python -m src.main
