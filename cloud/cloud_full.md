# Cloud Computing — Full Learning Guide

Cloud Computing is essential for Data Engineers because most modern data platforms run on cloud services. This document summarizes concepts and a practical learning path.

---

## Table of Contents

| Section | Description |
|---|---|
| [1. Core Cloud Concepts](#1-core-cloud-concepts) | IaaS/PaaS/SaaS, regions, networking, IAM, storage, compute |
| [2. Cloud for Data Engineering](#2-cloud-for-data-engineering) | Common services and platform layers |
| [3. Recommended Learning Order](#3-recommended-learning-order) | Roadmap from fundamentals to real workloads |
| [4. Infrastructure as Code](#4-infrastructure-as-code) | Terraform + environment management |
| [5. Security Best Practices](#5-security-best-practices) | IAM, encryption, secrets, audit |
| [6. Cost Awareness](#6-cost-awareness) | Cost drivers and cost controls |
| [7. Hands-on Projects](#7-hands-on-projects) | Portfolio projects |
| [8. Choosing a Provider](#8-choosing-a-provider) | AWS vs GCP vs Azure |

---

## 1. Core Cloud Concepts

| Topic | What to learn | Why it matters |
|---|---|---|
| IaaS / PaaS / SaaS | definitions + examples | choose the right abstraction level |
| Regions & AZs | latency, compliance, HA | availability and legal constraints |
| Networking | VPC/VNet, subnets, routes, NAT, firewall rules | most production issues involve networking |
| IAM | roles/policies, least privilege | secure access to data and services |
| Storage | object/block/file | data lakes rely on object storage |
| Compute | VM, containers, serverless | scalable processing for pipelines |

---

## 2. Cloud for Data Engineering

| Platform layer | Typical services | What to practice |
|---|---|---|
| Data Lake | S3 / GCS / ADLS | Parquet, partitioning, lifecycle rules |
| Warehouse | BigQuery / Redshift / Snowflake / Synapse | load patterns, cost model, permissions |
| Batch | Spark (EMR/Dataproc), serverless jobs | retries, idempotency, tuning basics |
| Streaming | Kafka, Kinesis, Pub/Sub, Event Hubs | consumer lag, delivery semantics |
| Orchestration | Airflow (MWAA/Composer), Prefect, Dagster | scheduling, retries, alerting |
| Governance | OpenMetadata, catalogs | ownership, lineage, classification |
| Observability | logs/metrics/alerts | detect failures early |

---

## 3. Recommended Learning Order

| Step | Learn | Output |
|---|---|---|
| 1 | IAM + networking + storage + compute | build a secure baseline |
| 2 | Containers + registry | run container workloads |
| 3 | Data lake fundamentals | store & organize datasets |
| 4 | Batch processing | ETL to lake/warehouse |
| 5 | Orchestration | scheduled pipelines with retries |
| 6 | Modeling | warehouse modeling + tests (dbt) |
| 7 | Governance + security | access control + catalog basics |

---

## 4. Infrastructure as Code

| Topic | Tools | Minimum skills |
|---|---|---|
| IaC | Terraform | VPC/VNet, buckets, DB, container service |
| Environments | workspaces / separate state | dev/staging/prod separation |
| Reviews | PR + plan output | safe changes before apply |

---

## 5. Security Best Practices

| Principle | What to do | Avoid |
|---|---|---|
| Least privilege | minimal IAM policies | admin everywhere |
| Short-lived auth | roles/OIDC | static long-lived keys |
| Encryption | TLS + KMS | plaintext sensitive data |
| Secrets | secret manager | commit secrets to Git |
| Audit | enable audit logs | no traceability |

---

## 6. Cost Awareness

| Cost driver | Why expensive | Controls |
|---|---|---|
| Egress | moving data out | keep compute near storage |
| Always-on compute | 24/7 VMs/clusters | auto-shutdown dev |
| Storage growth | datasets + snapshots | retention + lifecycle rules |
| Warehouse queries | scan-based billing | partitioning + query discipline |

---

## 7. Hands-on Projects

| Project | Goal | Skills |
|---|---|---|
| Lake → Warehouse | batch ingest, transform, publish | Parquet, partitioning, dbt tests |
| Streaming → Analytics | real-time pipeline | streaming basics, monitoring lag |
| End-to-end platform | IaC + orchestration + CI/CD | how production platforms are built |

---

## 8. Choosing a Provider

| Provider | Strength | Good fit |
|---|---|---|
| AWS | broad ecosystem | general DE roles |
| GCP | analytics-first | BigQuery-centric stacks |
| Azure | enterprise Microsoft | orgs using AD/MS tooling |