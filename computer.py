from dataclasses import dataclass
from gates import AND, OR, NOT, MUX16, DMUX
from arithmetic import ALU
from memory import REGISTER16, RAM8K, RAM16K, ROM32K, PC
from utils import (
    ZERO16,
    is_n_bit_vector,
    is_negative,
    to_int,
)


# Symbol to machine code lookup tables for C-instructions
DEST_SYMBOL_TO_INSTRUCTION = {
    "null": 0b000,
    "M": 0b001,
    "D": 0b010,
    "MD": 0b011,
    "A": 0b100,
    "AM": 0b101,
    "AD": 0b110,
    "AMD": 0b111,
}

COMP_SYMBOL_TO_INSTRUCTION = {
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

JUMP_SYMBOL_TO_INSTRUCTION = {
    "null": 0b000,
    "JGT": 0b001,
    "JEQ": 0b010,
    "JGE": 0b011,
    "JLT": 0b100,
    "JNE": 0b101,
    "JLE": 0b110,
    "JMP": 0b111,
}


@dataclass(frozen=True)
class CPU:
    """The Central Processing Unit (CPU). Consists of an ALU and set of registers, designed to fetch and execute instructions written in the Hack machine language."""

    # inputs
    a_register: REGISTER16
    d_register: REGISTER16
    pc: PC

    # intermediate outputs of ALU
    _zr: bool
    _ng: bool

    # outputs
    out_m: tuple[bool, ...]
    write_m: bool

    def __post_init__(self) -> None:
        if self.out_m == ZERO16:
            assert self._zr, "`zr` must be `True` if `out_m` is zero"
            assert not self._ng, "`ng` must be `False` if `out_m` is zero"

        if is_negative(self.out_m):
            assert not self._zr, "`zr` must be `False` if `out_m` is negative"
            assert self._ng, "`ng` must be `True` if `out_m` is negative"

    def __call__(
        self,
        instruction: tuple[bool, ...],
        in_m: tuple[bool, ...],
        reset: bool,
    ) -> "CPU":
        """Returns the next state of the CPU."""
        # pre-conditions
        assert is_n_bit_vector(instruction, n=16), f"instruction must be a 16-bit tuple"
        assert is_n_bit_vector(in_m, n=16), "in_m must be a 16-bit tuple"
        assert isinstance(reset, bool), "reset must be a bool"

        assert isinstance(self.out_m, tuple), "out_m must be a tuple"
        assert is_n_bit_vector(self.out_m, n=16), "out_m must be a 16-bit tuple"
        assert isinstance(self._zr, bool), "zr must be a bool"
        assert isinstance(self._ng, bool), "ng must be a bool"

        assert is_valid_instruction(
            instruction
        ), "instruction must be a valid instruction"

        # body
        selected_register_value = MUX16(
            xs=self.a_register.out,  # A register in current time step
            ys=in_m,  # RAM[A] register in current time step
            sel=AND(
                x=instruction[0],  # is C-instruction
                y=instruction[3],  # a=1
            ),
        )

        new_out_m, new_zr, new_ng = ALU(
            xs=self.d_register.out,
            ys=selected_register_value,
            zx=instruction[4],  # c1
            nx=instruction[5],  # c2
            zy=instruction[6],  # c3
            ny=instruction[7],  # c4
            f=instruction[8],  # c5
            no=instruction[9],  # c6
        )

        new_a_register_value = MUX16(
            xs=instruction,  # A-instruction
            ys=new_out_m,  # new ALU output is immediately available since its combinational
            sel=instruction[0],  # is C-instruction
        )

        new_a_register = self.a_register(  # A register in next time step
            xs=new_a_register_value,
            load=OR(
                x=NOT(instruction[0]),  # is A-instruction
                y=AND(instruction[0], instruction[10]),  # is C-instruction and d1=1
            ),
        )

        new_d_register = self.d_register(  # D register in next time step
            xs=new_out_m,
            load=AND(
                instruction[0],  # is C-instruction
                instruction[11],  # is d2=1
            ),
        )

        is_jgt = AND(AND(NOT(instruction[13]), NOT(instruction[14])), instruction[15])
        is_jeq = AND(AND(NOT(instruction[13]), instruction[14]), NOT(instruction[15]))
        is_jge = AND(AND(NOT(instruction[13]), instruction[14]), instruction[15])
        is_jlt = AND(AND(instruction[13], NOT(instruction[14])), NOT(instruction[15]))
        is_jne = AND(AND(instruction[13], NOT(instruction[14])), instruction[15])
        is_jle = AND(AND(instruction[13], instruction[14]), NOT(instruction[15]))
        is_jmp = AND(AND(instruction[13], instruction[14]), instruction[15])

        should_jmp = AND(
            x=instruction[0],  # is C-instruction
            y=OR(
                x=AND(is_jgt, AND(NOT(self._ng), NOT(self._zr))),
                y=OR(
                    x=AND(is_jeq, self._zr),
                    y=OR(
                        x=AND(is_jge, NOT(self._ng)),
                        y=OR(
                            x=AND(is_jlt, self._ng),
                            y=OR(
                                x=AND(is_jne, NOT(self._zr)),
                                y=OR(
                                    x=AND(is_jle, OR(self._ng, self._zr)),
                                    y=is_jmp,
                                ),
                            ),
                        ),
                    ),
                ),
            ),
        )

        new_pc = self.pc(
            xs=self.a_register.out,
            load=should_jmp,
            inc=True,
            reset=reset,
        )

        new_write_m = AND(
            x=instruction[0],  # is C-instruction
            y=instruction[12],  # is d3=1
        )

        new_cpu = CPU(
            a_register=new_a_register,
            d_register=new_d_register,
            pc=new_pc,
            _zr=new_zr,
            _ng=new_ng,
            out_m=new_out_m,
            write_m=new_write_m,
        )

        # post-conditions
        assert isinstance(new_cpu, CPU), "output must be a CPU"
        assert is_n_bit_vector(new_cpu.out_m, n=16), "out_m must be a 16-bit tuple"
        assert isinstance(new_cpu.write_m, bool), "write_m must be a bool"
        assert is_n_bit_vector(
            new_cpu.address_m, n=15
        ), "address_m must be a 15-bit tuple"
        assert is_n_bit_vector(new_cpu.pc_out, n=15), "pc must be a 15-bit tuple"

        return new_cpu

    @property
    def address_m(self) -> tuple[bool, ...]:
        """Returns the memory address to which `out_m` should be written."""
        return self.a_register.out[1:]

    @property
    def pc_out(self) -> tuple[bool, ...]:
        """Returns the address of the next instruction."""
        return self.pc.out[1:]

    @staticmethod
    def create() -> "CPU":
        """Returns a new `CPU` with all registers initialized to zero."""
        a_register = REGISTER16.create()
        d_register = REGISTER16.create()
        pc = PC.create()
        return CPU(
            a_register=a_register,
            d_register=d_register,
            pc=pc,
            _zr=True,
            _ng=False,
            out_m=ZERO16,
            write_m=False,
        )


@dataclass(frozen=True)
class Memory:
    """The main memory of the computer. Consists of RAM, a screen memory map and a register storing the output of the keyboard."""

    ram: RAM16K
    screen: RAM8K
    keyboard: REGISTER16
    out: tuple[bool, ...]

    def __call__(
        self,
        xs: tuple[bool, ...],
        address: tuple[bool, ...],
        load: bool,
    ) -> "Memory":
        # pre-conditions
        assert is_n_bit_vector(xs, n=16), "xs must be a 16-bit tuple"
        assert is_n_bit_vector(address, n=15), "address must be a 15-bit tuple"
        assert isinstance(load, bool), "load must be a bool"
        assert (
            0 <= to_int(address) < 2**14 + 2**13
        ), "address must be in [0, 2^14 + 2^13)"

        # body
        load_bits = DMUX(
            x=load,
            sel=address[0],  # 15th bit is 1 means address >= 2^14
        )

        new_ram = self.ram(
            xs=xs,
            load=load_bits[0],
            address=address[1:],
        )

        new_screen = self.screen(
            xs=xs,
            load=load_bits[1],
            address=address[2:],  # last 13 bits goes to screen
        )

        new_keyboard = self.keyboard

        new_out = MUX16(
            xs=new_ram.out,
            ys=MUX16(
                xs=new_screen.out,
                ys=new_keyboard.out,
                sel=AND(
                    address[0],
                    address[1],
                ),
            ),
            sel=address[0],
        )

        new_memory = Memory(
            ram=new_ram,
            screen=new_screen,
            keyboard=new_keyboard,
            out=new_out,
        )

        # post-conditions
        assert isinstance(new_memory, Memory), "output must be of type `Memory`"

        return new_memory

    @property
    def state(self) -> tuple[tuple[bool, ...], ...]:
        """The entire state of the main memory."""
        return self.ram.state + self.screen.state + (self.keyboard.out,)

    @staticmethod
    def create() -> "Memory":
        """Returns a new `Memory` with all registers initialized to zero."""
        ram = RAM16K.create()
        screen = RAM8K.create()
        keyboard = REGISTER16.create()
        return Memory(ram, screen, keyboard, ZERO16)


@dataclass(frozen=True)
class Computer:
    """The Hack computer, including the CPU, ROM and RAM. When reset is zero, the program stored in the ROM is executed. When reset is one, the execution of the program restarts."""

    rom: ROM32K
    cpu: CPU
    memory: Memory

    def __call__(self, reset: bool) -> "Computer":
        new_cpu = self.cpu(
            instruction=self.rom(self.cpu.pc_out),
            in_m=self.memory.out,
            reset=reset,
        )

        new_memory = self.memory(
            xs=new_cpu.out_m,
            address=self.cpu.address_m,
            load=new_cpu.write_m,
        )

        new_computer = Computer(
            rom=self.rom,
            cpu=new_cpu,
            memory=new_memory,
        )

        return new_computer

    @staticmethod
    def create(instructions: tuple[tuple[bool, ...], ...]) -> "Computer":
        """Returns a new `Computer` with the given `instructions` loaded into ROM."""
        # pre-conditions
        assert isinstance(instructions, tuple), "`instructions` must be a tuple"
        assert all(
            isinstance(instruction, tuple) for instruction in instructions
        ), "each instruction must be a tuple"
        assert all(
            is_valid_instruction(instruction) for instruction in instructions
        ), "each instruction must be a valid instruction"

        # body
        rom = ROM32K.create(instructions)
        cpu = CPU.create()
        memory = Memory.create()
        computer = Computer(rom, cpu, memory)

        # post-conditions
        assert isinstance(computer, Computer), "output must be a `Computer`"

        return computer


def is_valid_instruction(instruction: tuple[bool, ...]) -> bool:
    """Returns `True` iff `instruction` is a valid 16-bit Hack machine language instruction."""
    if not is_n_bit_vector(instruction, n=16):
        return False

    if instruction[0] == False:
        return True

    comp = instruction[3:10]
    dest = instruction[10:13]
    jump = instruction[13:16]

    if to_int(comp) not in COMP_SYMBOL_TO_INSTRUCTION.values():
        return False

    if to_int(dest) not in DEST_SYMBOL_TO_INSTRUCTION.values():
        return False

    if to_int(jump) not in JUMP_SYMBOL_TO_INSTRUCTION.values():
        return False

    return True


def render_screen(screen: tuple[tuple[bool, ...], ...]) -> None:
    import matplotlib.pyplot as plt  # type: ignore
    import numpy as np

    # pre-conditions
    assert len(screen) == 2**13, "screen must be 2^13 16-bit numbers"
    assert all(is_n_bit_vector(v, n=16) for v in screen), "screen must be 16-bit tuples"

    # body
    img_array = np.zeros((256, 512), dtype=np.uint8)
    row, col = 0, 0

    for register in screen:
        for bit in register:
            color = 255 if bit else 0
            img_array[row, col] = color

            col += 1
            if col >= 512:
                col = 0
                row += 1

    plt.title("🔥 BitBlaster 16 🔥")
    plt.imshow(img_array, cmap="gray")
    plt.axis("off")
    plt.show()
