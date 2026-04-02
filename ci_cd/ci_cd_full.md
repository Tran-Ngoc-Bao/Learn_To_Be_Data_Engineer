# CI/CD — Full Learning Guide

This guide provides a structured roadmap to learn and apply **CI/CD (Continuous Integration / Continuous Delivery / Continuous Deployment)**. The focus is practical: what to automate, how to structure workflows, and how to deploy safely.

---

## Table of Contents

1. [Overview](#1-overview)  
2. [What You Should Automate](#2-what-you-should-automate)  
3. [Suggested Git Workflow](#3-suggested-git-workflow)  
4. [GitHub Actions (Recommended)](#4-github-actions-recommended)  
5. [Environments & Secrets Management](#5-environments--secrets-management)  
6. [Deployment Strategies](#6-deployment-strategies)  
7. [Suggested Roadmap](#7-suggested-roadmap)  

---

## 1. Overview

CI/CD is a set of practices that helps you **build, test, and release** software reliably and frequently.

- **CI (Continuous Integration):** automatically validates every change (lint, tests, build).
- **CD (Continuous Delivery):** automatically prepares a release artifact and keeps it deployable; deployment may be manual.
- **Continuous Deployment:** automatically deploys to an environment after CI passes.

In a data engineering context, CI/CD applies not only to applications, but also to:
- ETL/ELT pipelines (Airflow, dbt)
- Data quality checks
- Infrastructure (Terraform, Helm, Docker Compose)
- Metadata/governance tooling (e.g., OpenMetadata)

---

## 2. What You Should Automate

### Code quality (CI)
- Formatting (e.g., `black`)
- Linting (e.g., `ruff`, `flake8`)
- Type checking (optional: `mypy`)
- Unit tests (e.g., `pytest`)
- Integration tests (when you have services like Postgres/Redis/Kafka)

### Security & compliance
- Dependency scanning (Dependabot, `pip-audit`)
- Secret scanning (avoid committing credentials)
- SAST (e.g., CodeQL)
- Container vulnerability scanning (e.g., Trivy) if you build Docker images

### Packaging / artifacts
- Build & publish Docker images (to GHCR/DockerHub)
- Build Python packages (wheel/sdist) if you release libraries
- Upload test reports / coverage artifacts

### Deployment (CD)
- Deploy to **dev/staging/prod** using environment approvals
- Run migrations safely
- Smoke tests after deployment
- Rollback strategy (redeploy previous version/tag)

---

## 3. Suggested Git Workflow

A simple workflow that scales well:

- `main`: always deployable
- feature branches: `feature/...`
- open PR → run CI checks
- merge only if checks pass

Recommended practices:
- Protect `main` branch (require PR + required checks)
- Use semantic versioning tags: `vMAJOR.MINOR.PATCH` (e.g., `v1.2.0`)
- Keep PRs small and reviewable

---

## 4. GitHub Actions (Recommended)

### Where workflows live
Workflows are stored in:
- `.github/workflows/*.yml`

### Typical workflow triggers
- `pull_request`: run checks before merge
- `push` to `main`: build & optionally release/deploy
- `workflow_dispatch`: manual deployments (safer for prod)
- `schedule`: nightly jobs (security scans, data checks)

### Minimal CI pipeline for Python
For a Python-only repo, a good baseline pipeline is:

1. Checkout code  
2. Setup Python  
3. Install dependencies  
4. Run lint + tests  
5. (Optional) Upload coverage artifact  

---

## 5. Environments & Secrets Management

### Environments
Use separate environments:
- `dev`: auto-deploy allowed
- `staging`: optional approval
- `prod`: approval required + restricted secrets

### Secrets
Rules:
- Never commit secrets to Git
- Store credentials in **GitHub Actions Secrets**
- Use environment-specific secrets for staging/prod
- Rotate secrets regularly
- Prefer least-privilege permissions for tokens/keys

---

## 6. Deployment Strategies

When you start deploying, choose a strategy that matches your risk level:

- **Manual promotion:** deploy to dev → staging → prod
- **Blue/Green:** switch traffic to a new version after verification
- **Canary:** deploy to a small portion first, then expand gradually

Always plan for:
- Database migration strategy (backward compatible when possible)
- Rollback strategy (redeploy previous version/tag)
- Post-deploy smoke tests

---

## 7. Suggested Roadmap

### Phase 1 — CI foundation
- Add PR checks: lint + unit tests
- Add caching to speed up runs
- Add branch protection rules

### Phase 2 — Quality & security
- Enable CodeQL
- Enable Dependabot updates
- Add secret scanning and container scanning (if using Docker)

### Phase 3 — CD
- Build release artifacts on `main` or tags
- Add manual deploy workflow with environments
- Add smoke tests + rollback steps