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
from memory import (
    DFF,
    BIT,
    REGISTER16,
    RAM8,
    RAM64,
    RAM512,
    RAM4K,
    RAM8K,
    RAM16K,
    PC,
    ROM32K,
)
from computer import (
    DEST_SYMBOL_TO_INSTRUCTION,
    COMP_SYMBOL_TO_INSTRUCTION,
    JUMP_SYMBOL_TO_INSTRUCTION,
    CPU,
    Memory,
    Computer,
    is_valid_instruction,
)


NUMBER_OF_SAMPLES_TO_DRAW_PER_TEST = 1


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


def _create_random_a_instruction() -> tuple[bool, ...]:
    value = random.randint(0, 2**15 - 1)
    int_instruction = _build_a_instruction(value)
    out = int_to_bit_vector(int_instruction, n=16)

    # post-conditions
    assert out[0] == False, "A-instruction must start with a `0`"
    assert to_int(out) == value, "A-instruction must be the value in the instruction"

    return out


def _get_next_c_instruction() -> Generator[tuple[bool, ...], None, None]:
    """A generator of all possible CPU C-instructions."""
    for dest in DEST_SYMBOL_TO_INSTRUCTION.values():
        for comp in COMP_SYMBOL_TO_INSTRUCTION.values():
            for jump in JUMP_SYMBOL_TO_INSTRUCTION.values():
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


def _create_random_ram8() -> RAM8:
    registers = tuple(_create_random_register() for _ in range(8))
    out = registers[0].out
    return RAM8(registers, out)


def _create_random_ram64() -> RAM64:
    ram8s = tuple(_create_random_ram8() for _ in range(8))
    out = ram8s[0].out
    return RAM64(ram8s, out)


def _create_random_ram512() -> RAM512:
    ram64s = tuple(_create_random_ram64() for _ in range(8))
    out = ram64s[0].out
    return RAM512(ram64s, out)


def _create_random_ram4k() -> RAM4K:
    ram512s = tuple(_create_random_ram512() for _ in range(8))
    out = ram512s[0].out
    return RAM4K(ram512s, out)


def _create_random_ram8k() -> RAM8K:
    ram4ks = tuple(_create_random_ram4k() for _ in range(2))
    out = ram4ks[0].out
    return RAM8K(ram4ks, out)


def _create_random_ram16k() -> RAM16K:
    ram4ks = tuple(_create_random_ram4k() for _ in range(4))
    out = ram4ks[0].out
    return RAM16K(ram4ks, out)


def _create_random_pc() -> PC:
    register = _create_random_register()
    return PC(register)


def _create_random_memory() -> Memory:
    """Returns a random memory."""
    ram16k = _create_random_ram16k()
    screen = _create_random_ram8k()
    keyboard = _create_random_register()
    out = sample_bits(16)
    return Memory(ram16k, screen, keyboard, out)


def _create_random_valid_memory_address() -> tuple[bool, ...]:
    """Returns a random valid address for `Memory`."""
    idx = random.randint(0, 2**14 + 2**13 - 1)
    return int_to_bit_vector(idx, n=15)


def _create_random_invalid_memory_address() -> tuple[bool, ...]:
    """Returns a random invalid address for `Memory`."""
    idx = random.randint(2**14 + 2**13, 2**15 - 1)
    return int_to_bit_vector(idx, n=15)


def _create_random_cpu() -> CPU:
    a_register = _create_random_register()
    d_register = _create_random_register()
    pc = _create_random_pc()

    out_m = ZERO16
    write_m = False
    _zr = True
    _ng = False

    return CPU(
        a_register=a_register,
        d_register=d_register,
        pc=pc,
        _zr=_zr,
        _ng=_ng,
        out_m=out_m,
        write_m=write_m,
    )


def _create_random_rom32k() -> ROM32K:
    """Returns a random ROM32K."""
    ram16ks = tuple(_create_random_ram16k() for _ in range(2))
    state = ram16ks[0].state + ram16ks[1].state
    return ROM32K(state)


def _create_random_computer() -> Computer:
    rom = _create_random_rom32k()
    cpu = _create_random_cpu()
    memory = _create_random_memory()
    return Computer(rom, cpu, memory)


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

    dest_to_symbol = {v: k for k, v in DEST_SYMBOL_TO_INSTRUCTION.items()}
    comp_to_symbol = {v: k for k, v in COMP_SYMBOL_TO_INSTRUCTION.items()}
    jump_to_symbol = {v: k for k, v in JUMP_SYMBOL_TO_INSTRUCTION.items()}

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


def _create_valid_instruction() -> tuple[bool, ...]:
    """Returns a random 16-bit instruction."""
    return random.choice(
        [
            _create_random_a_instruction(),
            random.choice(list(_get_next_c_instruction())),
        ]
    )


