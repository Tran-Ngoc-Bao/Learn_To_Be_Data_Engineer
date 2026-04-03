
# 🧾 OpenMetadata — Learning Guide

> OpenMetadata is an open-source **metadata platform** (catalog + governance + collaboration) to discover, document, and manage data assets (tables, topics, dashboards, pipelines, ML models) with lineage, ownership, tags, and quality signals.

---

## 📚 Table of Contents

1. [Core Concepts](#1-core-concepts)
2. [Architecture Overview](#2-architecture-overview)
3. [UI Tour (What to click first)](#3-ui-tour-what-to-click-first)
4. [Entity Model](#4-entity-model)
5. [Services & Connectors](#5-services--connectors)
6. [Ingestion Basics](#6-ingestion-basics)
7. [Lineage](#7-lineage)
8. [Data Quality (concepts in OpenMetadata)](#8-data-quality-concepts-in-openmetadata)
9. [Governance Features](#9-governance-features)
10. [Security & Access Control](#10-security--access-control)
11. [APIs & Automation](#11-apis--automation)
12. [Operational Tips](#12-operational-tips)
13. [Learning Checklist](#13-learning-checklist)

---

## 1) Core Concepts

| Concept | Meaning |
|---|---|
| **Metadata** | Data about data: schema, owners, descriptions, tags, usage, lineage |
| **Entities** | Assets tracked by OM (tables, topics, dashboards, pipelines, etc.) |
| **Services** | Systems that OM connects to (Postgres, Kafka, Airflow, Superset, etc.) |
| **Ingestion** | Process to pull metadata/lineage/usage into OM |
| **Lineage** | Relationships between upstream and downstream entities |
| **Governance** | Ownership, classification, domains, glossary, policies |

---

## 2) Architecture Overview

A typical OpenMetadata setup includes:

- **OpenMetadata Server**: UI + API
- **Metadata store**: usually **PostgreSQL** or MySQL
- **Search backend**: **Elasticsearch** or OpenSearch
- **Ingestion/Agent**: runs connectors to ingest metadata + lineage

Your docker compose runs all of these locally.

---

## 3) UI Tour (What to click first)

Suggested order to explore in the UI:
1. **Explore**: search for tables/topics/dashboards
2. **Services**: see all connected systems
3. **Domains**: organize assets by business domains
4. **Glossary**: business terms and definitions
5. **Tags / Classifications**: labeling and PII classification
6. **Lineage**: understand data flow
7. **Activity Feed**: collaboration + change tracking

---

## 4) Entity Model

Common entities in OpenMetadata:

| Entity | Examples |
|---|---|
| **Table** | Postgres/MySQL/BigQuery tables |
| **Topic** | Kafka topics |
| **Dashboard / Chart** | Superset / Looker / Metabase |
| **Pipeline** | Airflow DAGs, dbt jobs |
| **ML Model** | model registry entities (depending on integrations) |
| **User / Team** | ownership & access control |
| **Glossary Term** | business definitions |
| **Tag / Classification** | e.g., PII.SSN, Finance, Customer |

Each entity typically supports:
- Description
- Owner (user/team)
- Tags / glossary terms
- Lineage
- Versioning / change history

---

## 5) Services & Connectors

A “Service” defines a system to ingest from.

Examples:
- Database service: Postgres / MySQL / Snowflake / BigQuery
- Messaging service: Kafka
- Dashboard service: Superset / Metabase
- Pipeline service: Airflow / Dagster (via custom integration) / dbt

What to learn:
- How to register a service in UI
- How connectors authenticate (host/user/password/secret)
- What metadata can be ingested (schemas, lineage, usage, queries)

---

## 6) Ingestion Basics

Ingestion usually pulls:
- **Metadata**: databases → schemas → tables → columns
- **Profiles** (optional): column stats, null %, distinct count
- **Lineage** (optional): pipelines or query-based lineage
- **Usage** (optional): query logs and popularity

Core ideas:
- Ingestion is often scheduled (daily/hourly)
- Ingestion jobs should be repeatable and observable (logs, retries)
- Secrets should not be committed into Git

---

## 7) Lineage

Lineage in OpenMetadata helps answer:
- “If this table changes, what dashboards break?”
- “Where does this KPI come from?”

Learn:
- Table-level lineage vs column-level lineage
- Pipeline-based lineage (Airflow/dbt)
- How to annotate lineage (descriptions on edges/nodes)

---

## 8) Data Quality (concepts in OpenMetadata)

OpenMetadata can store/visualize quality signals and tests depending on setup and integrations.

What to learn (conceptually):
- DQ checks and results are attached to datasets
- Monitoring freshness, row count anomalies
- Linking issues/incidents to data assets

(Your repo can later add an example with Great Expectations / Soda integrated into OM.)

---

## 9) Governance Features

Core governance building blocks:
- **Ownership**: user/team ownership on assets
- **Domains**: group datasets by business domain
- **Glossary**: define business terms and map them to assets
- **Tags/Classifications**: labels (e.g., PII, Finance, Public)
- **Announcements/Tasks**: collaboration around data assets

Suggested practice:
- Pick 5 tables and add: owner + description + tags + glossary terms.

---

## 10) Security & Access Control

OpenMetadata includes:
- Authentication (basic/OIDC/SAML depending on config)
- Authorization policies / roles
- Team & user management

What to learn:
- Role-based access concept (who can edit metadata vs view)
- How to keep admin actions limited
- How to handle secrets safely (env vars, secret managers)

---

## 11) APIs & Automation

OpenMetadata provides APIs to automate:
- Create/update services
- Update descriptions/owners/tags
- Trigger ingestion jobs (depending on setup)
- Export/import metadata (useful for migration)

Practice tasks:
- Use API token (if configured) to update a table description automatically.
- Bulk apply tags (scripted governance).

---

## 12) Operational Tips

- Treat the metadata DB (Postgres) as critical: backup strategy matters.
- Monitor Elasticsearch memory/CPU (it can be heavy).
- Keep versions consistent between server and ingestion components.
- Start with a small scope:
  - 1 database service
  - 1 pipeline service
  - minimal lineage
  - then expand

---

## 13) Learning Checklist

You “know OpenMetadata enough” when you can:
- [ ] Explain what entities/services are
- [ ] Connect a database service and ingest metadata
- [ ] Add ownership + documentation + tags
- [ ] Navigate lineage to understand dependencies
- [ ] Understand the basics of authn/authz options
- [ ] Automate one metadata change via API/script