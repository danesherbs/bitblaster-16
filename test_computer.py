import pytest
import random

from typing import Generator
from gates import NOT16, AND16, OR16
from utils import (
    ZERO16,
    int_to_bit_vector,
    to_int,
    sample_bits,
    is_n_bit_vector,
    is_non_negative,
    is_positive,
    SymbolicInstruction,
)
from arithmetic import INC16
from memory import DFF, BIT, REGISTER16, PC
from computer import CPU, Memory, Computer


NUMBER_OF_SAMPLES_TO_DRAW_PER_TEST = 128

# Symbol to machine code lookup tables for C-instructions
DEST = {
    "null": 0b000,
    "M": 0b001,
    "D": 0b010,
    "MD": 0b011,
    "A": 0b100,
    "AM": 0b101,
    "AD": 0b110,
    "AMD": 0b111,
}

COMP = {
    # a = 0
    "0": 0b0101010,
    "1": 0b0111111,
    "-1": 0b0111010,
    "D": 0b0001100,
    "A": 0b0110000,
    "!D": 0b0001101,
    "!A": 0b0110001,
    "-D": 0b0001111,
    "-A": 0b0110011,
    "D+1": 0b0011111,
    "A+1": 0b0110111,
    "D-1": 0b0001110,
    "A-1": 0b0110010,
    "D+A": 0b0000010,
    "D-A": 0b0010011,
    "A-D": 0b0000111,
    "D&A": 0b0000000,
    "D|A": 0b0010101,
    # a = 1
    "M": 0b1110000,
    "!M": 0b1110001,
    "-M": 0b1110011,
    "M+1": 0b1110111,
    "M-1": 0b1110010,
    "D+M": 0b1000010,
    "D-M": 0b1010011,
    "M-D": 0b1000111,
    "D&M": 0b1000000,
    "D|M": 0b1010101,
}

