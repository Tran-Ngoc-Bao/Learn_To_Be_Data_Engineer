# 🧭 Prefect — Learning Guide

> Prefect is a modern **workflow orchestration** framework for building reliable data pipelines in Python.  
> It focuses on a great developer experience, observability, retries, and flexible execution (local, server, cloud).

---

## 📚 Table of Contents

1. [Core Concepts](#1-core-concepts)
2. [Installation](#2-installation)
3. [Flows & Tasks](#3-flows--tasks)
4. [Parameters & Results](#4-parameters--results)
5. [Retries, Timeouts, Caching](#5-retries-timeouts-caching)
6. [State & Logging](#6-state--logging)
7. [Concurrency & Mapping](#7-concurrency--mapping)
8. [Blocks, Variables, Secrets](#8-blocks-variables-secrets)
9. [Deployments](#9-deployments)
10. [Work Pools & Workers](#10-work-pools--workers)
11. [Scheduling](#11-scheduling)
12. [Prefect Server vs Prefect Cloud](#12-prefect-server-vs-prefect-cloud)
13. [Testing](#13-testing)

---

## 1. Core Concepts

| Concept | Meaning |
|---|---|
| **Flow** | A workflow function (the “pipeline”) decorated with `@flow` |
| **Task** | A unit of work inside a flow, decorated with `@task` |
| **Flow Run / Task Run** | A single execution instance |
| **State** | Prefect’s status model for runs (Completed, Failed, Retrying, etc.) |
| **Deployment** | A packaged, runnable entry for a flow (with schedule, params, infra) |
| **Work Pool** | A queue of work for a given infrastructure type (process, docker, k8s, …) |
| **Worker** | A process that polls a work pool and executes flow runs |

---

## 2. Installation

```bash
pip install prefect
prefect version
```

Quick local run (no server needed):
```bash
python your_flow.py
```

---

## 3. Flows & Tasks

Minimal example:

```python
from prefect import flow, task

@task
def extract():
    return [1, 2, 3]

@task
def transform(data):
    return [x * 10 for x in data]

@task
def load(data):
    print("Loaded:", data)

@flow
def etl_flow():
    load(transform(extract()))

if __name__ == "__main__":
    etl_flow()
```

Key ideas:
- Use `@flow` for the pipeline function.
- Use `@task` for steps that need retries, caching, observability, or parallelism.

---

## 4. Parameters & Results

```python
from prefect import flow

@flow
def hello(name: str = "Bao"):
    print(f"Hello {name}")

hello("Prefect")
```

Prefect stores run metadata and logs; tasks can return Python objects.

---

## 5. Retries, Timeouts, Caching

Retries:

```python
from prefect import task

@task(retries=3, retry_delay_seconds=10)
def flaky():
    ...
```

Timeouts:

```python
@task(timeout_seconds=60)
def slow_task():
    ...
```

Caching (when appropriate):

```python
from datetime import timedelta
from prefect import task

@task(cache_expiration=timedelta(hours=1))
def expensive_call():
    ...
```

---

## 6. State & Logging

Prefect automatically captures logs; use Prefect logger:

```python
from prefect import flow, get_run_logger

@flow
def my_flow():
    logger = get_run_logger()
    logger.info("Flow started")
```

---

## 7. Concurrency & Mapping (Parallelism)

Mapping runs a task over a collection:

```python
from prefect import flow, task

@task
def square(x: int) -> int:
    return x * x

@flow
def map_flow():
    results = square.map([1, 2, 3, 4])
    print(results)

map_flow()
```

> Mapping is a common pattern for batch processing partitions/files.

---

## 8. Blocks, Variables, Secrets

Prefect provides blocks to store configuration (credentials, connections, etc.).
Typical examples:
- Secret block for API keys
- S3/GCS blocks for storage configuration
- Database credentials blocks

(Exact block types depend on installed integrations.)

---

## 9. Deployments

A **deployment** is how you operationalize a flow: give it a name, parameters, schedule, and a target work pool.

Common CLI pattern:
```bash
prefect deploy path/to/flow.py:flow_fn -n dev -p my-work-pool
```

---

## 10. Work Pools & Workers

Work pool (example: process pool):
```bash
prefect work-pool create --type process local-process-pool
```

Worker that executes jobs from the pool:
```bash
prefect worker start --pool local-process-pool --type process
```

---

## 11. Scheduling

Schedules can be attached to deployments (via CLI or code).  
The key idea: **a deployment can be scheduled**, and workers execute scheduled runs.

---

## 12. Prefect Server vs Prefect Cloud

| Option | When to use |
|---|---|
| **Local runs** | quick dev, no UI needed |
| **Prefect Server** | self-hosted UI + orchestration |
| **Prefect Cloud** | managed control plane + UI |

---

## 13. Testing

You can test flow logic as regular Python functions. For tasks, consider testing the underlying logic separately, and keep tasks thin.

```python
def transform_logic(data):
    return [x * 10 for x in data]

def test_transform_logic():
    assert transform_logic([1, 2]) == [10, 20]
```

---

## 📎 References

- Prefect docs: https://docs.prefect.io/
- Prefect GitHub: https://github.com/PrefectHQ/prefect