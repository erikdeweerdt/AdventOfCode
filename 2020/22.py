from typing import List

# region data
TEST_PLAYER1 = [9, 2, 6, 3, 1]
TEST_PLAYER2 = [5, 8, 4, 7, 10]
PLAYER1 = [38, 1, 28, 32, 43, 21, 42, 29, 18, 13, 39, 41,
           49, 31, 19, 26, 27, 40, 35, 14, 3, 36, 12, 16, 45]
PLAYER2 = [34, 15, 47, 20, 23, 2, 11, 9, 8, 7, 25, 50,
           48, 24, 46, 44, 10, 6, 22, 5, 33, 30, 4, 17, 37]
# endregion


def score(player: List[int]) -> int:
    return sum(i * player[-i] for i in range(1, len(player) + 1))


def part1(player1: List[int], player2: List[int]):
    while player1 and player2:
        p1 = player1.pop(0)
        p2 = player2.pop(0)
        if p1 > p2:
            player1.append(p1)
            player1.append(p2)
        else:
            player2.append(p2)
            player2.append(p1)
    print(score(player1) if player1 else score(player2))


if __name__ == "__main__":
    part1(PLAYER1, PLAYER2)
