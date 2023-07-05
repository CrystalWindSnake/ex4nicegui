from pathlib import Path
import shutil

root = Path(".").absolute()
target = root / "ex4nicegui"

for t in target.rglob("__pycache__"):
    shutil.rmtree(t)
