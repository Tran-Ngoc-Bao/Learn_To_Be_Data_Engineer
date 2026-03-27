import os
import sys
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DAGSTER_HOME = ROOT / "dagster_home"

def main():
    os.environ["DAGSTER_HOME"] = str(DAGSTER_HOME)

    # đảm bảo run từ root để import module ổn định
    os.chdir(ROOT)

    # Chọn 1 trong 2 cách sau:

    # (A) Khuyến nghị: chạy theo module (cần src là package: src/__init__.py)
    cmd = [
        sys.executable, "-m", "dagster", "code-server", "start",
        "-m", "src.definitions", "-a", "defs",
        "-h", "127.0.0.1", "-p", "4000",
    ]

    # (B) Nếu bạn chưa package hóa, chạy theo file:
    # cmd = [
    #     sys.executable, "-m", "dagster", "code-server", "start",
    #     "-f", str(ROOT / "src" / "definitions.py"),
    #     "-h", "127.0.0.1", "-p", "4000",
    # ]

    subprocess.run(cmd, check=True)

if __name__ == "__main__":
    main()