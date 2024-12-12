import time

import numpy as np

EXAMPLE1 = """
RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE
"""

DIRECTIONS = {
    (-1,  0): 0,
    ( 0,  1): 1,
    ( 1,  0): 2,
    ( 0, -1): 3,
}


def parse_input(text: str) -> np.array:
    mat = []
    for line in text.strip().split("\n"):
        mat.append(list(line.strip()))

    return np.array(mat, dtype="U1")


def explore_region_and_calculate_fencing_cost(
        starting_point: tuple[int, int],
        grid: np.array,
        visited: np.array,
        bulk_discount: bool,
) -> int:
    i_max, j_max = grid.shape
    if bulk_discount:
        # Add padding around the grid to avoid index out of bounds
        # when inspecting a perimeter at the grid edges. We encode
        # the direction, against which the perimeter shields, in
        # the third dimension of the is_perimeter array
        # (0 = up, 1 = right, 2 = down, 3 = left).
        is_perimeter = np.zeros((i_max + 4, j_max + 4, 4), dtype=bool)
    queue = [starting_point]
    region_type = grid[starting_point]
    region_area = 0
    region_perimeter = 0
    while queue:
        i, j = queue.pop(0)
        if visited[i, j]:
            continue
        visited[i, j] = True
        region_area += 1
        neighbors = ((i + 1, j), (i, j + 1), (i - 1, j), (i, j - 1))
        for n in neighbors:
            next_i, next_j = n
            if 0 <= next_i < i_max and 0 <= next_j < j_max and grid[next_i, next_j] == region_type:
                queue.append((next_i, next_j))
            else:
                if bulk_discount:
                    direction = DIRECTIONS[next_i - i, next_j - j]
                    # noinspection PyUnboundLocalVariable
                    if not (
                            is_perimeter[next_i + 3, next_j + 2, direction] or
                            is_perimeter[next_i + 2, next_j + 3, direction] or
                            is_perimeter[next_i + 1, next_j + 2, direction] or
                            is_perimeter[next_i + 2, next_j + 1, direction]
                    ):
                        region_perimeter += 1
                    is_perimeter[next_i + 2, next_j + 2, direction] = True
                else:
                    region_perimeter += 1

    return region_area * region_perimeter


def calculate_overall_fencing_cost(grid: np.array, bulk_discount: bool) -> int:
    i_max, j_max = grid.shape
    visited = np.zeros((i_max, j_max), dtype=bool)
    total_cost = 0
    for i in range(i_max):
        for j in range(j_max):
            if not visited[i, j]:
                total_cost += explore_region_and_calculate_fencing_cost(
                    (i, j), grid, visited, bulk_discount
                )

    return total_cost


if __name__ == "__main__":
    with open("../inputs/12.txt", "r") as fh:
        in_text = fh.read()

    garden_grid = parse_input(in_text)

    # PART 1
    start = time.perf_counter()
    res = calculate_overall_fencing_cost(garden_grid, False)
    end = time.perf_counter()
    print(f"Part 1 Result: {res}. Took {(end - start) * 1000:.2f} ms.")

    # PART 2
    start = time.perf_counter()
    res = calculate_overall_fencing_cost(garden_grid, True)
    end = time.perf_counter()
    print(f"Part 2 Result: {res}. Took {(end - start) * 1000:.2f} ms.")
