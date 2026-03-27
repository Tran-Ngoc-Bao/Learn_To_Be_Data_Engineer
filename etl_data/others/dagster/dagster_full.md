# 🧱 Dagster — Learning Guide

> Dagster is a **data orchestration platform** for developing, testing, and monitoring data pipelines. It is asset-centric, type-aware, and built for modern data engineering.

---

## 📚 Table of Contents

1. [Core Concepts](#1-core-concepts)
2. [Installation](#2-installation)
3. [Op](#3-op)
4. [Job](#4-job)
5. [Asset](#5-asset)
6. [Resource](#6-resource)
7. [Schedule](#7-schedule)
8. [Sensor](#8-sensor)
9. [Partition](#9-partition)
10. [Config](#10-config)
11. [Definitions](#11-definitions)
12. [Deployment Architecture](#12-deployment-architecture)
13. [Testing](#13-testing)

---

## 1. Core Concepts

| Concept | Description |
|---|---|
| **Op** | The smallest unit of computation (a single step/function) |
| **Job** | A pipeline composed of ops wired together |
| **Asset** | A persistent artifact (table, file, model) produced by a computation |
| **Resource** | A shared external connection (DB, S3, API client) |
| **Schedule** | Runs a job on a cron-based time trigger |
| **Sensor** | Runs a job in response to an external event |
| **Partition** | Splits a job into time or category slices |
| **Definitions** | The root object that registers all Dagster components |

---

## 2. Installation

```bash
pip install dagster dagster-webserver

# Quick start (single process, dev mode)
dagster dev -f my_pipeline.py
```

> **`DAGSTER_HOME`** — directory where Dagster stores metadata, logs, and run history.

---

## 3. Op

An **op** is the smallest unit of work — a plain Python function decorated with `@op`.

```python
from dagster import op

@op
def extract() -> list:
    return [1, 2, 3]

@op
def transform(numbers: list) -> list:
    return [n * 10 for n in numbers]

@op
def load(result: list) -> None:
    print("Loaded:", result)
```

---

## 4. Job

A **job** wires ops into a DAG (directed acyclic graph).

```python
from dagster import job

@job
def etl_job():
    load(transform(extract()))
```

---

## 5. Asset

**Assets** represent persistent data artifacts. Dagster tracks their lineage automatically.

```python
from dagster import asset

@asset
def raw_data() -> list:
    return [1, 2, 3]

@asset
def transformed_data(raw_data: list) -> list:
    return [n * 10 for n in raw_data]
```

---

## 6. Resource

Resources provide shared connections (databases, API clients, etc.) to ops and assets.

```python
from dagster import ConfigurableResource

class DatabaseResource(ConfigurableResource):
    connection_string: str

    def insert(self, data: list) -> None:
        print(f"Inserting into {self.connection_string}")
```

---

## 7. Schedule

Schedules run jobs automatically on a cron expression. Requires **Dagster Daemon**.

```python
from dagster import ScheduleDefinition

etl_schedule = ScheduleDefinition(
    job=etl_job,
    cron_schedule="0 8 * * *"   # every day at 8am
)
```

---

## 8. Sensor

Sensors poll for external conditions and trigger jobs when met. Requires **Dagster Daemon**.

```python
from dagster import sensor, RunRequest
import os

@sensor(job=etl_job)
def file_sensor(context):
    if os.path.exists("/data/input.csv"):
        yield RunRequest(run_key="/data/input.csv")
```

---

## 9. Partition

Partitions process data in slices (by date, category, etc.).

```python
from dagster import DailyPartitionsDefinition, asset

daily = DailyPartitionsDefinition(start_date="2024-01-01")

@asset(partitions_def=daily)
def daily_report(context) -> None:
    print(f"Processing: {context.partition_key}")
```

---

## 10. Config

Config classes pass runtime parameters to ops/assets.

```python
from dagster import Config, asset

class MyConfig(Config):
    batch_size: int = 100

@asset
def processed_data(config: MyConfig) -> list:
    return list(range(config.batch_size))
```

---

## 11. Definitions

`Definitions` is the root object Dagster uses to discover all components.

```python
from dagster import Definitions

defs = Definitions(
    jobs=[etl_job, cleanup_job],
    assets=[raw_data, transformed_data],
    schedules=[etl_schedule],
    resources={"database": DatabaseResource(connection_string="...")}
)
```

---

## 12. Deployment Architecture

### Single-process (Development)
```bash
dagster dev -f src/definitions.py
```

### Multi-process (Production)
```
┌──────────────────┐    workspace.yaml    ┌──────────────────────┐
│ dagster-webserver │ ──────────────────► │  Code Server (gRPC)  │
│   (port 3000)    │                      │     (port 4000)      │
└──────────────────┘                      └──────────────────────┘
         │
┌──────────────────┐
│  dagster-daemon  │  ← runs schedules & sensors
└──────────────────┘
```

All three processes share the same **`DAGSTER_HOME`** directory.

---

## 13. Testing

```python
# Test an op
def test_extract():
    assert extract() == [1, 2, 3]

# Test a job
def test_etl_job():
    result = etl_job.execute_in_process()
    assert result.success

# Test an asset
from dagster import materialize
def test_assets():
    result = materialize([raw_data, transformed_data])
    assert result.success
```

---

## 📎 Useful Links

- 📖 [Official Dagster Docs](https://docs.dagster.io)
- 🐙 [Dagster GitHub](https://github.com/dagster-io/dagster)
- 💬 [Dagster Slack Community](https://dagster.io/slack)