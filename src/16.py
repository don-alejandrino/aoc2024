import time
from queue import PriorityQueue

import numpy as np

EXAMPLE1 = """
###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############
"""

EXAMPLE2 = """
#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################
"""

# up: 0, right: 1, down: 2, left: 3
ORIENTATIONS = [
    {0, 1, 3},
    {0, 1, 2},
    {1, 2, 3},
    {0, 2, 3},
]

DISPLACEMENTS = [
    (lambda c: (c[0] - 1, c[1])),
    (lambda c: (c[0], c[1] + 1)),
    (lambda c: (c[0] + 1, c[1])),
    (lambda c: (c[0], c[1] - 1)),
]

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


def find_all_shortest_paths_dijkstra(
        grid: np.ndarray,
        start_coords: tuple[int, int],
        target_coords: tuple[int, int],
) -> tuple[int, int]:
    min_candidates = []

    nodes_to_visit = PriorityQueue()
    # Item structure of nodes_to_visit:
    # tuple(
    #     distance, tuple(
    #         list(<node history>),
    #         <from which direction was the node entered>
    #     )
    # )
    nodes_to_visit.put((0, ([start_coords], 1)))
    visited_nodes = {}

    while nodes_to_visit.queue:
        current_distance, (node_history, last_direction) = nodes_to_visit.get()
        current_coords = node_history[-1]
        if visited_nodes.get((current_coords, last_direction), np.inf) < current_distance:
            # We reject to re-inspect the node if a shorter path to it is already known,
            # but NOT if there is an already another known path of the same length
            continue
        if current_coords == target_coords:
            if not min_candidates or current_distance <= min(min_candidates, key=lambda x: x[0])[0]:
                min_candidates.append((current_distance, node_history))
            else:
                # Shortest paths are always found first
                break
        for next_dir in ORIENTATIONS[last_direction]:
            if next_dir == last_direction:
                step_cost = 1
            else:
                step_cost = 1001
            next_coords = DISPLACEMENTS[next_dir](current_coords)
            if visited_nodes.get((next_coords, next_dir)) is None:
                # Node hasn't already been visited
                if not grid[next_coords]:
                    # Note that here, a reindeer is considered to be stuck in a dead end
                    # and its path can't be continued. Although in reality, it might turn
                    # by 180 degrees and go back, such a move can't result in a shortest
                    # path anymore. Therefore, it is safe to ignore these paths
                    nodes_to_visit.put((current_distance + step_cost, (node_history + [next_coords], next_dir)))

        visited_nodes[(current_coords, last_direction)] = current_distance

    shortest_path_length = min(min_candidates, key=lambda x: x[0])[0]
    shortest_paths = [item[1] for item in min_candidates if item[0] == shortest_path_length]
    num_visited_nodes_on_all_shortest_paths = len(set([coords for path in shortest_paths for coords in path]))

    return shortest_path_length, num_visited_nodes_on_all_shortest_paths


if __name__ == "__main__":
    with open("../inputs/16.txt", "r") as fh:
        in_text = fh.read()

    maze_input = parse_input(in_text)

    # PART 1 + 2
    start = time.perf_counter()
    res = find_all_shortest_paths_dijkstra(*maze_input)
    end = time.perf_counter()
    print(f"Part 1 Result: {res[0]}. Part 2 Result: {res[1]}. Took {(end - start) * 1000:.2f} ms.")
