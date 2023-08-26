import pytest
import random

from typing import Generator
from utils import int_to_bit_vector, to_int, sample_bits
from arithmetic import INC16
from memory import DFF, BIT, REGISTER16, PC
from computer import CPU, Memory, Computer


NUMBER_OF_SAMPLES_TO_DRAW_PER_TEST = 64

# Symbol to machine code lookup tables for C-instructions
DEST = {
    "M": 0b001,
}

COMP = {
    "0": 0b0101010,
    "1": 0b0111111,
    "-1": 0b0111010,
    "D": 0b0001100,
}

JUMP = {
    "null": 0b000,
    "JGT": 0b001,
    "JEQ": 0b010,
}


def _build_a_instruction(value: int) -> int:
    """Helper function to build an A-instruction."""

    # pre-conditions
    assert 0 <= value < 2**15, "value must be an integer in [0, 2**15)"

    # body
    return value


def _build_c_instruction(dest: int, comp: int, jump: int) -> int:
    """Helper function to build a C-instruction."""

    # pre-conditions
    assert 0 <= dest < 8, "dest must be an integer in [0, 8)"
    assert 0 <= comp < 64, "comp must be an integer in [0, 64)"
    assert 0 <= jump < 8, "jump must be an integer in [0, 8)"

    # body
    out = (0b111 << 13) | (comp << 6) | (dest << 3) | jump

    # post-conditions
    assert isinstance(out, int), "output must be an integer"
    assert 0 <= out < 2**16, "output must be an integer in [0, 2**16)"

    return out


def _get_next_c_instruction() -> Generator[tuple[bool, ...], None, None]:
    """A generator of all possible CPU C-instructions."""
    for dest in DEST.values():
        for comp in COMP.values():
            for jump in JUMP.values():
                bin_instuction = _build_c_instruction(dest, comp, jump)
                yield int_to_bit_vector(bin_instuction, n=16)


def _create_random_dff() -> DFF:
    value = random.choice([True, False])
    return DFF(value)


def _create_random_bit() -> BIT:
    dff = _create_random_dff()
    return BIT(dff)


def _create_random_register() -> REGISTER16:
    bits = tuple(_create_random_bit() for _ in range(16))
    return REGISTER16(bits)


def _create_random_pc() -> PC:
    register = _create_random_register()
    return PC(register)


def _create_random_cpu() -> CPU:
    a_register = _create_random_register()
    d_register = _create_random_register()
    pc = _create_random_pc()
    return CPU(a_register, d_register, pc)


def _create_random_a_instruction() -> tuple[bool, ...]:
    value = random.randint(0, 2**15 - 1)
    int_instruction = _build_a_instruction(value)
    out = int_to_bit_vector(int_instruction, n=16)

    # post-conditions
    assert out[0] == False, "A-instruction must start with a `0`"
    assert to_int(out) == value, "A-instruction must be the value in the instruction"

    return out


@pytest.mark.parametrize(
    "cpu, a_instruction, in_m, reset",
    [
        (
            _create_random_cpu(),
            _create_random_a_instruction(),
            sample_bits(16),
            False,
        )
        for _ in range(NUMBER_OF_SAMPLES_TO_DRAW_PER_TEST)
    ],
)
def test_cpu_runs_a_instructions(
    cpu: CPU,
    a_instruction: tuple[bool, ...],
    in_m: tuple[bool, ...],
    reset: bool,
) -> None:
    # When
    new_cpu = cpu(a_instruction, in_m, reset)

    # Then
    new_out_m, new_write_m, new_address_m, new_pc = new_cpu.out

    assert (
        new_cpu.a_register.out == a_instruction
    ), "A register must store the value of the A-instruction"

    assert (
        new_cpu.d_register.out == cpu.d_register.out
    ), "D register must not change when executing an A-instruction"

    assert new_cpu.pc.out == INC16(
        cpu.pc.out
    ), "PC must increment by 1 when executing an A-instruction"

    assert not new_write_m, "write_m must be `False` when executing an A-instruction"


@pytest.mark.skip(reason="TODO: yet to be implemented")
@pytest.mark.parametrize(
    "cpu, c_instruction, in_m, reset",
    [
        (
            _create_random_cpu(),
            _get_next_c_instruction(),
            sample_bits(16),
            False,
        )
        for _ in range(len(DEST) * len(COMP) * len(JUMP))
    ],
)
def test_cpu_runs_c_instructions(
    cpu: CPU,
    c_instruction: tuple[bool, ...],
    in_m: tuple[bool, ...],
    reset: bool,
) -> None:
    # Given
    symbol = to_symbol(c_instruction)

    # When
    new_cpu = cpu(c_instruction, in_m, reset)

    # Then
    out_m, new_write_m, address_m, pc = new_cpu.out

    if "M" in symbol:
        assert new_write_m, "`new_write_m` must be `True` when M in destination"

    if "M" not in symbol:
        assert (
            not new_write_m
        ), "`new_write_m` must be `False` when M not in destination"
