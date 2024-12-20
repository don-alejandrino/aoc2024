import time
from queue import PriorityQueue

import numpy as np

EXAMPLE1 = """
###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############
"""


def parse_input(text: str) -> tuple[np.array, tuple[int, int], tuple[int, int]]:
    mat = []
    start_pos = end_pos = None
    for i, line in enumerate(text.strip().split("\n")):
        row = []
        for j, char in enumerate(line.strip()):
            if char == ".":
                row.append(0)
            elif char == "#":
                row.append(1)
            elif char == "S":
                row.append(0)
                start_pos = (i, j)
            elif char == "E":
                row.append(0)
                end_pos = (i, j)
        mat.append(row)

    return np.array(mat, dtype=bool), start_pos, end_pos


def take_step(
        position: tuple[int, int],
        grid: np.array,
        visited: set[tuple[int, int]] | dict[tuple[int, int], int]
) -> tuple[int, int]:
    for neighbor in [
        (position[0] + 1, position[1]),
        (position[0] - 1, position[1]),
        (position[0], position[1] + 1),
        (position[0], position[1] - 1),
    ]:
        if not grid[neighbor] and neighbor not in visited:
            return neighbor

    raise ValueError("Path blocked.")


def find_shortest_cheat_paths_if_a_cheat_could_only_go_through_walls(
        position: tuple[int, int],
        grid: np.array,
        visited_positions_on_course: set[tuple[int, int]],
        max_cheat_length: int,
) -> dict[tuple[int, int], int]:
    cheat_endpoints = {}
    i_max, j_max = grid.shape
    unvisited_nodes = PriorityQueue()
    # Item structure of unvisited_nodes:
    # Tuple(distance, Tuple(<node coordinates on the grid>))
    unvisited_nodes.put((0, position))
    visited_nodes = {}

    while unvisited_nodes.queue:
        current_distance, current_coords = unvisited_nodes.get()
        if visited_nodes.get(current_coords) is not None:
            # Node has already been visited
            continue
        if current_distance >= max_cheat_length:
            break
        neighbors = [
            (current_coords[0] + 1, current_coords[1]),
            (current_coords[0] - 1, current_coords[1]),
            (current_coords[0], current_coords[1] + 1),
            (current_coords[0], current_coords[1] - 1)
        ]
        for next_coords in neighbors:
            if 0 <= next_coords[0] < i_max and 0 <= next_coords[1] < j_max:
                next_distance = current_distance + 1
                if grid[next_coords]:
                    if visited_nodes.get(next_coords) is None:
                        # Node hasn't already been visited
                        unvisited_nodes.put((next_distance, next_coords))
                elif (
                        next_coords not in visited_positions_on_course and
                        next_distance > 1 and
                        next_coords not in cheat_endpoints.keys()
                ):
                    # "Cheats" of length 1 are not going through any walls,
                    # but just following the course. In addition, we just register
                    # the first encounter of an endpoint and ignore later ones,
                    # because the first encounter corresponds to the shortest path
                    cheat_endpoints[next_coords] = next_distance

        visited_nodes[current_coords] = current_distance

    return cheat_endpoints


def pass_course_and_find_number_of_good_enough_cheats_if_a_cheat_could_only_go_through_walls(
        course_grid: np.array,
        start_coords: tuple[int, int],
        end_coords: tuple[int, int],
        max_cheat_length: int,
        min_cheat_savings: int = 100,
) -> int:
    """
    I initially understood the puzzle in such a way that any cheat must "live"
    only within walls, i.e., can't cross any open space. However, as it turns
    out, this was wrong, making the correct solution much easier. I still keep
    this function here which should be correct if cheat paths were confined to
    walls only.
    """
    position = start_coords
    visited = set()
    cheat_step_counter = {}
    saved_steps = []
    while True:
        visited.add(position)

        # Collect saved steps for cheats that led to the current position
        current_cheat_steps = cheat_step_counter.pop(position, None)
        if current_cheat_steps is not None:
            # The number of saved steps for a cheat is the number of steps on the
            # original path between the cheat's start and end point, minus two
            # steps for the cheat itself. If a cheat does not save anything,
            # ignore it
            saved_steps.extend([ccs for ccs in current_cheat_steps if ccs > 0])

        # Find new cheats that start from the current position
        for endpoint, cheat_steps in find_shortest_cheat_paths_if_a_cheat_could_only_go_through_walls(
                position, course_grid, visited, max_cheat_length
        ).items():
            if endpoint in cheat_step_counter:
                cheat_step_counter[endpoint].append(-cheat_steps)
            else:
                cheat_step_counter[endpoint] = [-cheat_steps]

        # Advance on the course and increase step counter for each "active" cheat
        # (i.e., the ones with visited starting point, but not yet visited end point)
        if position == end_coords:
            break
        position = take_step(position, course_grid, visited)
        for cheat_steps in cheat_step_counter.values():
            for i, cheat_path_length in enumerate(cheat_steps):
                cheat_steps[i] += 1

    return len([item for item in saved_steps if item >= min_cheat_savings])


def pass_course_and_find_number_of_good_enough_cheats(
        course_grid: np.array,
        start_coords: tuple[int, int],
        end_coords: tuple[int, int],
        max_cheat_length: int,
        min_cheat_savings: int = 100,
) -> int:
    num_steps_to_position = {}
    position = start_coords
    saved_steps = []
    step_counter = 0
    while True:
        for i in range(-max_cheat_length, max_cheat_length + 1):
            for j in range(-max_cheat_length, max_cheat_length + 1):
                if i != 0 or j!= 0:
                    test_position = (position[0] + i, position[1] + j)
                    steps_on_path = num_steps_to_position.get(test_position)
                    if steps_on_path is not None:
                        shortest_path_to_test_position = abs(i) + abs(j)
                        if (
                                # We still need to filter here if the shortest path is indeed shorter than
                                # max_cheat_length, because our heuristic rectangular search region includes
                                # positions that can't be reached in max_cheat_length steps
                                shortest_path_to_test_position <= max_cheat_length and
                                shortest_path_to_test_position < step_counter - steps_on_path
                        ):
                            saved_steps.append(step_counter - steps_on_path - shortest_path_to_test_position)
        num_steps_to_position[position] = step_counter
        if position == end_coords:
            break
        position = take_step(position, course_grid, num_steps_to_position)
        step_counter += 1

    return len([item for item in saved_steps if item >= min_cheat_savings])


if __name__ == "__main__":
    with open("../inputs/20.txt", "r") as fh:
        in_text = fh.read()

    course = parse_input(in_text)

    # PART 1
    start = time.perf_counter()
    res = pass_course_and_find_number_of_good_enough_cheats(*course, max_cheat_length=2)
    end = time.perf_counter()
    print(f"Part 1 Result: {res}. Took {(end - start) * 1000:.2f} ms.")

    # PART 2
    start = time.perf_counter()
    res = pass_course_and_find_number_of_good_enough_cheats(*course, max_cheat_length=20)
    end = time.perf_counter()
    print(f"Part 2 Result: {res}. Took {(end - start) * 1000:.2f} ms.")
