from typing import Iterator

from shared.utils import fetch_input


def elves(data: list[str]) -> Iterator[list[int]]:
    current = []
    for item in data:
        if not item:
            yield current
            current = []
        else:
            current.append(int(item))


def solve():
    data = fetch_input(day=1)
    totals = [sum(elf_items) for elf_items in elves(data)]
    return max(totals), sum(sorted(totals, reverse=True)[:3])


if __name__ == "__main__":
    print(solve())
