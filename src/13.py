import re
import time

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


def solve_claw_and_get_game_cost(
        a_shift: tuple[int, int],
        b_shift: tuple[int, int],
        target: tuple[int, int]
) -> int:
    """
    The required numbers n_a and n_b of A and B button presses, respectively, to
    reach the target are given by the equation n_a * a_shift + n_b * b_shift = target.
    """
    a_x, a_y = a_shift
    b_x, b_y = b_shift
    t_x, t_y = target

    try:
        n_a = (t_x * b_y - b_x * t_y) / (a_x * b_y - b_x * a_y)
    except ZeroDivisionError:
        return 0

    if n_a < 0 or not n_a.is_integer():
        return 0
    n_a = int(n_a)

    try:
        n_b = (t_x - a_x * n_a) / b_x
    except ZeroDivisionError:
        return 0

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
