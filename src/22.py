import time
from collections import Counter

import numpy as np

EXAMPLE1 = """
1
10
100
2024
"""


def parse_input(text: str) -> list[int]:
    secrets = []
    for line in text.strip().split("\n"):
        secrets.append(int(line.strip()))

    return secrets


def generate_pseudorandom_number(seed: int, num_iterations:int) -> np.ndarray:
    sequence = np.empty(num_iterations, dtype=int)
    sequence[0] = seed
    for i in range(num_iterations):
        seed = ((seed * 64) ^ seed) % 16777216
        seed = ((seed // 32) ^ seed) % 16777216
        seed = ((seed * 2048) ^ seed) % 16777216
        sequence[i] = seed

    return sequence


def generate_pseudorandom_numbers_vectorized(seeds: np.ndarray, num_iterations:int) -> np.ndarray:
    for i in range(num_iterations):
        np.mod(np.bitwise_xor((seeds * 64), seeds), 16777216, out=seeds)
        np.mod(np.bitwise_xor((np.floor_divide(seeds, 32)), seeds), 16777216, out=seeds)
        np.mod(np.bitwise_xor((seeds * 2048), seeds), 16777216, out=seeds)

    return seeds


def sum_secret_numbers_after_iterations(initial_secrets: list[int], num_iterations: int) -> int:
    secrets = np.array(initial_secrets)

    return generate_pseudorandom_numbers_vectorized(secrets, num_iterations).sum()


def calculate_4_step_differences(
        initial_secrets: list[int],
        num_iterations: int
) -> list[dict[tuple[int, int, int, int], int]]:
    secrets = initial_secrets.copy()
    differences = []
    for secret in secrets:
        sequence = list(
            map(
                lambda n: int(str(n)[-1]),
                generate_pseudorandom_number(secret, num_iterations)
            )
        )
        diffs = np.diff(sequence, 1)
        diff_dict = {}
        for i in range(4, len(sequence)):
            price = sequence[i]
            diff_tuple = tuple(diffs[i - 4:i])
            # We collect only the first appearance of a differences pattern
            if diff_tuple not in diff_dict:
                diff_dict[diff_tuple] = price
        differences.append(diff_dict)

    # noinspection PyTypeChecker
    return differences


def get_max_num_bananas_by_finding_the_best_diff_sequence(
        differences: list[dict[tuple[int, int, int, int], int]]
) -> int:
    """
    Merge all the differences dictionaries of the buyers, adding the values of
    common keys. Then return the maximum value of the merged dictionary.
    """

    all_differences = Counter({})
    for diff_dict in differences:
        all_differences = Counter(diff_dict) + all_differences

    return max(all_differences.values())


if __name__ == "__main__":
    with open("../inputs/22.txt", "r") as fh:
        in_text = fh.read()

    secret_inputs = parse_input(in_text)

    # PART 1
    start = time.perf_counter()
    res = sum_secret_numbers_after_iterations(secret_inputs, 2000)
    end = time.perf_counter()
    print(f"Part 1 Result: {res}. Took {(end - start) * 1000:.2f} ms.")

    # PART 2
    start = time.perf_counter()
    res = get_max_num_bananas_by_finding_the_best_diff_sequence(
        calculate_4_step_differences(secret_inputs, 2000)
    )
    end = time.perf_counter()
    print(f"Part 2 Result: {res}. Took {(end - start) * 1000:.2f} ms.")
