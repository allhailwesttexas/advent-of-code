from typing import Iterable

from shared.utils import fetch_input


def is_visible(trees: list[str], x: int, y: int) -> bool:
    left = trees[y][:x]
    right = trees[y][x+1:]
    above = "".join(row[x] for row in trees[:y])
    below = "".join(row[x] for row in trees[y+1:])
    for direction in [above, below, left, right]:
        if max(direction) < trees[y][x]:
            return True
    return False


def count_visible_trees(trees: list[str]) -> int:
    count = 0
    for y, tree_row in enumerate(trees[1:-1], start=1):
        for x, tree in enumerate(tree_row[1:-1], start=1):
            if is_visible(trees, x, y):
                count += 1
    return count + 2 * len(trees) + 2 * len(trees[0]) - 4


def highest_scenic_score(trees: list[str]) -> int:
    highest = 0
    for y, tree_row in enumerate(trees):
        for x, tree in enumerate(tree_row):
            score = scenic_score(trees, x, y)
            highest = max(highest, score)
    return highest


def scenic_score(trees: list[str], x: int, y: int) -> int:
    location = trees[y][x]
    left = trees[y][:x]
    right = trees[y][x+1:]
    above = "".join(row[x] for row in trees[:y])
    below = "".join(row[x] for row in trees[y+1:])
    return (
        score_direction(location, reversed(left))
        * score_direction(location, right)
        * score_direction(location, reversed(above))
        * score_direction(location, below)
    )


def score_direction(location: str, direction: Iterable[str]) -> int:
    score = 0
    for tree in direction:
        score += 1
        if tree >= location:
            break
    return score


def solve() -> tuple[int, int]:
    trees = fetch_input(day=8)
    first_score = count_visible_trees(trees)
    second_score = highest_scenic_score(trees)
    return first_score, second_score


if __name__ == "__main__":
    print(solve())
