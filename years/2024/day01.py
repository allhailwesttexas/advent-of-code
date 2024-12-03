from collections import Counter

from shared.utils import fetch_input


def solve() -> tuple[int, int]:
    data = fetch_input(year=2024, day=1)
    pairs = [map(int, line.split()) for line in data]
    cols = list(zip(*pairs))
    first_score = sum(abs(v1 - v2) for v1, v2 in zip(sorted(cols[0]), sorted(cols[1])))

    counter = Counter(cols[1])
    second_score = sum(v1 * counter[v1] for v1 in cols[0])

    return first_score, second_score


if __name__ == "__main__":
    print(solve())
