import re
import time
from collections import Counter

import numpy as np

EXAMPLE1 = """
3   4
4   3
2   5
1   3
3   9
3   3
"""


def parse_input(text: str, ignore_z: bool = True) -> tuple[list[int], list[int]]:
    left_list = []
    right_list = []
    for line in text.strip().split("\n"):
        left_id, right_id = re.split(r"\s+", line.strip())
        left_list.append(int(left_id.strip()))
        right_list.append(int(right_id.strip()))
    assert len(left_list) == len(right_list), "Left and right list must have the same length."

    return left_list, right_list


def get_distances(left_list: list[int], right_list: list[int]) -> np.array:
    left_ids = np.sort(np.array(left_list, dtype=int))
    right_ids = np.sort(np.array(right_list, dtype=int))

    return np.abs(left_ids - right_ids)


def get_total_distance(distances: np.array) -> int:
    return distances.sum()


def get_similarity_score(left_list: list[int], right_list: list[int]) -> int:
    score = 0
    right_frequencies = Counter(right_list)
    for left_id in left_list:
        score += left_id * right_frequencies.get(left_id, 0)

    return score


if __name__ == "__main__":
    with open("../inputs/01.txt", "r") as fh:
        in_text = fh.read()

    lists = parse_input(in_text)

    # PART 1
    start = time.perf_counter()
    res = get_total_distance(get_distances(*lists))
    end = time.perf_counter()
    print(f"Part 1 Result: {res}. Took {(end - start) * 1000:.2f} ms.")

    # PART 2
    start = time.perf_counter()
    res = get_similarity_score(*lists)
    end = time.perf_counter()
    print(f"Part 2 Result: {res}. Took {(end - start) * 1000:.2f} ms.")
