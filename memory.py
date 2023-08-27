from dataclasses import dataclass
from gates import MUX, MUX16, MUX4WAY16, MUX8WAY16, DMUX, DMUX4WAY, DMUX8WAY
from arithmetic import INC16
from utils import is_n_bit_vector, to_int

ZERO16 = (False,) * 16


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
class REGISTER16:
    """A 16-bit register."""

    bits: tuple[BIT, ...]

    def __post_init__(self) -> None:
        assert all(isinstance(b, BIT) for b in self.bits), "`bits` must be `BIT`s"
        assert len(self.bits) == 16, "`bits` must be a 16-tuple of `BIT`s"

    def __call__(self, xs: tuple[bool, ...], load: bool) -> "REGISTER16":
        # pre-conditions
        assert is_n_bit_vector(xs, n=16), "`xs` must be a 16-tuple of `bool`s"
        assert isinstance(load, bool), "`load` must be a `bool`"

        # body
        new_bits = tuple(bit(x, load) for bit, x in zip(self.bits, xs))
        new_register = REGISTER16(new_bits)

        # post-conditions
        assert isinstance(
            new_register, REGISTER16
        ), "`new_register` must be a `REGISTER16`"

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

    registers: tuple[REGISTER16, ...]
    out: tuple[bool, ...]

    def __post_init__(self) -> None:
        assert all(
            isinstance(r, REGISTER16) for r in self.registers
        ), "`registers` must be a tuple of `REGISTER16`s"
        assert (
            len(self.registers) == 8
        ), "`registers` must be a 8-tuple of `REGISTER16`s"
        assert is_n_bit_vector(self.out, n=16), "`out` must be a 16-tuple of `bool`s"

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
        new_out = MUX8WAY16(*[r.out for r in new_registers], sel=address)  # type: ignore
        new_ram8 = RAM8(new_registers, new_out)

        # post-conditions
        assert isinstance(new_ram8, RAM8), "`new_ram8` must be a `RAM8`"
        assert all(
            isinstance(r, REGISTER16) for r in new_ram8.registers
        ), "`new_ram8.registers` must be an 8-tuple of `REGISTER16`s"

        if load:
            address_idx = to_int(address)
            selected_register = new_ram8.registers[address_idx]
            assert all(
                v == x for v, x in zip(selected_register.out, xs)
            ), "new value must be stored when load=1"

        if not load:
            assert new_ram8.state == self.state, "old value must be kept when load=0"

        return new_ram8

    @property
    def state(self) -> tuple[tuple[bool, ...], ...]:
        return tuple(r.out for r in self.registers)


@dataclass(frozen=True)
class RAM64:
    """64-register memory, each 16-bits."""

    ram8s: tuple[RAM8, ...]
    out: tuple[bool, ...]

    def __post_init__(self) -> None:
        assert all(
            isinstance(r, RAM8) for r in self.ram8s
        ), "`ram8s` must be a tuple of `RAM8`s"
        assert len(self.ram8s) == 8, "`ram8s` must be a 8-tuple of `RAM8`s"
        assert is_n_bit_vector(self.out, n=16), "`out` must be a 16-tuple of `bool`s"

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
        new_out = MUX8WAY16(*[r.out for r in new_ram8s], sel=address[:3])  # type: ignore
        new_ram64 = RAM64(new_ram8s, new_out)

        # post-conditions
        assert isinstance(new_ram64, RAM64), "`new_ram64` must be a `RAM64`"
        assert all(
            isinstance(r, RAM8) for r in new_ram64.ram8s
        ), "`new_ram64.ram8s` must be an 8-tuple of `RAM8`s"

        if load:
            address_idx = to_int(address)
            assert (
                new_ram64.state[address_idx] == xs
            ), "new value must be stored when load=1"
            assert (
                new_ram64.out == xs
            ), "new value must be returned as `out` when load=1"

        if not load:
            address_idx = to_int(address)
            assert self.state == new_ram64.state, "old value must be kept when load=0"
            assert (
                new_ram64.out == self.state[address_idx]
            ), "old value must be returned as `out` when load=0"

        return new_ram64

    @property
    def state(self) -> tuple[tuple[bool, ...], ...]:
        output: tuple[tuple[bool, ...], ...] = ()

        for ram8 in self.ram8s:
            output += ram8.state

        return output


