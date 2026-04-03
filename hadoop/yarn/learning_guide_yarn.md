# 🧶 Apache YARN — Learning Guide

> Apache YARN (Yet Another Resource Negotiator) is the **resource management layer of Hadoop**. It separates resource management from job scheduling, enabling multiple processing frameworks (MapReduce, Spark, Tez, Flink) to share a Hadoop cluster.
>
> 📖 Official Docs: https://hadoop.apache.org/docs/stable/hadoop-yarn/hadoop-yarn-site/YARN.html

---

## 📚 Table of Contents

1. [Core Concepts](#1-core-concepts)
2. [Architecture](#2-architecture)
3. [Application Lifecycle](#3-application-lifecycle)
4. [Resource Model](#4-resource-model)
5. [Schedulers](#5-schedulers)
6. [YARN CLI](#6-yarn-cli)
7. [YARN Web UI](#7-yarn-web-ui)
8. [Key Configuration](#8-key-configuration)
9. [YARN & Spark](#9-yarn--spark)
10. [Monitoring & Troubleshooting](#10-monitoring--troubleshooting)

---

## 1. Core Concepts

| Concept | Description |
|---|---|
| **ResourceManager (RM)** | Master daemon — manages cluster resources and schedules applications |
| **NodeManager (NM)** | Worker daemon on each node — manages containers and reports to RM |
| **ApplicationMaster (AM)** | Per-application process — negotiates resources and tracks task progress |
| **Container** | A unit of resources (CPU + Memory) allocated on a node |
| **Queue** | Logical grouping of resources for scheduling and access control |
| **Client** | Submits applications to the ResourceManager |

---

## 2. Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Client                               │
│  (spark-submit / hadoop jar / hive query)               │
└──────────────────────┬──────────────────────────────────┘
                       │ Submit Application
                       ↓
┌─────────────────────────────────────────────────────────┐
│              ResourceManager (Master)                   │
│  ┌─────────────────┐   ┌───────────────────────────┐   │
│  │    Scheduler    │   │  ApplicationsManager      │   │
│  │ (allocate       │   │  (track app lifecycle)    │   │
│  │  containers)    │   └───────────────────────────┘   │
│  └─────────────────┘                                    │
└──────┬─────────────────────────┬───────────────────────┘
       │                         │
       ↓                         ↓
┌──────────────┐         ┌──────────────┐
│  NodeManager │  ...    │  NodeManager │
│  (Worker 1)  │         │  (Worker N)  │
│  ┌─────────┐ │         │  ┌─────────┐ │
│  │Container│ │         │  │Container│ │
│  │  (AM)   │ │         │  │ (Task)  │ │
│  └─────────┘ │         │  └─────────┘ │
│  ┌─────────┐ │         │  ┌─────────┐ │
│  │Container│ │         │  │Container│ │
│  │ (Task)  │ │         │  │ (Task)  │ │
│  └─────────┘ │         │  └─────────┘ │
└──────────────┘         └──────────────┘
```

---

## 3. Application Lifecycle

```
1. Client submits application to ResourceManager
        ↓
2. ResourceManager allocates a container for ApplicationMaster
        ↓
3. ApplicationMaster starts on a NodeManager
        ↓
4. ApplicationMaster registers with ResourceManager
        ↓
5. ApplicationMaster requests containers for tasks
        ↓
6. ResourceManager allocates containers (based on scheduler)
        ↓
7. ApplicationMaster launches tasks in allocated containers
        ↓
8. NodeManagers execute tasks, report status to ApplicationMaster
        ↓
9. ApplicationMaster reports completion to ResourceManager
        ↓
10. ResourceManager releases all containers
```

---

## 4. Resource Model

### Container resources

Each container is allocated:
- **Memory (MB)** — heap + overhead
- **vCores** — virtual CPU cores

### Key resource settings (`yarn-site.xml`)

```xml
<!-- Total memory on each NodeManager node -->
<property>
  <name>yarn.nodemanager.resource.memory-mb</name>
  <value>8192</value>   <!-- 8 GB -->
</property>

<!-- Total vCores on each NodeManager node -->
<property>
  <name>yarn.nodemanager.resource.cpu-vcores</name>
  <value>8</value>
</property>

<!-- Minimum container memory allocation -->
<property>
  <name>yarn.scheduler.minimum-allocation-mb</name>
  <value>1024</value>   <!-- 1 GB -->
</property>

<!-- Maximum container memory allocation -->
<property>
  <name>yarn.scheduler.maximum-allocation-mb</name>
  <value>4096</value>   <!-- 4 GB -->
</property>

<!-- Minimum container vCores -->
<property>
  <name>yarn.scheduler.minimum-allocation-vcores</name>
  <value>1</value>
</property>

<!-- Maximum container vCores -->
<property>
  <name>yarn.scheduler.maximum-allocation-vcores</name>
  <value>4</value>
</property>
```

---

## 5. Schedulers

YARN provides 3 built-in schedulers, configured in `yarn-site.xml`.

```xml
<property>
  <name>yarn.resourcemanager.scheduler.class</name>
  <value>org.apache.hadoop.yarn.server.resourcemanager.scheduler.capacity.CapacityScheduler</value>
</property>
```

### FIFO Scheduler

- Processes jobs in order of submission
- Simple but no multi-tenancy support
- ❌ Not recommended for production

### Capacity Scheduler (default)

- Divides cluster into **queues**, each with a guaranteed capacity
- Allows multiple teams/projects to share the cluster
- Supports queue hierarchy, elasticity, and priorities

```xml
<!-- capacity-scheduler.xml -->
<property>
  <name>yarn.scheduler.capacity.root.queues</name>
  <value>engineering,data,default</value>
</property>

<!-- engineering queue gets 50% of cluster capacity -->
<property>
  <name>yarn.scheduler.capacity.root.engineering.capacity</name>
  <value>50</value>
</property>

<!-- data queue gets 30% -->
<property>
  <name>yarn.scheduler.capacity.root.data.capacity</name>
  <value>30</value>
</property>

<!-- default queue gets 20% -->
<property>
  <name>yarn.scheduler.capacity.root.default.capacity</name>
  <value>20</value>
</property>
```

### Fair Scheduler

- Shares resources equally across all running applications
- No guaranteed queue capacity — resources are distributed dynamically
- Good for short interactive jobs mixed with long batch jobs

```xml
<!-- yarn-site.xml -->
<property>
  <name>yarn.resourcemanager.scheduler.class</name>
  <value>org.apache.hadoop.yarn.server.resourcemanager.scheduler.fair.FairScheduler</value>
</property>
```

### Comparison

| Feature | FIFO | Capacity | Fair |
|---|---|---|---|
| Multi-tenancy | ❌ | ✅ | ✅ |
| Guaranteed capacity | ❌ | ✅ | ❌ |
| Dynamic sharing | ❌ | ✅ (elastic) | ✅ |
| Priority support | ❌ | ✅ | ✅ |
| Best for | Dev/testing | Production (multi-team) | Mixed workloads |

---

## 6. YARN CLI

### Application management

```bash
# List all running applications
yarn application -list

# List applications by state
yarn application -list -appStates RUNNING
yarn application -list -appStates FINISHED,FAILED,KILLED

# Kill an application
yarn application -kill <application_id>

# Get application status
yarn application -status <application_id>

# View application logs
yarn logs -applicationId <application_id>

# View logs for a specific container
yarn logs -applicationId <application_id> -containerId <container_id>
```

### Node management

```bash
# List all nodes
yarn node -list

# List nodes by state
yarn node -list -states RUNNING
yarn node -list -states UNHEALTHY,DECOMMISSIONED

# Get node status
yarn node -status <node_id>
```

### Queue management

```bash
# List all queues
yarn queue -list

# Get queue status
yarn queue -status <queue_name>
```

### Cluster info

```bash
# Show cluster summary
yarn cluster --lnl

# Check YARN version
yarn version

# Show top applications by resource usage
yarn top
```

---

## 7. YARN Web UI

Access the YARN Web UI at:

```
http://<ResourceManager-host>:8088
```

### Key pages

| Page | URL | Description |
|---|---|---|
| Cluster Overview | `/cluster` | Overall cluster health and resource usage |
| Applications | `/cluster/apps` | All submitted applications |
| Nodes | `/cluster/nodes` | All NodeManager nodes and their status |
| Scheduler | `/cluster/scheduler` | Queue hierarchy and resource allocation |
| App Details | `/cluster/app/<app_id>` | Logs, containers, progress for a specific app |

---

## 8. Key Configuration

### `yarn-site.xml` — important properties

```xml
<!-- Enable ResourceManager HA (High Availability) -->
<property>
  <name>yarn.resourcemanager.ha.enabled</name>
  <value>true</value>
</property>

<!-- Application log aggregation (collect logs to HDFS after job completes) -->
<property>
  <name>yarn.log-aggregation-enable</name>
  <value>true</value>
</property>
<property>
  <name>yarn.nodemanager.remote-app-log-dir</name>
  <value>/var/log/hadoop-yarn/apps</value>
</property>

<!-- Log retention period -->
<property>
  <name>yarn.log-aggregation.retain-seconds</name>
  <value>604800</value>   <!-- 7 days -->
</property>

<!-- Container memory overhead (JVM off-heap, etc.) -->
<property>
  <name>yarn.nodemanager.vmem-pmem-ratio</name>
  <value>2.1</value>
</property>

<!-- Disable virtual memory check (common fix on modern Linux) -->
<property>
  <name>yarn.nodemanager.vmem-check-enabled</name>
  <value>false</value>
</property>

<!-- ResourceManager Web UI address -->
<property>
  <name>yarn.resourcemanager.webapp.address</name>
  <value>0.0.0.0:8088</value>
</property>
```

---

## 9. YARN & Spark

When submitting a Spark job to YARN, Spark runs in two modes:

### Cluster mode (recommended for production)

The Spark Driver runs **inside the cluster** (as ApplicationMaster).

```bash
spark-submit \
  --master yarn \
  --deploy-mode cluster \
  --num-executors 4 \
  --executor-memory 2g \
  --executor-cores 2 \
  --driver-memory 1g \
  --queue data \
  my_spark_job.py
```

### Client mode (useful for debugging)

The Spark Driver runs on the **submitting machine**. Logs are visible locally.

```bash
spark-submit \
  --master yarn \
  --deploy-mode client \
  --num-executors 4 \
  --executor-memory 2g \
  --executor-cores 2 \
  my_spark_job.py
```

### Resource allocation comparison

| Mode | Driver location | Use case |
|---|---|---|
| `cluster` | Inside YARN cluster | Production jobs |
| `client` | Local machine | Interactive / debugging |

### Dynamic Allocation (auto-scale executors)

```bash
spark-submit \
  --master yarn \
  --deploy-mode cluster \
  --conf spark.dynamicAllocation.enabled=true \
  --conf spark.dynamicAllocation.minExecutors=2 \
  --conf spark.dynamicAllocation.maxExecutors=20 \
  --conf spark.shuffle.service.enabled=true \
  my_spark_job.py
```

---

## 10. Monitoring & Troubleshooting

### Common issues and fixes

| Issue | Cause | Fix |
|---|---|---|
| `Container killed: exceeded memory` | Container exceeded its memory limit | Increase `--executor-memory` or `spark.driver.memoryOverhead` |
| `Application stuck in ACCEPTED` | No resources available in queue | Check queue capacity; kill other jobs |
| `NodeManager UNHEALTHY` | Disk space or memory threshold exceeded | Free up disk; check `yarn.nodemanager.disk-health-checker` |
| Virtual memory exceeded | Linux over-commitment | Set `yarn.nodemanager.vmem-check-enabled=false` |
| Logs not found | Log aggregation disabled | Enable `yarn.log-aggregation-enable=true` |

### Useful diagnostic commands

```bash
# Check ResourceManager logs
cat $HADOOP_HOME/logs/yarn-*-resourcemanager-*.log

# Check NodeManager logs
cat $HADOOP_HOME/logs/yarn-*-nodemanager-*.log

# View container logs directly
yarn logs -applicationId application_XXXX_XXXX

# Check node health
yarn node -list -states UNHEALTHY

# Check queue usage
yarn queue -status default
```

### Memory tuning tips for Spark on YARN

```
Total executor memory YARN allocates =
    spark.executor.memory
  + spark.executor.memoryOverhead   (default: max(384MB, 10% of executor memory))

Total driver memory YARN allocates =
    spark.driver.memory
  + spark.driver.memoryOverhead
```

---

## 📎 Useful Links

- 📖 [Official YARN Docs](https://hadoop.apache.org/docs/stable/hadoop-yarn/hadoop-yarn-site/YARN.html)
- 📖 [Capacity Scheduler Guide](https://hadoop.apache.org/docs/stable/hadoop-yarn/hadoop-yarn-site/CapacityScheduler.html)
- 📖 [Fair Scheduler Guide](https://hadoop.apache.org/docs/stable/hadoop-yarn/hadoop-yarn-site/FairScheduler.html)
- 📖 [Spark on YARN](https://spark.apache.org/docs/latest/running-on-yarn.html)
- 🐙 [Hadoop GitHub](https://github.com/apache/hadoop)