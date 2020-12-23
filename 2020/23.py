import sys
from typing import List

TESTDATA = [3, 8, 9, 1, 2, 5, 4, 6, 7]
DATA = [9, 7, 4, 6, 1, 8, 3, 5, 2]


class Cup:
    value: int
    prv: "Cup"
    nxt: "Cup"

    def __init__(self, value: int):
        self.value = value

    def __str__(self):
        return f"{self.prv.value if self.prv else None} << {self.value} >> {self.nxt.value if self.nxt else None}"

    def __repr__(self):
        return self.__str__()


def play_round(cups: List[int]) -> List[int]:
    """
    Naive approach that maintains a list in cup order.
    This works for part 1, but is way too slow for part 2.
    """
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


def play_round_2(cups: List[Cup], head: Cup, max_value: int) -> Cup:
    """
    Play a round of the game on a doubly linked list of cups.
    """
    removed = [head.nxt, head.nxt.nxt, head.nxt.nxt.nxt]
    dest_value = head.value - 1 if head.value > 1 else max_value
    dest_cup = cups[dest_value]
    while dest_cup in removed:
        dest_value = dest_value - 1 if dest_value > 1 else max_value
        dest_cup = cups[dest_value]
    # change links
    removed[-1].nxt.prv = head
    head.nxt = removed[-1].nxt
    dest_cup.nxt.prv = removed[-1]
    removed[-1].nxt = dest_cup.nxt
    dest_cup.nxt = removed[0]
    removed[0].prv = dest_cup
    # new head is the next cup
    return head.nxt


def part1(data: List[int]):
    cups = data[:]
    # print(cups)
    for _ in range(100):
        cups = play_round(cups)
        # print(cups)
    index = cups.index(1)
    print("".join(str(cup) for cup in cups[index+1:]+cups[:index]))


def part2(data: List[int], list_size=1000000, iterations=10000000):
    cup_max = len(data)  # all numbers are used, so max == len
    # first build the initial list
    cups = [None] + [Cup(cup) for cup in range(1, cup_max + 1)]
    head = cups[data[0]]
    tail = cups[data[-1]]
    for cup in cups:
        if cup:
            index = data.index(cup.value)
            cup.prv = cups[data[index - 1 if index > 0 else -1]
                           ] if cup is not head else tail
            cup.nxt = cups[data[index + 1 if index < cup_max -
                                1 else 0]] if cup is not tail else head
    # extend the list up to the specified size
    # takes a second or two for 1000000 entries
    # some links are overwritten on the next iteration, but kept for correctness
    for i in range(cup_max + 1, list_size + 1):
        cup = Cup(i)
        cup.prv = tail
        cup.nxt = head
        tail.nxt = cup
        head.prv = cup
        tail = cup
        cups.append(cup)
    # play the game
    for i in range(iterations):
        head = play_round_2(cups, head, list_size)
    # print result
    print(cups[1].nxt.value * cups[1].nxt.nxt.value)


if __name__ == "__main__":
    # part1(DATA)
    part2(DATA)