def _create_invalid_instruction() -> tuple[bool, ...]:
    """Returns a random 16-bit instruction."""
    instruction = (True,) + sample_bits(15)

    while is_valid_instruction(instruction):
        instruction = (True,) + sample_bits(15)

    # post-conditions
    assert is_n_bit_vector(instruction, n=16), "instruction must be 16-bit"
    assert not is_valid_instruction(instruction), "instruction must be invalid"

    return instruction


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


@pytest.mark.parametrize(
    "cpu, invalid_instruction, in_m, reset",
    [
        (
            _create_random_cpu(),
            _create_invalid_instruction(),
            sample_bits(16),
            True,
        )
        for _ in range(NUMBER_OF_SAMPLES_TO_DRAW_PER_TEST)
    ],
)
def test_cpu_throws_assertion_error_when_given_invalid_instruction(
    cpu: CPU,
    invalid_instruction: tuple[bool, ...],
    in_m: tuple[bool, ...],
    reset: bool,
) -> None:
    # When / Then
    with pytest.raises(AssertionError):
        cpu(invalid_instruction, in_m, reset)


@pytest.mark.parametrize(
    "cpu, instruction, in_m, reset",
    [
        (
            _create_random_cpu(),
            _create_valid_instruction(),
            sample_bits(16),
            True,
        )
        for _ in range(NUMBER_OF_SAMPLES_TO_DRAW_PER_TEST)
    ],
)
def test_program_counter_is_reset_when_reset_control_bit_is_asserted(
    cpu: CPU,
    instruction: tuple[bool, ...],
    in_m: tuple[bool, ...],
    reset: bool,
) -> None:
    # When
    new_cpu = cpu(instruction, in_m, reset)

    # Then
    assert (
        new_cpu.pc.out == ZERO16
    ), "PC must be reset to `0` when reset control bit is asserted"


@pytest.mark.parametrize(
    "memory, xs, address, load",
    [
        (
            _create_random_memory(),
            sample_bits(16),
            _create_random_valid_memory_address(),
            True,
        )
        for _ in range(NUMBER_OF_SAMPLES_TO_DRAW_PER_TEST)
    ],
)
def test_memory_loads_value_at_valid_address_and_returns_it_next_time_step(
    memory: Memory,
    xs: tuple[bool, ...],
    address: tuple[bool, ...],
    load: bool,
) -> None:
    # Given
    address_idx = to_int(address)

    # When
    new_memory = memory(xs, address, load)

    # Then
    if 0 <= address_idx < 2**14:
        assert (
            new_memory.ram.state[address_idx] == xs
        ), "memory must load value at address when load is asserted"

    if 2**14 <= address_idx < 2**14 + 2**13:
        offset_address_idx = address_idx - 2**14

        assert (
            new_memory.screen.state[offset_address_idx] == xs
        ), "screen must load value at address when load is asserted"

    assert (
        new_memory.out == xs
    ), "out must return the value stored at the previous time step"


@pytest.mark.parametrize(
    "memory, xs, address, load",
    [
        (
            _create_random_memory(),
            sample_bits(16),
            _create_random_invalid_memory_address(),
            True,
        )
        for _ in range(NUMBER_OF_SAMPLES_TO_DRAW_PER_TEST)
    ],
)
def test_memory_throws_assertion_error_when_given_invalid_address(
    memory: Memory,
    xs: tuple[bool, ...],
    address: tuple[bool, ...],
    load: bool,
) -> None:
    # When / Then
    with pytest.raises(AssertionError):
        memory(xs, address, load)


@pytest.mark.parametrize(
    "memory, xs, address, load",
    [
        (
            _create_random_memory(),
            sample_bits(16),
            _create_random_valid_memory_address(),
            False,
        )
        for _ in range(NUMBER_OF_SAMPLES_TO_DRAW_PER_TEST)
    ],
)
def test_memory_does_not_load_value_at_valid_address_but_outputs_it_next_time_step_when_load_is_false(
    memory: Memory,
    xs: tuple[bool, ...],
    address: tuple[bool, ...],
    load: bool,
) -> None:
    # Given
    address_idx = to_int(address)

    # When
    new_memory = memory(xs, address, load)

    # Then
    assert (
        new_memory.ram.state == memory.ram.state
    ), "RAM must not change when load is `False`"
    assert (
        new_memory.screen.state == memory.screen.state
    ), "screen must not change when load is `False`"
    assert (
        new_memory.keyboard.out == memory.keyboard.out
    ), "keyboard must not change when load is `False`"

    if 0 <= address_idx < 2**14:
        assert (
            new_memory.out == memory.ram.state[address_idx]
        ), "out must be the value at address of the RAM"

    if 2**14 <= address_idx < 2**14 + 2**13:
        offset_address_idx = address_idx - 2**14

        assert (
            new_memory.out == memory.screen.state[offset_address_idx]
        ), "out must be the value at offset address of the screen"

    if address_idx == 2**14 + 2**13:
        assert new_memory.out == memory.keyboard.out, "out must be the value at address"
