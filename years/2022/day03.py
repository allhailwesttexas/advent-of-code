import string
from typing import Iterable

from shared.utils import fetch_input

PRIORITY = dict(zip(string.ascii_lowercase + string.ascii_uppercase, range(1, 53)))


def get_contents(row: str) -> tuple[str, str]:
    return row[:len(row)//2], row[len(row)//2:]


def get_common(*strs) -> str:
    sets = [set(s) for s in strs]
    intersection = sets[0].intersection(*sets[1:])
    return list(intersection)[0]


def row_to_score(row: str) -> int:
    a, b = get_contents(row)
    common = get_common(a, b)
    return PRIORITY[common]


def group_to_score(group: list[str]) -> int:
    common = get_common(*group)
    return PRIORITY[common]


def chunks(data: list, chunksize: int) -> Iterable[list]:
    for i in range(0, len(data), chunksize):
        yield data[i:i+chunksize]


def solve() -> tuple[int, int]:
    data = fetch_input(day=3)
    first_score = sum(row_to_score(row) for row in data)

    groups = list(chunks(data, 3))
    second_score = sum(group_to_score(group) for group in groups)
    return first_score, second_score


def test():
    ss = [
        "vJrwpWtwJgWrhcsFMMfFFhFp",
        "jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL",
        "PmmdzqPrVvPwwTWBwg" "wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn",
        "ttgJtRGJQctTZtZT",
        "CrZsJsPPZsGzwwsLwLmpwMDw",
    ]
    for s in ss:
        a, b = get_contents(s)
        assert a + b == s
    s = ss[0]
    a, b = s[:len(s)//2], s[len(s)//2:]
    assert a == "vJrwpWtwJgWr"
    assert b == "hcsFMMfFFhFp"


if __name__ == "__main__":
    print(solve())
