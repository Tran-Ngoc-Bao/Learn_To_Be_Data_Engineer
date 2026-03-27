import os
import subprocess
import sys

POOL_NAME = "local-process-pool"

def main():
    os.environ.setdefault("PREFECT_API_URL", "http://127.0.0.1:4200/api")
    os.environ.setdefault("NO_PROXY", "localhost,127.0.0.1")
    os.environ.setdefault("no_proxy", os.environ["NO_PROXY"])

    subprocess.run(
        [sys.executable, "-m", "prefect", "worker", "start", "--pool", POOL_NAME, "--type", "process"],
        check=True,
    )

if __name__ == "__main__":
    main()