import re
import time

EXAMPLE1 = """
Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0
"""

EXAMPLE2 = """
Register A: 2024
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0
"""


def parse_input(text: str) -> tuple[list[int], list[int]]:
    registers = []
    for register in ("A", "B", "C"):
        registers.append(int(re.findall(rf"Register {register}: (\d+)", text)[0]))
    instructions = list(map(int, re.findall(r"Program: ((?:\d,)+\d)$", text)[0].split(",")))


    return registers, instructions


class Program:
    def __init__(self, registers: list[int], instructions: list[int]):
        self.registers = registers.copy()
        self.instructions = instructions
        self.pointer = 0
        self.opcodes = [
            lambda x: self.adv(x),
            lambda x: self.bxl(x),
            lambda x: self.bst(x),
            lambda x: self.jnz(x),
            lambda x: self.bxc(x),
            lambda x: self.out(x),
            lambda x: self.bdv(x),
            lambda x: self.cvd(x),
        ]
        self.output = []

    def combo(self, x: int) -> int:
        if x <= 3:
            return x
        else:
            return self.registers[x - 4]

    def adv(self, x: int):
        self.registers[0] = self.registers[0] >> self.combo(x)
        return 2

    def bxl(self, x: int):
        self.registers[1] = self.registers[1] ^ x
        return 2

    def bst(self, x: int):
        self.registers[1] = self.combo(x) % 8
        return 2

    def jnz(self, x: int):
        if self.registers[0] != 0:
            self.pointer = x
            return 0
        else:
            return 2

    def bxc(self, _: int):
        self.registers[1] = self.registers[1] ^ self.registers[2]
        return 2

    def out(self, x: int):
        self.output.append(self.combo(x) % 8)
        return 2

    def bdv(self, x: int):
        self.registers[1] = self.registers[0] >> self.combo(x)
        return 2

    def cvd(self, x: int):
        self.registers[2] = self.registers[0] >> self.combo(x)
        return 2

    def run(self):
        while self.pointer < len(self.instructions):
            opcode = self.instructions[self.pointer]
            arg = self.instructions[self.pointer + 1]
            pointer_increase = self.opcodes[opcode](arg)
            self.pointer += pointer_increase
        return self.output


def find_correct_register_a_value(registers: list[int], instructions: list[int]) -> int:
    """
    Looking at the problem input, we see that the program loops until the A register is zero.
    In each loop iteration, the program outputs exactly one value and the value of the A register
    is integer-divided by 8. Therefore, the initial value of the A register to produce an output
    of length equal to the length of the instructions list must be greater equal than
    8 ** (len(instructions) - 1) and less than 8 ** len(instructions).

    Furthermore, because of the structure of the problem input (the B and C registers are overwritten
    by values from the A register in each loop and therefore, there is no state transfer between two
    different loop iterations except the integer-division of the A register), the initial value of the
    A register must be of the form Σ_(i = 0)^L [n_i * 8 ** i], where 0 <= n_i < 8
    and L = len(instructions) - 1. The factors n_i can then be found by recursively reconstructing the
    desired output in reverse order.

    That is, let f(A) denote the output of the program for a given initial value of the A register.
    First, we find all possible n_L by solving f(n_L) == instructions[-1].
    In the next step, we find all possible combinations (n_L, n_(L - 1)) by solving
    f(n_L * 8 + n_(L - 1)) == instructions[-2:] ∀ valid n_L. Then, we find all possible combinations
    (n_L, n_(L - 1), n_(L - 2)) by solving
    f(n_L * 8 ** 2 + n_(L - 1) * 8 + n_(L - 2)) == instructions[-3:] ∀ valid pairs (n_L, n_(L - 1)),
    and so on. We repeat this process in total L times to find all possible combinations (n_L, ..., n_0).
    From these, we calculate all possible initial values of the A register and return the smallest of
    them.
    """

    possible_a_values = {-1: [0]}
    l = len(instructions)
    for i in range(l):
        for a_value in possible_a_values[i - 1]:
            for a in range(8):
                next_a_value = a_value * 8 + a
                registers[0] = next_a_value
                output = Program(registers, instructions).run()
                if output == instructions[-1 - i:]:
                    if i in possible_a_values.keys():
                        possible_a_values[i].append(next_a_value)
                    else:
                        possible_a_values[i]=[next_a_value]

    return min(possible_a_values[l-1])


if __name__ == "__main__":
    with open("../inputs/17.txt", "r") as fh:
        in_text = fh.read()

    program = parse_input(in_text)

    # PART 1
    start = time.perf_counter()
    res = ",".join([str(i) for i in Program(*program).run()])
    end = time.perf_counter()
    print(f"Part 1 Result: {res}. Took {(end - start) * 1000:.2f} ms.")

    # PART 2
    start = time.perf_counter()
    res = find_correct_register_a_value(*program)
    end = time.perf_counter()
    print(f"Part 2 Result: {res}. Took {(end - start) * 1000:.2f} ms.")
