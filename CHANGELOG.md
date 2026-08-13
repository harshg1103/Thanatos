# CHANGELOG - Project THANATOS

All notable changes, commits, and progress for Project THANATOS will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased] - 2026-08-13

### Added
- Created monorepo workspace structure (`packages/core`, `packages/swarm`, `packages/formal`, `packages/probing`, `packages/aegis`, `apps/dashboard`, `services/api`, `emulators/sandbox`).
- Added configuration templates: `.env.example`, `.gitignore`, `pyproject.toml`, `requirements.txt`.
- Created project evaluation documentation: `TIMELINE.md`, `README.md`, `CHANGELOG.md`.
- Implemented core Pydantic domain models in `packages/core/schemas/` (`belief.py`, `proof.py`, `attack.py`).
- Scaffolded Docker sandbox configuration and LangGraph target pipeline runner under `emulators/`.
- Created FastAPI backend skeleton with health check and WebSocket streaming stubs in `services/api/main.py`.
