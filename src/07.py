import time
from typing import Callable

EXAMPLE1 = """
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
"""


def parse_input(text: str) -> list[tuple[int, list[int]]]:
    out = []
    for line in text.strip().split("\n"):
        lhs, rhs = line.strip().split(":")
        out.append((int(lhs.strip()), list(map(lambda x: int(x.strip()), rhs.strip().split()))))

    return out


def check_validity_part_1(equation: tuple[int, list[int]]) -> bool:
    lhs, rhs = equation

    stack = [(rhs[0], 0)]
    i_max = len(rhs) - 1

    while stack:
        num, i = stack.pop(-1)
        if i < i_max:
            next_num = rhs[i + 1]
            agg_sum = num + next_num
            agg_prod = num * next_num
            # eliminate branches that exceed the expected result since
            # all possible operations are monotonically increasing
            if agg_sum <= lhs:
                stack.append((agg_sum, i + 1))
            if agg_prod <= lhs:
                stack.append((agg_prod, i + 1))
        else:
            if num == lhs:
                return True

    return False


def check_validity_part_2(equation: tuple[int, list[int]]) -> bool:
    lhs, rhs = equation

    stack = [(rhs[0], 0)]
    i_max = len(rhs) - 1

    while stack:
        num, i = stack.pop(-1)
        if i < i_max:
            next_num = rhs[i + 1]
            agg_sum = num + next_num
            agg_prod = num * next_num
            agg_concat = int(f"{num}{next_num}")
            if agg_sum <= lhs:
                stack.append((agg_sum, i + 1))
            if agg_prod <= lhs:
                stack.append((agg_prod, i + 1))
            if agg_concat <= lhs:
                stack.append((agg_concat, i + 1))
        else:
            if num == lhs:
                return True

    return False


def sum_valid_equations(
        eqs: list[tuple[int, list[int]]],
        validity_crit: Callable[[tuple[int, list[int]]], bool]
) -> int:
    out = 0
    for eq in eqs:
        if validity_crit(eq):
            out += eq[0]

    return out


if __name__ == "__main__":
    with open("../inputs/07.txt", "r") as fh:
        in_text = fh.read()

    equations = parse_input(in_text)

    # PART 1
    start = time.perf_counter()
    res = sum_valid_equations(equations, check_validity_part_1)
    end = time.perf_counter()
    print(f"Part 1 Result: {res}. Took {(end - start) * 1000:.2f} ms.")

    # PART 2
    start = time.perf_counter()
    res = sum_valid_equations(equations, check_validity_part_2)
    end = time.perf_counter()
    print(f"Part 2 Result: {res}. Took {(end - start) * 1000:.2f} ms.")
