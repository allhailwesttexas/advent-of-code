from collections import deque
from dataclasses import dataclass
from itertools import chain
from typing import Iterator

from shared.utils import fetch_input


@dataclass(frozen=True)
class Point:
    x: int
    y: int


class Grid:
    def __init__(self, lines: list[str]):
        self.lines = lines
        self.start = self.location_of("S")
        self.goal = self.location_of("E")
        self.lines[self.start.y] = self.lines[self.start.y].replace("S", "a")
        self.lines[self.goal.y] = self.lines[self.goal.y].replace("E", "z")

    def location_of(self, loc: str) -> Point:
        for y, line in enumerate(self.lines):
            if (x := line.find(loc)) != -1:
                return Point(x, y)

    def char_at(self, point: Point) -> str:
        return self.lines[point.y][point.x]

    def height_at(self, point: Point) -> int:
        return ord(self.char_at(point))

    def find_starting_points(self, char: str) -> Iterator[Point]:
        for y, line in enumerate(self.lines):
            yield from (Point(x, y) for x, ch in enumerate(line) if ch == char)

    def __contains__(self, p: Point):
        return not (p.x < 0 or p.y < 0 or p.x >= len(self.lines[0]) or p.y >= len(self.lines))


class Journey:
    def __init__(self, grid: Grid, start: Point, goal: Point):
        self.grid = grid
        self.start = start
        self.goal = goal
        self.visited = set()

    @staticmethod
    def adjacent(p: Point) -> tuple[Point, Point, Point, Point]:
        return Point(p.x, p.y-1), Point(p.x, p.y+1), Point(p.x-1, p.y), Point(p.x+1, p.y)

    def possible_moves(self, point: Point) -> Iterator[Point]:
        return [p for p in self.adjacent(point) if self.is_allowed(current=point, target=p)]

    def is_allowed(self, current: Point, target: Point) -> bool:
        if target in self.visited or target not in self.grid:
            return False
        return self.grid.height_at(target) - self.grid.height_at(current) <= 1

    def find_shortest_path(self) -> int:
        steps = 0
        to_explore = deque([[self.start]])

        while to_explore:
            step_locations = to_explore.popleft()
            if self.goal in step_locations:
                return steps
            neighbours = list(chain.from_iterable(self.explore_neighbours(p) for p in step_locations))
            if neighbours:
                to_explore.append(neighbours)
            steps += 1
        return -1

    def explore_neighbours(self, point: Point) -> Iterator[Point]:
        for p in self.possible_moves(point):
            self.visited.add(p)
            yield p


def test():
    data = [
        "Sabqponm",
        "abcryxxl",
        "accszExk",
        "acctuvwj",
        "abdefghi",
    ]

    grid = Grid(lines=data)
    j = Journey(grid, grid.start, grid.goal)
    r = j.find_shortest_path()
    assert r == 31, r

    paths = []
    for start in grid.find_starting_points("a"):
        j = Journey(grid, start, grid.goal)
        paths.append(j.find_shortest_path())
    assert min(paths) == 29


def solve() -> None:
    test()
    data = fetch_input(day=12)
    grid = Grid(lines=data)
    j = Journey(grid, grid.start, grid.goal)
    print("Part 1:", j.find_shortest_path())

    paths = []
    for start in grid.find_starting_points("a"):
        j = Journey(grid, start, grid.goal)
        path = j.find_shortest_path()
        if path > -1:
            paths.append(path)
    print("Part 2:", min(paths))


if __name__ == "__main__":
    solve()
