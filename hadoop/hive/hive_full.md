# 🐝 Apache Hive — Learning Guide

> Apache Hive is a **data warehouse system built on top of Hadoop** that provides SQL-like querying (HiveQL) over large datasets stored in HDFS. It translates SQL queries into MapReduce / Tez / Spark jobs.
>
> 📖 Official Docs: https://hive.apache.org

---

## 📚 Table of Contents

1. [Core Concepts](#1-core-concepts)
2. [Architecture](#2-architecture)
3. [Data Model](#3-data-model)
4. [HiveQL — DDL](#4-hiveql--ddl)
5. [HiveQL — DML](#5-hiveql--dml)
6. [HiveQL — Querying](#6-hiveql--querying)
7. [Partitioning](#7-partitioning)
8. [Bucketing](#8-bucketing)
9. [File Formats](#9-file-formats)
10. [Built-in Functions](#10-built-in-functions)
11. [UDF — User Defined Functions](#11-udf--user-defined-functions)
12. [Hive on Tez vs Spark](#12-hive-on-tez-vs-spark)
13. [Performance Tuning](#13-performance-tuning)

---

## 1. Core Concepts

| Concept | Description |
|---|---|
| **HiveQL** | SQL-like query language for Hive |
| **Metastore** | Stores metadata (schema, table info) in a relational DB (MySQL, PostgreSQL) |
| **Driver** | Receives and compiles HiveQL queries |
| **Execution Engine** | Translates queries into jobs (MapReduce, Tez, Spark) |
| **SerDe** | Serializer/Deserializer — defines how data is read/written |
| **Managed Table** | Hive owns the data; dropping the table deletes the data |
| **External Table** | Hive does NOT own the data; dropping the table keeps the data in HDFS |

---

## 2. Architecture

```
┌──────────────────────────────────────────────────┐
│                  Hive Client                     │
│         (CLI / JDBC / Thrift / Web UI)           │
└────────────────────┬─────────────────────────────┘
                     ↓
┌──────────────────────────────────────────────────┐
│                Hive Driver                       │
│  Parser → Planner → Optimizer → Executor         │
└──────┬─────────────────────────┬─────────────────┘
       ↓                         ↓
┌─────────────┐         ┌────────────────┐
│  Metastore  │         │ Execution      │
│ (MySQL/PG)  │         │ Engine         │
│ schema info │         │ MapReduce/Tez/ │
└─────────────┘         │ Spark          │
                        └───────┬────────┘
                                ↓
                    ┌───────────────────────┐
                    │        HDFS           │
                    │  (actual data files)  │
                    └───────────────────────┘
```

---

## 3. Data Model

```
Database
└── Table
    ├── Partition (optional, by column value)
    │   └── Bucket (optional, hash-based split)
    └── Row (stored in files: ORC, Parquet, CSV, ...)
```

---

## 4. HiveQL — DDL

### Database

```sql
-- Create a database
CREATE DATABASE IF NOT EXISTS my_db;

-- Use a database
USE my_db;

-- Show databases
SHOW DATABASES;

-- Drop a database
DROP DATABASE IF EXISTS my_db CASCADE;
```

### Managed Table

Hive manages both metadata and data. Dropping the table **deletes the data**.

```sql
CREATE TABLE IF NOT EXISTS employees (
    id      INT,
    name    STRING,
    dept    STRING,
    salary  DOUBLE
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE;
```

### External Table

Hive manages only metadata. Dropping the table **keeps the data in HDFS**.

```sql
CREATE EXTERNAL TABLE IF NOT EXISTS sales (
    order_id    INT,
    product     STRING,
    amount      DOUBLE,
    sale_date   STRING
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION '/user/hive/warehouse/sales/';
```

### Other DDL

```sql
-- Show tables
SHOW TABLES;

-- Describe a table
DESCRIBE employees;
DESCRIBE FORMATTED employees;   -- detailed info

-- Alter table
ALTER TABLE employees ADD COLUMNS (email STRING);
ALTER TABLE employees RENAME TO staff;

-- Drop table
DROP TABLE IF EXISTS employees;
```

---

## 5. HiveQL — DML

```sql
-- Load data from local file system
LOAD DATA LOCAL INPATH '/home/user/employees.csv'
INTO TABLE employees;

-- Load data from HDFS
LOAD DATA INPATH '/hdfs/path/employees.csv'
INTO TABLE employees;

-- Overwrite existing data
LOAD DATA LOCAL INPATH '/home/user/employees.csv'
OVERWRITE INTO TABLE employees;

-- Insert from query
INSERT INTO TABLE employees
SELECT id, name, dept, salary FROM temp_employees;

-- Insert overwrite
INSERT OVERWRITE TABLE employees
SELECT id, name, dept, salary FROM temp_employees;

-- Insert into multiple tables at once
FROM source_table
INSERT INTO TABLE table_a SELECT col1, col2 WHERE dept = 'IT'
INSERT INTO TABLE table_b SELECT col1, col2 WHERE dept = 'HR';

-- CTAS — Create Table As Select
CREATE TABLE dept_summary AS
SELECT dept, COUNT(*) AS count, AVG(salary) AS avg_salary
FROM employees
GROUP BY dept;
```

---

## 6. HiveQL — Querying

### Basic SELECT

```sql
SELECT name, salary
FROM employees
WHERE dept = 'Engineering'
  AND salary > 50000
ORDER BY salary DESC
LIMIT 10;
```

### JOIN

```sql
-- Inner Join
SELECT e.name, d.dept_name
FROM employees e
JOIN departments d ON e.dept = d.dept_id;

-- Left Outer Join
SELECT e.name, d.dept_name
FROM employees e
LEFT OUTER JOIN departments d ON e.dept = d.dept_id;

-- Map Join (small table optimization)
SELECT /*+ MAPJOIN(d) */ e.name, d.dept_name
FROM employees e
JOIN departments d ON e.dept = d.dept_id;
```

### Aggregation

```sql
SELECT
    dept,
    COUNT(*)        AS headcount,
    AVG(salary)     AS avg_salary,
    MAX(salary)     AS max_salary,
    MIN(salary)     AS min_salary
FROM employees
GROUP BY dept
HAVING COUNT(*) > 5;
```

### Window Functions

```sql
SELECT
    name,
    dept,
    salary,
    RANK() OVER (PARTITION BY dept ORDER BY salary DESC) AS rank_in_dept,
    SUM(salary) OVER (PARTITION BY dept)                 AS dept_total
FROM employees;
```

### Subquery

```sql
SELECT name, salary
FROM employees
WHERE salary > (SELECT AVG(salary) FROM employees);
```

---

## 7. Partitioning

Partitioning splits data into subdirectories by column value, dramatically improving query performance by scanning only relevant partitions.

### Static Partition

```sql
-- Create partitioned table
CREATE TABLE sales_partitioned (
    order_id    INT,
    product     STRING,
    amount      DOUBLE
)
PARTITIONED BY (sale_year INT, sale_month INT)
STORED AS ORC;

-- Insert into a specific partition
INSERT INTO TABLE sales_partitioned
PARTITION (sale_year=2024, sale_month=1)
SELECT order_id, product, amount
FROM sales
WHERE YEAR(sale_date) = 2024 AND MONTH(sale_date) = 1;
```

### Dynamic Partition

```sql
-- Enable dynamic partitioning
SET hive.exec.dynamic.partition = true;
SET hive.exec.dynamic.partition.mode = nonstrict;

-- Insert with dynamic partitions
INSERT INTO TABLE sales_partitioned
PARTITION (sale_year, sale_month)
SELECT order_id, product, amount,
       YEAR(sale_date), MONTH(sale_date)
FROM sales;
```

```sql
-- Query a specific partition (partition pruning)
SELECT * FROM sales_partitioned
WHERE sale_year = 2024 AND sale_month = 3;

-- Show partitions
SHOW PARTITIONS sales_partitioned;
```

---

## 8. Bucketing

Bucketing divides data within a partition into a fixed number of files using a hash function on a column. Useful for joins and sampling.

```sql
-- Enable bucketing
SET hive.enforce.bucketing = true;

-- Create bucketed table
CREATE TABLE employees_bucketed (
    id      INT,
    name    STRING,
    dept    STRING,
    salary  DOUBLE
)
CLUSTERED BY (id) INTO 4 BUCKETS
STORED AS ORC;

-- Insert data (respects bucketing)
INSERT INTO TABLE employees_bucketed
SELECT * FROM employees;

-- Efficient bucketed join (no shuffle needed)
SELECT /*+ MAPJOIN(d) */ e.name, d.dept_name
FROM employees_bucketed e
JOIN departments_bucketed d ON e.dept = d.dept_id;

-- Sampling from buckets
SELECT * FROM employees_bucketed
TABLESAMPLE(BUCKET 1 OUT OF 4 ON id);
```

---

## 9. File Formats

| Format | Description | Best For |
|---|---|---|
| `TEXTFILE` | Plain text, CSV | Simple data, compatibility |
| `SEQUENCEFILE` | Binary key-value pairs | MapReduce compatibility |
| `ORC` | Optimized Row Columnar — compressed, splittable | Hive production workloads |
| `PARQUET` | Columnar, widely supported | Spark, Presto, Trino interop |
| `AVRO` | Row-based, schema evolution support | Kafka, schema changes |

```sql
-- ORC (recommended for Hive)
CREATE TABLE my_table (...)
STORED AS ORC
TBLPROPERTIES ("orc.compress"="SNAPPY");

-- Parquet
CREATE TABLE my_table (...)
STORED AS PARQUET;

-- Convert existing table to ORC
CREATE TABLE my_table_orc
STORED AS ORC AS
SELECT * FROM my_table_text;
```

---

## 10. Built-in Functions

### String

```sql
SELECT
    UPPER(name),
    LOWER(name),
    LENGTH(name),
    SUBSTR(name, 1, 3),
    TRIM(name),
    CONCAT(first_name, ' ', last_name),
    SPLIT(email, '@')[0]      AS username,
    REGEXP_REPLACE(phone, '[^0-9]', '')
FROM employees;
```

### Date & Time

```sql
SELECT
    CURRENT_DATE,
    CURRENT_TIMESTAMP,
    YEAR(sale_date),
    MONTH(sale_date),
    DAY(sale_date),
    DATE_FORMAT(sale_date, 'yyyy-MM'),
    DATEDIFF('2024-12-31', '2024-01-01')  AS days_diff,
    DATE_ADD(sale_date, 30)               AS future_date
FROM sales;
```

### Conditional

```sql
SELECT
    name,
    CASE
        WHEN salary >= 100000 THEN 'Senior'
        WHEN salary >= 60000  THEN 'Mid'
        ELSE 'Junior'
    END AS level,
    IF(dept = 'Engineering', salary * 1.1, salary) AS adjusted_salary,
    COALESCE(email, phone, 'N/A')                  AS contact
FROM employees;
```

### Collection

```sql
-- Array
SELECT arr[0] FROM t;                  -- index
SELECT SIZE(arr) FROM t;               -- length
SELECT ARRAY_CONTAINS(arr, 'x') FROM t;

-- Map
SELECT m['key'] FROM t;                -- access by key
SELECT MAP_KEYS(m), MAP_VALUES(m) FROM t;

-- Explode (one row per element)
SELECT name, tag
FROM employees
LATERAL VIEW EXPLODE(tags) t AS tag;
```

---

## 11. UDF — User Defined Functions

```java
// Java UDF example
import org.apache.hadoop.hive.ql.exec.UDF;
import org.apache.hadoop.io.Text;

public class UpperCaseUDF extends UDF {
    public Text evaluate(Text input) {
        if (input == null) return null;
        return new Text(input.toString().toUpperCase());
    }
}
```

```sql
-- Register and use UDF
ADD JAR /path/to/my-udf.jar;
CREATE TEMPORARY FUNCTION my_upper AS 'com.example.UpperCaseUDF';

SELECT my_upper(name) FROM employees;
```

---

## 12. Hive on Tez vs Spark

| Feature | MapReduce | Tez | Spark |
|---|---|---|---|
| Speed | Slow (disk I/O) | Fast (DAG-based) | Fastest (in-memory) |
| Memory usage | Low | Medium | High |
| Fault tolerance | High | High | High |
| Default engine | Legacy | Hive default | Optional |

```sql
-- Set execution engine
SET hive.execution.engine = tez;     -- default
SET hive.execution.engine = spark;   -- use Spark
SET hive.execution.engine = mr;      -- legacy MapReduce
```

---

## 13. Performance Tuning

```sql
-- Enable vectorized query execution (batch row processing)
SET hive.vectorized.execution.enabled = true;

-- Enable Cost-Based Optimizer (CBO)
SET hive.cbo.enable = true;
SET hive.stats.autogather = true;

-- Compute table statistics for CBO
ANALYZE TABLE employees COMPUTE STATISTICS;
ANALYZE TABLE employees COMPUTE STATISTICS FOR COLUMNS;

-- Enable map-side join for small tables (< 25MB)
SET hive.auto.convert.join = true;
SET hive.mapjoin.smalltable.filesize = 25000000;

-- Merge small output files
SET hive.merge.mapfiles = true;
SET hive.merge.mapredfiles = true;

-- Tune number of reducers
SET hive.exec.reducers.bytes.per.reducer = 256000000;
SET mapreduce.job.reduces = 10;

-- Enable compression
SET hive.exec.compress.output = true;
SET mapreduce.output.fileoutputformat.compress.codec = org.apache.hadoop.io.compress.SnappyCodec;
```

### Key tuning strategies

| Strategy | Description |
|---|---|
| **Partitioning** | Avoid full table scans by pruning partitions |
| **ORC + Snappy** | Use columnar + compressed format |
| **Bucketing** | Speed up joins and aggregations on high-cardinality columns |
| **Map Join** | Broadcast small tables to avoid shuffle |
| **CBO** | Let Hive choose the optimal join order |
| **Vectorization** | Process batches of rows instead of one at a time |

---

## 📎 Useful Links

- 📖 [Official Hive Docs](https://hive.apache.org/docs/latest/)
- 📖 [HiveQL Language Manual](https://cwiki.apache.org/confluence/display/Hive/LanguageManual)
- 🐙 [Hive GitHub](https://github.com/apache/hive)