from dataclasses import dataclass
from gates import MUX, MUX16
from utils import is_n_bit_vector


@dataclass(frozen=True)
class DFF:
    """A data flip-flop gate that stores a single bit from the previous timestep. This should be called on the edge of each clock signal. This is a primitive component."""

    value: bool

    def __post_init__(self) -> None:
        assert isinstance(self.value, bool), "`value` must be a `bool`"

    def __call__(self, new_value: bool) -> "DFF":
        # pre-conditions
        assert isinstance(new_value, bool), "`value` must be a `bool`"

        # body
        new_dff = DFF(new_value)

        # post-conditions
        assert isinstance(new_dff, DFF), "`out` must be a `DFF`"
        assert new_dff.value == new_value, "dff must store `new_value`"

        return new_dff


@dataclass(frozen=True)
class BIT:
    """A 1-bit register."""

    value: bool
    dff: DFF

    def __post_init__(self) -> None:
        assert isinstance(self.value, bool), "`value` must be a `bool`"
        assert isinstance(self.dff, DFF), "`dff` must be a `DFF`"

    def __call__(self, value: bool, load: bool) -> "BIT":
        # pre-conditions
        assert isinstance(value, bool), "`value` must be a `bool`"
        assert isinstance(load, bool), "`load` must be a `bool`"

        # body
        old_value = self.dff.value
        new_value = MUX(old_value, value, load)
        new_dff = self.dff(new_value)
        new_bit = BIT(new_value, new_dff)

        # post-conditions
        assert isinstance(new_bit, BIT), "`new_bit` must be a `BIT`"

        if load:
            assert new_bit.value == value, "new value must be stored when load=1"

        if not load:
            assert new_bit.value == old_value, "old value must be kept when load=0"

        return new_bit


@dataclass(frozen=True)
class REGISTER:
    """A 16-bit register."""

    bits: tuple[BIT, ...]

    def __post_init__(self) -> None:
        assert all(isinstance(b, BIT) for b in self.bits), "`bits` must be `BIT`s"
        assert len(self.bits) == 16, "`bits` must be a 16-tuple of `BIT`s"

    def __call__(self, values: tuple[bool, ...], load: bool) -> "REGISTER":
        # pre-conditions
        assert is_n_bit_vector(values, n=16), "`value` must be a 16-tuple of `bool`s"
        assert isinstance(load, bool), "`load` must be a `bool`"

        # body
        new_bits = tuple(bit(v, load) for bit, v in zip(self.bits, values))
        new_register = REGISTER(new_bits)
        
        # post-conditions
        assert isinstance(new_register, REGISTER), "`new_register` must be a `REGISTER`"

        if load:
            assert all(b.value == v for b, v in zip(new_register.bits, values)), "new value must be stored when load=1"

        if not load:
            assert all(new_b.value == old_b.value for new_b, old_b in zip(new_register.bits, self.bits)), "old value must be kept when load=0"
        
        return new_register


@dataclass(frozen=True)
class RAM8:
    """8-register memory, each 16-bits."""

    value: tuple[bool, ...]
    registers: tuple[REGISTER, ...]

    def __post_init__(self) -> None:
        assert is_n_bit_vector(self.value, n=16), "`value` must be a 16-bit vector"
        assert all(
            isinstance(r, REGISTER) for r in self.registers
        ), "`registers` must be an 8-tuple of `REGISTER`s"

    def __call__(
        self,
        value: tuple[bool, ...],
        load: bool,
        address: tuple[bool, ...],
    ) -> "RAM8":
        # pre-conditions
        assert is_n_bit_vector(value, n=16), "`value` must be a 16-tuple of `bool`s"
        assert isinstance(load, bool), "`load` must be a `bool`"
        assert is_n_bit_vector(address, n=3), "`address` must be a 3-tuple of `bool`s"

        # body
        raise NotImplementedError()
