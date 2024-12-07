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

    rhs_agg = {rhs[0]}
    for i in rhs[1:]:
        rhs_agg_next = set()
        for j in rhs_agg:
            agg_sum = j + i
            agg_prod = j * i
            # eliminate branches that exceed the expected result since
            # all possible operations are monotonically increasing
            if agg_sum <= lhs:
                rhs_agg_next.add(agg_sum)
            if agg_prod <= lhs:
                rhs_agg_next.add(agg_prod)
        rhs_agg = rhs_agg_next

    if lhs in rhs_agg:
        return True

    return False


def check_validity_part_2(equation: tuple[int, list[int]]) -> bool:
    lhs, rhs = equation

    rhs_agg = {rhs[0]}
    for i in rhs[1:]:
        rhs_agg_next = set()
        for j in rhs_agg:
            agg_sum = j + i
            agg_prod = j * i
            agg_concat = int(f"{j}{i}")
            if agg_sum <= lhs:
                rhs_agg_next.add(agg_sum)
            if agg_prod <= lhs:
                rhs_agg_next.add(agg_prod)
            if agg_concat <= lhs:
                rhs_agg_next.add(agg_concat)
        rhs_agg = rhs_agg_next

    if lhs in rhs_agg:
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
