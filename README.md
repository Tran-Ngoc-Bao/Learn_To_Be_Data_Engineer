# 🛠️ Learn To Be a Data Engineer

> A structured, hands-on learning roadmap covering the core technologies and skills required to become a **Data Engineer**.

Each folder in this repository corresponds to a technology group or domain that is essential in modern data engineering.

---

## 🗺️ Learning Roadmap

```
Learn_To_Be_Data_Engineer/
├── programming_languages/   # Python & Java fundamentals
├── general_knowledge/       # SQL, Docker, Linux, Big Data concepts
├── hadoop/                  # HDFS, YARN, Hive, HBase
├── data_processing/         # Spark, Kafka
├── query_engine/            # Trino/Presto
├── etl_data/                # Airflow & Others
├── data_governance/         # Quality, lineage, catalog, security, contracts
├── ci_cd/                   # Build, test, release, deploy automation
└── cloud/                   # AWS/GCP/Azure + IaC + Observability
```

---

## 📚 Contents

### 1. 🐍 Programming Languages
| Technology | Folder |
|---|---|
| Python | [programming_languages/python](programming_languages/python) |
| Java | [programming_languages/java](programming_languages/java) |

---

### 2. 📖 General Knowledge
📁 [general_knowledge](general_knowledge)

- **SQL & NoSQL** – SQL Server, PostgreSQL and NoSQL
- **Docker & Linux** – containerization, shell scripting, system management
- **Computer Networks & Operating Systems** – fundamentals for distributed systems
- **Big Data Overview** – core concepts and ecosystem
- **Data Architecture & Data Modeling** – designing scalable data systems

---

### 3. 🐘 Hadoop Ecosystem
| Technology | Folder | Description |
|---|---|---|
| HDFS | [hadoop/hdfs](hadoop/hdfs) | Distributed file system |
| YARN | [hadoop/yarn](hadoop/yarn) | Resource management |
| Hive | [hadoop/hive](hadoop/hive) | SQL-on-Hadoop data warehouse |
| HBase | [hadoop/hbase](hadoop/hbase) | NoSQL columnar store on Hadoop |

---

### 4. ⚡ Data Processing & Query Engine
| Technology | Folder | Description |
|---|---|---|
| Apache Spark | [data_processing/spark](data_processing/spark) | Distributed data processing engine |
| Trino/Presto | [query_engine/trino](query_engine/trino) | Fast distributed SQL query engine |
| Apache Kafka | [data_processing/kafka](data_processing/kafka) | Distributed event streaming platform |

---

### 5. 🔄 ETL / ELT Pipelines
| Technology | Folder | Description |
|---|---|---|
| Apache Airflow | [etl_data/airflow](etl_data/airflow) | Workflow orchestration *(includes docker-compose)* |
| Others | [etl_data/others](etl_data/others) | Workflow orchestration *(Dagster, Prefect)* |

---

### 6. 🧾 Data Governance
| Topic | Folder | Description |
|---|---|---|
| Data Quality | [data_governance](data_governance) | Validation, freshness, completeness |
| Metadata & Catalog | [data_governance](data_governance) | Ownership, documentation, discovery |
| Data Lineage | [data_governance](data_governance) | Upstream/downstream tracking |
| Security & Access Control | [data_governance](data_governance) | RBAC, encryption, audits |
| OpenMetadata | [data_governance/open_metadata](data_governance/open_metadata) | Metadata catalog tool |

---

### 7. 🔁 CI/CD (Build, Test, Release, Deploy)
| Topic | Folder | Description |
|---|---|---|
| CI basics | [ci_cd](ci_cd) | Linting, testing, build pipelines |
| CD basics | [ci_cd](ci_cd) | Promotion, environments, approvals |
| GitHub Actions | [ci_cd](ci_cd) | Workflows, runners, secrets |
| Docker | [ci_cd/docker](ci_cd/docker) | Build images, tags, push to registry |
| Kubernetes | [ci_cd/kubernetes](ci_cd/kubernetes) | Deploy strategies, manifests, Helm |

---

### 8. ☁️ Cloud Computing

| Topic | Folder | Description |
|---|---|---|
| Cloud fundamentals | [cloud](cloud) | Regions/zones, shared responsibility model, core cloud concepts. |
| IAM & networking | [cloud](cloud) | Roles/policies, VPC/VNet, security groups, private access patterns. |
| Storage & compute | [cloud](cloud) | Object storage + compute options (VM/containers/serverless) for DE workloads. |
| Managed data services | [cloud](cloud) | Warehouses/lakehouses, managed Spark, orchestration, streaming services. |
| IaC & operations | [cloud](cloud) | Terraform basics, observability (logs/metrics), and cost controls. |

---

## 🧭 Suggested Learning Order

```
1. Programming Languages (Python / Java)
        ↓
2. General Knowledge (SQL, Linux, Docker, Big Data concepts)
        ↓
3. Hadoop Ecosystem (HDFS, YARN, Hive, HBase)
        ↓
4. Data Processing & Query Engine (Spark, Trino, Kafka)
        ↓
5. ETL / ELT Pipelines (Airflow, Dagster, Prefect)
        ↓
6. Data Governance (Quality, lineage, security, metadata)
        ↓
7. CI/CD (GitHub Actions, build/test, Docker, Kubernetes deploy)
        ↓
8. Cloud Computing (IAM, storage, managed services, IaC)
```

---

> 💡 *This repository is a personal learning journal. Each folder contains notes, configurations, and practical exercises for the respective technology.*