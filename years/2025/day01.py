from operator import add, sub

from shared.utils import fetch_input


def count_occurrences(at: int, start_at: int, rotations: list[tuple[str, int]]) -> int:
    count = 0
    current = start_at
    operator_map = {"L": sub, "R": add}
    for rotation in rotations:
        current = operator_map[rotation[0]](current, rotation[1]) % 100
        if current == at:
            count += 1
    return count


def count_passes(at: int, start_at: int, rotations: list[tuple[str, int]]) -> int:
    count = 0
    current = start_at
    operator_map = {"L": sub, "R": add}
    for direction, ticks in rotations:
        op = operator_map[direction]
        for _ in range(ticks):
            current = op(current, 1) % 100
            if current == at:
                count += 1
    return count


def parse_input(data: list[str]) -> list[tuple[str, int]]:
    return [(r[0], int(r[1:])) for r in data]


def solve() -> tuple[int, int]:
    data = fetch_input(year=2025, day=1)
    rotations = parse_input(data)
    count = count_occurrences(0, 50, rotations)
    first_score = count
    pass_count = count_passes(0, 50, rotations)
    second_score = pass_count

    return first_score, second_score

def test() -> None:
    data = ["L68", "L30", "R48", "L5", "R60", "L55", "L1", "L99", "R14", "L82"]
    rotations = parse_input(data)
    count = count_occurrences(0, 50, rotations)
    assert count == 3, count
    pass_count = count_passes(0, 50, rotations)
    assert pass_count == 6, pass_count


if __name__ == "__main__":
    test()
    print(solve())
