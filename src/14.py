import math
import re
import time

import numpy as np
import skimage

EXAMPLE1 = """
p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3
"""


def parse_input(text: str) -> list[tuple[tuple[int, int], tuple[int, int]]]:
    out = []
    for line in text.strip().split("\n"):
        position = tuple(map(int, re.findall(r"p=([\d,]+)", line)[0].split(",")))
        velocity = tuple(map(int, re.findall(r"v=([\d,\-]+)", line)[0].split(",")))
        out.append((position, velocity))

    # noinspection PyTypeChecker
    return out


def simulate_robot_step(
        current_state: tuple[tuple[int, int], tuple[int, int]],
        grid_size: tuple[int, int]
) -> tuple[tuple[int, int], tuple[int, int]]:
    position, velocity = current_state
    i_max, j_max = grid_size
    next_position = (position[0] + velocity[0]) % i_max, (position[1] + velocity[1]) % j_max

    return next_position, velocity


def simulate_robots_and_calculate_safety_factor(
        robot_states: list[tuple[tuple[int, int], tuple[int, int]]],
        grid_size: tuple[int, int],
        steps: int
) -> int:
    quadrants = {i: 0 for i in range(4)}
    i_max, j_max = grid_size
    for robot_state in robot_states:
        for _ in range(steps):
            robot_state = simulate_robot_step(robot_state, grid_size)
        robot_pos_i, robot_pos_j = robot_state[0]
        if robot_pos_i < i_max // 2:
            if robot_pos_j < j_max // 2:
                quadrants[0] += 1
            elif robot_pos_j > j_max // 2:
                quadrants[3] += 1
        elif robot_pos_i > i_max // 2:
            if robot_pos_j < j_max // 2:
                quadrants[1] += 1
            elif robot_pos_j > j_max // 2:
                quadrants[2] += 1

    return math.prod(quadrants.values())


def simulate_robots_and_find_num_steps_to_form_christmas_tree(
        robot_states: list[tuple[tuple[int, int], tuple[int, int]]],
        grid_size: tuple[int, int],
        steps: int
) -> int:
    """
    Simulate the robots for a given number of steps and calculate the image they form.
    We assume that the Christmas tree is formed by the robots when the entropy of the
    image has the lowest value.
    """
    min_entropy = np.inf
    best_image = None
    tree_found_after_steps = 0
    for n in range(steps):
        image = np.zeros(grid_size, dtype=int)
        for robot_state in robot_states:
            position, _ = robot_state
            image[position] += 1
        entropy = skimage.measure.shannon_entropy(image)
        if entropy < min_entropy:
            min_entropy = entropy
            best_image = image
            tree_found_after_steps = n
        robot_states = [simulate_robot_step(robot_state, grid_size) for robot_state in robot_states]

    # We need to check manually if the "best image" really contains a Christmas tree.
    # Else, we need to increase the number of steps
    display_image(best_image)

    return tree_found_after_steps


def display_image(image: np.ndarray):
    for row in image:
        print("".join("#" if x > 0 else "." for x in row))


if __name__ == "__main__":
    with open("../inputs/14.txt", "r") as fh:
        in_text = fh.read()

    robots = parse_input(in_text)

    # PART 1
    start = time.perf_counter()
    res = simulate_robots_and_calculate_safety_factor(robots, (101, 103), 100)
    end = time.perf_counter()
    print(f"Part 1 Result: {res}. Took {(end - start) * 1000:.2f} ms.")

    # PART 2
    start = time.perf_counter()
    res = simulate_robots_and_find_num_steps_to_form_christmas_tree(robots, (101, 103), 10000)
    end = time.perf_counter()
    print(f"Part 2 Result: {res}. Took {(end - start) * 1000:.2f} ms.")
