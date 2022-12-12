import os
from dataclasses import dataclass
from itertools import zip_longest
from pathlib import Path
from typing import Iterator

from shared.utils import fetch_input


@dataclass
class File:
    name: str
    size: int

    @classmethod
    def from_line(cls, line: str):
        size, name = line.split()
        return cls(name=name, size=int(size))


def split_into_commands_and_responses(lines: list[str]) -> Iterator[tuple[str, str]]:
    command_inds = [i for i, cmd in enumerate(lines) if cmd.startswith("$")]
    for i, inext in zip_longest(command_inds, command_inds[1:]):
        yield lines[i][2:], lines[i+1:inext]


def build_directory_tree(commands: list[tuple[str, str]]) -> dict:
    tree = {}
    cwd = Path("/")
    for command, response in commands:
        if command == "cd /":
            cwd = Path("/")
        elif command == "cd ..":
            cwd = cwd.parent
        elif command.startswith("cd "):
            cwd = cwd / command.split()[1]
        elif command == "ls":
            files = [
                File.from_line(line) for line in response if not line.startswith("dir")
            ]
            folders = [
                cwd / Path(line[4:]) for line in response if line.startswith("dir")
            ]
            tree[cwd] = {
                "files": files,
                "folders": folders,
                "size": sum(f.size for f in files),
            }
    for path, contents in tree.items():
        matching_folders = [p for p in tree if path in p.parents]
        contents["total_size"] = (
            sum(tree[mf]["size"] for mf in matching_folders) + tree[path]["size"]
        )
    return tree


def find_sum_of_folders_smaller_than(tree: dict, threshold: int) -> int:
    return sum(
        contents["total_size"]
        for contents in tree.values()
        if contents["total_size"] <= threshold
    )


def find_smallest_folder_larger_than(tree: dict, threshold: int) -> tuple[Path, int]:
    folders_with_diff = sorted(
        [
            (folder, contents["total_size"])
            for folder, contents in tree.items()
            if contents["total_size"] > threshold
        ],
        key=lambda x: x[1],
    )
    return folders_with_diff[0]


def solve() -> tuple[int, int]:
    data = fetch_input(day=7)
    commands = list(split_into_commands_and_responses(data))
    tree = build_directory_tree(commands)
    first_score = find_sum_of_folders_smaller_than(tree, threshold=100000)

    fs_size, target_free = 70000000, 30000000
    current_free = fs_size - tree[Path("/")]["total_size"]
    threshold = target_free - current_free
    second_score = find_smallest_folder_larger_than(tree, threshold)[1]
    return first_score, second_score


if __name__ == "__main__":
    print(solve())
