from pathlib import Path
path = Path("/here/your/path/file.txt")
print(path.parent / "db.log")