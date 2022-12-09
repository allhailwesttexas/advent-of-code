from collections import defaultdict
from typing import cast, Iterator

from shared.utils import fetch_input

Port = dict[int, list[str]]


def build_port(strs: list[str]) -> Port:
    strs = list(reversed(strs))
    d = defaultdict(list)
    for row in strs[1:]:
        for i, item in enumerate(row[1::4], start=1):
            if item != " ":
                d[i].append(item)
    return cast(Port, d)


def moves(raw_moves: list[str]) -> Iterator[tuple[int, int, int]]:
    for move in raw_moves:
        _, count, _, src, _, dest = move.split()
        yield int(count), int(src), int(dest)


def do_move(port: Port, src: int, dest: int, count: int) -> Port:
    for _ in range(count):
        item = port[src].pop()
        port[dest].append(item)
    return port


def do_batch_move(port: Port, src: int, dest: int, count: int) -> Port:
    items = port[src][-count:]
    port[src] = port[src][:-count]
    port[dest].extend(items)
    return port


def split_input(data: list[str]) -> tuple[list[str], list[str]]:
    empty = 0
    for i, row in enumerate(data):
        if not row:
            empty = i
            break
    return data[:empty], data[empty+1:]


def solve() -> tuple[str, str]:
    data = fetch_input(day=5)
    port_layout, raw_moves = split_input(data)
    port = build_port(port_layout)
    for count, src, dest in moves(raw_moves):
        port = do_move(port, src, dest, count)
    first_score = "".join([v[-1] for v in port.values()])

    port = build_port(port_layout)
    for count, src, dest in moves(raw_moves):
        port = do_batch_move(port, src, dest, count)
    second_score = "".join([v[-1] for v in port.values()])
    return first_score, second_score


if __name__ == "__main__":
    print(solve())
