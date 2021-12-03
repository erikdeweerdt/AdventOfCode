def part1():
    with open("data/3.txt") as f:
        data = [l.strip() for l in f.readlines() if l]
    counters = []
    for line in data:
        for i, c in enumerate(line):
            if i >= len(counters):
                counters.append([0, 0])
            if c == '0':
                counters[i][0] += 1
            else:
                counters[i][1] += 1
    # print(counters)
    gamma = ''
    epsilon = ''
    for c in counters:
        if c[0] > c[1]:
            gamma += '0'
            epsilon += '1'
        else:
            gamma += '1'
            epsilon += '0'
    g = int(gamma, 2)
    e = int(epsilon, 2)
    print(f'gamma = {gamma} ({g}), epsilon = {epsilon} ({e}), answer = {g*e}')


def part2():
    with open("data/3.txt") as f:
        data = [l.strip() for l in f.readlines() if l]
    oxy = data
    car = data
    for pos in range(len(data[0])):
        if len(oxy) > 1:
            oxy, _ = divide(oxy, pos)
        if len(car) > 1:
            _, car = divide(car, pos)
    o = int(oxy[0], 2)
    c = int(car[0], 2)
    print(f'oxy = {oxy} ({o}), car = {car} ({c}), answer = {o*c}')


def divide(data, pos):
    zero = []
    one = []
    for line in data:
        if line[pos] == '0':
            zero.append(line)
        else:
            one.append(line)
    if len(zero) > len(one):
        return zero, one
    else:
        return one, zero


if __name__ == '__main__':
    part1()
    part2()
