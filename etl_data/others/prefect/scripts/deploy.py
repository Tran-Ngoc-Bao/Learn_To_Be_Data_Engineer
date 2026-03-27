import os
import subprocess
import sys

POOL_NAME = "local-process-pool"

def main():
    os.environ.setdefault("PREFECT_API_URL", "http://127.0.0.1:4200/api")
    os.environ.setdefault("NO_PROXY", "localhost,127.0.0.1")
    os.environ.setdefault("no_proxy", os.environ["NO_PROXY"])

    subprocess.run(
        [sys.executable, "-m", "prefect", "work-pool", "create", "--type", "process", POOL_NAME],
        check=False,
    )

    subprocess.run(
        [sys.executable, "-m", "prefect", "deploy", r".\flows\hello_flow.py:hello_flow", "-n", "dev", "-p", POOL_NAME],
        check=True,
    )

if __name__ == "__main__":
    main()