# CI/CD — Roadmap (Data Engineer)

This document is a practical CI/CD roadmap for **data engineering** projects (pipelines, dbt, Airflow, APIs, infrastructure). It tells you **what to automate first**, what “good” looks like, and what to learn next.

---

## Table of Contents

1. [Overview](#1-overview)
2. [What to Automate (Checklist)](#2-what-to-automate-checklist)
3. [Git Workflow (PR-based)](#3-git-workflow-pr-based)
4. [CI Pipelines (Python/dbt/Airflow)](#4-ci-pipelines-pythondbtairflow)
5. [Secrets & Environments](#5-secrets--environments)
6. [CD / Deployment Patterns](#6-cd--deployment-patterns)
7. [Suggested Learning Roadmap](#7-suggested-learning-roadmap)

---

## 1. Overview

**CI (Continuous Integration)** validates every change automatically (lint/tests/build).

**CD (Continuous Delivery/Deployment)** automates packaging and releasing, and optionally deploys to environments (dev/staging/prod).

In data engineering, CI/CD applies to:
- Code: Python services, libraries, dbt models/macros, Airflow DAGs
- Data quality: unit tests, dbt tests, Great Expectations, custom checks
- Infra: Terraform, Helm, Docker, Kubernetes manifests

---

## 2. What to Automate (Checklist)

Start small; make it reliable; then add coverage.

### A) Code quality (CI)
- Formatter: `black` (or `ruff format`)
- Linter: `ruff` (or `flake8`)
- Tests: `pytest`
- Type checking (optional): `mypy`
- Coverage (optional): `pytest-cov`

### B) Data workflow quality
- dbt: `dbt compile`, `dbt test` (with a CI target)
- SQL linting (optional): `sqlfluff`
- Data quality framework (optional): Great Expectations

### C) Security
- Dependency updates: Dependabot
- Dependency audit: `pip-audit` (or similar)
- SAST: CodeQL
- Secret scanning: never commit credentials

### D) Artifacts
- Build Docker image (if you deploy services): publish to GHCR/DockerHub
- Save test reports / coverage artifacts

---

## 3. Git Workflow (PR-based)

Recommended baseline:
- `main` is always **deployable**
- feature branches: `feature/...`
- open PR → CI runs → review → merge

Best practices:
- Protect `main` (require PR + required checks)
- Keep PRs small
- Use tags/releases when you start deploying (SemVer is a good default)

---

## 4. CI Pipelines (Python/dbt/Airflow)

### Typical triggers
- `pull_request`: run validation before merge
- `push` to `main`: build artifacts and/or deploy
- `workflow_dispatch`: manual run (useful for production deployments)
- `schedule`: nightly security scans or data checks

### Minimal CI for a Python repo
1. Checkout
2. Setup Python
3. Install dependencies
4. Run `ruff` + `pytest`
5. (Optional) Upload coverage

### CI for dbt
- Validate formatting/linting (optional)
- `dbt deps`
- `dbt compile`
- `dbt test` (using a CI profile/target)

### CI for Airflow (DAGs)
- Lint DAGs (Python lint)
- Import test (ensure DAGs can be parsed)
- Unit tests for custom operators/hooks

---

## 5. Secrets & Environments

### Environments
Use separate environments:
- `dev`: auto deploy is OK
- `staging`: optional approval
- `prod`: approval required + restricted secrets

### Secrets rules
- Store secrets in GitHub Actions Secrets (or a cloud secret manager)
- Use environment-level secrets for staging/prod
- Least privilege + rotation

---

## 6. CD / Deployment Patterns

Choose the simplest approach that fits your risk:
- Manual promotion: dev → staging → prod
- Blue/Green (advanced)
- Canary (advanced)

Always include:
- Safe migrations strategy
- Smoke tests after deploy
- Rollback plan (previous tag/image)

---

## 7. Suggested Learning Roadmap

### Phase 1 — CI foundation
- PR checks: lint + unit tests
- Speed up with caching
- Branch protection rules

### Phase 2 — Quality & security
- Add coverage reports
- Enable CodeQL
- Enable Dependabot
- Add `pip-audit` and secret scanning

### Phase 3 — CD
- Build artifacts on `main` or tags
- Add manual deploy workflow + environments
- Add smoke tests + rollback steps