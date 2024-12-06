import time

import numpy as np
from tqdm import tqdm

EXAMPLE1 = """
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
"""

"""
Direction indices: up = 0, right = 1, down = 2, left = 3
"""

TRANSLATIONS = [np.array([-1, 0]), np.array([0, 1]), np.array([1, 0]), np.array([0, -1])]  # up, right, down, left


def parse_input(text: str) -> np.array:
    mat = []
    for line in text.strip().split("\n"):
        mat.append(list(line.strip()))

    return np.array(mat)


def take_step(
        direction: int,
        pos: tuple[int, int],
        mat: np.array,
        i_max: int,
        j_max: int
) -> tuple[int, np.array]:
    next_pos = pos + TRANSLATIONS[direction]
    if next_pos[0] < 0 or next_pos[0] >= i_max or next_pos[1] < 0 or next_pos[1] >= j_max:
        raise IndexError

    while mat[tuple(next_pos)] == "#":
        direction = (direction + 1) % 4
        next_pos = pos + TRANSLATIONS[direction]
        if next_pos[0] < 0 or next_pos[0] >= i_max or next_pos[1] < 0 or next_pos[1] >= j_max:
            raise IndexError

    return direction, next_pos


def count_steps(mat: np.array) -> tuple[int, set[tuple[int, int]]]:
    i_max, j_max = mat.shape
    pos = np.argwhere(mat == "^")[0]
    direction = 0
    steps = 0
    visited_positions = set()
    while True:
        visited_positions.add(tuple(pos))
        try:
            direction, next_pos = take_step(direction, pos, mat, i_max, j_max)
        except IndexError:
            break
        if tuple(next_pos) not in visited_positions:
            steps += 1
        pos = next_pos

    return steps + 1, visited_positions  # +1 for the starting position


def place_obstacle_and_detect_cycle(mat: np.array, obstacle_position: tuple[int, int]) -> int:
    i_max, j_max = mat.shape
    pos = np.argwhere(mat == "^")[0]
    if obstacle_position == tuple(pos):
        return False
    mat[obstacle_position] = "#"
    direction = 0
    visited_positions = set()
    while True:
        visited_positions.add((direction, tuple(pos)))
        try:
            direction, next_pos = take_step(direction, pos, mat, i_max, j_max)
        except IndexError:
            return False

        if (direction, tuple(next_pos)) in visited_positions:
            return True

        pos = next_pos


def find_num_cycles(mat: np.array, original_trajectory: set[tuple[int, int]]) -> int:
    cycles = 0
    for pos in tqdm(original_trajectory):
        if place_obstacle_and_detect_cycle(mat.copy(), pos):
            cycles += 1

    return cycles


if __name__ == "__main__":
    with open("../inputs/06.txt", "r") as fh:
        in_text = fh.read()

    grid = parse_input(in_text)

    # PART 1
    start = time.perf_counter()
    res, trajectory = count_steps(grid)
    end = time.perf_counter()
    print(f"Part 1 Result: {res}. Took {(end - start) * 1000:.2f} ms.")

    # PART 2
    start = time.perf_counter()
    res = find_num_cycles(grid, trajectory)
    end = time.perf_counter()
    print(f"Part 2 Result: {res}. Took {(end - start) * 1000:.2f} ms.")
