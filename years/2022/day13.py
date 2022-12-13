import json
from functools import cmp_to_key
from itertools import zip_longest, chain

from shared.utils import fetch_input, chunks


def compare(lefts: list, rights: list) -> int:
    for left, right in zip_longest(lefts, rights):
        if left == right:
            continue
        if left is None:
            return 1
        elif right is None:
            return -1
        elif isinstance(left, int) and isinstance(right, int):
            return 1 if left < right else -1
        left = [left] if isinstance(left, int) else left
        right = [right] if isinstance(right, int) else right
        is_valid = compare(left, right)
        if is_valid == 0:
            continue
        return is_valid
    return 0


def test():
    examples = [
        ([1, 1, 3, 1, 1], [1, 1, 5, 1, 1], 1),
        ([[1], [2, 3, 4]], [[1], 4], 1),
        ([9], [[8, 7, 6]], -1),
        ([[4, 4], 4, 4], [[4, 4], 4, 4, 4], 1),
        ([7, 7, 7, 7], [7, 7, 7], -1),
        ([], [3], 1),
        ([[[]]], [[]], -1),
        ([1, [2, [3, [4, [5, 6, 7]]]], 8, 9],
         [1, [2, [3, [4, [5, 6, 0]]]], 8, 9],
         -1,
         ),
    ]
    for left, right, expected in examples:
        r = compare(left, right)
        assert r is expected, (left, right, expected)
    total = 0
    for i, (left, right, _) in enumerate(examples, start=1):
        if compare(left, right) == 1:
            total += i
    assert total == 13, total


def solve() -> None:
    test()
    data = fetch_input(day=13) + [""]
    pairs = [(json.loads(left), json.loads(right)) for left, right, _ in chunks(data, 3)]
    total = sum(i for i, pair in enumerate(pairs, start=1) if compare(*pair) == 1)
    print("Part 1:", total)

    packets = list(chain(*pairs)) + [[[2]], [[6]]]
    sorted_packets = sorted(packets, key=cmp_to_key(compare), reverse=True)
    i2 = next(i for i, p in enumerate(sorted_packets, start=1) if p == [[2]])
    i6 = next(i for i, p in enumerate(sorted_packets, start=1) if p == [[6]])
    print("Part 2:", i2 * i6)


if __name__ == "__main__":
    solve()
