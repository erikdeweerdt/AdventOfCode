import re
from typing import List

TESTDATA = """
0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb
""".splitlines()


def compile_pattern(rules: List[str], index=0) -> str:
    pattern = ""
    rule = rules[index].split(" ")
    for token in rule:
        if token == "|":
            pattern += "|"
        elif token.startswith("\""):
            pattern += token[1]
        else:
            pattern += compile_pattern(rules, int(token))
    return "(" + pattern + ")" if "|" in rule else pattern


def parse_rules(data: List[str]) -> List[str]:
    # rules in the input are not ordered
    # collect them first and return a list by sorting the keys
    rules = {}
    for line in data:
        match = re.match(r"^(\d+): (.*)", line)
        if match:
            rules[int(match.group(1))] = match.group(2)
    return [rules[index] for index in sorted(rules.keys())]


def parse_messages(data: List[str]) -> List[str]:
    return [line for line in data if line.startswith("a") or line.startswith("b")]


def part1(data):
    rules = parse_rules(data)
    messages = parse_messages(data)
    pattern = compile_pattern(rules)
    # print(rules)
    # print(messages)
    print(pattern)
    regex = re.compile(pattern)
    print(sum(1 if regex.fullmatch(message) else 0 for message in messages))


if __name__ == "__main__":
    with open("data/19.txt") as f:
        data = f.read()
    data = data.splitlines()
    part1(data)
