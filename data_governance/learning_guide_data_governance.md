# 🧾 Data Governance — Learning Guide

> Data Governance helps ensure data is **trusted, secure, consistent, and discoverable**.  
> As a Data Engineer, governance is not only “policy” — it’s also **automation** (checks, monitoring, access control, and metadata).

---

## 📚 Topics Covered (in this guide)

1. Data Quality  
2. Metadata & Catalog (concepts, not tools)  
3. Data Lineage  
4. Security & Access Control  

> Note: **OpenMetadata** is intentionally excluded here and should live in a separate section under `data_governance/open_metadata/`.

---

## 1) Data Quality

### What to learn
- **Dimensions** (common metrics):
  - **Freshness**: is data up-to-date?
  - **Completeness**: are required fields populated?
  - **Validity**: does data match allowed formats/ranges?
  - **Uniqueness**: are keys unique where expected?
  - **Consistency**: do related datasets agree?
- **DQ checks location**:
  - Ingest time (raw → bronze)
  - Transform time (bronze → silver/gold)
  - Serving time (before BI / APIs)

### What you should be able to do (practical)
- Define a **DQ checklist** per dataset/table (10–20 rules is a good start)
- Implement automated checks as part of:
  - Airflow/Dagster/Prefect tasks
  - SQL checks (COUNT, NULL rate, duplicates)
  - Alerting when thresholds break

### Example checklist (template)
For each dataset, document:
- Owner
- SLA / update schedule
- Primary key (if any)
- Critical columns (must not be NULL)
- Range rules (e.g., amount >= 0)
- Duplicate constraints
- Freshness threshold (e.g., data lag < 2 hours)

---

## 2) Metadata & Catalog (Concepts)

### What metadata means
Metadata is “data about data”, including:
- **Technical metadata**: schema, partitions, file formats, locations, job definitions
- **Business metadata**: definitions, business meaning, owners, tags
- **Operational metadata**: run history, row counts, pipeline status

### What to learn
- Dataset documentation basics:
  - description, owners, contacts
  - schema + column descriptions
  - sample queries
  - update frequency and SLAs
- Naming conventions:
  - table naming, column naming, event naming
- Ownership model:
  - data owner, steward, producer/consumer

### What you should be able to do (practical)
- Create a **dataset documentation template**
- Keep schema documentation and pipeline ownership up to date
- Tag datasets by domain (sales, finance, product, etc.)

---

## 3) Data Lineage

### What lineage is
Lineage explains:
- **Upstream**: where the data came from (sources, ingestion jobs)
- **Downstream**: who uses it (tables, dashboards, ML features)
- **Transformations**: what changed (joins, filters, aggregations)

### What to learn
- Lineage levels:
  - **Dataset/Table-level lineage** (good starting point)
  - Column-level lineage (advanced)
- Where lineage should be captured:
  - Orchestrator runs (Airflow/Dagster/Prefect)
  - Query engines / warehouses
  - dbt transformations (if used)

### What you should be able to do (practical)
- Draw a simple **lineage map** for one pipeline:
  - Sources → Raw tables → Curated tables → BI dashboards
- Identify “blast radius”:
  - If a source column changes, what breaks downstream?

---

## 4) Security & Access Control

### What to learn
- **Access control models**:
  - **RBAC**: role-based access (common)
  - **ABAC**: attribute-based access (fine-grained, advanced)
- **Secrets management**:
  - never commit secrets to Git
  - store secrets in env vars / secret managers
- **Encryption**:
  - at rest (storage encryption)
  - in transit (TLS)
- **Auditing**:
  - who accessed which dataset and when

### What you should be able to do (practical)
- Define roles:
  - read-only analyst, engineer, admin
- Apply least privilege:
  - only grant access to necessary datasets
- Ensure pipeline credentials are stored safely:
  - environment variables, secret stores

---

## ✅ Suggested Learning Order (within Governance)

1. Data Quality (rules + automation)
2. Metadata basics (ownership + documentation)
3. Lineage mapping (table-level)
4. Security (RBAC + secrets + audits)

---

## 🎯 Mini-project (recommended)

Pick one dataset/pipeline and produce:
- A DQ checklist + automated checks
- A dataset documentation page (schema, owner, SLA)
- A lineage diagram (at least table-level)
- A simple access policy (roles + permissions)

---

## 📎 References (optional)

- Data quality concepts: completeness, validity, freshness
- Metadata & catalog: data dictionary, ownership, tagging
- Lineage: upstream/downstream dependency mapping
- Security: RBAC, secrets handling, auditing