# Contributing

Thanks for your interest in contributing to **fastapi-template**! All contributions are welcome — bug fixes, new features, documentation improvements, and more.

## Getting Started

### Prerequisites

- Python 3.14+
- Docker and Docker Compose
- Make

### Setup

1. Fork and clone the repository:

   ```bash
   git clone https://github.com/<your-username>/fastapi-template.git
   cd fastapi-template
   ```

2. Copy the `secrets/` folder into the project root. It must contain a `.env` file with `DATABASE_URL` and other required settings. Ask a maintainer if you need help with this.

3. Install dependencies and run formatters/linters:

   ```bash
   make all
   ```

## Development Workflow

### Branching

Create a branch from `main` using the appropriate prefix:

- `feature/` — new functionality
- `fix/` — bug fixes
- `perf/` — performance improvements
- `refactor/` — code restructuring

### Running the App

```bash
make start    # Start all services (Docker Compose)
make stop     # Stop all services
```

### Running Tests

```bash
make test-unit-local    # Unit tests locally (fast, no Docker)
make test               # Full test suite (Docker)
make test-unit          # Unit tests (Docker)
make test-integration   # Integration tests (Docker)
make test-e2e           # End-to-end tests (Docker)
make test-cov           # Tests with coverage report
```

## Code Style

This project uses **Ruff** for linting and formatting. Run these before committing:

```bash
make fmt     # Format code
make lint    # Lint and auto-fix
```

Key rules:

- Strict typing — use `|` union syntax, not `Optional`. Explicit return types on all functions. No `Any`.
- Async/await for all I/O operations.
- Absolute imports starting with `src/` (e.g., `from src.contexts.auth.domain.aggregates import User`).
- No comments unless the code is genuinely non-obvious.
- English for all code, names, and comments.

## Commit Conventions

Commits follow **Conventional Commits with gitmoji** (commitizen `cz_gitmoji`):

```
:emoji: type(scope): description
```

Examples:

- `:sparkles: feat(users): add email verification endpoint`
- `:bug: fix(auth): handle inactive key edge case`
- `:recycle: refactor(shared): extract base repository class`

## Pull Requests

- Write a clear description of **what** changed and **why**.
- Ensure CI passes (linting, tests).
- Link related issues if applicable.
- Keep PRs focused — one logical change per PR.

## Architecture Overview

The project follows a **hexagonal DDD** structure. Each bounded context lives under `src/contexts/` with three layers:

- **Domain** — pure Python, no infrastructure dependencies. Aggregates, value objects, domain errors, and repository ports.
- **Application** — use cases that orchestrate domain logic. Dependencies are injected via ports.
- **Infrastructure** — SQLAlchemy repositories, HTTP controllers, CLI commands, and DI container configuration.

## License

By contributing, you agree that your contributions will be licensed under the [MIT License](LICENSE).
