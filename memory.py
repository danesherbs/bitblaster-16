from dataclasses import dataclass
from gates import MUX, DMUX8WAY
from utils import is_n_bit_vector, bool_tuple_to_int


@dataclass(frozen=True)
class DFF:
    """A data flip-flop gate that stores a single bit from the previous timestep. This should be called on the edge of each clock signal. This is a primitive component."""

    out: bool

    def __post_init__(self) -> None:
        assert isinstance(self.out, bool), "`self.out` must be a `bool`"

    def __call__(self, x: bool) -> "DFF":
        # pre-conditions
        assert isinstance(x, bool), "`x` must be a `bool`"

        # body
        new_dff = DFF(x)

        # post-conditions
        assert isinstance(new_dff, DFF), "`out` must be a `DFF`"
        assert new_dff.out == x, "dff must store `x`"

        return new_dff


@dataclass(frozen=True)
class BIT:
    """A 1-bit register."""

    dff: DFF

    def __post_init__(self) -> None:
        assert isinstance(self.dff, DFF), "`dff` must be a `DFF`"

    def __call__(self, x: bool, load: bool) -> "BIT":
        # pre-conditions
        assert isinstance(x, bool), "`x` must be a `bool`"
        assert isinstance(load, bool), "`load` must be a `bool`"

        # body
        old_x = self.dff.out
        new_x = MUX(old_x, x, load)
        new_dff = self.dff(new_x)
        new_bit = BIT(new_dff)

        # post-conditions
        assert isinstance(new_bit, BIT), "`new_bit` must be a `BIT`"

        if load:
            assert new_bit.out == x, "new value must be stored when load=1"

        if not load:
            assert new_bit.out == old_x, "old value must be kept when load=0"

        return new_bit

    @property
    def out(self) -> bool:
        return self.dff.out


@dataclass(frozen=True)
class REGISTER:
    """A 16-bit register."""

    bits: tuple[BIT, ...]

    def __post_init__(self) -> None:
        assert all(isinstance(b, BIT) for b in self.bits), "`bits` must be `BIT`s"
        assert len(self.bits) == 16, "`bits` must be a 16-tuple of `BIT`s"

    def __call__(self, xs: tuple[bool, ...], load: bool) -> "REGISTER":
        # pre-conditions
        assert is_n_bit_vector(xs, n=16), "`xs` must be a 16-tuple of `bool`s"
        assert isinstance(load, bool), "`load` must be a `bool`"

        # body
        new_bits = tuple(bit(x, load) for bit, x in zip(self.bits, xs))
        new_register = REGISTER(new_bits)

        # post-conditions
        assert isinstance(new_register, REGISTER), "`new_register` must be a `REGISTER`"

        if load:
            assert all(
                b.out == v for b, v in zip(new_register.bits, xs)
            ), "new value must be stored when load=1"

        if not load:
            assert self.out == new_register.out, "old value must be kept when load=0"

        return new_register

    @property
    def out(self) -> tuple[bool, ...]:
        return tuple(b.out for b in self.bits)


@dataclass(frozen=True)
class RAM8:
    """8-register memory, each 16-bits."""

    registers: tuple[REGISTER, ...]

    def __post_init__(self) -> None:
        assert all(
            isinstance(r, REGISTER) for r in self.registers
        ), "`registers` must be a tuple of `REGISTER`s"
        assert len(self.registers) == 8, "`registers` must be a 8-tuple of `REGISTER`s"

    def __call__(
        self,
        xs: tuple[bool, ...],
        load: bool,
        address: tuple[bool, ...],
    ) -> "RAM8":
        # pre-conditions
        assert is_n_bit_vector(xs, n=16), "`xs` must be a 16-tuple of `bool`s"
        assert isinstance(load, bool), "`load` must be a `bool`"
        assert is_n_bit_vector(address, n=3), "`address` must be a 3-tuple of `bool`s"

        # body
        load_bits = DMUX8WAY(load, address)
        new_registers = tuple(r(xs, load_bits[i]) for i, r in enumerate(self.registers))
        new_ram8 = RAM8(new_registers)

        # post-conditions
        assert isinstance(new_ram8, RAM8), "`new_ram8` must be a `RAM8`"
        assert all(
            isinstance(r, REGISTER) for r in new_ram8.registers
        ), "`new_ram8.registers` must be an 8-tuple of `REGISTER`s"

        if load:
            address_idx = bool_tuple_to_int(address)
            selected_register = new_ram8.registers[address_idx]
            assert all(
                v == x for v, x in zip(selected_register.out, xs)
            ), "new value must be stored when load=1"

        if not load:
            assert new_ram8.out == self.out, "old value must be kept when load=0"

        return new_ram8

    @property
    def out(self) -> tuple[tuple[bool, ...], ...]:
        return tuple(r.out for r in self.registers)


