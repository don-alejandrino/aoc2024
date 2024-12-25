import itertools
import time


EXAMPLE1 = """
#####
.####
.####
.####
.#.#.
.#...
.....

#####
##.##
.#.##
...##
...#.
...#.
.....

.....
#....
#....
#...#
#.#.#
#.###
#####

.....
.....
#.#..
###..
###.#
###.#
#####

.....
.....
.....
#....
#.#..
#.#.#
#####
"""


def parse_input(text: str) -> tuple[list[list[int]], list[list[int]]]:
    locks = []
    keys = []
    for block in text.strip().split("\n\n"):
        lines = block.strip().split("\n")
        columns = [0] * len(lines[0])
        if all(char == "#" for char in lines[0]):
            for line in lines[1:]:
                for i, pin in enumerate(line):
                    if pin == "#":
                       columns[i] += 1
            locks.append(columns)
        else:
            for line in lines[:-1]:
                for i, pin in enumerate(line):
                    if pin == "#":
                        columns[i] += 1
            keys.append(columns)

    return locks, keys


def find_num_possible_combinations(locks: list[list[int]], keys: list[list[int]], max_height: int = 5) -> int:
    out = 0
    for lock, key in itertools.product(locks, keys):
        if all(lock[i] + key[i] <= max_height for i in range(len(lock))):
            out += 1

    return out


if __name__ == "__main__":
    with open("../inputs/25.txt", "r") as fh:
        in_text = fh.read()

    lock_schematics, key_schematics = parse_input(in_text)

    # PART 1
    start = time.perf_counter()
    res = find_num_possible_combinations(lock_schematics, key_schematics)
    end = time.perf_counter()
    print(f"Part 1 Result: {res}. Took {(end - start) * 1000:.2f} ms.")
