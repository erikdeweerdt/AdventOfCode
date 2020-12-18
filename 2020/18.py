import re
from typing import Any,List


def evaluate(expr: List[Any]) -> int:
    result = None
    operator = None
    for subexpr in expr:
        operand = None
        if isinstance(subexpr, list):
            operand = evaluate(subexpr)
        elif subexpr == "+" or subexpr == "*":
            operator = subexpr
        else:
            operand = int(subexpr)
        if operand is not None:
            if operator == "+":
                result += operand
            elif operator == "*":
                result *= operand
            else:
                result = operand
    # print(f"<< {result}")
    return result


def process_parens(expr: List[str], index=0):
    result = []
    while index < len(expr):
        token = expr[index]
        index += 1
        if token == "(":
            index, subexpr = process_parens(expr, index)
            result.append(subexpr)
        elif token == ")":
            break
        else:
            result.append(token)
    return (index, result)


def to_expr(line: str) -> List[str]:
    return process_parens(re.findall(r"(\d+|\(|\)|\+|\*)", line))[1]


def part1(data):
    return sum([evaluate(to_expr(line)) for line in data if line])


if __name__ == "__main__":
    with open("data/18.txt") as f:
        data = f.read()
    data = data.splitlines()
    print(evaluate(to_expr("1 + (2 * 3) + (4 * (5 + 6))")))
    print(evaluate(to_expr("2 * 3 + (4 * 5)")))
    print(evaluate(to_expr("5 + (8 * 3 + 9 + 3 * 4 * 3)")))
    print(evaluate(to_expr("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))")))
    print(evaluate(to_expr("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2")))
    # print(process_parens(to_expr("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2"))[1])
    # print(part1(data))
