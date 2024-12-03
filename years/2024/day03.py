import itertools
import re

from shared.utils import fetch_input


def solve() -> tuple[int, int]:
    data = fetch_input(year=2024, day=3)

    pattern = r"mul\((\d+),(\d+)\)"
    rows_with_pairs = [re.findall(pattern, row) for row in data]
    first_score = sum(int(p[0]) * int(p[1]) for p in itertools.chain.from_iterable(rows_with_pairs))

    cond_pattern = "mul\((\d+),(\d+)\)|(do\(\))|(don't\(\))"
    cond_rows_with_pairs = [re.findall(cond_pattern, row) for row in data]

    cond_total = 0
    enabled = True
    for row in cond_rows_with_pairs:
        for item in row:
            if item[2] == "do()":
                enabled = True
                continue
            elif item[3] == "don't()":
                enabled = False
                continue
            if enabled:
                cond_total += int(item[0]) * int(item[1])

    second_score = cond_total

    return first_score, second_score


if __name__ == "__main__":
    print(solve())
