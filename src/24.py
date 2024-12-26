import time

import graphviz

EXAMPLE1 = """
x00: 1
x01: 0
x02: 1
x03: 1
x04: 0
y00: 1
y01: 1
y02: 1
y03: 1
y04: 1

ntg XOR fgs -> mjb
y02 OR x01 -> tnw
kwq OR kpj -> z05
x00 OR x03 -> fst
tgd XOR rvg -> z01
vdt OR tnw -> bfw
bfw AND frj -> z10
ffh OR nrd -> bqk
y00 AND y03 -> djm
y03 OR y00 -> psh
bqk OR frj -> z08
tnw OR fst -> frj
gnj AND tgd -> z11
bfw XOR mjb -> z00
x03 OR x00 -> vdt
gnj AND wpb -> z02
x04 AND y00 -> kjc
djm OR pbm -> qhw
nrd AND vdt -> hwm
kjc AND fst -> rvg
y04 OR y02 -> fgs
y01 AND x02 -> pbm
ntg OR kjc -> kwq
psh XOR fgs -> tgd
qhw XOR tgd -> z09
pbm OR djm -> kpj
x03 XOR y03 -> ffh
x00 XOR y04 -> ntg
bfw OR bqk -> z06
nrd XOR fgs -> wpb
frj XOR qhw -> z04
bqk OR frj -> z07
y03 OR x01 -> nrd
hwm AND bqk -> z03
tgd XOR rvg -> z12
tnw OR pbm -> gnj
"""


def parse_input(text: str) -> tuple[dict[str, bool], dict[tuple[str, str, str], str]]:
    cables = {}
    gates = {}
    initial_cables_block, gates_block = text.strip().split("\n\n")
    for line in initial_cables_block.strip().split("\n"):
        cable_id, value = line.strip().split(": ")
        cables[cable_id] = bool(int(value))
    for line in gates_block.strip().split("\n"):
        in1, operation, in2, _, out = line.strip().split(" ")
        gates[(in1, in2, operation)] = out

    return cables, gates


def evaluate_gate(in1: bool, in2: bool, operation: str) -> bool:
    if operation == "AND":
        return in1 and in2
    elif operation == "OR":
        return in1 or in2
    elif operation == "XOR":
        return in1 ^ in2
    else:
        raise ValueError(f"Invalid operation: {operation}")


def evaluate_circuit(
        initial_cables: dict[str, bool],
        gates: dict[tuple[str, str, str], str],
) -> dict[str, bool]:
    cables = initial_cables.copy()
    gates = gates.copy()
    while gates:
        stack_reduced = False
        for (in1, in2, operation), out in gates.copy().items():
            if cables.get(in1) is not None and cables.get(in2) is not None:
                gates.pop((in1, in2, operation))
                stack_reduced = True
                cables[out] = evaluate_gate(cables[in1], cables[in2], operation)
        if not stack_reduced:
            raise RecursionError("Not all gates can be activated.")

    return cables


def get_output_value(cables: dict[str, bool]) -> bool:
    out = 0
    n = 0
    for cable_id, value in sorted(cables.items(), key=lambda x: x[0]):
        if cable_id.startswith("z"):
            out += int(value) << n
            n += 1

    return out


def visualize_circuit(gates: dict[tuple[str, str, str], str]):
    dot = graphviz.Digraph()
    for (in1, in2, operation), out in gates.items():
        dot.node(out, f"{operation}", shape="box")
        if out.startswith("z"):
            dot.node(out + "_output", out)
            dot.edge(out, out + "_output", out)
        dot.edge(in1, out, in1)
        dot.edge(in2, out, in2)
    dot.render('graph', view=True)


def identify_faulty_wirings(gates: dict[tuple[str, str, str], str]) -> set[str]:
    num_output_bits = len([out for out in gates.values() if out.startswith("z")])
    incorrect_wirings = set()
    inv_gates = {v: k for k, v in gates.items()}
    for bit in range(num_output_bits):
        incorrect_wirings.update(find_incorrect_wirings_recursively(
            out_wire=f"z{bit:02d}",
            inv_gates_mapping=inv_gates,
            downstream_operation=None,
            highest_bit_z_wire=max([out for out in gates.values() if out.startswith("z")]),
            recursion_depth=0,
            max_recursion_depth=3,
        ))

    return incorrect_wirings


def is_wiring_incorrect(
        in_wire_1: str,
        in_wire_2: str,
        operation: str,
        out_wire: str,
        downstream_operation: str | None,
        highest_z_wire: str,
) -> bool:
    """
    These rules are somewhat empiric and are derived from an analysis of the puzzle input's
    structure, more specifically from comparing it with the general mode of operation of a
    binary adder.
    """

    return (
        # Except for the highest-bit z wire, all z wires must be the output of an XOR gate
        (
            out_wire.startswith("z") and out_wire != highest_z_wire and operation != "XOR"
        ) or

        # XOR gates that don't feed into z wires must have inputs from x and y wires
        (
            operation == "XOR" and not out_wire.startswith("z") and not (
                (in_wire_1.startswith("x") and in_wire_2.startswith("y")) or
                (in_wire_1.startswith("y") and in_wire_2.startswith("x"))
            )
        ) or

        # XOR gates must not feed into OR gates
        (
            operation == "XOR" and downstream_operation == "OR"
        ) or

        # Except for the LSB input (x00 and y00 wires), AND gates must feed into OR gates only
        (
            operation == "AND" and downstream_operation != "OR" and not (
                (in_wire_1 == "x00" and in_wire_2 == "y00") or
                (in_wire_1 == "y00" and in_wire_2 == "x00")
            )
        )
    )


def find_incorrect_wirings_recursively(
        out_wire: str,
        inv_gates_mapping: dict[str, tuple[str, str, str]],
        downstream_operation: str | None,
        highest_bit_z_wire: str,
        recursion_depth: int,
        max_recursion_depth: int,
) -> set[str]:
    if recursion_depth >= max_recursion_depth:
        return set()
    incorrect_wires = set()
    gate_info = inv_gates_mapping.get(out_wire)
    if gate_info is not None:
        (in_wire_1, in_wire_2, operation) = gate_info
        if is_wiring_incorrect(
                in_wire_1, in_wire_2, operation, out_wire, downstream_operation, highest_bit_z_wire
        ):
            incorrect_wires.add(out_wire)
        for in_wire in (in_wire_1, in_wire_2):
            incorrect_wires.update(
                find_incorrect_wirings_recursively(
                    in_wire,
                    inv_gates_mapping,
                    operation,
                    highest_bit_z_wire,
                    recursion_depth + 1,
                    max_recursion_depth,
                )
            )

    return incorrect_wires


if __name__ == "__main__":
    with open("../inputs/24.txt", "r") as fh:
        in_text = fh.read()

    circuit_cables, circuit_gates = parse_input(in_text)

    # PART 1
    start = time.perf_counter()
    res = get_output_value(evaluate_circuit(circuit_cables, circuit_gates))
    end = time.perf_counter()
    print(f"Part 1 Result: {res}. Took {(end - start) * 1000:.2f} ms.")

    # PART 2
    visualize_circuit(circuit_gates)
    start = time.perf_counter()
    res = ",".join(sorted(identify_faulty_wirings(circuit_gates)))
    end = time.perf_counter()
    print(f"Part 2 Result: {res}. Took {(end - start) * 1000:.2f} ms.")
