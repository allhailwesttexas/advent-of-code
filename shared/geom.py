from __future__ import annotations

from dataclasses import dataclass
from typing import Iterator


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def __add__(self, other: Point) -> Point:
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Point) -> Point:
        return Point(self.x - other.x, self.y - other.y)

    def __eq__(self, other: Point) -> bool:
        return self.x == other.x and self.y == other.y

    def manhattan(self, other: Point) -> int:
        return abs(self.x - other.x) + abs(self.y - other.y)

    def points_at_distance(self, d: int) -> Iterator[Point]:
        for v in [Point(0, d), Point(0, -d), Point(d, 0), Point(-d, 0)]:
            yield self + v

    def nearby_points(self, other: Point) -> Iterator[Point]:
        for distance in range(1, self.manhattan(other)):
            yield from self.points_at_distance(distance)


@dataclass
class PointCollection:
    points: list[Point]

    def bbox(self) -> tuple[Point, Point]:
        xs = [p.x for p in self.points]
        ys = [p.y for p in self.points]
        return Point(min(xs), min(ys)), Point(max(xs), max(ys))


class Grid:
    def __init__(self, lines: list[list[str]], offset: Point = Point(0, 0)):
        self.lines = lines

    def __contains__(self, p: Point):
        return not (p.x < 0 or p.y < 0 or p.x >= len(self.lines[0]) or p.y >= len(self.lines))

    def __getitem__(self, p: Point | int):
        if isinstance(p, Point):
            return self.lines[p.y][p.x]
        return self.lines[p]

    def __setitem__(self, p: Point, value: str):
        self.lines[p.y][p.x] = value

    def __str__(self):
        lines = ['    ' + ''.join(map(str, range(len(self.lines[0]))))] + \
            [f"{i:<4d}" + ''.join(row) for i, row in enumerate(self.lines)]
        return '\n'.join(lines) + '\n'

    @classmethod
    def from_bbox_points(cls, pmin: Point, pmax: Point):
        line = ['.' for _ in range(pmax.x - pmin.x + 1)]
        lines = [list(line) for _ in range(pmax.y - pmin.y + 1)]
        return cls(lines, offset=pmin)

    def add_char_at(self, char: str, point: Point):
        self[point] = char
