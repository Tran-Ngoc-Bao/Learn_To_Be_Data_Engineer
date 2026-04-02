# OpenMetadata (Docker Compose + Postgres) — Deployment Guide

This document explains how to run **OpenMetadata** locally using Docker Compose with your compose file:

- `data_governance/open_metadata/deployment/docker-compose-postgres.yml`

Your stack (based on the compose you mentioned) typically includes:
- **PostgreSQL**: metadata database for OpenMetadata
- **Elasticsearch**: search backend
- **OpenMetadata Server**: UI + API
- **OpenMetadata Ingestion** (includes Airflow): runs ingestion workflows

---

## 1) Prerequisites

### Required
- Docker
- Docker Compose plugin (`docker compose version`)

### Recommended (local resources)
- RAM: **8GB+** (6GB minimum)
- Disk: **10GB+** free (depends on images + data size)

---

## 2) Folder structure

Deployment folder:

```
data_governance/open_metadata/deployment/
├── docker-compose-postgres.yml
└── docker-volume/
    └── db-data-postgres/   # Postgres persistent data (auto-created on first run)
```

> `docker-volume/` will be created automatically on the first run if it doesn’t exist.

---

## 3) Start OpenMetadata

### Step 1 — Go to the deployment directory

```bash
cd data_governance/open_metadata/deployment
```

### Step 2 — Start the services

```bash
docker compose -f docker-compose-postgres.yml up -d
```

### Step 3 — Check running containers

```bash
docker ps
```

### Step 4 — Follow logs (first startup can take a while)

```bash
docker compose -f docker-compose-postgres.yml logs -f
```

> The first run may take longer because Docker needs to pull images and OpenMetadata will run migrations.  
> Wait until `openmetadata_server` is healthy and the UI becomes available.

---

## 4) Access OpenMetadata

With the usual defaults in this compose style:

- OpenMetadata UI: `http://localhost:8585`
- OpenMetadata API base: `http://localhost:8585/api`
- OpenMetadata health/admin port: `http://localhost:8586`

If you changed ports in `docker-compose-postgres.yml`, use your mapped ports instead.

---

## 5) Default credentials

This depends on your authentication configuration (basic / OIDC / SAML).  
For the default **basic** auth, the common default is:

- Username: `admin`
- Password: `admin`

If login does not work, check server logs:

```bash
docker logs openmetadata_server --tail 200
```

---

## 6) Quick checks (health)

### 6.1 OpenMetadata Server healthcheck
```bash
curl -s http://localhost:8586/healthcheck
```

### 6.2 Elasticsearch cluster health
```bash
curl -s http://localhost:9200/_cluster/health?pretty
```

### 6.3 Postgres connectivity test
> The command below assumes your Postgres container is named `openmetadata_postgresql`
> and the database is `openmetadata_db`. If your compose uses different values, update accordingly.

```bash
docker exec -it openmetadata_postgresql psql -U postgres -d openmetadata_db -c "select 1;"
```

---

## 7) Stop / restart / reset

### Stop (keep data)
```bash
docker compose -f docker-compose-postgres.yml down
```

### Start again
```bash
docker compose -f docker-compose-postgres.yml up -d
```

### Full reset (remove volumes → deletes Postgres/Elasticsearch data)
```bash
docker compose -f docker-compose-postgres.yml down -v
```

---

## 8) Troubleshooting

### 8.1 Port conflicts
This stack commonly uses:
- Postgres: `5432`
- Elasticsearch: `9200`, `9300`
- OpenMetadata: `8585`, `8586`
- Airflow (Ingestion): `8080`

If you already have Postgres/Elasticsearch/Airflow running locally, you may hit port conflicts.
Fix by:
- changing port mappings in `docker-compose-postgres.yml`, or
- stopping the services that are using those ports.

### 8.2 UI not loading
- Wait 2–5 minutes (migrations + initialization can take time)
- Follow logs:
  ```bash
  docker compose -f docker-compose-postgres.yml logs -f
  ```
- Verify health checks in section (6)

### 8.3 Elasticsearch is resource-heavy
Elasticsearch can use significant RAM/CPU.
If your machine is limited:
- allocate more memory to Docker (Docker Desktop settings)
- close other heavy applications
- reduce ingestion workload (if you enabled scheduling)

---

## 9) Next steps (recommended)

Once the UI is running:
1. Go to **Services** and configure your source systems (Database/Messaging/Dashboard/Pipeline)
2. Run **Ingestion** to pull metadata into OpenMetadata
3. Enrich assets with:
   - Owner
   - Descriptions
   - Tags / Classifications
   - Glossary terms
4. Explore **Lineage** to understand upstream/downstream dependencies