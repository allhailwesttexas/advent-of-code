import enum

from shared.utils import fetch_input


class Choice(enum.Enum):
    rock = "A"
    paper = "B"
    scissors = "C"


class Outcome(enum.Enum):
    lose = "X"
    draw = "Y"
    win = "Z"


SHAPE_SCORES = {
    Choice.rock: 1,
    Choice.paper: 2,
    Choice.scissors: 3,
}

OUTCOME_SCORES = {
    Outcome.win: 6,
    Outcome.lose: 0,
    Outcome.draw: 3,
}


def get_outcome(opponent: Choice, mine: Choice) -> Outcome:
    if mine == opponent:
        return Outcome.draw
    if any(
        [
            mine == Choice.rock and opponent == Choice.scissors,
            mine == Choice.scissors and opponent == Choice.paper,
            mine == Choice.paper and opponent == Choice.rock,
        ]
    ):
        return Outcome.win
    return Outcome.lose


def row_score(opponent: Choice, mine: Choice) -> int:
    return SHAPE_SCORES[mine] + OUTCOME_SCORES[get_outcome(opponent, mine)]


def second_row_score(opponent: Choice, outcome: Outcome) -> int:
    mine = choose(outcome, opponent)
    return SHAPE_SCORES[mine] + OUTCOME_SCORES[outcome]


def parse_row(row: str) -> tuple[Choice, Choice]:
    data = row.split()
    opponent = Choice(data[0])
    mine = Choice(chr(ord(data[1]) - 23))
    return opponent, mine


def second_parse_row(row: str) -> tuple[Choice, Outcome]:
    data = row.split()
    return Choice(data[0]), Outcome(data[1])


def choose(outcome: Outcome, opponent: Choice) -> Choice:
    if outcome == Outcome.draw:
        return opponent
    elif outcome == Outcome.win:
        if opponent == Choice.rock:
            return Choice.paper
        elif opponent == Choice.paper:
            return Choice.scissors
        return Choice.rock
    elif outcome == Outcome.lose:
        if opponent == Choice.rock:
            return Choice.scissors
        elif opponent == Choice.paper:
            return Choice.rock
        return Choice.paper


def solve() -> tuple[int, int]:
    data = fetch_input(day=2)
    first_score = sum(row_score(*parse_row(row)) for row in data)
    second_score = sum(second_row_score(*second_parse_row(row)) for row in data)
    return first_score, second_score


if __name__ == "__main__":
    print(solve())
