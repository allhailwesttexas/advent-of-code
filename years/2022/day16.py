from __future__ import annotations
from dataclasses import dataclass

from shared.utils import fetch_input


@dataclass
class Valve:
    id: str
    rate: int
    valves: set[str]

    @classmethod
    def from_line(cls, line: str) -> Valve:
        line = line \
                .replace('Valve ', '') \
                .replace(' has flow rate=', '|') \
                .replace('; tunnels lead to valves ', '|') \
                .replace('; tunnel leads to valve ', '|')
        id_, rate, valves = line.split('|')
        valves = set(v.strip() for v in valves.split(','))
        return Valve(id=id_, rate=int(rate), valves=valves)


class ValveNetwork:
    def __init__(self, valves: dict[str, Valve]):
        self.DP: dict[tuple[str, int, frozenset[str], int], int] = {}
        self.valves = valves

    # If I'm at valve <valve> and I've opened the set of valve ids <opened>, and
    # I have <time> minutes left and there are <other_players> other players after
    # me, how many points can I score from this position?
    def score(self, valve: Valve, opened: frozenset[str], time: int, other_players: int):
        if time == 0:
            if other_players > 0:
                return self.score(self.valves["AA"], opened, 26, other_players-1)
            else:
                return 0

        # generate the key and check if we've been here
        key = (valve.id, time, frozenset(opened), other_players)
        if key in self.DP:
            return self.DP[key]

        ans = 0

        # op1: open current valve
        should_open = valve.id not in opened and valve.rate > 0
        if should_open:
            opened |= {valve.id}
            ans = max(ans, (time-1)*valve.rate + self.score(valve, opened, time-1, other_players))

        # op2: take a tunnel
        for dest_valve_id in sorted(valve.valves, key=lambda s: self.valves[s].rate, reverse=True):
            dest_valve = self.valves[dest_valve_id]
            ans = max(ans, self.score(dest_valve, opened, time-1, other_players))
        self.DP[key] = ans
        return ans


def test():
    data = [
        "Valve AA has flow rate=0; tunnels lead to valves DD, II, BB",
        "Valve BB has flow rate=13; tunnels lead to valves CC, AA",
        "Valve CC has flow rate=2; tunnels lead to valves DD, BB",
        "Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE",
        "Valve EE has flow rate=3; tunnels lead to valves FF, DD",
        "Valve FF has flow rate=0; tunnels lead to valves EE, GG",
        "Valve GG has flow rate=0; tunnels lead to valves FF, HH",
        "Valve HH has flow rate=22; tunnel leads to valve GG",
        "Valve II has flow rate=0; tunnels lead to valves AA, JJ",
        "Valve JJ has flow rate=21; tunnel leads to valve II",
    ]
    valves = [Valve.from_line(row) for row in data]
    valves = {v.id: v for v in valves}
    vn = ValveNetwork(valves)
    score = vn.score(valves["AA"], frozenset(), 30, 0)


def solve() -> None:
    test()
    data = fetch_input(day=16)
    valves = [Valve.from_line(row) for row in data]
    valves = {v.id: v for v in valves}
    vn = ValveNetwork(valves)
    score = vn.score(valves["AA"], frozenset(), 30, 0)
    print("Part 1:", score)
    score = vn.score(valves["AA"], frozenset(), 26, 1)
    print("Part 2:", score)


if __name__ == "__main__":
    solve()
