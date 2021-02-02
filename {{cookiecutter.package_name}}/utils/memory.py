#!/usr/bin/env python
"""
-------------------------------------------------------
2021-02-01 -- Christian Foerster
christian.foerster@eawag.ch
-------------------------------------------------------
"""
from pathlib import Path

def delete_memory(workdir, memory_ids):

    for memory_id in memory_ids:
        memory_file = Path(workdir) / f"{memory_id.lower()}.memory"

        if memory_file.exists():
            memory_file.unlink()


def read_memory(workdir, memory_id):
    memory_file = Path(workdir) / f"{memory_id.lower()}.memory"

    if not memory_file.exists():
        memory_file.touch()

    return memory_file.read_text().split("\n")[:-1]


def write_memory(workdir, memory_id, file_list):
    memory_file = Path(workdir) / f"{memory_id.lower()}.memory"

    with memory_file.open("a") as f:
        f.write("\n".join(file_list) + "\n")


