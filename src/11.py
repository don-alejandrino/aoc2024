import math
import time


EXAMPLE1 = """
125 17
"""


def parse_input(text: str) -> list[int]:
    return list(map(lambda x : int(x.strip()), text.strip().split(" ")))


def transform_stone(stone: int) -> list[int]:
    new_stones = []
    if stone == 0:
        new_stones.append(1)
    else:
        num_digits = int(math.log10(stone)) + 1
        if num_digits % 2 == 0:
            next_stones = [stone // 10 ** (num_digits // 2), stone % 10 ** (num_digits // 2)]
            new_stones.extend(next_stones)
        else:
            next_stone = stone * 2024
            new_stones.append(next_stone)

    return new_stones


def blink_n_times_and_get_number_of_stones_total(stones: list[int], n: int) -> int:
    result = 0
    lookup = {}
    for stone in stones:
        result += blink_n_times_and_get_number_of_stones(stone, n, lookup)

    return result


def blink_n_times_and_get_number_of_stones(start_stone: int, n: int, lookup: dict[tuple[int, int], int]) -> int:
    if n == 0:
        return 1
    try:
        return lookup[(start_stone, n)]
    except KeyError:
        result = 0
        for stone in transform_stone(start_stone):
            result += blink_n_times_and_get_number_of_stones(stone, n - 1, lookup)

        lookup[(start_stone, n)] = result
        return result


if __name__ == "__main__":
    with open("../inputs/11.txt", "r") as fh:
        in_text = fh.read()

    stone_row = parse_input(in_text)

    # PART 1
    start = time.perf_counter()
    res = blink_n_times_and_get_number_of_stones_total(stone_row, 25)
    end = time.perf_counter()
    print(f"Part 1 Result: {res}. Took {(end - start) * 1000:.2f} ms.")

    # PART 2
    start = time.perf_counter()
    res = blink_n_times_and_get_number_of_stones_total(stone_row, 75)
    end = time.perf_counter()
    print(f"Part 2 Result: {res}. Took {(end - start) * 1000:.2f} ms.")
