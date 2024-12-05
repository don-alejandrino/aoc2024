import time

import numpy as np

EXAMPLE1 = """
MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
"""

VALID_NEIGHBORS = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
VALID_DIAGONAL_NEIGHBORS = [(1, 1), (-1, -1), (1, -1), (-1, 1)]


def parse_input(text: str) -> np.array:
    arr = []
    for line in text.strip().split("\n"):
        arr.append(list(line.strip()))

    return np.array(arr)


def get_num_valid_words_from_starting_point(
        letter_arr: np.array,
        starting_point: tuple[int, int],
        word="XMAS",
        shift: tuple[int, int] = None
) -> int:
    if letter_arr[starting_point] != word[0]:
        return 0
    elif len(word) == 1:
        return 1

    i_max, j_max = letter_arr.shape

    if shift is None:
        shifts = VALID_NEIGHBORS
    else:
        shifts = [shift]

    num_words = 0
    for shift in shifts:
        next_i = starting_point[0] + shift[0]
        next_j = starting_point[1] + shift[1]
        if 0 <= next_i < i_max and 0 <= next_j < j_max:
            num_words += get_num_valid_words_from_starting_point(
                letter_arr, (next_i, next_j), word[1:], shift
            )

    return num_words


def find_num_words(letter_arr: np.array, valid_word_finding_function) -> int:
    num_words = 0
    i_max, j_max = letter_arr.shape
    for i in range(i_max):
        for j in range(j_max):
            num_words += valid_word_finding_function(letter_arr, (i, j))

    return num_words


def is_valid_xmas_cross(letter_arr: np.array, pos: tuple[int, int]) -> int:
    i_max, j_max = letter_arr.shape
    if (
            letter_arr[pos] != "A" or
            pos[0] == 0 or
            pos[0] == i_max - 1 or
            pos[1] == 0 or
            pos[1] == j_max - 1
    ):
        return 0

    if (
            (
                    (letter_arr[pos[0] + 1, pos[1] + 1] == "M" and letter_arr[pos[0] - 1, pos[1] - 1] == "S") or
                    (letter_arr[pos[0] + 1, pos[1] + 1] == "S" and letter_arr[pos[0] - 1, pos[1] - 1] == "M")
            ) and
            (
                    (letter_arr[pos[0] + 1, pos[1] - 1] == "M" and letter_arr[pos[0] - 1, pos[1] + 1] == "S") or
                    (letter_arr[pos[0] + 1, pos[1] - 1] == "S" and letter_arr[pos[0] - 1, pos[1] + 1] == "M")
            )
    ):
        return 1

    return 0


if __name__ == "__main__":
    with open("../inputs/04.txt", "r") as fh:
        in_text = fh.read()

    letter_array = parse_input(in_text)

    # PART 1
    start = time.perf_counter()
    res = find_num_words(letter_array, get_num_valid_words_from_starting_point)
    end = time.perf_counter()
    print(f"Part 1 Result: {res}. Took {(end - start) * 1000:.2f} ms.")

    # PART 2
    start = time.perf_counter()
    res = find_num_words(letter_array, is_valid_xmas_cross)
    end = time.perf_counter()
    print(f"Part 2 Result: {res}. Took {(end - start) * 1000:.2f} ms.")
