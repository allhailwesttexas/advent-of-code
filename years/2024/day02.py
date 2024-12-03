import itertools

from shared.utils import fetch_input


def is_safe(report: list[int]) -> bool:
    has_duplicates = len(set(report)) < len(report)
    if has_duplicates:
        return False
    is_monotonic = report == sorted(report) or report == sorted(report, reverse=True)
    if not is_monotonic:
        return False
    for p1, p2 in itertools.pairwise(report):
        if abs(p1 - p2) > 3:
            return False
    return True


def is_safe_dampened(report: list[int]) -> bool:
    for i in range(len(report)):
        new_report = list(report)
        new_report.pop(i)
        if is_safe(new_report):
            return True
    return False


def solve() -> tuple[int, int]:
    data = fetch_input(year=2024, day=2)
    reports = [list(map(int, row.split())) for row in data]
    first_score = sum(1 for report in reports if is_safe(report))
    second_score = sum(1 for report in reports if is_safe_dampened(report))
    return first_score, second_score


def test():
    assert is_safe([14, 16, 19, 22, 24])


if __name__ == "__main__":
    test()
    print(solve())
