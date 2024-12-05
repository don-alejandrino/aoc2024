import time

EXAMPLE1 = """
47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
"""


def parse_input(text: str) -> tuple[list[tuple[int, int]], list[list[int]]]:
    rules_block, updates_block = text.strip().split("\n\n")
    rules = []
    for line in rules_block.strip().split("\n"):
        left, right = map(int, line.strip().split("|"))
        rules.append((left, right))
    updates = []
    for line in updates_block.strip().split("\n"):
        updates.append(list(map(lambda x: int(x.strip()), line.strip().split(","))))

    return rules, updates


def check_update(rules: list[tuple[int, int]], update: list[int]) -> bool:
    for i, page in enumerate(update):
        for rule in rules:
            if page == rule[0]:
                if rule[1] in update[:i]:
                    return False

    return True


def find_valid_updates(rules: list[tuple[int, int]], updates: list[list[int]]) -> int:
    out = 0
    for update in updates:
        if check_update(rules, update):
            out += update[len(update) // 2]

    return out


def prepare_pages_in_front_dict(rules: list[tuple[int, int]]) -> dict[int, set[int]]:
    all_pages = set()
    for rule in rules:
        all_pages.update(rule)
    pages_in_front = {}
    for page in all_pages:
        pages_in_front[page] = set()
        for rule in rules:
            if rule[1] == page:
                pages_in_front[page].add(rule[0])

    return pages_in_front


def get_numbers_in_front(pages_in_front_dict: dict[int, set[int]], update: set[int], page: int) -> int:
    number_of_pages_in_front = 0
    pages_to_visit = [page]
    for curr_page in pages_to_visit:
        before_pages = pages_in_front_dict[curr_page]
        for bp in before_pages:
            if bp in update and bp not in pages_to_visit:
                number_of_pages_in_front += 1
                pages_to_visit.append(bp)

    return number_of_pages_in_front


def sum_middle_numbers_of_reordered_updates(rules: list[tuple[int, int]], updates: list[list[int]]) -> int:
    out = 0
    pages_in_font_dict = prepare_pages_in_front_dict(rules)
    for update in updates:
        if not check_update(rules, update):
            for page in update:
                if get_numbers_in_front(pages_in_font_dict, set(update), page) == len(update) // 2:
                    out += page
                    break

    return out


if __name__ == "__main__":
    with open("../inputs/05.txt", "r") as fh:
        in_text = fh.read()

    ordering_rules, updated_pages = parse_input(in_text)

    # PART 1
    start = time.perf_counter()
    res = find_valid_updates(ordering_rules, updated_pages)
    end = time.perf_counter()
    print(f"Part 1 Result: {res}. Took {(end - start) * 1000:.2f} ms.")

    # PART 2
    start = time.perf_counter()
    res = sum_middle_numbers_of_reordered_updates(ordering_rules, updated_pages)
    end = time.perf_counter()
    print(f"Part 2 Result: {res}. Took {(end - start) * 1000:.2f} ms.")
