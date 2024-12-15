import time
from collections.abc import Callable

import numpy as np

EXAMPLE1 = """
########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<
"""

EXAMPLE2 = """
##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^
"""


def parse_input(text: str) -> tuple[np.array, list[str]]:
    grid_block, instructions_block = text.strip().split("\n\n")

    grid_list = []
    for line in grid_block.strip().split("\n"):
        grid_list.append(list(line.strip()))

    instructions = list(instructions_block.strip().replace("\n", ""))

    return np.array(grid_list, dtype=str), instructions


def sum_gps_coordinates_after_robot_moving(
        grid: np.array,
        instructions: list[str],
        push_boxes_callback:Callable[[np.array, tuple[int, int], tuple[int, int], str], tuple[int, int]],
        box_identifier: str
) -> int:
    grid = grid.copy()
    navigate_robot(grid, instructions, push_boxes_callback)

    return (np.argwhere(grid == box_identifier) * np.array([100, 1])).sum()


def move(position: tuple[int, int], direction: str) -> tuple[int, int]:
    i, j = position
    if direction == "^":
        return i - 1, j
    elif direction == "v":
        return i + 1, j
    elif direction == "<":
        return i, j - 1
    elif direction == ">":
        return i, j + 1
    else:
        raise ValueError(f"Unknown direction: {direction}")


def navigate_robot(
        grid: np.array,
        instructions: list[str],
        push_boxes_callback: Callable[[np.array, tuple[int, int], tuple[int, int], str], tuple[int, int]],
):
    pos = tuple(np.argwhere(grid == "@")[0])
    for instruction in instructions:
        next_pos = move(pos, instruction)
        if grid[next_pos] == ".":
            grid[pos] = "."
            grid[next_pos] = "@"
            pos = next_pos
        elif grid[next_pos] in ("O", "[", "]"):
            pos = push_boxes_callback(grid, pos, next_pos, instruction)


def push_boxes_part_1(
        grid: np.array,
        robot_pos: tuple[int, int],
        first_box_pos: tuple[int, int],
        instruction: str
) -> tuple[int, int]:
    next_pos = first_box_pos
    row_positions = [robot_pos, first_box_pos]
    while grid[next_pos] in ("O", "[", "]"):
        next_pos = move(next_pos, instruction)
        row_positions.append(next_pos)
        if grid[next_pos] == ".":
            source_indices_i = [p[0] for p in row_positions[0: -1]]
            source_indices_j = [p[1] for p in row_positions[0: -1]]
            target_indices_i = [p[0] for p in row_positions[1:]]
            target_indices_j = [p[1] for p in row_positions[1:]]
            grid[target_indices_i, target_indices_j] = grid[source_indices_i, source_indices_j]
            grid[row_positions.pop(0)] = "."
            break

    return row_positions[0]


def push_boxes_part_2(
        grid: np.array,
        robot_pos: tuple[int, int],
        first_box_pos: tuple[int, int],
        instruction: str
) -> tuple[int, int]:
    if instruction in ("<", ">"):
        return push_boxes_part_1(grid, robot_pos, first_box_pos, instruction)

    next_layer_seed = first_box_pos
    next_robot_pos = robot_pos
    cluster_positions = {0: {robot_pos}}
    l = 1
    get_full_cluster_layer(cluster_positions, grid, next_layer_seed, l)
    while is_not_blocked(grid, cluster_positions[l], instruction):
        if is_free_space(grid, cluster_positions[l], instruction):
            if instruction == "^":
                for layer in reversed(cluster_positions.values()):
                    for pos in layer:
                        grid[pos[0] - 1, pos[1]] = grid[pos]
                        grid[pos] = "."
                next_robot_pos = (next_robot_pos[0] - 1, next_robot_pos[1])
            elif instruction == "v":
                for layer in reversed(cluster_positions.values()):
                    for pos in layer:
                        grid[pos[0] + 1, pos[1]] = grid[pos]
                        grid[pos] = "."
                next_robot_pos = (next_robot_pos[0] + 1, next_robot_pos[1])
            break
        l += 1
        next_layer_seed = move(next_layer_seed, instruction)
        get_full_cluster_layer(cluster_positions, grid, next_layer_seed, l)

    return next_robot_pos


def get_full_cluster_layer(
        cluster_positions: dict[int, set[tuple[int, int]]],
        grid: np.array,
        layer_seed: tuple[int, int],
        layer: int
):
    cluster_positions[layer] = set()
    i_next, _ = layer_seed
    for i, j in cluster_positions[layer - 1]:
        if grid[i_next, j] in ("[", "]"):
            cluster_positions[layer].add((i_next, j))
        if grid[i_next, j + 1] == "]" and (i, j + 1) not in cluster_positions[layer - 1]:
            cluster_positions[layer].add((i_next, j + 1))
        if grid[i_next, j - 1] == "[" and (i, j - 1) not in cluster_positions[layer - 1]:
            cluster_positions[layer].add((i_next, j - 1))


def is_not_blocked(grid: np.array, cluster_positions_layer: set[tuple[int, int]], direction: str) -> bool:
    if direction == "^":
        return all([grid[p[0] - 1, p[1]] != "#" for p in cluster_positions_layer])
    elif direction == "v":
        return all([grid[p[0] + 1, p[1]] != "#" for p in cluster_positions_layer])


def is_free_space(grid: np.array, cluster_positions_layer: set[tuple[int, int]], direction: str) -> bool:
    if direction == "^":
        return all([grid[p[0] - 1, p[1]] == "." for p in cluster_positions_layer])
    elif direction == "v":
        return all([grid[p[0] + 1, p[1]] == "." for p in cluster_positions_layer])


def create_wider_warehouse(grid: np.array) -> np.array:
    i_max, j_max = grid.shape
    new_grid = np.empty((i_max, j_max * 2), dtype=str)
    for i, line in enumerate(grid):
        for j, char in enumerate(line):
            if char == "#":
                new_grid[i, 2 * j] = "#"
                new_grid[i, 2 * j + 1] = "#"
            elif char == "O":
                new_grid[i, 2 * j] = "["
                new_grid[i, 2 * j + 1] = "]"
            elif char == ".":
                new_grid[i, 2 * j] = "."
                new_grid[i, 2 * j + 1] = "."
            elif char == "@":
                new_grid[i, 2 * j] = "@"
                new_grid[i, 2 * j + 1] = "."

    return new_grid


if __name__ == "__main__":
    with open("../inputs/15.txt", "r") as fh:
        in_text = fh.read()

    warehouse_grid, robot_movements = parse_input(in_text)

    # PART 1
    start = time.perf_counter()
    res = sum_gps_coordinates_after_robot_moving(warehouse_grid, robot_movements, push_boxes_part_1, "O")
    end = time.perf_counter()
    print(f"Part 1 Result: {res}. Took {(end - start) * 1000:.2f} ms.")

    # PART 2
    start = time.perf_counter()
    res = sum_gps_coordinates_after_robot_moving(
        create_wider_warehouse(warehouse_grid), robot_movements, push_boxes_part_2, "["
    )
    end = time.perf_counter()
    print(f"Part 2 Result: {res}. Took {(end - start) * 1000:.2f} ms.")
