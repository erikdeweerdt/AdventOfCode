def part1():
    with open("data/2.txt") as f:
        data = [l.strip().split(' ') for l in f.readlines() if l]
    horizontal = 0
    depth = 0
    for k,v in data:
        if k == 'forward':
            horizontal += int(v)
        elif k == 'down':
            depth += int(v)
        elif k == 'up':
            depth -= int(v)
        else:
            raise ValueError()
    print(f'h = {horizontal}, d = {depth}, answer = {horizontal * depth}')

def part2():
    with open("data/2.txt") as f:
        data = [l.strip().split(' ') for l in f.readlines() if l]
    horizontal = 0
    aim = 0
    depth = 0
    for k,v in data:
        if k == 'forward':
            horizontal += int(v)
            depth += int(v) * aim
        elif k == 'down':
            aim += int(v)
        elif k == 'up':
            aim -= int(v)
        else:
            raise ValueError()
    print(f'h = {horizontal}, a = {aim}, d = {depth}, answer = {horizontal * depth}')

if __name__ == '__main__':
    part1()
    part2()
