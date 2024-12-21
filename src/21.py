import functools
import time

import numpy as np

EXAMPLE1 = """
029A
980A
179A
456A
379A
"""

KEYPAD_GRID = np.array(["7", "8", "9", "4", "5", "6", "1", "2", "3", "", "0", "A"], dtype=str).reshape(4, 3)
ARROWPAD_GRID = np.array(["", "^", "A", "<", "v", ">"], dtype=str).reshape(2, 3)

KEYPAD_MAP = {
    button: tuple(map(lambda x: x[0], np.where(KEYPAD_GRID == button))) for button in KEYPAD_GRID.flatten()
}
ARROWPAD_MAP = {
    button: tuple(map(lambda x: x[0], np.where(ARROWPAD_GRID == button))) for button in ARROWPAD_GRID.flatten()
}


def parse_input(text: str) -> list[list[str]]:
    codes = []
    for line in text.strip().split("\n"):
        codes.append(list(line))

    return codes


def navigate_on_keypad_and_press_button(from_button: str, to_button: str) -> list[list[str]]:
    """
    The shortest path between two buttons is the one with the fewest number of button presses
    on the final terminal. Therefore, the shortest path is the one with the fewest number of
    "corners" (i.e. the fewest number of times the direction changes). This means that we either
    have to go along the rows first (dimension_order = 0) or along the columns first
    (dimension_order = 1). If in one of these two possible shortest paths, we would hover over
    an empty terminal position, this path must be dropped, and we only have one unique shortest
    path.
    """

    from_index = KEYPAD_MAP[from_button]
    to_index = KEYPAD_MAP[to_button]
    delta = (to_index[0] - from_index[0], to_index[1] - from_index[1])

    # Avoid hovering over empty terminal positions
    if (
            from_button in ("0", "A") and to_button in ("1", "4", "7") or
            from_button in ("1", "4", "7") and to_button in ("0", "A")
    ):
        if delta[0] >= 0:
            dimension_order = 1
        else:
            dimension_order = 0
    else:
        dimension_order = None

    if dimension_order is None:
        navigation_sequence = [
            navigate_on_grid(delta, 0), navigate_on_grid(delta, 1)
        ]
    else:
        navigation_sequence = [navigate_on_grid(delta, dimension_order)]

    return navigation_sequence


@functools.cache
def navigate_on_arrowpads_and_press_button(
        from_button: str,
        to_button: str,
        depth: int,
        max_depth: int,
) -> int:
    from_index = ARROWPAD_MAP[from_button]
    to_index = ARROWPAD_MAP[to_button]
    delta = (to_index[0] - from_index[0], to_index[1] - from_index[1])

    # dimension_order: 0 -> go along rows first, 1 -> go along columns first.
    # Avoid hovering over empty terminal positions
    if (
            from_button == "<" and to_button in ("^", "A") or
            from_button in ("^", "A") and to_button == "<"
    ):
        if delta[0] >= 0:
            dimension_order = 0
        else:
            dimension_order = 1
    else:
        dimension_order = None

    if dimension_order is None:
        navigation_sequence_possibilities = [
            navigate_on_grid(delta, 0), navigate_on_grid(delta, 1)
        ]
    else:
        navigation_sequence_possibilities = [navigate_on_grid(delta, dimension_order)]

    if depth < max_depth:
        current_button = "A"
        number_button_presses_on_last_terminal_possibilities = []
        for navigation_sequence in navigation_sequence_possibilities:
            number_button_presses_on_last_terminal = 0
            for next_button in navigation_sequence:
                number_button_presses_on_last_terminal += navigate_on_arrowpads_and_press_button(
                    current_button, next_button, depth + 1, max_depth
                )
                current_button = next_button
            number_button_presses_on_last_terminal_possibilities.append(number_button_presses_on_last_terminal)
        return min(number_button_presses_on_last_terminal_possibilities)
    else:
        # Arrived at last terminal
        return min(map(len, navigation_sequence_possibilities))


def navigate_on_grid(delta: tuple[int, int], dimension_order: int) -> list[str]:
    row_steps = ["v" if delta[0] > 0 else "^"] * abs(delta[0])
    col_steps = [">" if delta[1] > 0 else "<"] * abs(delta[1])
    if dimension_order == 0:
        navigation_sequence = row_steps + col_steps
    else:
        navigation_sequence = col_steps + row_steps

    return navigation_sequence + ["A"]


def open_door_and_get_sum_of_complexities(codes: list[list[str]], num_nested_arrowpads: int) -> int:
    overall_complexity = 0
    current_button = "A"
    current_arrow_button = "A"
    for code in codes:
        number_overall_button_presses_on_last_terminal = 0
        for button in code:
            arrow_instructions_possibilities = navigate_on_keypad_and_press_button(current_button, button)
            number_button_presses_on_last_terminal_possibilities = []
            for arrow_instructions in arrow_instructions_possibilities:
                number_button_presses_on_last_terminal = 0
                for arrow_button in arrow_instructions:
                    number_button_presses_on_last_terminal += navigate_on_arrowpads_and_press_button(
                            current_arrow_button, arrow_button, 0, num_nested_arrowpads
                    )
                    current_arrow_button = arrow_button
                number_button_presses_on_last_terminal_possibilities.append(number_button_presses_on_last_terminal)
            number_overall_button_presses_on_last_terminal += min(number_button_presses_on_last_terminal_possibilities)
            current_button = button
        overall_complexity += number_overall_button_presses_on_last_terminal * int("".join(code[:-1]))

    return overall_complexity


if __name__ == "__main__":
    with open("../inputs/21.txt", "r") as fh:
        in_text = fh.read()

    code_input = parse_input(in_text)

    # PART 1
    start = time.perf_counter()
    res = open_door_and_get_sum_of_complexities(code_input, 1)
    end = time.perf_counter()
    print(f"Part 1 Result: {res}. Took {(end - start) * 1000:.2f} ms.")

    # PART 2
    start = time.perf_counter()
    res = open_door_and_get_sum_of_complexities(code_input, 24)
    end = time.perf_counter()
    print(f"Part 2 Result: {res}. Took {(end - start) * 1000:.2f} ms.")
