import time

import numpy as np

EXAMPLE1 = """
89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
"""


def parse_input(text: str) -> np.array:
    mat = []
    for line in text.strip().split("\n"):
        mat.append(list(line.strip()))

    return np.array(mat, dtype=int)


def find_num_paths_from_starting_position(
        starting_position: tuple[int, int],
        topo_grid: np.array,
        count_only_unique_tops: bool
) -> int:
    i_max, j_max = topo_grid.shape

    num_paths = 0
    visited_tops = set()
    stack = [starting_position]
    while stack:
        i, j = stack.pop(-1)
        neighbors = ((i + 1, j), (i, j + 1), (i - 1, j), (i, j - 1))
        for n in neighbors:
            next_i, next_j = n
            if (
                    0 <= next_i < i_max and 0 <= next_j < j_max and
                    topo_grid[next_i, next_j] == topo_grid[i, j] + 1
            ):
                if topo_grid[next_i, next_j] == 9:
                    if (next_i, next_j) not in visited_tops:
                        num_paths += 1
                        if count_only_unique_tops:
                            visited_tops.add((next_i, next_j))
                else:
                    stack.append((next_i, next_j))

    return num_paths


def find_overall_num_paths(grid: np.array, count_only_unique_tops: bool) -> int:
    starting_positions = np.argwhere(grid == 0)
    num_paths = 0
    for sp in starting_positions:
        # noinspection PyTypeChecker
        num_paths += find_num_paths_from_starting_position(tuple(sp), grid, count_only_unique_tops)

    return num_paths


if __name__ == "__main__":
    with open("../inputs/10.txt", "r") as fh:
        in_text = fh.read()

    topo_map = parse_input(in_text)

    # PART 1
    start = time.perf_counter()
    res = find_overall_num_paths(topo_map, True)
    end = time.perf_counter()
    print(f"Part 1 Result: {res}. Took {(end - start) * 1000:.2f} ms.")

    # PART 2
    start = time.perf_counter()
    res = find_overall_num_paths(topo_map, False)
    end = time.perf_counter()
    print(f"Part 2 Result: {res}. Took {(end - start) * 1000:.2f} ms.")
