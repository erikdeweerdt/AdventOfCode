import re
from typing import List


def evaluate(expr: List[str], index: int = 0) -> int:
    result = None
    operator = None
    # print(f">> [{index}]")
    while index < len(expr):
        token = expr[index]
        index += 1
        operand = None
        if token == "+" or token == "*":
            operator = token
        elif token == "(":
            index, operand = evaluate(expr, index)
        elif token == ")":
            break
        else:
            operand = int(token)
        # print(result, operator, operand)
        if operand is not None:
            if operator == "+":
                result += operand
            elif operator == "*":
                result *= operand
            else:
                result = operand
    # print(f"<< {result}")
    return (index, result)


def to_expr(line: str) -> List[str]:
    return re.findall(r"(\d+|\(|\)|\+|\*)", line)

def part1(data):
    return sum([evaluate(to_expr(line))[1] for line in data if line])

if __name__ == "__main__":
    with open("data/18.txt") as f:
        data = f.read()
    data = data.splitlines()
    # print(evaluate(to_expr("2 * 3 + (4 * 5)")))
    # print(evaluate(to_expr("5 + (8 * 3 + 9 + 3 * 4 * 3)")))
    # print(evaluate(to_expr("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))")))
    # print(evaluate(to_expr("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2")))
    print(part1(data))
