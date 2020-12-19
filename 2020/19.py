# import re
from typing import List

# https://pypi.org/project/regex/
import regex

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
TESTDATA2 = """
42: 9 14 | 10 1
9: 14 27 | 1 26
10: 23 14 | 28 1
1: "a"
11: 42 31
5: 1 14 | 15 1
19: 14 1 | 14 14
12: 24 14 | 19 1
16: 15 1 | 14 14
31: 14 17 | 1 13
6: 14 14 | 1 14
2: 1 24 | 14 4
0: 8 11
13: 14 3 | 1 12
15: 1 | 14
17: 14 2 | 1 7
23: 25 1 | 22 14
28: 16 1
4: 1 1
20: 14 14 | 1 15
3: 5 14 | 16 1
27: 1 6 | 14 18
14: "b"
21: 14 1 | 1 14
25: 1 1 | 1 14
22: 14 14
8: 42
26: 14 22 | 1 20
18: 15 15
7: 14 5 | 1 21
24: 14 1

abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa
bbabbbbaabaabba
babbbbaabbbbbabbbbbbaabaaabaaa
aaabbbbbbaaaabaababaabababbabaaabbababababaaa
bbbbbbbaaaabbbbaaabbabaaa
bbbababbbbaaaaaaaabbababaaababaabab
ababaaaaaabaaab
ababaaaaabbbaba
baabbaaaabbaaaababbaababb
abbbbabbbbaaaababbbbbbaaaababb
aaaaabbaabaaaaababaa
aaaabbaaaabbaaa
aaaabbaabbaaaaaaabbbabbbaaabbaabaaa
babaaabbbaaabaababbaabababaaab
aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba
""".splitlines()


def compile_pattern(rules: List[str], index=0) -> str:
    pattern = ""
    rule = rules[index] if isinstance(rules[index], list) else rules[index].split(" ")
    for token in rule:
        if token.startswith("\""):
            pattern += token[1]
        elif token.isdigit():
            pattern += compile_pattern(rules, int(token))
        else:
            pattern += token
    return "(?:" + pattern + ")" if "|" in rule else pattern


def parse_rules(data: List[str]) -> List[str]:
    # rules in the input are not ordered
    # some rules numbers may not be defined
    rules = {}
    max_index = 0
    for line in data:
        match = regex.match(r"^(\d+): (.*)", line)
        if match:
            index = int(match.group(1))
            rules[index] = match.group(2)
            max_index = index if index > max_index else max_index
    return [rules.pop(index, None) for index in range(max_index + 1)]


def parse_messages(data: List[str]) -> List[str]:
    return [line for line in data if line.startswith("a") or line.startswith("b")]


def part1(data):
    rules = parse_rules(data)
    messages = parse_messages(data)
    pattern = compile_pattern(rules)
    # print(rules)
    # print(messages)
    print(pattern)
    expr = regex.compile(pattern)
    print(sum(1 if expr.fullmatch(message) else 0 for message in messages))


def part2(data):
    rules = parse_rules(data)
    messages = parse_messages(data)
    rules[8] = "42 +"
    # in rule 11, 42 and 31 must be balanced
    # re doesn't support recursive regexes and we have to "cheat" if using that
    # rules[11] = " | ".join(("42 " * i + "31 " * i).strip() for i in range(1,10))
    # the newer regex module does support recursion
    rules[11] = "(?<x>,42,(?&x)?,31,)".split(",")
    pattern = compile_pattern(rules)
    # print(pattern)
    expr = regex.compile(pattern)
    print(sum(1 if expr.fullmatch(message) else 0 for message in messages))


if __name__ == "__main__":
    with open("data/19.txt") as f:
        data = f.read()
    data = data.splitlines()
    # part1(data)
    part2(data)
