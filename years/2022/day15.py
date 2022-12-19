import itertools
import re
from dataclasses import dataclass

from shared.geom import Point
from shared.utils import fetch_input

SENSOR_RE = re.compile(r"x=(.+),.*?y=(.+):.*?x=(.+),.*?y=(.+)$")


@dataclass
class Sensor:
    location: Point
    beacon: Point

    def distance(self):
        return self.location.manhattan(self.beacon)


def parse_row(row: str) -> Sensor:
    m = list(map(int, *re.findall(SENSOR_RE, row)))
    return Sensor(Point(m[0], m[1]), Point(m[2], m[3]))


def compute_at_row(sensors: list[Sensor], yt: int) -> int:
    intervals = []
    for s in sensors:
        dx = s.distance() - abs(s.location.y - yt)
        if dx <= 0:
            continue
        intervals.append((s.location.x - dx, s.location.x + dx))

    # Overlap
    allowed_x = {s.beacon.x for s in sensors if s.beacon.y == yt}

    # Start and end intervals
    min_x = min([i[0] for i in intervals])
    max_x = max([i[1] for i in intervals])

    count = 0
    for x in range(min_x, max_x + 1):
        if x in allowed_x:
            continue

        for left, right in intervals:
            if left <= x <= right:
                count += 1
                break
    return count


def find_missing_beacon(sensors: list[Sensor]):
    # use the "one weird trick" of shifting the equation up/down/left/right
    # when there's a single location not covered by sensors
    pos_lines = []
    neg_lines = []
    for s in sensors:
        d = s.distance()
        neg_lines.extend([s.location.x + s.location.y - d, s.location.x + s.location.y + d])
        pos_lines.extend([s.location.x - s.location.y - d, s.location.x - s.location.y + d])

    pos = neg = None
    for p1, p2 in itertools.permutations(pos_lines, 2):
        if abs(p1 - p2) == 2:
            # if diff is 2, the beacon can be in between
            pos = min(p1, p2) + 1

    for p1, p2 in itertools.permutations(neg_lines, 2):
        if abs(p1 - p2) == 2:
            # if diff is 2, the beacon can be in between
            neg = min(p1, p2) + 1

    # x - y = pos
    # x + y = neg
    x, y = (pos + neg) // 2, (neg - pos) // 2
    return x * 4_000_000 + y


def test():
    rows = [
        "Sensor at x=2, y=18: closest beacon is at x=-2, y=15",
        "Sensor at x=9, y=16: closest beacon is at x=10, y=16",
        "Sensor at x=13, y=2: closest beacon is at x=15, y=3",
        "Sensor at x=12, y=14: closest beacon is at x=10, y=16",
        "Sensor at x=10, y=20: closest beacon is at x=10, y=16",
        "Sensor at x=14, y=17: closest beacon is at x=10, y=16",
        "Sensor at x=8, y=7: closest beacon is at x=2, y=10",
        "Sensor at x=2, y=0: closest beacon is at x=2, y=10",
        "Sensor at x=0, y=11: closest beacon is at x=2, y=10",
        "Sensor at x=20, y=14: closest beacon is at x=25, y=17",
        "Sensor at x=17, y=20: closest beacon is at x=21, y=22",
        "Sensor at x=16, y=7: closest beacon is at x=15, y=3",
        "Sensor at x=14, y=3: closest beacon is at x=15, y=3",
        "Sensor at x=20, y=1: closest beacon is at x=15, y=3",
    ]
    sensors = [parse_row(row) for row in rows]
    ans = compute_at_row(sensors, 10)
    assert ans == 26


def solve() -> None:
    data = fetch_input(day=15)
    sensors = [parse_row(row) for row in data]
    yt = 2_000_000
    count = compute_at_row(sensors, yt)
    print("Part 1:", count)
    print("Part 2:", find_missing_beacon(sensors))


if __name__ == "__main__":
    solve()
