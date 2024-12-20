import time
from queue import PriorityQueue

EXAMPLE1 = """
5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0
"""


class PathNotFoundError(Exception):
    pass


def parse_input(text: str) -> list[tuple[int, int]]:
    coords = []
    for lines in text.strip().split("\n"):
        coords.append(tuple(map(lambda x: int(x.strip()), lines.strip().split(","))))

    # noinspection PyTypeChecker
    return coords


def find_shortest_path(
        start_coords: tuple[int, int],
        target_coords: tuple[int, int],
        byte_coords: list[tuple[int, int]],
        grid_size: int,
        num_already_fallen_bytes: int
) -> int:
    blocked_grid_coords = set(byte_coords[:num_already_fallen_bytes])

    unvisited_nodes = PriorityQueue()
    # Item structure of unvisited_nodes:
    # Tuple(distance, Tuple(<node coordinates on the grid>))
    unvisited_nodes.put((0, start_coords))
    visited_nodes = {}

    while unvisited_nodes.queue:
        current_distance, current_coords = unvisited_nodes.get()
        if visited_nodes.get(current_coords) is not None:
            # Node has already been visited
            continue
        if current_coords == target_coords:
            return current_distance
        neighbors = [
            (current_coords[0] + 1, current_coords[1]),
            (current_coords[0] - 1, current_coords[1]),
            (current_coords[0], current_coords[1] + 1),
            (current_coords[0], current_coords[1] - 1)
        ]
        for next_coords in neighbors:
            if visited_nodes.get(next_coords) is None:
                # Node hasn't already been visited
                if (
                        0 <= next_coords[0] < grid_size and 0 <= next_coords[1] < grid_size and
                        next_coords not in blocked_grid_coords
                ):
                    new_distance = current_distance + 1
                    unvisited_nodes.put((new_distance, next_coords))

        visited_nodes[current_coords] = current_distance

    raise PathNotFoundError("No path found.")


def find_first_blocking_byte(
        start_coords: tuple[int, int],
        target_coords: tuple[int, int],
        byte_coords: list[tuple[int, int]],
        grid_size: int,
        last_known_non_blocking_number_of_bytes: int
) -> tuple[int, int]:
    for i in range(last_known_non_blocking_number_of_bytes, len(byte_coords)):
        # Floodfill might be faster here, but it's easier to reuse the function from part 1
        try:
            find_shortest_path(start_coords, target_coords, byte_coords, grid_size, i)
        except PathNotFoundError:
            return byte_coords[i - 1]
    else:
        raise ValueError("No blocking byte found.")


if __name__ == "__main__":
    with open("../inputs/18.txt", "r") as fh:
        in_text = fh.read()

    byte_positions = parse_input(in_text)

    # PART 1
    start = time.perf_counter()
    res = find_shortest_path(
        (0, 0),
        (70, 70),
        byte_positions,
        71,
        1024,
    )
    end = time.perf_counter()
    print(f"Part 1 Result: {res}. Took {(end - start) * 1000:.2f} ms.")

    # PART 2
    start = time.perf_counter()
    res = ",".join(
        [
            str(i) for i in find_first_blocking_byte(
                (0, 0),
                (70, 70),
                byte_positions,
                71,
                1024,
            )
        ]
    )
    end = time.perf_counter()
    print(f"Part 2 Result: {res}. Took {(end - start) * 1000:.2f} ms.")
