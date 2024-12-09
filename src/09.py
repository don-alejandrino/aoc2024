import time

EXAMPLE1 = """
2333133121414131402
"""


def parse_input(text: str) -> list[int]:
    layout = []
    file_id = 0
    for i, block_size_str in enumerate(text.strip()):
        block_size = int(block_size_str)
        if i % 2 == 0:
            layout.extend([file_id] * block_size)
            file_id += 1
        else:
            layout.extend([-1] * block_size)

    return layout


def defragment_disk_part_1(layout: list[int]):
    layout = layout.copy()
    occupied_disk_size = len(layout) - layout.count(-1)
    free_space_idcs= []
    for i, block in enumerate(layout):
        if block == -1 and i < occupied_disk_size:
            free_space_idcs.append(i)

    for i, block in enumerate(layout[::-1]):
        idx = len(layout) - i - 1
        if free_space_idcs and block != -1:
            layout[free_space_idcs.pop(0)] = block
            layout[idx] = -1

    return layout


def defragment_disk_part_2(layout: list[int]):
    layout = layout.copy()
    current_file_id = layout[0]
    block_start_idx = 0
    file_blocks = {}
    for i, block in enumerate(layout):
        if block != current_file_id or i == len(layout) - 1:
            if current_file_id in file_blocks:
                file_blocks[current_file_id].append((block_start_idx, i - 1 if i < len(layout) - 1 else i))
            else:
                file_blocks[current_file_id] = [(block_start_idx, i - 1 if i < len(layout) - 1 else i)]
            block_start_idx = i
            current_file_id = block

    empty_blocks = file_blocks.pop(-1, [])
    for file_id, positions in reversed(file_blocks.items()):
        start_idx, end_idx = positions[0]
        file_size = end_idx - start_idx + 1
        for i, (s, e) in enumerate(empty_blocks):
            empty_space_size = e - s + 1
            if s <= start_idx:
                if empty_space_size >= file_size:
                    layout[s:s + file_size] = [file_id] * file_size
                    layout[start_idx:end_idx + 1] = [-1] * file_size
                    if empty_space_size > file_size:
                        empty_blocks[i] = (s + file_size, e)
                    else:
                        empty_blocks.pop(i)
                    break
            else:
                break


    return layout


def get_checksum(layout: list[int]):
    checksum = 0
    for i, block in enumerate(layout):
        if block != -1:
            checksum += block * i

    return checksum


if __name__ == "__main__":
    with open("../inputs/09.txt", "r") as fh:
        in_text = fh.read()

    disk_layout = parse_input(in_text)

    # PART 1
    start = time.perf_counter()
    res = get_checksum(defragment_disk_part_1(disk_layout))
    end = time.perf_counter()
    print(f"Part 1 Result: {res}. Took {(end - start) * 1000:.2f} ms.")

    # PART 2
    start = time.perf_counter()
    res = get_checksum(defragment_disk_part_2(disk_layout))
    end = time.perf_counter()
    print(f"Part 2 Result: {res}. Took {(end - start) * 1000:.2f} ms.")
