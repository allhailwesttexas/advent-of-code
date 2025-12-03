from shared.utils import fetch_input, chunks


def parse_input(data: str) -> list[tuple[int, int]]:
    raw_ids = data.split(",")
    raw_pairs = [row.split("-") for row in raw_ids]
    return [(int(start), int(end)) for start, end in raw_pairs]


def sum_all_invalid_ids(pairs: list[tuple[int, int]]) -> int:
    running_total = 0
    for start, end in pairs:
        count, total = count_invalid(start, end)
        running_total += total
    return running_total


def count_invalid(start: int, end: int) -> tuple[int, int]:
    count = 0
    total = 0
    for n in range(start, end + 1):
        s = str(n)
        if is_repeated(s):
            count += 1
            total += n
    return count, total


def sum_all_invalid_ids_part2(pairs: list[tuple[int, int]]) -> int:
    running_total = 0
    for start, end in pairs:
        count, total = count_invalid_part2(start, end)
        running_total += total
    return running_total


def count_invalid_part2(start: int, end: int) -> tuple[int, int]:
    count = 0
    total = 0
    for n in range(start, end + 1):
        s = str(n)
        if is_only_repeated(s):
            count += 1
            total += n
    return count, total


def is_repeated(s: str) -> bool:
    size = len(s)
    if size % 2 != 0:
        return False
    start, end = s[:size // 2], s[size // 2:]
    return start == end


def is_only_repeated(s: str) -> bool:
    """Now, an ID is invalid if it is made only of some sequence of digits repeated at least twice."""
    size = len(s)
    for width in range(1, size // 2 + 1):
        parts = set(chunks(s, width))
        if len(parts) == 1:
            return True  # if the set only has one item in it, the number fulfils the criteria
    return False


def solve() -> tuple[int, int]:
    data = fetch_input(year=2025, day=2)
    pairs = parse_input(data[0])
    total = sum_all_invalid_ids(pairs)
    first_score = total
    total_part2 = sum_all_invalid_ids_part2(pairs)
    second_score = total_part2

    return first_score, second_score

def test() -> None:
    data = (
        "11-22,95-115,998-1012,1188511880-1188511890,222220-222224,"
        "1698522-1698528,446443-446449,38593856-38593862,565653-565659,"
        "824824821-824824827,2121212118-2121212124"
    )
    ids = parse_input(data)
    total = sum_all_invalid_ids(ids)
    assert total == 1227775554, total

    total_part2 = sum_all_invalid_ids_part2(ids)
    assert total_part2 == 4174379265, total_part2


if __name__ == "__main__":
    test()
    print(solve())
