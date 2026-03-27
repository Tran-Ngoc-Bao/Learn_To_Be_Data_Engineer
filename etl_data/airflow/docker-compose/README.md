# 🐳 Airflow Docker Compose Deployment Guide

This setup runs Apache Airflow using **Docker Compose** with a custom Docker image that supports installing additional Python packages via `requirements.txt`.

---

## 📁 Project Structure

```
docker-compose/
├── .env                        # Environment variables (Airflow UID, image version)
├── dockerfile                  # Custom Airflow image with extra dependencies
├── requirements.txt            # Additional Python packages to install
├── docker-compose.yaml         # Main Docker Compose configuration
├── docker-compose-origin.yaml  # Original Airflow Docker Compose (reference only)
└── dags/
    └── example_dag_decorator.py  # Example DAG using TaskFlow API + custom operator
```

---

## ⚙️ Prerequisites

- [Docker](https://docs.docker.com/get-docker/) installed
- [Docker Compose](https://docs.docker.com/compose/install/) installed
- At least **4GB RAM** allocated to Docker

---

## 🔧 Configuration

### `.env`

```dotenv
AIRFLOW_UID=50000
AIRFLOW_IMAGE_VERSION=3.1.8
```

| Variable | Description |
|---|---|
| `AIRFLOW_UID` | UID of the user inside the container (use `50000` on Linux/macOS) |
| `AIRFLOW_IMAGE_VERSION` | Airflow image version to use |

> 💡 To find your local UID on Linux/macOS, run: `echo $(id -u)`

### `dockerfile`

Extends the official Airflow image and installs extra packages:

```dockerfile
ARG AIRFLOW_IMAGE_VERSION
FROM apache/airflow:${AIRFLOW_IMAGE_VERSION}

ADD requirements.txt .
RUN pip install -r requirements.txt
```

### `requirements.txt`

Add any additional Python packages here:

```text
# Example:
httpx
pandas
```

> After modifying `requirements.txt`, rebuild the image with `docker compose build`.

---

## 🚀 Getting Started

### Step 1 — Initialize the database

This must be run **once** before starting Airflow for the first time:

```bash
docker compose up airflow-init
```

Wait until you see:
```
airflow-init-1 exited with code 0
```

### Step 2 — Start all services

```bash
docker compose up -d
```

### Step 3 — Open the Airflow UI

```
http://localhost:8080
```

Default credentials:
| Field | Value |
|---|---|
| Username | `airflow` |
| Password | `airflow` |

---

## 🔄 Common Commands

```bash
# Start all services in background
docker compose up -d

# Stop all services
docker compose down

# Stop and remove volumes (full reset, deletes all data)
docker compose down --volumes --remove-orphans

# View logs of all services
docker compose logs -f

# View logs of a specific service
docker compose logs -f airflow-scheduler

# Rebuild image after changing requirements.txt
docker compose build
docker compose up -d
```

---

## 📂 Adding DAGs

Place your DAG files in the `dags/` folder. Airflow will automatically detect and load them.

```
dags/
└── my_new_dag.py
```

> Changes to DAG files are picked up automatically — no restart needed.

---

## 🧪 Example DAG

The included [`dags/example_dag_decorator.py`](dags/example_dag_decorator.py) demonstrates:

- **Custom Operator** — `GetRequestOperator` extends `BaseOperator` to make an HTTP GET request
- **TaskFlow `@task`** — `prepare_command` processes the response and returns a Bash command
- **Classic Operator** — `BashOperator` executes the generated command

**Pipeline flow:**
```
get_ip (GetRequestOperator)
    ↓
prepare_command (@task)
    ↓
echo_ip_info (BashOperator)
```

To trigger it manually, go to the UI → find `example_dag_decorator` → click **▶ Trigger DAG**.

---

## 🛑 Stopping

```bash
# Stop services but keep data
docker compose down

# Stop services and delete all data (volumes)
docker compose down --volumes --remove-orphans
```

---

## ⚠️ Notes

- The `docker-compose-origin.yaml` file is the **unmodified official Airflow Docker Compose** for reference. Use `docker-compose.yaml` for this deployment.
- All Airflow metadata (runs, logs, connections, variables) is stored in Docker volumes and persists across restarts.
- Schedules only run while the **scheduler** service is running.