from io import StringIO


def find_marker(input, length):
    for i in range(len(input) - length):
        if len(set(input[i:i+length])) == length:
            return i + length


def part1():
    # data = read('bvwbjplbgvbhsrlpgdmjqwftvncz')
    # data = read('nppdvjthqldpwncqszvftbrmjlhg')
    # data = read('nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg')
    # data = read('zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw')
    print(find_marker(read(), 4))


def part2():
    print(find_marker(read(), 14))


def read(data=None):
    with StringIO(data) if data else open(f'data/{__file__.replace(".py", ".txt")}') as f:
        data = list(map(str.strip, f.readlines()))
    return data[0]


if __name__ == '__main__':
    part1()
    part2()
