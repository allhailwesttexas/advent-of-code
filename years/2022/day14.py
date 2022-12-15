from dataclasses import dataclass
from itertools import chain
from typing import Iterator

from shared.geom import Grid
from shared.utils import fetch_input


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def __add__(self, other: "Point"):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Point"):
        return Point(self.x - other.x, self.y - other.y)

    def bbox_points(self, other: "Point") -> Iterator["Point"]:
        for x in range(min(self.x, other.x), max(self.x, other.x)+1):
            yield Point(x, self.y)
        for y in range(min(self.y, other.y), max(self.y, other.y)+1):
            yield Point(self.x, y)


class Cave(Grid):
    def __init__(self, paths: list[list[tuple[int, int]]], floor=False):
        xs, ys = list(zip(*[path for path in chain(*paths)]))
        xmin, xmax, ymax = min(xs), max(xs), max(ys)

        if floor:
            xmin -= ymax
            xmax += ymax
            ymax += 2
            paths.append([(xmin, ymax), (xmax, ymax)])
        row = ['.' for _ in range(xmax - xmin + 1)]
        lines = [list(row) for _ in range(ymax + 1)]
        super().__init__(lines)

        self.offset = Point(xmin, 0)
        for path in paths:
            points = [Point(*xy) - self.offset for xy in path]
            self.add_path(points)

    def add_path(self, path: list[Point]):
        for p1, p2 in zip(path, path[1:]):
            for p in p1.bbox_points(p2):
                self[p] = '#'


class SandEvent:
    SAND_SOURCE = Point(500, 0)

    def __init__(self, cave: Cave):
        self.cave = cave
        self.origin = self.SAND_SOURCE - self.cave.offset
        self.sand_point = self.origin
        self.sand_count = 0

    def tick(self) -> str:
        result = self.move_sand()
        if result == "did_not_move":
            self.add_sand()
        return result

    def move_sand(self) -> str:
        for vector in [Point(0, 1), Point(-1, 1), Point(1, 1)]:
            p = self.sand_point + vector
            if p not in self.cave:
                return "entered_the_abyss"
            elif self.cave[p] == '.':
                self.cave[self.sand_point] = '.'
                self.cave[p] = 'o'
                self.sand_point = p
                return "moved"
        if self.sand_point == self.origin:
            self.sand_count += 1
            return "hit_the_top"
        return "did_not_move"

    def run_simulation(self) -> int:
        result = ""
        while result not in {"entered_the_abyss", "hit_the_top"}:
            result = self.tick()
        return self.sand_count

    def add_sand(self) -> None:
        self.cave[self.origin] = 'o'
        self.sand_point = self.origin
        self.sand_count += 1


def test():
    paths = [
        [(498, 4), (498, 6), (496, 6)],
        [(503, 4), (502, 4), (502, 9), (494, 9)]
    ]
    cave = Cave(paths)
    print(cave)
    sand = SandEvent(cave=cave)
    sand_count = sand.run_simulation()
    assert sand_count == 24, sand_count

    cave = Cave(paths, floor=True)
    sand = SandEvent(cave=cave)
    sand_count = sand.run_simulation()
    print(cave)

    assert sand_count == 93, sand_count


def parse_line(line: str):
    pairs = line.split(' -> ')
    return [(int(pair.split(',')[0]), int(pair.split(',')[1])) for pair in pairs]


def solve() -> None:
    test()
    data = fetch_input(day=14)
    paths = [parse_line(line) for line in data]
    cave = Cave(paths)
    sand = SandEvent(cave=cave)
    sand_count = sand.run_simulation()
    print("Part 1:", sand_count)

    cave = Cave(paths, floor=True)
    sand = SandEvent(cave=cave)
    sand_count = sand.run_simulation()
    print(cave)
    print("Part 2:", sand_count)


if __name__ == "__main__":
    solve()
