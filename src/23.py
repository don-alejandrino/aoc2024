import itertools
import time
from typing import Callable

EXAMPLE1 = """
kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn
"""


def parse_input(text: str) -> dict[str, set[str]]:
    graph = {}
    for line in text.strip().split("\n"):
        left, right = line.strip().split("-")
        if left in graph:
            graph[left].add(right)
        else:
            graph[left] = {right}
        if right in graph:
            graph[right].add(left)
        else:
            graph[right] = {left}

    return graph


def dfs_recursion(
        node: str,
        start_node: str,
        previous_node: str | None,
        graph: dict[str, set[str]],
        recursion_level: int,
        max_recursion_level: int,
) -> list[list[str]]:
    cycle_chains = []
    if recursion_level < max_recursion_level:
        for neighbor in graph[node]:
            if neighbor != previous_node:
                for chain in dfs_recursion(
                    neighbor,
                    start_node,
                    node,
                    graph,
                    recursion_level + 1,
                    max_recursion_level,
                ):
                    if previous_node is None:
                        cycle_chains.append(chain)
                    else:
                        cycle_chains.append(chain + [previous_node])
            if neighbor == start_node and recursion_level == max_recursion_level - 1:
                cycle_chains.append([node, previous_node])

    return cycle_chains


def get_cycles_including_t_nodes(
        start_node: str,
        graph: dict[str, set[str]],
        cycle_length: int,
        chain_relevancy_criterion: Callable[[list[str]], bool],
) -> int:
    cycle_chains = dfs_recursion(start_node, start_node, None, graph, 0, cycle_length)
    relevant_chains = [c for c in cycle_chains if chain_relevancy_criterion(c)]

    # Each cycle is detected twice (in both directions)
    return len(relevant_chains) // 2


def get_all_cycles(
        graph: dict[str, set[str]],
        cycle_length: int,
        chain_relevancy_criterion: Callable[[list[str]], bool],
) -> int:
    num_cycles = 0
    for start_node in graph.keys():
        num_cycles += get_cycles_including_t_nodes(start_node, graph, cycle_length, chain_relevancy_criterion)

    # Each cycle is detected cycle_length times (starting from each node in the cycle)
    return num_cycles // cycle_length


def does_chain_contain_t(chain: list[str]) -> bool:
    for node in chain:
        if node.startswith("t"):
            return True

    return False


def get_largest_fully_connected_cluster(graph: dict[str, set[str]]) -> str:
    for n in range(min(len(v) for v in graph.values())):
        for node, neighbors in graph.items():
            for neighbor_subset in itertools.combinations(neighbors, len(neighbors) - n):
                for neighbor in neighbor_subset:
                    expected_neighbors = set(neighbor_subset)
                    expected_neighbors.remove(neighbor)
                    expected_neighbors.add(node)
                    if not expected_neighbors.issubset(graph[neighbor]):
                        break
                else:
                    return ",".join(sorted(neighbor_subset + (node,)))


if __name__ == "__main__":
    with open("../inputs/23.txt", "r") as fh:
        in_text = fh.read()

    network_graph = parse_input(in_text)

    # PART 1
    start = time.perf_counter()
    res = get_all_cycles(network_graph, 3, does_chain_contain_t)
    end = time.perf_counter()
    print(f"Part 1 Result: {res}. Took {(end - start) * 1000:.2f} ms.")

    # PART 2
    start = time.perf_counter()
    res = get_largest_fully_connected_cluster(network_graph)
    end = time.perf_counter()
    print(f"Part 2 Result: {res}. Took {(end - start) * 1000:.2f} ms.")
