import pytest
import random
import utils

from arithmetic import INC16
from memory import DFF, BIT, REGISTER16, RAM8, RAM64, RAM512, RAM4K, RAM16K, PCOUNTER

NUMBER_OF_SAMPLES_TO_DRAW_PER_TEST = 16
ZERO16 = (False,) * 16


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
    return RAM8(registers)


def _create_random_ram64() -> RAM64:
    ram8s = tuple(_create_random_ram8() for _ in range(8))
    return RAM64(ram8s)


def _create_random_ram512() -> RAM512:
    ram64s = tuple(_create_random_ram64() for _ in range(8))
    return RAM512(ram64s)


def _create_random_ram4k() -> RAM4K:
    ram512s = tuple(_create_random_ram512() for _ in range(8))
    return RAM4K(ram512s)


def _create_random_ram16k() -> RAM16K:
    ram4ks = tuple(_create_random_ram4k() for _ in range(4))
    return RAM16K(ram4ks)


@pytest.mark.parametrize(
    "initial_value, x",
    [
        (False, True),
        (False, False),
        (True, True),
        (True, False),
    ],
)
def test_dff(initial_value: bool, x: bool) -> None:
    # Given
    dff = DFF(initial_value)

    # When
    new_dff = dff(x)
    
    # Then
    assert dff.out == initial_value
    assert new_dff.out == x


@pytest.mark.parametrize(
    "initial_value, x, load",
    [
        (False, False, False),
        (False, True, False),
        (True, False, False),
        (True, True, False),
        (False, False, True),
        (False, True, True),
        (True, False, True),
        (True, True, True),
    ],
)
def test_bit(initial_value: bool, x: bool, load: bool) -> None:
    # Given
    dff = DFF(initial_value)
    bit = BIT(dff)

    # When
    new_bit = bit(x, load)

    # Then
    if load:
        assert new_bit.out == x

    if not load:
        assert new_bit.out == initial_value


@pytest.mark.parametrize(
    "register, xs, load",
    [
        (
            _create_random_register(),
            utils.sample_bits(16),
            random.choice([True, False]),
        )
        for _ in range(NUMBER_OF_SAMPLES_TO_DRAW_PER_TEST)
    ],
)
def test_register(
    register: REGISTER16,
    xs: tuple[bool, ...],
    load: bool,
) -> None:
    # When
    new_register = register(xs, load)

    # Then
    if load:
        assert all(
            new_v == x for new_v, x in zip(new_register.out, xs)
        ), "new value must be stored when load=1"

    if not load:
        assert all(
            new_v == old_v for new_v, old_v in zip(new_register.out, register.out)
        ), "old value must be kept when load=0"


@pytest.mark.parametrize(
    "ram8, xs, load, address",
    [
        (
            _create_random_ram8(),
            utils.sample_bits(16),
            random.choice([True, False]),
            utils.sample_bits(3),
        )
        for _ in range(NUMBER_OF_SAMPLES_TO_DRAW_PER_TEST)
    ],
)
def test_ram8(
    ram8: RAM8,
    xs: tuple[bool, ...],
    load: bool,
    address: tuple[bool, ...],
) -> None:
    # When
    new_ram8 = ram8(xs, load, address)

    # Then
    address_idx = utils.to_int(address)

    if load:
        assert all(
            b.out == v for b, v in zip(new_ram8.registers[address_idx].bits, xs)
        ), "new value must be stored when load=1"

    if not load:
        assert all(
            new_b.out == old_b.out
            for new_b, old_b in zip(
                new_ram8.registers[address_idx].bits,
                ram8.registers[address_idx].bits,
            )
        ), "old value must be kept when load=0"

    for i in range(8):
        if i == address_idx:
            continue  # skip the address index

        assert all(
            new_b.out == old_b.out
            for new_b, old_b in zip(
                new_ram8.registers[i].bits,
                ram8.registers[i].bits,
            )
        ), f"register at index {i} should not change"