@dataclass(frozen=True)
class RAM512:
    """512-register memory, each 16-bits."""

    ram64s: tuple[RAM64, ...]
    out: tuple[bool, ...]

    def __post_init__(self) -> None:
        assert all(
            isinstance(r, RAM64) for r in self.ram64s
        ), "`ram64s` must be a tuple of `RAM64`s"
        assert len(self.ram64s) == 8, "`ram64s` must be a 8-tuple of `RAM8`s"
        assert is_n_bit_vector(self.out, n=16), "`out` must be a 16-tuple of `bool`s"

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
        new_out = MUX8WAY16(*[r.out for r in new_ram64s], sel=address[:3])  # type: ignore
        new_ram512 = RAM512(new_ram64s, new_out)

        # post-conditions
        assert isinstance(new_ram512, RAM512), "`new_ram512` must be a `RAM512`"
        assert all(
            isinstance(r, RAM64) for r in new_ram512.ram64s
        ), "`new_ram512.ram64s` must be an 8-tuple of `RAM64`s"
        
        address_idx = to_int(address)

        if load:
            assert (
                new_ram512.state[address_idx] == xs
            ), "new value must be stored when load=1"
            assert (
                new_ram512.out == xs
            ), "new value must be returned as `out` when load=1"

        if not load:
            assert new_ram512.state == self.state, "old value must be kept when load=0"
            assert (
                new_ram512.out == self.state[address_idx]
            ), "out must be value of RAM at `address` when load=0"

        return new_ram512

    @property
    def state(self) -> tuple[tuple[bool, ...], ...]:
        output: tuple[tuple[bool, ...], ...] = ()

        for ram64 in self.ram64s:
            output += ram64.state

        return output


@dataclass(frozen=True)
class RAM4K:
    """4,096-register memory, each 16-bits."""

    ram512s: tuple[RAM512, ...]
    out: tuple[bool, ...]

    def __post_init__(self) -> None:
        assert all(
            isinstance(r, RAM512) for r in self.ram512s
        ), "`ram512s` must be a tuple of `RAM512`s"
        assert len(self.ram512s) == 8, "`ram512s` must be a 8-tuple of `RAM8`s"
        assert is_n_bit_vector(self.out, n=16), "`out` must be a 16-tuple of `bool`s"

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
        new_out = MUX8WAY16(*[r.out for r in new_ram512s], sel=address[:3])  # type: ignore
        new_ram4k = RAM4K(new_ram512s, new_out)

        # post-conditions
        assert isinstance(new_ram4k, RAM4K), "`new_ram4k` must be a `RAM4K`"
        assert all(
            isinstance(r, RAM512) for r in new_ram4k.ram512s
        ), "`new_ram4k.ram512s` must be an 8-tuple of `RAM512`s"
        
        address_idx = to_int(address)

        if load:
            assert (
                new_ram4k.state[address_idx] == xs
            ), "new value must be stored when load=1"
            assert (
                new_ram4k.out == xs
            ), "new value must be returned as `out` when load=1"

        if not load:
            assert self.state == new_ram4k.state, "old value must be kept when load=0"
            assert (
                new_ram4k.out == self.state[address_idx]
            ), "out must be value of RAM at `address` when load=0"

        return new_ram4k

    @property
    def state(self) -> tuple[tuple[bool, ...], ...]:
        output: tuple[tuple[bool, ...], ...] = ()

        for ram512 in self.ram512s:
            output += ram512.state

        return output


# now write one for RAM8K
@dataclass(frozen=True)
class RAM8K:
    """8,192-register memory, each 16-bits."""

    ram4ks: tuple[RAM4K, ...]
    out: tuple[bool, ...]

    def __post_init__(self) -> None:
        assert all(
            isinstance(r, RAM4K) for r in self.ram4ks
        ), "`ram4ks` must be a tuple of `RAM4K`s"
        assert len(self.ram4ks) == 2, "`ram4ks` must be a 2-tuple of `RAM4K`s"
        assert is_n_bit_vector(self.out, n=16), "`out` must be a 16-tuple of `bool`s"

    def __call__(
        self,
        xs: tuple[bool, ...],
        load: bool,
        address: tuple[bool, ...],
    ) -> "RAM8K":
        # pre-conditions
        assert is_n_bit_vector(xs, n=16), "`xs` must be a 16-tuple of `bool`s"
        assert isinstance(load, bool), "`load` must be a `bool`"
        assert is_n_bit_vector(address, n=13), "`address` must be a 13-tuple of `bool`s"

        # body
        load_bits = DMUX(load, address[0])
        new_ram4ks = tuple(
            r(xs, load_bits[i], address[1:]) for i, r in enumerate(self.ram4ks)
        )
        new_out = MUX16(
            new_ram4ks[0].out,
            new_ram4ks[1].out,
            address[0],
        )
        new_ram8k = RAM8K(new_ram4ks, new_out)

        # post-conditions
        assert isinstance(new_ram8k, RAM8K), "`new_ram8k` must be a `RAM8K`"
        assert all(
            isinstance(r, RAM4K) for r in new_ram8k.ram4ks
        ), "`new_ram8k.ram4ks` must be an 2-tuple of `RAM4K`s"

        address_idx = to_int(address)

        if load:
            assert (
                new_ram8k.state[address_idx] == xs
            ), "new value must be stored when load=1"
            assert (
                new_ram8k.out == xs
            ), "new value must be returned as `out` when load=1"

        if not load:
            assert self.state == new_ram8k.state, "old value must be kept when load=0"
            assert (
                new_ram8k.out == self.state[address_idx]
            ), "out must be value of RAM at `address` when load=0"

        return new_ram8k

    @property
    def state(self) -> tuple[tuple[bool, ...], ...]:
        output: tuple[tuple[bool, ...], ...] = ()

        for ram4k in self.ram4ks:
            output += ram4k.state

        return output


