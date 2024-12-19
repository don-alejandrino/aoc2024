import time

EXAMPLE1 = """
r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb
"""


def parse_input(text: str) -> tuple[set[str], list[str]]:
    towels_text, designs_text = text.strip().split("\n\n")
    towels = set(towels_text.strip().split(", "))

    designs = []
    for line in designs_text.strip().split("\n"):
        designs.append(line.strip())

    return towels, designs


def is_design_possible(design: str, towels: set[str]) -> bool:
    sub_designs = [design]
    while sub_designs:
        sub_design = sub_designs.pop(-1)
        for towel in towels:
            if sub_design.startswith(towel):
                next_sub_design = sub_design[len(towel):]
                if next_sub_design == "":
                    return True
                else:
                    sub_designs.append(sub_design[len(towel):])

    return False


def get_num_possibilities_to_create_design(
        design: str,
        towels: set[str],
        sub_design_possibilities: dict[str, int]
) -> int:
    num_possibilities = 0
    for towel in towels:
        if design.startswith(towel):
            sub_design = design[len(towel):]
            if sub_design == "":
                num_possibilities += 1
            else:
                try:
                    num_possibilities += sub_design_possibilities[sub_design]
                except KeyError:
                    num_possibilities += get_num_possibilities_to_create_design(
                        sub_design, towels, sub_design_possibilities
                    )
    sub_design_possibilities[design] = num_possibilities

    return num_possibilities


def get_num_possible_designs(towels: set[str], designs: list[str]) -> int:
    num_possible_designs = 0
    for design in designs:
        if is_design_possible(design, towels):
            num_possible_designs += 1

    return num_possible_designs


def get_overall_num_possibilities_to_create_designs(towels: set[str], designs: list[str]) -> int:
    num_overall_designs = 0
    for design in designs:
        num_overall_designs += get_num_possibilities_to_create_design(design, towels, {})

    return num_overall_designs


if __name__ == "__main__":
    with open("../inputs/19.txt", "r") as fh:
        in_text = fh.read()

    towel_puzzle = parse_input(in_text)

    # PART 1
    start = time.perf_counter()
    res = get_num_possible_designs(*towel_puzzle)
    end = time.perf_counter()
    print(f"Part 1 Result: {res}. Took {(end - start) * 1000:.2f} ms.")

    # PART 2
    start = time.perf_counter()
    res = get_overall_num_possibilities_to_create_designs(*towel_puzzle)
    end = time.perf_counter()
    print(f"Part 2 Result: {res}. Took {(end - start) * 1000:.2f} ms.")
