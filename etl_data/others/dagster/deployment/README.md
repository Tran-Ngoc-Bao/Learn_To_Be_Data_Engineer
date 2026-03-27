# 🚀 Dagster Deployment Guide

This deployment runs Dagster in **multi-process mode** using a Code Server, Webserver, and Daemon — each as a separate process.

---

## 📁 Project Structure

```
deployment/
├── pyproject.toml          # Project metadata & dependencies
├── workspace.yaml          # Tells webserver where to find code server
├── dagster_home/           # Dagster metadata, logs, run history (auto-created)
├── scripts/
│   ├── run_codeserver.py   # Starts the gRPC Code Server (port 4000)
│   ├── run_webserver.py    # Starts the Dagster UI (port 3000)
│   └── run_daemon.py       # Starts the Daemon (schedules & sensors)
└── src/
    ├── definitions.py      # Root Definitions object
    ├── jobs/
    │   ├── etl_job.py      # ETL pipeline (extract → transform → load)
    │   └── cleanup_job.py  # Cleanup pipeline
    └── schedules/
        └── schedules.py    # Schedule definitions
```

---

## ⚙️ Prerequisites

- Python >= 3.11
- `pip` or `uv`

---

## 🛠️ Setup

**1. Create and activate a virtual environment:**

```bash
python -m venv .venv

# Linux / macOS
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

**2. Install dependencies:**

```bash
pip install -e .
```

> This installs `dagster` and `dagster-webserver` as defined in `pyproject.toml`.

**3. Create the `dagster_home` directory:**

```bash
mkdir dagster_home
```

---

## ▶️ Running the Deployment

You need to start **3 processes** in separate terminals, all from the `deployment/` directory.

### Terminal 1 — Code Server

Hosts your pipeline code as a gRPC server on port `4000`.

```bash
python scripts/run_codeserver.py
```

### Terminal 2 — Webserver

Serves the Dagster UI on port `3000`, connecting to the code server via `workspace.yaml`.

```bash
python scripts/run_webserver.py
```

### Terminal 3 — Daemon

Runs schedules and sensors in the background.

```bash
python scripts/run_daemon.py
```

---

## 🌐 Access the UI

Once all three processes are running, open your browser at:

```
http://127.0.0.1:3000
```

---

## 📦 Registered Components

### Jobs

| Job | Description |
|---|---|
| `etl_job` | Runs `extract → transform → load` ops |
| `cleanup_job` | Runs a `cleanup` op |

### Schedules

| Schedule | Job | Cron | Frequency |
|---|---|---|---|
| `etl_schedule` | `etl_job` | `*/2 * * * *` | Every 2 minutes |
| `cleanup_schedule` | `cleanup_job` | `*/5 * * * *` | Every 5 minutes |

---

## 🔑 Key Configuration Files

### `workspace.yaml`
Connects the webserver to the code server:
```yaml
load_from:
  - grpc_server:
      host: 127.0.0.1
      port: 4000
      location_name: my_dagster_app
```

### `pyproject.toml`
Defines the package and dependencies:
```toml
[project]
name = "my-dagster-app"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = ["dagster", "dagster-webserver"]

[tool.setuptools]
package-dir = {"" = "src"}
```

---

## 🛑 Stopping

Press `Ctrl+C` in each terminal to stop the respective process.

---

## ⚠️ Notes

- All 3 processes must share the same `DAGSTER_HOME` directory (handled automatically by the scripts).
- Schedules will **only run** if the Daemon is running.
- The `src/` directory must be a Python package — ensure `src/__init__.py` exists for module-based imports.