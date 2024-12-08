import time
from itertools import combinations
from typing import Callable

EXAMPLE1 = """
............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
"""


def parse_input(text: str) -> tuple[dict[str, list[tuple[int, int]]], tuple[int, int]]:
    antenna_positions_dict = {}
    rows = text.strip().split("\n")
    i_max = len(rows) - 1
    j_max = len(rows[0]) - 1

    for i, line in enumerate(rows):
        for j, char in enumerate(line.strip()):
            if char != ".":
                if char in antenna_positions_dict:
                    antenna_positions_dict[char].append((i, j))
                else:
                    antenna_positions_dict[char] = [(i, j)]

    return antenna_positions_dict, (i_max, j_max)


def find_antinodes_part_1(
        antenna_of_single_type_positions: list[tuple[int, int]],
        antinodes: set[tuple[int, int]],
        grid_size: tuple[int, int]
):
    i_max, j_max = grid_size
    if len(antenna_of_single_type_positions) >= 2:
        antenna_pairs = combinations(antenna_of_single_type_positions, 2)
        for pair in antenna_pairs:
            diff_vec = (pair[1][0] - pair[0][0], pair[1][1] - pair[0][1])
            antinode_1 = (pair[1][0] + diff_vec[0], pair[1][1] + diff_vec[1])
            antinode_2 = (pair[0][0] - diff_vec[0], pair[0][1] - diff_vec[1])
            if 0 <= antinode_1[0] <= i_max and 0 <= antinode_1[1] <= j_max:
                antinodes.add(antinode_1)
            if 0 <= antinode_2[0] <= i_max and 0 <= antinode_2[1] <= j_max:
                antinodes.add(antinode_2)


def find_antinodes_part_2(
        antenna_of_single_type_positions: list[tuple[int, int]],
        antinodes: set[tuple[int, int]],
        grid_size: tuple[int, int]
):
    i_max, j_max = grid_size
    if len(antenna_of_single_type_positions) >= 2:
        antenna_pairs = combinations(antenna_of_single_type_positions, 2)
        for pair in antenna_pairs:
            antinodes.update(pair)
            diff_vec = (pair[1][0] - pair[0][0], pair[1][1] - pair[0][1])

            antinode_1 = (pair[1][0] + diff_vec[0], pair[1][1] + diff_vec[1])
            while 0 <= antinode_1[0] <= i_max and 0 <= antinode_1[1] <= j_max:
                antinodes.add(antinode_1)
                antinode_1 = (antinode_1[0] + diff_vec[0], antinode_1[1] + diff_vec[1])

            antinode_2 = (pair[0][0] - diff_vec[0], pair[0][1] - diff_vec[1])
            while 0 <= antinode_2[0] <= i_max and 0 <= antinode_2[1] <= j_max:
                antinodes.add(antinode_2)
                antinode_2 = (antinode_2[0] - diff_vec[0], antinode_2[1] - diff_vec[1])


def get_num_unique_antinode_positions(
        antenna_positions_dict: dict[str, list[tuple[int, int]]],
        grid_size: tuple[int, int],
        antinode_detection_function: Callable[[list[tuple[int, int]], set[tuple[int, int]], tuple[int, int]], None]
) -> int:
    antinodes = set()
    for antenna_positions in antenna_positions_dict.values():
        antinode_detection_function(antenna_positions, antinodes, grid_size)

    return len(antinodes)


if __name__ == "__main__":
    with open("../inputs/08.txt", "r") as fh:
        in_text = fh.read()

    all_antenna_positions, grid_limits = parse_input(in_text)

    # PART 1
    start = time.perf_counter()
    res = get_num_unique_antinode_positions(all_antenna_positions, grid_limits, find_antinodes_part_1)
    end = time.perf_counter()
    print(f"Part 1 Result: {res}. Took {(end - start) * 1000:.2f} ms.")

    # PART 2
    start = time.perf_counter()
    res = get_num_unique_antinode_positions(all_antenna_positions, grid_limits, find_antinodes_part_2)
    end = time.perf_counter()
    print(f"Part 2 Result: {res}. Took {(end - start) * 1000:.2f} ms.")
