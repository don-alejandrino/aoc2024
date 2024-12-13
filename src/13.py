import math
import re
import time

from sympy import And
from sympy.abc import x, y
# noinspection PyProtectedMember
from sympy.solvers.diophantine.diophantine import diop_linear
from sympy.solvers.inequalities import reduce_rational_inequalities

EXAMPLE1 = """
Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279
"""


def parse_input(text: str) -> list[tuple[tuple[int, int], tuple[int, int], tuple[int, int]]]:
    out = []
    for block in text.strip().split("\n\n"):
        a_shift = tuple(map(int, re.findall(r"Button A: X\+(\d+), Y\+(\d+)", block)[0]))
        b_shift = tuple(map(int, re.findall(r"Button B: X\+(\d+), Y\+(\d+)", block)[0]))
        target = tuple(map(int, re.findall(r"Prize: X=(\d+), Y=(\d+)", block)[0]))
        out.append((a_shift, b_shift, target))

    # noinspection PyTypeChecker
    return out


def solve_diophantine_equation(a: int, b: int, c: int) -> int:
    sol = diop_linear(a * x + b * y - c)
    k = sol.free_symbols.pop()
    # The solution is a parametrized set of points of the form (x0 + k * b, y0 - k * a),
    # where k is an arbitrary integer. We only accept solutions that have non-negative
    # values and pick from these the one with the lowest cost 3 * x[0] + x[1]
    k_range_x = reduce_rational_inequalities([[sol[0] >= 0]], k)
    k_range_y = reduce_rational_inequalities([[sol[1] >= 0]], k)
    valid_k_values = And(k_range_y, k_range_x).as_set()
    if valid_k_values.is_empty:
        return 0
    candidates = [sol.subs({k: i}) for i in range(valid_k_values.left, valid_k_values.right + 1)]
    n_a, n_b = min(candidates, key=lambda z: 3 * z[0] + z[1])

    return 3 * n_a + n_b


def solve_claw_and_get_game_cost(
        a_shift: tuple[int, int],
        b_shift: tuple[int, int],
        target: tuple[int, int]
) -> int:
    """
    The required numbers n_a and n_b of A and B button presses, respectively, to
    reach the target are given by the equation n_a * a_shift + n_b * b_shift = target.
    This equation has a unique solution iff a_shift and b_shift are linearly independent,
    i.e., not parallel to each other (note, however, that this solution does not necessarily
    have to be an integer one). If a_shift and b_shift are parallel, on the other hand,
    the equation has either no solution or infinitely many solutions (again not necessarily
    integer ones). In the latter case, the target point is on the same line as a_shift and
    b_shift, and we have to solve a linear Diophantine equation to get all possible integer
    solutions. From these, we then have to pick the one with the lowest cost.
    """
    a_x, a_y = a_shift
    b_x, b_y = b_shift
    t_x, t_y = target

    try:
        n_a = (t_x * b_y - b_x * t_y) / (a_x * b_y - b_x * a_y)
    except ZeroDivisionError:
        # a_shift and b_shift are parallel
        if a_x * t_y - a_y * t_x == 0:
            # target is on the same line as a_shift and b_shift
            a_shift_len = math.sqrt(a_x ** 2 + a_y ** 2)
            b_shift_len = math.sqrt(b_x ** 2 + b_y ** 2)
            target_len = math.sqrt(t_x ** 2 + t_y ** 2)
            if a_shift_len.is_integer() and b_shift_len.is_integer() and target_len.is_integer():
                # all coefficients have to be integers, else we can't solve the equation
                return solve_diophantine_equation(int(a_shift_len), int(b_shift_len), int(target_len))
        return 0

    if n_a < 0 or not n_a.is_integer():
        return 0
    n_a = int(n_a)

    try:
        n_b = (t_x - a_x * n_a) / b_x
    except ZeroDivisionError:
        # if b_x == 0, b_y can't be 0, else we would have run
        # into a ZeroDivisionError already when calculating n_a
        n_b = (t_y - a_y * n_a) / b_y

    if n_b < 0 or not n_b.is_integer():
        return 0
    n_b = int(n_b)

    return 3 * n_a + n_b


def get_total_game_costs(
        claws: list[tuple[tuple[int, int], tuple[int, int], tuple[int, int]]]
) -> int:
    return sum(
        solve_claw_and_get_game_cost(a_shift, b_shift, target)
        for a_shift, b_shift, target in claws
    )


def correct_unit_conversion(
        claws: list[tuple[tuple[int, int], tuple[int, int], tuple[int, int]]]
) -> list[tuple[tuple[int, int], tuple[int, int], tuple[int, int]]]:
    return [
        (a_shift, b_shift, (target[0] + 10000000000000, target[1] + 10000000000000))
        for a_shift, b_shift, target in claws
    ]


if __name__ == "__main__":
    with open("../inputs/13.txt", "r") as fh:
        in_text = fh.read()

    claw_machines = parse_input(in_text)

    # PART 1
    start = time.perf_counter()
    res = get_total_game_costs(claw_machines)
    end = time.perf_counter()
    print(f"Part 1 Result: {res}. Took {(end - start) * 1000:.2f} ms.")

    # PART 2
    start = time.perf_counter()
    res = get_total_game_costs(correct_unit_conversion(claw_machines))
    end = time.perf_counter()
    print(f"Part 2 Result: {res}. Took {(end - start) * 1000:.2f} ms.")
