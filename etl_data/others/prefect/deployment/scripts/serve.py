import os
import subprocess
import sys
from pathlib import Path

def main():
    os.environ.setdefault("PREFECT_API_URL", "http://127.0.0.1:4200/api")

    os.environ.setdefault("NO_PROXY", "localhost,127.0.0.1")
    os.environ.setdefault("no_proxy", os.environ["NO_PROXY"])

    os.environ.setdefault("PREFECT_HOME", str((Path(__file__).resolve().parents[1]) / ".prefect"))

    subprocess.run([sys.executable, "-m", "prefect", "server", "start"], check=True)

if __name__ == "__main__":
    main()