@dataclass(frozen=True)
class RAM64:
    """64-register memory, each 16-bits."""

    ram8s: tuple[RAM8, ...]

    def __post_init__(self) -> None:
        assert all(
            isinstance(r, RAM8) for r in self.ram8s
        ), "`ram8s` must be a tuple of `RAM8`s"
        assert len(self.ram8s) == 8, "`ram8s` must be a 8-tuple of `RAM8`s"

    def __call__(
        self,
        xs: tuple[bool, ...],
        load: bool,
        address: tuple[bool, ...],
    ) -> "RAM64":
        # pre-conditions
        assert is_n_bit_vector(xs, n=16), "`xs` must be a 16-tuple of `bool`s"
        assert isinstance(load, bool), "`load` must be a `bool`"
        assert is_n_bit_vector(address, n=6), "`address` must be a 6-tuple of `bool`s"

        # body
        load_bits = DMUX8WAY(load, address[:3])
        new_ram8s = tuple(
            r(xs, load_bits[i], address[3:]) for i, r in enumerate(self.ram8s)
        )
        new_ram64 = RAM64(new_ram8s)

        # post-conditions
        assert isinstance(new_ram64, RAM64), "`new_ram64` must be a `RAM64`"
        assert all(
            isinstance(r, RAM8) for r in new_ram64.ram8s
        ), "`new_ram64.ram8s` must be an 8-tuple of `RAM8`s"

        if load:
            address_idx = bool_tuple_to_int(address)
            assert new_ram64.out[address_idx] == xs, "new value must be stored when load=1"

        if not load:
            assert self.out == new_ram64.out, "old value must be kept when load=0"

        return new_ram64

    @property
    def out(self) -> tuple[tuple[bool, ...], ...]:
        output: tuple[tuple[bool, ...], ...] = ()

        for ram8 in self.ram8s:
            output += ram8.out
    
        return output

@dataclass(frozen=True)
class RAM512:
    """512-register memory, each 16-bits."""

    ram64s: tuple[RAM64, ...]

    def __post_init__(self) -> None:
        assert all(
            isinstance(r, RAM64) for r in self.ram64s
        ), "`ram64s` must be a tuple of `RAM64`s"
        assert len(self.ram64s) == 8, "`ram64s` must be a 8-tuple of `RAM8`s"

    def __call__(
        self,
        xs: tuple[bool, ...],
        load: bool,
        address: tuple[bool, ...],
    ) -> "RAM512":
        # pre-conditions
        assert is_n_bit_vector(xs, n=16), "`xs` must be a 16-tuple of `bool`s"
        assert isinstance(load, bool), "`load` must be a `bool`"
        assert is_n_bit_vector(address, n=9), "`address` must be a 9-tuple of `bool`s"

        # body
        load_bits = DMUX8WAY(load, address[:3])
        new_ram64s = tuple(
            r(xs, load_bits[i], address[3:]) for i, r in enumerate(self.ram64s)
        )
        new_ram512 = RAM512(new_ram64s)

        # post-conditions
        assert isinstance(new_ram512, RAM512), "`new_ram512` must be a `RAM512`"
        assert all(
            isinstance(r, RAM64) for r in new_ram512.ram64s
        ), "`new_ram512.ram64s` must be an 8-tuple of `RAM64`s"

        if load:
            address_idx = bool_tuple_to_int(address)
            assert new_ram512.out[address_idx] == xs, "new value must be stored when load=1"

        if not load:
            assert self.out == new_ram512.out, "old value must be kept when load=0"

        return new_ram512

    @property
    def out(self) -> tuple[tuple[bool, ...], ...]:
        output: tuple[tuple[bool, ...], ...] = ()

        for ram64 in self.ram64s:
            output += ram64.out

        return output

@dataclass(frozen=True)
class RAM4K:
    """4,096-register memory, each 16-bits."""

    ram512s: tuple[RAM512, ...]

    def __post_init__(self) -> None:
        assert all(
            isinstance(r, RAM512) for r in self.ram512s
        ), "`ram512s` must be a tuple of `RAM512`s"
        assert len(self.ram512s) == 8, "`ram512s` must be a 8-tuple of `RAM8`s"
    
    def __call__(
        self,
        xs: tuple[bool, ...],
        load: bool,
        address: tuple[bool, ...],
    ) -> "RAM4K":
        # pre-conditions
        assert is_n_bit_vector(xs, n=16), "`xs` must be a 16-tuple of `bool`s"
        assert isinstance(load, bool), "`load` must be a `bool`"
        assert is_n_bit_vector(address, n=12), "`address` must be a 12-tuple of `bool`s"

        # body
        load_bits = DMUX8WAY(load, address[:3])
        new_ram512s = tuple(
            r(xs, load_bits[i], address[3:]) for i, r in enumerate(self.ram512s)
        )
        new_ram4k = RAM4K(new_ram512s)

        # post-conditions
        assert isinstance(new_ram4k, RAM4K), "`new_ram4k` must be a `RAM4K`"
        assert all(
            isinstance(r, RAM512) for r in new_ram4k.ram512s
        ), "`new_ram4k.ram512s` must be an 8-tuple of `RAM512`s"

        if load:
            address_idx = bool_tuple_to_int(address)
            assert new_ram4k.out[address_idx] == xs, "new value must be stored when load=1"

        if not load:
            assert self.out == new_ram4k.out, "old value must be kept when load=0"

        return new_ram4k

    @property
    def out(self) -> tuple[tuple[bool, ...], ...]:
        output: tuple[tuple[bool, ...], ...] = ()

        for ram512 in self.ram512s:
            output += ram512.out

        return output
