from shared.utils import fetch_input


def is_start_of_packet(signal: str):
    return len(set(signal)) == len(signal)


def find_index_after_marker(data: str, size=4):
    for i in range(size, len(data)):
        signal = data[i-size:i]
        if is_start_of_packet(signal):
            return i


def solve() -> tuple[int, int]:
    data = fetch_input(day=6)[0]
    first_score = find_index_after_marker(data, size=4)
    second_score = find_index_after_marker(data, size=14)
    return first_score, second_score


if __name__ == "__main__":
    print(solve())
