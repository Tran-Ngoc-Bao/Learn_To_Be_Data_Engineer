import os
import subprocess
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
DAGSTER_HOME = ROOT / "dagster_home"

def find_executable(name: str) -> str:
    exe = shutil.which(name)
    if exe:
        return exe

    if os.name == "nt":
        candidate = ROOT / ".venv" / "Scripts" / f"{name}.exe"
    else:
        candidate = ROOT / ".venv" / "bin" / name

    if candidate.exists():
        return str(candidate)

    raise RuntimeError(
        f"Cannot find executable '{name}'. "
        f"Make sure your venv is created at {ROOT / '.venv'} and dependencies are installed."
    )

def main():
    os.environ["DAGSTER_HOME"] = str(DAGSTER_HOME)
    os.chdir(ROOT)

    dagster_daemon = find_executable("dagster-daemon")
    subprocess.run([dagster_daemon, "run"], check=True)

if __name__ == "__main__":
    main()