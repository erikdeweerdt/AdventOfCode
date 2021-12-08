import re

#    ct ct
# lt       rt
# lt       rt
#    cc cc
# lb       rb
# lb       rb
#    cb cb

SEVEN_SEGMENT = ['lt', 'lb', 'ct', 'cc', 'cb', 'rt', 'rb']
DIGITS = [
    sorted(['lt', 'lb', 'ct', 'cb', 'rt', 'rb']),  # 0
    sorted(['rt', 'rb']),  # 1
    sorted(['lb', 'ct', 'cc', 'cb', 'rt']),  # 2
    sorted(['ct', 'cc', 'cb', 'rt', 'rb']),  # 3
    sorted(['lt', 'cc', 'rt', 'rb']),  # 4
    sorted(['lt', 'ct', 'cc', 'cb', 'rb']),  # 5
    sorted(['lt', 'lb', 'ct', 'cc', 'cb', 'rb']),  # 6
    sorted(['ct', 'rt', 'rb']),  # 7
    sorted(['lt', 'lb', 'ct', 'cc', 'cb', 'rt', 'rb']),  # 8
    sorted(['lt', 'ct', 'cc', 'cb', 'rt', 'rb']),  # 9
]


def part1():
    with open("data/8.txt") as f:
        data = [l.strip().split(' | ') for l in f.readlines() if l]
    count = 0
    # count how many times 1, 4, 7 or 8 show up in the output
    # these are the only digits with 2, 4, 3 and 7 segments respectively
    for signals, outputs in data:
        count += sum((1 if len(o) in [2, 3, 4, 7] else 0 for o in outputs.split(' ')))
    print(count)


def part2():
    with open("data/8.txt") as f:
        data = [l.strip().split(' | ') for l in f.readlines() if l]
    # print(wire('acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab'.split(' ')))
    # wire(['dab','ab'])
    # data = ['acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf'.split(' | ')]
    valuesum = 0
    for s, o in data:
        wiring = wire(s.split(' '))
        val = 0
        for char in o.split(' '):
            ss = []
            for c in char:
                ss.append(wiring[c])
            val = 10*val + DIGITS.index(sorted(ss))
        valuesum += val
        print(val)
    print(valuesum)


def wire(signals):
    ss = {s: 'abcdefg' for s in SEVEN_SEGMENT}
    for signal in signals:
        # print('signal', signal)
        possible = {}
        matches = 0
        for d in DIGITS:
            if len(signal) == len(d):
                matches += 1
                for segment in d:
                    if segment in possible:
                        possible[segment] += 1
                    else:
                        possible[segment] = 1
        # print('possible', possible)
        for segment in ss:
            if segment in possible:
                if possible[segment] == matches:
                    ss[segment] = re.sub(f'[^{signal}]', '', ss[segment])
            else:
                ss[segment] = re.sub(f'[{signal}]', '', ss[segment])
            if len(ss[segment]) == 1:
                for s in ss:
                    if s != segment:
                        ss[s] = ss[s].replace(ss[segment], '')
    if sum(len(v) for v in ss.values()) > 7:
        # doesn't happen
        raise ValueError(ss)
    return {v: k for k, v in ss.items()}


if __name__ == '__main__':
    # part1()
    part2()
