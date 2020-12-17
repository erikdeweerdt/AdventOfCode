import itertools


def play_game(starting_numbers):
    turn = len(starting_numbers)
    numbers = {starting_numbers[index]: index + 1 for index in range(turn - 1)}
    last = starting_numbers[-1]
    while True:
        # print(numbers, last, turn)
        if last in numbers:
            previous = numbers[last]
            numbers[last] = turn
            last = turn - previous
        else:
            numbers[last] = turn
            last = 0
        turn += 1
        yield last


def main(starting_numbers, turn):
    game = play_game(starting_numbers)
    *_, last = itertools.islice(game, turn - len(starting_numbers))
    print(last)


if __name__ == "__main__":
    # part 1
    # main([9, 6, 0, 10, 18, 2, 1], 2020)
    # part 2
    main([9, 6, 0, 10, 18, 2, 1], 30000000)