JUMP = {
    "null": 0b000,
    "JGT": 0b001,
    "JEQ": 0b010,
    "JGE": 0b011,
    "JLT": 0b100,
    "JNE": 0b101,
    "JLE": 0b110,
    "JMP": 0b111,
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
    assert 0 <= dest < 2**3, "dest must be an integer in [0, 8)"
    assert 0 <= comp < 2**7, "comp must be an integer in [0, 128)"
    assert 0 <= jump < 2**3, "jump must be an integer in [0, 8)"

    # body
    out = 0b111 << 13 | comp << 6 | dest << 3 | jump

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


def _to_symbol(c_instruction: tuple[bool, ...]) -> SymbolicInstruction:
    """Converts a C-instruction into a symbolic instruction."""
    # pre-conditions
    assert is_n_bit_vector(
        c_instruction, n=16
    ), f"instruction must be a 16-bit tuple, got: {c_instruction}"

    # body
    comp = c_instruction[3:10]
    dest = c_instruction[10:13]
    jump = c_instruction[13:16]

    dest_to_symbol = {v: k for k, v in DEST.items()}
    comp_to_symbol = {v: k for k, v in COMP.items()}
    jump_to_symbol = {v: k for k, v in JUMP.items()}

    dest_symbol = dest_to_symbol[to_int(dest)]
    comp_symbol = comp_to_symbol[to_int(comp)]
    jump_symbol = jump_to_symbol[to_int(jump)]

    out = SymbolicInstruction(
        dest=dest_symbol,
        comp=comp_symbol,
        jump=jump_symbol,
    )

    # post-conditions
    assert isinstance(out, SymbolicInstruction), "output must be a SymbolicInstruction"

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
    assert (
        new_cpu.a_register.out == a_instruction
    ), "A register must store the value of the A-instruction"

    assert (
        new_cpu.d_register.out == cpu.d_register.out
    ), "D register must not change when executing an A-instruction"

    assert new_cpu.pc.out == INC16(
        cpu.pc.out
    ), "PC must increment by 1 when executing an A-instruction"

    assert (
        not new_cpu.write_m
    ), "write_m must be `False` when executing an A-instruction"


@pytest.mark.parametrize(
    "cpu, c_instruction, in_m, reset",
    [
        (
            _create_random_cpu(),
            c_instruction,
            sample_bits(16),
            False,
        )
        for c_instruction in _get_next_c_instruction()
    ],
)
def test_cpu_runs_c_instructions(
    cpu: CPU,
    c_instruction: tuple[bool, ...],
    in_m: tuple[bool, ...],
    reset: bool,
) -> None:
    # Given
    symbolic_instruction = _to_symbol(c_instruction)

    # When
    new_cpu = cpu(c_instruction, in_m, reset)

    # Then
    assert isinstance(cpu.out_m, tuple), "`out_m` must be a tuple"
    assert is_n_bit_vector(cpu.out_m, n=16), "`out_m` must be a 16-bit tuple"

    assert isinstance(new_cpu.out_m, tuple), "`out_m` must be a tuple"
    assert is_n_bit_vector(new_cpu.out_m, n=16), "`out_m` must be a 16-bit tuple"

    # Then (dest)
    if "A" in symbolic_instruction.dest:
        assert new_cpu.a_register.out == cpu.out_m, "`A` must be written to `out_m`"

    if "A" not in symbolic_instruction.dest:
        assert new_cpu.a_register.out == cpu.a_register.out, "`A` must not be changed"

    if "M" in symbolic_instruction.dest:
        assert new_cpu.write_m, "`new_write_m` must be `True` when M in destination"

    if "M" not in symbolic_instruction.dest:
        assert (
            not new_cpu.write_m
        ), "`new_write_m` must be `False` when M not in destination"

    if "D" in symbolic_instruction.dest:
        assert new_cpu.d_register.out == cpu.out_m, "`D` must be written to `out_m`"

    if "D" not in symbolic_instruction.dest:
        assert new_cpu.d_register.out == cpu.d_register.out, "`D` must not be changed"

    # Then (comp)
    if symbolic_instruction.comp == "0":
        assert to_int(new_cpu.out_m) == 0, "`out_m` must be `0` when comp is `0`"

    if symbolic_instruction.comp == "1":
        assert to_int(new_cpu.out_m) == 1, "`out_m` must be `1` when comp is `1`"

    if symbolic_instruction.comp == "-1":
        assert all(b for b in new_cpu.out_m), f"`out_m` must be `-1` when comp is `-1`"

    if symbolic_instruction.comp == "D":
        assert (
            new_cpu.out_m == cpu.d_register.out
        ), "`out_m` must be `D` when comp is `D`"

    if symbolic_instruction.comp == "A":
        assert (
            new_cpu.out_m == cpu.a_register.out
        ), "`out_m` must be `A` when comp is `A`"

    if symbolic_instruction.comp == "!D":
        assert new_cpu.out_m == NOT16(
            cpu.d_register.out
        ), "`out_m` must be `!D` when comp is `!D`"

    if symbolic_instruction.comp == "!A":
        assert new_cpu.out_m == NOT16(
            cpu.a_register.out
        ), "`out_m` must be `!A` when comp is `!A`"

    if symbolic_instruction.comp == "-D":
        assert new_cpu.out_m == INC16(
            NOT16(cpu.d_register.out)
        ), "`out_m` must be `-D` when comp is `-D`"

    if symbolic_instruction.comp == "-A":
        assert new_cpu.out_m == INC16(
            NOT16(cpu.a_register.out)
        ), "`out_m` must be `-A` when comp is `-A`"

    if symbolic_instruction.comp == "D+1":
        assert new_cpu.out_m == INC16(
            cpu.d_register.out
        ), "`out_m` must be `D+1` when comp is `D+1`"

    if symbolic_instruction.comp == "A+1":
        assert new_cpu.out_m == INC16(
            cpu.a_register.out
        ), "`out_m` must be `A+1` when comp is `A+1`"

    if symbolic_instruction.comp == "D-1":
        assert (
            to_int(new_cpu.out_m) == (to_int(cpu.d_register.out) - 1) % 2**16
        ), "`out_m` must be `D-1` when comp is `D-1`"

    if symbolic_instruction.comp == "A-1":
        assert (
            to_int(new_cpu.out_m) == (to_int(cpu.a_register.out) - 1) % 2**16
        ), "`out_m` must be `A-1` when comp is `A-1`"

    if symbolic_instruction.comp == "D+A":
        assert (
            to_int(new_cpu.out_m)
            == (to_int(cpu.d_register.out) + to_int(cpu.a_register.out)) % 2**16
        ), "`out_m` must be `D+A` when comp is `D+A`"

    if symbolic_instruction.comp == "D-A":
        assert (
            to_int(new_cpu.out_m)
            == (to_int(cpu.d_register.out) - to_int(cpu.a_register.out)) % 2**16
        ), "`out_m` must be `D-A` when comp is `D-A`"

    if symbolic_instruction.comp == "A-D":
        assert (
            to_int(new_cpu.out_m)
            == (to_int(cpu.a_register.out) - to_int(cpu.d_register.out)) % 2**16
        ), "`out_m` must be `A-D` when comp is `A-D`"

    if symbolic_instruction.comp == "D&A":
        assert new_cpu.out_m == AND16(
            cpu.d_register.out, cpu.a_register.out
        ), "`out_m` must be `D&A` when comp is `D&A`"

    if symbolic_instruction.comp == "D|A":
        assert new_cpu.out_m == OR16(
            cpu.d_register.out, cpu.a_register.out
        ), "`out_m` must be `D|A` when comp is `D|A`"

    if symbolic_instruction.comp == "M":
        assert new_cpu.out_m == in_m, "`out_m` must be `in_m` when comp is `M`"

    if symbolic_instruction.comp == "!M":
        assert new_cpu.out_m == NOT16(in_m), "`out_m` must be `!M` when comp is `!M`"

    if symbolic_instruction.comp == "-M":
        assert new_cpu.out_m == INC16(
            NOT16(in_m)
        ), "`out_m` must be `-M` when comp is `-M`"

    if symbolic_instruction.comp == "M+1":
        assert new_cpu.out_m == INC16(in_m), "`out_m` must be `M+1` when comp is `M+1`"

    if symbolic_instruction.comp == "M-1":
        assert (
            to_int(new_cpu.out_m) == (to_int(in_m) - 1) % 2**16
        ), "`out_m` must be `M-1` when comp is `M-1`"

    if symbolic_instruction.comp == "D+M":
        assert (
            to_int(new_cpu.out_m)
            == (to_int(cpu.d_register.out) + to_int(in_m)) % 2**16
        ), "`out_m` must be `D+M` when comp is `D+M`"

    if symbolic_instruction.comp == "D-M":
        assert (
            to_int(new_cpu.out_m)
            == (to_int(cpu.d_register.out) - to_int(in_m)) % 2**16
        ), "`out_m` must be `D-M` when comp is `D-M`"

    if symbolic_instruction.comp == "M-D":
        assert (
            to_int(new_cpu.out_m)
            == (to_int(in_m) - to_int(cpu.d_register.out)) % 2**16
        ), "`out_m` must be `M-D` when comp is `M-D`"

    if symbolic_instruction.comp == "D&M":
        assert new_cpu.out_m == AND16(
            cpu.d_register.out, in_m
        ), "`out_m` must be `D&M` when comp is `D&M`"

    if symbolic_instruction.comp == "D|M":
        assert new_cpu.out_m == OR16(
            cpu.d_register.out, in_m
        ), "`out_m` must be `D|M` when comp is `D|M`"

    # Then (jump)
    if symbolic_instruction.jump == "null":
        assert new_cpu.pc.out == INC16(
            cpu.pc.out
        ), "PC must increment by 1 when jump is `null`"

    if symbolic_instruction.jump == "JGT":
        if is_positive(cpu.out_m):
            assert (
                new_cpu.pc.out == cpu.a_register.out
            ), "PC must jump to `A` when jump is `JGT` and ALU output is positive"

        if not is_positive(cpu.out_m):
            assert new_cpu.pc.out == INC16(
                cpu.pc.out
            ), "PC must increment by 1 when jump is `JGT` and ALU output is negative"

    if symbolic_instruction.jump == "JEQ":
        if cpu.out_m == ZERO16:
            assert (
                new_cpu.pc.out == cpu.a_register.out
            ), "PC must jump to `A` when jump is `JEQ` and ALU output is zero"

        if cpu.out_m != ZERO16:
            assert new_cpu.pc.out == INC16(
                cpu.pc.out
            ), "PC must increment by 1 when jump is `JEQ` and ALU output is non-zero"

    if symbolic_instruction.jump == "JGE":
        if is_non_negative(cpu.out_m):
            assert (
                new_cpu.pc.out == cpu.a_register.out
            ), "PC must jump to `A` when jump is `JGE` and ALU output is non-negative"

        if not is_non_negative(cpu.out_m):
            assert new_cpu.pc.out == INC16(
                cpu.pc.out
            ), "PC must increment by 1 when jump is `JGE` and ALU output is negative"

    if symbolic_instruction.jump == "JLT":
        if not is_non_negative(cpu.out_m):
            assert (
                new_cpu.pc.out == cpu.a_register.out
            ), "PC must jump to `A` when jump is `JLT` and ALU output is negative"

        if is_non_negative(cpu.out_m):
            assert new_cpu.pc.out == INC16(
                cpu.pc.out
            ), "PC must increment by 1 when jump is `JLT` and ALU output is non-negative"

    if symbolic_instruction.jump == "JNE":
        if cpu.out_m != ZERO16:
            assert (
                new_cpu.pc.out == cpu.a_register.out
            ), "PC must jump to `A` when jump is `JNE` and ALU output is non-zero"

        if cpu.out_m == ZERO16:
            assert new_cpu.pc.out == INC16(
                cpu.pc.out
            ), "PC must increment by 1 when jump is `JNE` and ALU output is zero"

    if symbolic_instruction.jump == "JLE":
        if not is_positive(cpu.out_m):
            assert (
                new_cpu.pc.out == cpu.a_register.out
            ), "PC must jump to `A` when jump is `JLE` and ALU output is negative"

        if is_positive(cpu.out_m):
            assert new_cpu.pc.out == INC16(
                cpu.pc.out
            ), "PC must increment by 1 when jump is `JLE` and ALU output is positive"

    if symbolic_instruction.jump == "JMP":
        assert (
            new_cpu.pc.out == cpu.a_register.out
        ), "PC must jump to `A` when jump is an unconditional `JMP`"


@pytest.mark.skip(reason="TODO: yet to be implemented")
def test_cpu_throws_assertion_error_when_given_invalid_instruction() -> None:
    pass


@pytest.mark.skip(reason="TODO: yet to be implemented")
def test_program_counter_is_reset_when_reset_control_bit_is_asserted() -> None:
    pass
