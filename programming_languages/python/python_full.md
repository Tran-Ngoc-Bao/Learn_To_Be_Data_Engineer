# 🐍 Python — Learning Guide (for Data Engineers)

> Python is the most common language for Data Engineering: scripting, ETL/ELT, orchestration (Airflow/Dagster), data quality checks, and integrations with databases/APIs.

---

## 🗺️ Suggested Roadmap

1. Python basics (syntax, types, control flow)
2. Functions, modules, virtual environments
3. Data structures (list/dict/set/tuple)
4. File I/O + JSON + CSV + Parquet basics
5. Exceptions + Logging
6. Type hints + Dataclasses
7. Testing (pytest)
8. Dependency management (pip / requirements.txt / pyproject.toml)
9. pandas (core), optional: polars
10. DB access (psycopg2 / SQLAlchemy)
11. Async & concurrency (optional)

---

## 1. Environment Setup

### Create venv
```bash
python -m venv .venv
source .venv/bin/activate     # Linux/macOS
.venv\Scripts\activate        # Windows
```

### Install packages
```bash
pip install -U pip
pip install pandas requests pytest
```

### Freeze dependencies
```bash
pip freeze > requirements.txt
```

---

## 2. Python Basics

### Types
```python
x: int = 10
pi: float = 3.14
ok: bool = True
name: str = "Bao"
items: list[int] = [1, 2, 3]
```

### Control flow
```python
if x > 0:
    ...
elif x == 0:
    ...
else:
    ...

for i in range(3):
    ...

while condition:
    ...
```

---

## 3. Functions

```python
def add(a: int, b: int) -> int:
    return a + b

def greet(name: str = "world") -> str:
    return f"hello {name}"
```

### `*args` / `**kwargs`
```python
def f(*args, **kwargs):
    print(args, kwargs)
```

---

## 4. Data Structures

### List comprehension
```python
nums = [1, 2, 3]
squares = [n * n for n in nums]
```

### Dict / Set
```python
user = {"name": "Bao", "age": 22}
uniq = set([1, 1, 2])  # {1, 2}
```

---

## 5. Modules & Imports

Example structure:
```
my_project/
  main.py
  utils.py
```

```python
# utils.py
def norm(x: float) -> float:
    return abs(x)

# main.py
from utils import norm
print(norm(-3.2))
```

---

## 6. File I/O + JSON + CSV

### Text
```python
from pathlib import Path

Path("out.txt").write_text("hello", encoding="utf-8")
content = Path("out.txt").read_text(encoding="utf-8")
```

### JSON
```python
import json

data = {"a": 1}
json_str = json.dumps(data)
obj = json.loads(json_str)
```

### CSV
```python
import csv

with open("data.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["id", "name"])
    writer.writeheader()
    writer.writerow({"id": 1, "name": "Bao"})
```

---

## 7. Exceptions & Logging

### Exceptions
```python
try:
    x = int("abc")
except ValueError as e:
    print("Bad number:", e)
```

### Logging (recommended)
```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("pipeline started")
```

---

## 8. Type Hints & Dataclasses

### Type hints
```python
from typing import Optional

def find_user(user_id: int) -> Optional[str]:
    ...
```

### Dataclass
```python
from dataclasses import dataclass

@dataclass(frozen=True)
class User:
    id: int
    name: str
```

---

## 9. pandas Essentials (for DE)

### Read / Write
```python
import pandas as pd

df = pd.read_csv("data.csv")
df.to_parquet("data.parquet", index=False)
```

### Transform
```python
df["amount_usd"] = df["amount"] * 1.1
summary = df.groupby("category")["amount"].sum().reset_index()
```

> If your data no longer fits RAM, consider Spark/Trino or Polars (lazy mode).

---

## 10. Database Access (PostgreSQL examples)

### psycopg2 (raw SQL)
```python
import psycopg2

conn = psycopg2.connect("dbname=mydb user=postgres password=secret host=localhost")
cur = conn.cursor()
cur.execute("SELECT 1")
print(cur.fetchone())
cur.close()
conn.close()
```

### SQLAlchemy (common in real projects)
```python
from sqlalchemy import create_engine, text

engine = create_engine("postgresql+psycopg2://postgres:secret@localhost:5432/mydb")
with engine.begin() as conn:
    r = conn.execute(text("SELECT 1")).scalar()
    print(r)
```

---

## 11. Testing (pytest)

```python
def add(a: int, b: int) -> int:
    return a + b

def test_add():
    assert add(1, 2) == 3
```

Run:
```bash
pytest -q
```

---

## 12. What Python Skills Matter Most for Data Engineers?

### Must-have
- Functions + modules + clean code
- File I/O (CSV/JSON/Parquet)
- Logging + exception handling
- SQL + database client usage
- Writing orchestration code (Airflow/Dagster): schedules, config, retries

### Nice-to-have
- Type hints
- pytest
- Async/concurrency basics

---

## 📎 References
- Python Docs: https://docs.python.org/3/
- pandas: https://pandas.pydata.org/docs/
- pytest: https://docs.pytest.org/en/stable/
- requests: https://requests.readthedocs.io/