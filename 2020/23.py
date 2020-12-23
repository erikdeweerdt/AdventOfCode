from typing import List

TESTDATA = [3, 8, 9, 1, 2, 5, 4, 6, 7]
DATA = [9, 7, 4, 6, 1, 8, 3, 5, 2]


def play_round(cups: List[int]):
    # maintain a list order so that the next cup is always at position 0
    min_value = min(cups)
    dest_value = cups[0] - 1
    dest_index = None
    while dest_index is None:
        if dest_value < min_value:
            dest_value = max(cups)
        try:
            # start searching at index 4; after the selected and picked up cups
            dest_index = cups.index(dest_value, 4)
        except ValueError:
            dest_value -= 1
    return cups[4:dest_index+1] + cups[1:4] + cups[dest_index+1:] + cups[0:1]


def part1(data: List[int]):
    cups = data[:]
    # print(cups)
    for _ in range(100):
        cups = play_round(cups)
        # print(cups)
    index = cups.index(1)
    print("".join(str(cup) for cup in cups[index+1:]+cups[:index]))


if __name__ == "__main__":
    part1(DATA)