@pytest.mark.parametrize(
    "ram64, xs, load, address",
    [
        (
            _create_random_ram64(),
            utils.sample_bits(16),
            random.choice([True, False]),
            utils.sample_bits(6),
        )
        for _ in range(NUMBER_OF_SAMPLES_TO_DRAW_PER_TEST)
    ],
)
def test_ram64(
    ram64: RAM64,
    xs: tuple[bool, ...],
    load: bool,
    address: tuple[bool, ...],
) -> None:
    # When
    new_ram64 = ram64(xs, load, address)

    # Then
    address_idx = utils.to_int(address)

    if load:
        assert new_ram64.out[address_idx] == xs, "new value must be stored when load=1"

    if not load:
        assert ram64.out == new_ram64.out, "old value must be kept when load=0"

    for i in range(64):
        if i == address_idx:
            continue  # skip the address index

        assert (
            new_ram64.out[i] == ram64.out[i]
        ), f"register at index {i} should not change"


@pytest.mark.parametrize(
    "ram512, xs, load, address",
    [
        (
            _create_random_ram512(),
            utils.sample_bits(16),
            random.choice([True, False]),
            utils.sample_bits(9),
        )
        for _ in range(NUMBER_OF_SAMPLES_TO_DRAW_PER_TEST)
    ],
)
def test_ram512(
    ram512: RAM512,
    xs: tuple[bool, ...],
    load: bool,
    address: tuple[bool, ...],
) -> None:
    # When
    new_ram512 = ram512(xs, load, address)

    # Then
    address_idx = utils.to_int(address)
    old_out = ram512.out
    new_out = new_ram512.out

    if load:
        assert new_out[address_idx] == xs, "new value must be stored when load=1"

    if not load:
        assert old_out == new_out, "old value must be kept when load=0"

    for i in range(512):
        if i == address_idx:
            continue  # skip the address index

        assert new_out[i] == old_out[i], f"register at index {i} should not change"


@pytest.mark.parametrize(
    "ram4k, xs, load, address",
    [
        (
            _create_random_ram4k(),
            utils.sample_bits(16),
            random.choice([True, False]),
            utils.sample_bits(12),
        )
        for _ in range(NUMBER_OF_SAMPLES_TO_DRAW_PER_TEST)
    ],
)
def test_ram4k(
    ram4k: RAM4K,
    xs: tuple[bool, ...],
    load: bool,
    address: tuple[bool, ...],
) -> None:
    # When
    new_ram4k = ram4k(xs, load, address)

    # Then
    address_idx = utils.to_int(address)
    old_out = ram4k.out
    new_out = new_ram4k.out

    if load:
        assert new_out[address_idx] == xs, "new value must be stored when load=1"

    if not load:
        assert old_out == new_out, "old value must be kept when load=0"

    for i in range(4_096):
        if i == address_idx:
            continue  # skip the address index

        assert new_out[i] == old_out[i], f"register at index {i} should not change"


@pytest.mark.parametrize(
    "ram16k, xs, load, address",
    [
        (
            _create_random_ram16k(),
            utils.sample_bits(16),
            random.choice([True, False]),
            utils.sample_bits(14),
        )
        for _ in range(NUMBER_OF_SAMPLES_TO_DRAW_PER_TEST)
    ],
)
def test_ram16k(
    ram16k: RAM16K,
    xs: tuple[bool, ...],
    load: bool,
    address: tuple[bool, ...],
) -> None:
    # When
    new_ram16k = ram16k(xs, load, address)

    # Then
    address_idx = utils.to_int(address)
    old_out = ram16k.out
    new_out = new_ram16k.out

    if load:
        assert new_out[address_idx] == xs, "new value must be stored when load=1"

    if not load:
        assert old_out == new_out, "old value must be kept when load=0"

    for i in range(2**14):
        if i == address_idx:
            continue  # skip the address index

        assert new_out[i] == old_out[i], f"register at index {i} should not change"


def test_pc() -> None:
    # Given
    xs = utils.sample_bits(16)
    register = _create_random_register()
    pc = PCOUNTER(register)

    # When / Then
    assert pc(xs, False, False, False).out == pc.out
    assert pc(xs, False, False, True).out == ZERO16
    assert pc(xs, False, True, False).out == INC16(pc.out)
    assert pc(xs, True, False, False).out == xs
    assert pc(xs, True, False, True).out == ZERO16
    assert pc(xs, True, True, False).out == xs
    assert pc(xs, True, True, True).out == ZERO16
