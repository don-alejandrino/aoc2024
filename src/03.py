import re
import time

EXAMPLE1 = """
xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))
"""

EXAMPLE2 = """
xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))
"""

def parse_input(text: str) -> str:
    input = ""
    for line in text.strip().split("\n"):
        input += line.strip()

    return input


def find_active_sections(memory: str) -> list[str]:
    sections = re.findall(r"(?:^|do\(\))(.*?)(?:$|don't\(\))", memory)

    return sections


def find_valid_statements(memory: str) -> list[tuple[int, int]]:
    valid_statements = re.findall(r"mul\((\d+),(\d+)\)", memory)

    return list(map(lambda x: (int(x[0]), int(x[1])), valid_statements))


def add_multiplications(multiplication_statements: list[tuple[int, int]]) -> int:
    result = 0
    for item in multiplication_statements:
        result += item[0] * item[1]

    return result


if __name__ == "__main__":
    with open("../inputs/03.txt", "r") as fh:
        in_text = fh.read()

    statements = parse_input(in_text)

    # PART 1
    start = time.perf_counter()
    res = add_multiplications(find_valid_statements(statements))
    end = time.perf_counter()
    print(f"Part 1 Result: {res}. Took {(end - start) * 1000:.2f} ms.")

    # PART 2
    start = time.perf_counter()
    active_sections = find_active_sections(statements)
    res = 0
    for section in active_sections:
        res += add_multiplications(find_valid_statements(section))
    end = time.perf_counter()
    print(f"Part 2 Result: {res}. Took {(end - start) * 1000:.2f} ms.")
