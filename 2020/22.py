from typing import List, Optional, Tuple

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


def hand_id(player: List[int]) -> int:
    # using calculated id's is more efficient than storing and comparing lists
    # all cards are lower than 64 (2**6)
    hid = 0
    for card in player:
        hid = (hid << 6) | card
    return hid


def play_game(player1: List[int], player2: List[int], recurse: bool = False, game: int = 1) -> Tuple[int, List[int]]:
    history = set()
    # print()
    # print(f"=== Game {game} ===")
    rnd = 1
    while player1 and player2:
        # print()
        # print(f"-- Round {rnd} (game {game}) --")
        # print(f"Player 1's deck: {player1}")
        # print(f"Player 2's deck: {player2}")
        # infinite loop protection
        # to clarify: the same state must have occurred previously, i.e. that of _both_ player's hands
        hid1 = hand_id(player1)
        hid2 = hand_id(player2)
        if (hid1, hid2) in history:
            # print("Loop detected, awarding game to player 1")
            return 1, player1
        history.add((hid1, hid2))
        # play round
        p1 = player1.pop(0)
        p2 = player2.pop(0)
        # print(f"Player 1 plays: {p1}")
        # print(f"Player 2 plays: {p2}")
        if recurse and p1 <= len(player1) and p2 <= len(player2):
            # print("Playing sub-game")
            winner, _ = play_game(player1[:p1], player2[:p2], True, game + 1)
            # print()
            # print(f"... anyway, back to game {game}")
        else:
            winner = 1 if p1 > p2 else 2
        # the cards are awarded to the winner with their card on top
        # print(f"Player {winner} wins round {rnd} of game {game}")
        if winner == 1:
            player1.append(p1)
            player1.append(p2)
        else:
            player2.append(p2)
            player2.append(p1)
        rnd += 1
    if player1:
        # print(f"Player 1 wins game {game}")
        return 1, player1
    # print(f"Player 2 wins game {game}")
    return 2, player2


def part1(player1: List[int], player2: List[int]):
    _, hand = play_game(player1[:], player2[:])
    print(score(hand))


def part2(player1: List[int], player2: List[int]):
    _, hand = play_game(player1[:], player2[:], True)
    print(score(hand))


if __name__ == "__main__":
    # part1(PLAYER1, PLAYER2)
    part2(PLAYER1, PLAYER2)
    # print(hand_id(PLAYER1))
