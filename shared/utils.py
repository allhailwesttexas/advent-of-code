import os
from pathlib import Path
from typing import Iterable

import requests


def find_repo_folder() -> Path | None:
    cwd = Path.cwd()
    for parent in [cwd] + list(cwd.parents):
        if "advent-of-code" in parent.name:
            return parent


ADVENT_URL = "https://adventofcode.com"
REPO_FOLDER = find_repo_folder()
CACHE_FOLDER = REPO_FOLDER / Path(".aoc_cache")


def fetch_input(*, year=2022, day, session=None, use_cache=True):
    folder = CACHE_FOLDER / Path(f"{year}")
    folder.mkdir(exist_ok=True)
    fpath = folder / Path(f"input{day}.txt")
    if fpath.exists() and use_cache:
        with open(fpath, "r") as fi:
            return [line.rstrip() for line in fi]
    cookies = {"session": session or os.getenv("AOC_SESSION")}

    r = requests.get(f"{ADVENT_URL}/{year}/day/{day}/input", cookies=cookies)

    if not r.text.startswith("Puzzle inputs vary by user"):
        with open(fpath.absolute(), "w") as fo:
            fo.writelines(r.text)

    return r.text.splitlines()


def chunks(data: list, chunksize: int) -> Iterable[list]:
    for i in range(0, len(data), chunksize):
        yield data[i:i+chunksize]
