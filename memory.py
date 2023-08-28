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

    @staticmethod
    def create() -> "REGISTER16":
        """Creates a new 16-bit register with all bits set to 0."""
        dffs = tuple(DFF(False) for _ in range(16))
        bits = tuple(BIT(dff) for dff in dffs)
        register = REGISTER16(bits)

        # post-conditions
        assert isinstance(register, REGISTER16), "`register` must be a `REGISTER16`"
        assert all(
            isinstance(b, BIT) for b in register.bits
        ), "`register.bits` must be a 16-tuple of `BIT`s"
        assert all(
            isinstance(b.dff, DFF) for b in register.bits
        ), "`register.bits` must be a 16-tuple of `BIT`s"
        assert all(
            isinstance(b.dff.out, bool) for b in register.bits
        ), "`register.bits` must be a 16-tuple of `BIT`s"
        assert all(
            b.dff.out == False for b in register.bits
        ), "`register.bits` must be a 16-tuple of `BIT`s"

        return register


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

    @staticmethod
    def create() -> "RAM8":
        """Creates a new 8-register memory with all bits set to 0."""
        registers = tuple(REGISTER16.create() for _ in range(8))
        out = ZERO16
        ram8 = RAM8(registers, out)

        # post-conditions
        assert isinstance(ram8, RAM8), "`ram8` must be a `RAM8`"
        assert all(
            s == ZERO16 for s in ram8.state
        ), "`ram8.state` must be a 8-tuple of 16-tuples of `bool`s"
        assert ram8.out == ZERO16, "`ram8.out` must be a 16-tuple of `bool`s"

        return ram8


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

    @staticmethod
    def create() -> "RAM64":
        """Creates a new 64-register memory with all bits set to 0."""
        ram8s = tuple(RAM8.create() for _ in range(8))
        out = ZERO16
        ram64 = RAM64(ram8s, out)

        # post-conditions
        assert isinstance(ram64, RAM64), "`ram64` must be a `RAM64`"
        assert all(
            s == ZERO16 for s in ram64.state
        ), "`ram64.state` must be a 64-tuple of 16-tuples of `bool`s"
        assert ram64.out == ZERO16, "`ram64.out` must be a 16-tuple of `bool`s"

        return ram64


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

    @staticmethod
    def create() -> "RAM512":
        """Creates a new 512-register memory with all bits set to 0."""
        ram64s = tuple(RAM64.create() for _ in range(8))
        out = ZERO16
        ram512 = RAM512(ram64s, out)

        # post-conditions
        assert isinstance(ram512, RAM512), "`ram512` must be a `RAM512`"
        assert all(
            s == ZERO16 for s in ram512.state
        ), "`ram512.state` must be a 512-tuple of 16-tuples of `bool`s"
        assert ram512.out == ZERO16, "`ram512.out` must be a 16-tuple of `bool`s"

        return ram512


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

    @staticmethod
    def create() -> "RAM4K":
        """Creates a new 4,096-register memory with all bits set to 0."""
        ram512s = tuple(RAM512.create() for _ in range(8))
        out = ZERO16
        ram4k = RAM4K(ram512s, out)

        # post-conditions
        assert isinstance(ram4k, RAM4K), "`ram4k` must be a `RAM4K`"
        assert all(
            s == ZERO16 for s in ram4k.state
        ), "`ram4k.state` must be a 4,096-tuple of 16-tuples of `bool`s"
        assert ram4k.out == ZERO16, "`ram4k.out` must be a 16-tuple of `bool`s"

        return ram4k


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
    
    @staticmethod
    def create() -> "RAM8K":
        """Creates a new 8,192-register memory with all bits set to 0."""
        ram4ks = tuple(RAM4K.create() for _ in range(2))
        out = ZERO16
        ram8k = RAM8K(ram4ks, out)

        # post-conditions
        assert isinstance(ram8k, RAM8K), "`ram8k` must be a `RAM8K`"
        assert all(
            s == ZERO16 for s in ram8k.state
        ), "`ram8k.state` must be a 8,192-tuple of 16-tuples of `bool`s"
        assert ram8k.out == ZERO16, "`ram8k.out` must be a 16-tuple of `bool`s"

        return ram8k


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

    @staticmethod
    def create() -> "RAM16K":
        """Creates a new 16,384-register memory with all bits set to 0."""
        ram4ks = tuple(RAM4K.create() for _ in range(4))
        ram16k = RAM16K(ram4ks, ZERO16)

        # post-conditions
        assert isinstance(ram16k, RAM16K), "`ram16k` must be a `RAM16K`"
        assert all(
            s == ZERO16 for s in ram16k.state
        ), "`ram16k.state` must be a 16,384-tuple of 16-tuples of `bool`s"
        assert ram16k.out == ZERO16, "`ram16k.out` must be `ZERO16`"

        return ram16k


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

    @staticmethod
    def create() -> "PC":
        """Creates a new 16-bit program counter with all bits set to 0."""
        pc = PC(REGISTER16.create())

        # post-conditions
        assert isinstance(pc, PC), "`pc` must be a `PC`"
        assert pc.out == ZERO16, "`pc.out` must be `ZERO16`"

        return pc


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
        # pre-conditions
        assert is_n_bit_vector(address, n=15), "`address` must be a 15-tuple of `bool`s"
        
        # body
        register_idx = to_int(address)
        out = self.registers[register_idx]
        
        # post-conditions
        assert is_n_bit_vector(out, n=16), "`out` must be a 16-tuple of `bool`s"
        
        return out

    @staticmethod
    def create(instructions: tuple[tuple[bool, ...], ...] = tuple()) -> "ROM32K":
        """Creates a `ROM32K` from a tuple of 16-bit instructions. Pads with 0's to reach 32,768 instructions if necessary."""
        # pre-conditions
        assert all(
            is_n_bit_vector(xs, n=16) for xs in instructions
        ), "`instructions` must be a tuple of 16-tuples of `bool`s"
        assert (
            len(instructions) <= 2**15
        ), "`instructions` must be at most a 32,768-tuple"

        # body
        padding = ((False,) * 16,) * (2**15 - len(instructions))
        padded_instructions = instructions + padding
        rom32k = ROM32K(padded_instructions)

        # post-conditions
        assert isinstance(rom32k, ROM32K), "`rom32k` must be a `ROM32K`"

        return rom32k
