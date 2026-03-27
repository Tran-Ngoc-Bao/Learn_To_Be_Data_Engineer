import os
import sys
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DAGSTER_HOME = ROOT / "dagster_home"

def main():
    os.environ["DAGSTER_HOME"] = str(DAGSTER_HOME)
    os.chdir(ROOT)

    cmd = [
        sys.executable, "-m", "dagster_webserver",
        "-h", "127.0.0.1", "-p", "3000",
        "-w", str(ROOT / "workspace.yaml"),
    ]
    subprocess.run(cmd, check=True)

if __name__ == "__main__":
    main()