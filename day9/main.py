from shared.utils import fetch_input


def tick(head: tuple[int, int], tails: list[tuple[int, int]], visited: set[tuple[int, int]], move: str) -> tuple[tuple[int, int], list[tuple[int, int]]]:
    op, size = move.split()
    for _ in range(int(size)):
        if op == "L":
            head = head[0] - 1, head[1]
        elif op == "R":
            head = head[0] + 1, head[1]
        elif op == "U":
            head = head[0], head[1] - 1
        elif op == "D":
            head = head[0], head[1] + 1
        new_tails = []
        old_tail = head
        for tail in tails:
            new_tail = move_tail(old_tail, tail)
            new_tails.append(new_tail)
            old_tail = new_tail
        visited.add(new_tails[-1])
        tails = new_tails
        # print(f"{move=}")
        # render_map(5, 6, head, tails)
    # print(f"{move=}: {head=}, {tails=}")
    # print(f"{visited=}")
    return head, tails


def render_map(rows, cols, head, tails):
    print("== State ==")
    print()
    row = list('.'*cols)
    the_map = [list(row) for _ in range(rows)]
    for i, tail in enumerate(reversed(tails), start=1):
        the_map[tail[1]][tail[0]] = str(len(tails) - i + 1)
    the_map[head[1]][head[0]] = "H"
    print('  ' + ''.join(map(str, range(cols))))
    print()
    for i, row in enumerate(the_map):
        print(str(i) + ' ' + ''.join(row))
    print()


def move_tail(head: tuple[int, int], tail: tuple[int, int]) -> tuple[int, int]:
    dx = head[0] - tail[0]
    dy = head[1] - tail[1]

    if touching(head, tail):
        return tail
    elif two_steps_away_x(head, tail):
        return tail[0] + dx - (1 if dx > 0 else -1), tail[1]
    elif two_steps_away_y(head, tail):
        return tail[0], tail[1] + dy - (1 if dy > 0 else -1)

    # diagonal move
    new_x = tail[0] + (1 if dx > 0 else -1)
    new_y = tail[1] + (1 if dy > 0 else -1)
    return new_x, new_y


def two_steps_away_x(head, tail) -> bool:
    dx = head[0] - tail[0]
    dy = head[1] - tail[1]
    return abs(dx) == 2 and not dy


def two_steps_away_y(head, tail) -> bool:
    dx = head[0] - tail[0]
    dy = head[1] - tail[1]
    return abs(dy) == 2 and not dx


def touching(head, tail) -> bool:
    dx = head[0] - tail[0]
    dy = head[1] - tail[1]
    return any(
        [
            head == tail,
            not dx and abs(dy) == 1,
            not dy and abs(dx) == 1,
            abs(dy) == 1 and abs(dx) == 1,
        ]
    )


def test():
    head = (0, 0)
    tails = [(0, 0)]
    visited = set()
    for move in ['R 4', 'U 4', 'L 3', 'D 1', 'R 4', 'D 1', 'L 5', 'R 2']:
        head, tails = tick(head, tails, visited, move)
    assert len(visited) == 13, len(visited)

    head = (0, 4)
    tails = [(0, 4) for _ in range(9)]
    visited = set()
    for move in ['R 4', 'U 4', 'L 3', 'D 1', 'R 4', 'D 1', 'L 5', 'R 2']:
        head, tails = tick(head, tails, visited, move)
    assert len(visited) == 1

    head = (11, 15)
    tails = [(11, 15) for _ in range(9)]
    visited = set()
    for move in ['R 5', 'U 8', 'L 8', 'D 3', 'R 17', 'D 10', 'L 25', 'U 20']:
        head, tails = tick(head, tails, visited, move)
    assert len(visited) == 36, len(visited)


def solve() -> tuple[int, int]:
    test()
    data = fetch_input(day=9)
    head = (0, 0)
    tails = [(0, 0)]
    visited = set()
    for move in data:
        head, tails = tick(head, tails, visited, move)
    first_score = len(visited)

    head = (0, 0)
    tails = [(0, 0) for _ in range(9)]
    v2 = set()
    for move in data:
        head, tails = tick(head, tails, v2, move)
    second_score = len(v2)
    return first_score, second_score


if __name__ == "__main__":
    print(solve())
