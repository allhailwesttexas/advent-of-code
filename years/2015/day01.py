from shared.utils import fetch_input


def get_negative_position(data: str) -> int:
    count = 0
    for i, ch in enumerate(data, start=1):
        count += (1 if ch == '(' else -1)
        if count < 0:
            return i


def solve():
    data = fetch_input(year=2015, day=1)[0]
    floor = sum(1 for item in data if item == '(') - sum(1 for item in data if item == ')')
    position = get_negative_position(data)
    return floor, position


if __name__ == "__main__":
    print(solve())
