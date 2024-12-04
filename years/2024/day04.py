from shared.utils import fetch_input


def is_vertical_match(rows: list[str], s: str, x: int, y: int) -> bool:
    h = len(rows)
    if y < (h - len(s) + 1):
        found = rows[y][x] + "".join([rows[y + dy][x] for dy in range(1, len(s))])
        if found in {s, s[::-1]}:
            return True
    return False


def is_horizontal_match(rows: list[str], s: str, x: int, y: int) -> bool:
    w = len(rows[0])
    if x < (w - len(s) + 1):
        found = rows[y][x : x + len(s)]
        if found in {s, s[::-1]}:
            return True
    return False


def is_diagonal_down_match(rows: list[str], s: str, x: int, y: int) -> bool:
    h = len(rows)
    w = len(rows[0])
    if (y < h - len(s) + 1) and (x < w - len(s) + 1):
        found = rows[y][x] + "".join([rows[y + dd][x + dd] for dd in range(1, len(s))])
        if found in {s, s[::-1]}:
            return True
    return False


def is_diagonal_up_match(rows: list[str], s: str, x: int, y: int) -> bool:
    w = len(rows[0])
    if (y >= len(s) - 1) and (x < w - len(s) + 1):
        found = rows[y][x] + "".join([rows[y - dd][x + dd] for dd in range(1, len(s))])
        if found in {s, s[::-1]}:
            return True
    return False


def count_xmas(rows: list[str]) -> int:
    w = len(rows[0])
    h = len(rows)

    total = 0
    for y in range(h):
        for x in range(w):
            if is_horizontal_match(rows, "XMAS", x, y):
                total += 1
            if is_vertical_match(rows, "XMAS", x, y):
                total += 1
            if is_diagonal_down_match(rows, "XMAS", x, y):
                total += 1
            if is_diagonal_up_match(rows, "XMAS", x, y):
                total += 1
    return total


def count_mases(rows: list[str]) -> int:
    w = len(rows[0])
    h = len(rows)

    total = 0
    for y in range(h):
        for x in range(w):
            if is_diagonal_down_match(rows, "MAS", x, y) and is_diagonal_up_match(rows, "MAS", x, y + 2):
                total += 1
    return total


def solve() -> tuple[int, int]:
    data = fetch_input(year=2024, day=4)

    first_score = count_xmas(data)
    second_score = count_mases(data)

    return first_score, second_score


def test():
    data = [
        "MMMSXXMASM",
        "MSAMXMSMSA",
        "AMXSXMAAMM",
        "MSAMASMSMX",
        "XMASAMXAMM",
        "XXAMMXXAMA",
        "SMSMSASXSS",
        "SAXAMASAAA",
        "MAMMMXMMMM",
        "MXMXAXMASX",
    ]
    result = count_xmas(data)
    assert result == 18, result
    mas_result = count_mases(data)
    assert mas_result == 9, mas_result


if __name__ == "__main__":
    test()
    print(solve())
