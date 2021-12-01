def part1():
    with open("data/1.txt") as f:
        data = [int(l) for l in f.readlines() if l]
    count = 0
    for i in range(1, len(data)):
        if data[i] > data[i-1]:
            count += 1
    print(count)

def part2():
    with open("data/1.txt") as f:
        data = [int(l) for l in f.readlines() if l]
    windows = [data[i-2] + data[i-1] + data[i] for i in range(2, len(data))]
    count = 0
    for i in range(1, len(windows)):
        if windows[i] > windows[i-1]:
            count += 1
    print(count)


if __name__ == '__main__':
    part1()
    part2()
