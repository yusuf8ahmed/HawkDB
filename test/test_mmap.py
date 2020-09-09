import mmap
import json
import pathlib

filepath = pathlib.Path("Users.json").resolve()

print(filepath)

fileo = open(filepath, "r+")
file = mmap.mmap(fileo.fileno(), length=0, access=mmap.ACCESS_WRITE)

file.write(b"hello")
file.flush()
