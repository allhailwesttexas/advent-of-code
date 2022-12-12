import itertools
from collections import deque
from dataclasses import dataclass

from shared.utils import fetch_input, chunks


@dataclass
class Instruction:
    op: str
    value: int
    duration: int


class CRT:
    def __init__(self):
        self.register = 1
        self.cycles = 0
        self.instructions: deque[Instruction] = deque()
        self.current: Instruction | None = None
        self.history: list[int] = []

    def add_instruction(self, raw_instruction: str):
        if raw_instruction == "noop":
            instruction = Instruction(raw_instruction, 0, 1)
        else:
            op, value = raw_instruction.split()
            instruction = Instruction(op, int(value), 2)
        self.instructions.append(instruction)

    def execute_instruction(self, instruction: Instruction):
        self.register += instruction.value

    def cycle(self):
        self.history.append(self.register)
        self.cycles += 1
        if self.instructions and not self.current:
            self.current = self.instructions.popleft()

        self.current.duration -= 1
        if self.current.duration == 0:
            self.execute_instruction(self.current)
            self.current = None

    def run(self):
        while True:
            self.cycle()
            if not self.instructions and not self.current:
                break

    def get_total_sum(self, inds: list[int]) -> int:
        total = 0
        for i, value in enumerate(self.history, start=1):
            if i in inds:
                total += value * i
        return total

    def render_pixels(self, width: int):
        pixels: list[str] = []
        positions = itertools.cycle(range(width))
        for cycle, value in enumerate(self.history, start=1):
            pixel_center = next(positions)
            pixel = '#' if abs(value - pixel_center) <= 1 else '.'
            pixels.append(pixel)
        prows = list(chunks(pixels, width))
        for row in prows:
            print(''.join(row))


def test():
    instructions = ["noop", "addx 3", "addx -5"]
    crt = CRT()
    for i, instruction in enumerate(instructions):
        crt.add_instruction(instruction)
    crt.run()

    instructions = ["addx 15", "addx -11", "addx 6", "addx -3", "addx 5", "addx -1", "addx -8", "addx 13", "addx 4", "noop", "addx -1", "addx 5", "addx -1", "addx 5", "addx -1", "addx 5", "addx -1", "addx 5", "addx -1", "addx -35", "addx 1", "addx 24", "addx -19", "addx 1", "addx 16", "addx -11", "noop", "noop", "addx 21", "addx -15", "noop", "noop", "addx -3", "addx 9", "addx 1", "addx -3", "addx 8", "addx 1", "addx 5", "noop", "noop", "noop", "noop", "noop", "addx -36", "noop", "addx 1", "addx 7", "noop", "noop", "noop", "addx 2", "addx 6", "noop", "noop", "noop", "noop", "noop", "addx 1", "noop", "noop", "addx 7", "addx 1", "noop", "addx -13", "addx 13", "addx 7", "noop", "addx 1", "addx -33", "noop", "noop", "noop", "addx 2", "noop", "noop", "noop", "addx 8", "noop", "addx -1", "addx 2", "addx 1", "noop", "addx 17", "addx -9", "addx 1", "addx 1", "addx -3", "addx 11", "noop", "noop", "addx 1", "noop", "addx 1", "noop", "noop", "addx -13", "addx -19", "addx 1", "addx 3", "addx 26", "addx -30", "addx 12", "addx -1", "addx 3", "addx 1", "noop", "noop", "noop", "addx -9", "addx 18", "addx 1", "addx 2", "noop", "noop", "addx 9", "noop", "noop", "noop", "addx -1", "addx 2", "addx -37", "addx 1", "addx 3", "noop", "addx 15", "addx -21", "addx 22", "addx -6", "addx 1", "noop", "addx 2", "addx 1", "noop", "addx -10", "noop", "noop", "addx 20", "addx 1", "addx 2", "addx 2", "addx -6", "addx -11", "noop", "noop", "noop"]
    crt = CRT()
    for i, instruction in enumerate(instructions):
        crt.add_instruction(instruction)
    crt.run()
    inds = [20, 60, 100, 140, 180, 220]
    assert crt.get_total_sum(inds) == 13140
    crt.render_pixels(width=40)


def solve():
    test()
    data = fetch_input(day=10)
    crt = CRT()
    for i, instruction in enumerate(data):
        crt.add_instruction(instruction)
    crt.run()
    inds = [20, 60, 100, 140, 180, 220]
    print(crt.get_total_sum(inds))
    crt.render_pixels(40)


if __name__ == "__main__":
    solve()
