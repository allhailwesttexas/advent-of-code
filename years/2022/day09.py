from shared.utils import fetch_input


class Rope:
    def __init__(self, rope_length: int):
        self.head = (0, 0)
        self.tails = [(0, 0) for _ in range(rope_length-1)]
        self.visited = set()

    def move(self, move: str):
        op, steps = move.split()
        for _ in range(int(steps)):
            self.head = self.move_head(op)
            new_tails = []
            old_tail = self.head
            for tail in self.tails:
                new_tail = self.move_tail(old_tail, tail)
                new_tails.append(new_tail)
                old_tail = new_tail
            self.visited.add(new_tails[-1])
            self.tails = new_tails

    def move_head(self, op: str) -> tuple[int, int]:
        if op == "L":
            return self.head[0] - 1, self.head[1]
        elif op == "R":
            return self.head[0] + 1, self.head[1]
        elif op == "U":
            return self.head[0], self.head[1] - 1
        elif op == "D":
            return self.head[0], self.head[1] + 1

    @classmethod
    def move_tail(cls, head: tuple[int, int], tail: tuple[int, int]) -> tuple[int, int]:
        if cls.touching(head, tail):
            return tail

        dx = head[0] - tail[0]
        dy = head[1] - tail[1]
        x_move = y_move = 0

        if abs(dx):
            x_move = 1 if dx > 0 else -1
        if abs(dy):
            y_move = 1 if dy > 0 else -1
        return tail[0] + x_move, tail[1] + y_move

    @classmethod
    def touching(cls, head, tail) -> bool:
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


def test():
    rope = Rope(rope_length=2)
    for move in ['R 4', 'U 4', 'L 3', 'D 1', 'R 4', 'D 1', 'L 5', 'R 2']:
        rope.move(move)
    assert len(rope.visited) == 13

    rope = Rope(rope_length=10)
    for move in ['R 4', 'U 4', 'L 3', 'D 1', 'R 4', 'D 1', 'L 5', 'R 2']:
        rope.move(move)
    assert len(rope.visited) == 1

    rope = Rope(rope_length=10)
    for move in ['R 5', 'U 8', 'L 8', 'D 3', 'R 17', 'D 10', 'L 25', 'U 20']:
        rope.move(move)
    assert len(rope.visited) == 36


def solve() -> tuple[int, int]:
    test()
    data = fetch_input(day=9)

    r2 = Rope(rope_length=2)
    for move in data:
        r2.move(move)

    r10 = Rope(rope_length=10)
    for move in data:
        r10.move(move)
    return len(r2.visited), len(r10.visited)


if __name__ == "__main__":
    print(solve())
