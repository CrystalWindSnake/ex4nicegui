from pathlib import Path
import shutil

root = Path(".").absolute()
targets = ["build", "dist", "ex4nicegui.egg-info"]

for target in targets:
    folder = root / target
    if folder.exists():
        shutil.rmtree(folder)
