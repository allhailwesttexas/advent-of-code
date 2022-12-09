from typing import Sequence

from shared.utils import fetch_input


def row_to_ranges(row) -> tuple[Sequence[int], Sequence[int]]:
    a, b = row.split(",")
    astart, aend = [int(num) for num in a.split("-")]
    bstart, bend = [int(num) for num in b.split("-")]
    return range(astart, aend + 1), range(bstart, bend + 1)


def one_is_subset(a: Sequence[int], b: Sequence[int]) -> bool:
    s1, s2 = set(a), set(b)
    return s1.issubset(s2) or s2.issubset(s1)


def has_common_elements(a: Sequence[int], b: Sequence[int]) -> bool:
    return len(set(a) & set(b)) > 0


def solve() -> tuple[int, int]:
    data = fetch_input(day=4)
    first_score = len([pair for pair in data if one_is_subset(*row_to_ranges(pair))])
    second_score = len(
        [pair for pair in data if has_common_elements(*row_to_ranges(pair))]
    )
    return first_score, second_score


if __name__ == "__main__":
    print(solve())
