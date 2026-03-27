# 🚀 Prefect (Local Server) — Setup & Usage

This folder contains a minimal Prefect setup using:
- **Prefect Server (self-hosted)** for UI + orchestration
- A **Process work pool** and **Process worker** for local execution
- A simple example flow: `flows/hello_flow.py`

---

## 📁 Structure

```
deployment/
├── README.md
├── flows/
│   └── hello_flow.py
└── scripts/
    ├── serve.py     # start Prefect server (UI/API)
    ├── worker.py    # start a Prefect worker (process type)
    └── deploy.py    # create pool (if needed) + create deployment
```

---

## ✅ Prerequisites

- Python 3.10+ recommended
- A virtual environment

---

## 1) Create & activate a virtual environment

From the repo root (or from this folder), create venv:

```bash
python -m venv .venv

# Linux/macOS
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

---

## 2) Install Prefect

```bash
pip install -U pip
pip install prefect
prefect version
```

---

## 3) Start Prefect Server (UI + API)

Run from this folder (`etl_data/others/prefect/`):

```bash
python scripts/serve.py
```

This will start the server and set defaults:
- `PREFECT_API_URL=http://127.0.0.1:4200/api`
- `PREFECT_HOME=./.prefect` (inside this folder)

Open the UI:
```
http://127.0.0.1:4200
```

---

## 4) Create deployment (and work pool)

In a **new terminal** (same venv), run:

```bash
python scripts/deploy.py
```

What this script does:
1. Creates a process work pool named `local-process-pool` (safe to run multiple times)
2. Creates a deployment:
   - Flow entry: `flows/hello_flow.py:hello_flow`
   - Deployment name: `dev`
   - Work pool: `local-process-pool`

---

## 5) Start a worker

In a **new terminal** (same venv), run:

```bash
python scripts/worker.py
```

This worker polls the pool `local-process-pool` and executes flow runs.

---

## 6) Run the flow

### Option A — Trigger from UI (recommended)
Go to the UI → Deployments → `hello-flow/dev` → **Run**

### Option B — Run locally without server (quick dev)
```bash
python flows/hello_flow.py
```

---

## 🔧 Useful Prefect CLI Commands

```bash
# Check configuration
prefect config view

# List work pools
prefect work-pool ls

# List deployments
prefect deployment ls

# Inspect a deployment
prefect deployment inspect "hello-flow/dev"

# Start server (alternative to scripts/serve.py)
prefect server start
```

---

## 🧹 Cleanup / Notes

- Prefect local state is stored in:
  - `./.prefect/` (because scripts set `PREFECT_HOME` here)
- If you don’t want to push it to GitHub, add to `.gitignore`:
  - `.prefect/`

Stop services:
- Press `Ctrl + C` in each terminal (server / worker).

---

## 📎 References
- Prefect docs: https://docs.prefect.io/