@dataclass(frozen=True)
class RAM16K:
    """16,384-register memory, each 16-bits."""

    ram4ks: tuple[RAM4K, ...]
    out: tuple[bool, ...]

    def __post_init__(self) -> None:
        assert all(
            isinstance(r, RAM4K) for r in self.ram4ks
        ), "`ram4ks` must be a tuple of `RAM4K`s"
        assert len(self.ram4ks) == 4, "`ram4ks` must be a 4-tuple of `RAM4K`s"
        assert is_n_bit_vector(self.out, n=16), "`out` must be a 16-tuple of `bool`s"

    def __call__(
        self,
        xs: tuple[bool, ...],
        load: bool,
        address: tuple[bool, ...],
    ) -> "RAM16K":
        # pre-conditions
        assert is_n_bit_vector(xs, n=16), "`xs` must be a 16-tuple of `bool`s"
        assert isinstance(load, bool), "`load` must be a `bool`"
        assert is_n_bit_vector(address, n=14), "`address` must be a 14-tuple of `bool`s"

        # body
        load_bits = DMUX4WAY(load, address[:2])
        new_ram4ks = tuple(
            r(xs, load_bits[i], address[2:]) for i, r in enumerate(self.ram4ks)
        )
        new_out = MUX4WAY16(  # type: ignore
            *[r.out for r in new_ram4ks],
            sel=address[:2],
        ) 
        new_ram16k = RAM16K(new_ram4ks, new_out)

        # post-conditions
        assert isinstance(new_ram16k, RAM16K), "`new_ram16k` must be a `RAM16K`"
        assert all(
            isinstance(r, RAM4K) for r in new_ram16k.ram4ks
        ), "`new_ram16k.ram4ks` must be an 4-tuple of `RAM4K`s"
        
        address_idx = to_int(address)

        if load:
            assert (
                new_ram16k.state[address_idx] == xs
            ), "new value must be stored when load=1"
            assert (
                new_ram16k.out == xs
            ), "new value must be returned as `out` when load=1"

        if not load:
            assert self.state == new_ram16k.state, "old value must be kept when load=0"
            assert (
                new_ram16k.out == self.state[address_idx]
            ), "out must be value of RAM at `address` when load=0"

        return new_ram16k

    @property
    def state(self) -> tuple[tuple[bool, ...], ...]:
        output: tuple[tuple[bool, ...], ...] = ()

        for ram4k in self.ram4ks:
            output += ram4k.state

        return output


@dataclass(frozen=True)
class PC:
    """A 16-bit program counter with load, inc and reset control bits."""

    register: REGISTER16

    def __post_init__(self) -> None:
        assert isinstance(
            self.register, REGISTER16
        ), "`register` must be a `REGISTER16`"

    def __call__(
        self,
        xs: tuple[bool, ...],
        load: bool,
        inc: bool,
        reset: bool,
    ) -> "PC":
        # pre-conditions
        assert is_n_bit_vector(xs, n=16), "`xs` must be a 16-tuple of `bool`s"
        assert isinstance(load, bool), "`load` must be a `bool`"
        assert isinstance(inc, bool), "`inc` must be a `bool`"
        assert isinstance(reset, bool), "`reset` must be a `bool`"

        # body
        a = MUX16(self.out, INC16(self.out), inc)
        b = MUX16(a, xs, load)
        c = MUX16(b, ZERO16, reset)
        new_register = self.register(c, True)
        new_pcounter = PC(new_register)

        # post-conditions
        assert isinstance(new_pcounter, PC), "`new_pcounter` must be a `PCOUNTER`"
        assert isinstance(
            new_pcounter.register, REGISTER16
        ), "`new_pcounter.register` must be a `REGISTER16`"

        if reset:
            assert new_pcounter.out == ZERO16, "counter must be reset when reset=1"
        elif load:
            assert new_pcounter.out == xs, "new value must be stored when load=1"
        elif inc:
            assert new_pcounter.out == INC16(self.out), "counter must be incremented"
        else:
            assert new_pcounter.out == self.out, "counter must be unchanged"

        return new_pcounter

    @property
    def out(self) -> tuple[bool, ...]:
        return self.register.out


@dataclass(frozen=True)
class ROM32K:
    """32,768-register memory, each 16-bits. This is a primitive component."""

    registers: tuple[tuple[bool, ...], ...]

    def __post_init__(self) -> None:
        assert all(
            is_n_bit_vector(xs, n=16) for xs in self.registers
        ), "`registers` must be a tuple of 16-tuples of `bool`s"
        assert len(self.registers) == 2**15, "`registers` must be a 32,768-tuple"

    def __call__(self, address: tuple[bool, ...]) -> tuple[bool, ...]:
        register_idx = to_int(address)
        return self.registers[register_idx]
