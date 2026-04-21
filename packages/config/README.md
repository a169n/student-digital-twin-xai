# Shared Config Conventions

This package documents cross-repo conventions:

- Environment variable naming: upper snake case (`APP_ENV`, `API_PORT`).
- `.env.example` present per app/service.
- Keep secrets out of repository.
- Prefer explicit typed settings modules in runtime apps.

> TODO: Add shared typed config helpers once multiple apps require the same runtime logic.
