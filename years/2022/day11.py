from functools import partial
from math import lcm
from operator import mul, add, mod
from typing import Callable, Iterator

from shared.utils import fetch_input, chunks


class Monkey:
    def __init__(
            self,
            items: list[int],
            inspecter: Callable[[int], int],
            divisible_by: int,
            targets: tuple[int, int],
            worry_func: Callable[[int], int] = lambda x: x,
    ):
        self.items = items
        self.inspecter = inspecter
        self.divisible_by = divisible_by
        self.targets = targets
        self.worry_func = worry_func
        self.inspections = 0

    def take_turn(self) -> list[tuple[int, int]]:
        to_throw: list[tuple[int, int]] = []
        for item in self.items:
            item = self.inspecter(item)
            item = self.worry_func(item)
            target = self.targets[item % self.divisible_by != 0]
            to_throw.append((item, target))
            self.inspections += 1
        self.items = []
        return to_throw

    def receive(self, item: int) -> None:
        self.items.append(item)

    @classmethod
    def from_raw_data(cls, raw: list[str]) -> "Monkey":
        items = [int(it) for it in raw[1].replace("Starting items: ", "").split(',')]
        inspecter = raw[2].split('= ')[1]
        tester_val = raw[3].replace("Test: divisible by ", "")
        targets = (
            int(raw[4].replace("If true: throw to monkey ", "")),
            int(raw[5].replace("If false: throw to monkey ", "")),
        )
        divisible_by = int(tester_val)
        inspecter = cls.get_inspecter(inspecter)
        return Monkey(items, inspecter, divisible_by, targets)

    @classmethod
    def get_inspecter(cls, parsed: str) -> Callable[[int], int]:
        if parsed == "old * old":
            return lambda x: x*x
        value = int(parsed.split()[-1])
        func = add if '+' in parsed else mul
        inspecter = partial(func, value)
        return inspecter


class Game:
    def __init__(self, monkeys: list[Monkey]):
        self.round = 0
        self.monkeys = monkeys

    def play_round(self) -> None:
        for monkey in self.monkeys:
            for item, target in monkey.take_turn():
                self.monkeys[target].receive(item)
        self.round += 1

    def play_rounds(self, count: int) -> None:
        for i in range(count):
            self.play_round()

    def print_state(self) -> None:
        for i, monkey in enumerate(self.monkeys):
            print(f"Monkey {i}: " + ', '.join(map(str, monkey.items)))
        print()

    def get_monkey_business_level(self) -> int:
        m1, m2 = sorted(self.monkeys, key=lambda m: m.inspections, reverse=True)[:2]
        return m1.inspections * m2.inspections


def test():
    monkeys = [
        Monkey(items=[79, 98], inspecter=partial(mul, 19), divisible_by=23, targets=(2, 3)),
        Monkey(items=[54, 65, 75, 74], inspecter=partial(add, 6), divisible_by=19, targets=(2, 0)),
        Monkey(items=[79, 60, 97], inspecter=lambda x: x*x, divisible_by=13, targets=(1, 3)),
        Monkey(items=[74], inspecter=partial(add, 3), divisible_by=17, targets=(0, 1)),
    ]
    for monkey in monkeys:
        monkey.worry_func = lambda x: x // 3
    game = Game(monkeys)
    for _ in range(20):
        game.play_round()
    level = game.get_monkey_business_level()
    assert level == 10605, level


def solve() -> tuple[int, int]:
    test()

    data = fetch_input(day=11)
    monkeys = [Monkey.from_raw_data(raw) for raw in chunks(data, 7)]
    for monkey in monkeys:
        monkey.worry_func = lambda x: x // 3
    game = Game(monkeys)
    game.play_rounds(20)
    first_score = game.get_monkey_business_level()

    monkeys = [Monkey.from_raw_data(raw) for raw in chunks(data, 7)]
    cap = lcm(*[monkey.divisible_by for monkey in monkeys])
    for monkey in monkeys:
        monkey.worry_func = lambda x: x % cap
    game = Game(monkeys)
    game.play_rounds(10000)
    second_score = game.get_monkey_business_level()
    return first_score, second_score


if __name__ == "__main__":
    print(solve())
