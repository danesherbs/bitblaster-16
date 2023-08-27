import random

from dataclasses import dataclass, field
from typing import Optional
from utils import is_n_bit_vector, sample_bits, is_non_negative, ZERO16
from gates import AND, OR, OR16, NOT, MUX16
from arithmetic import ALU
from memory import REGISTER16, PC


@dataclass(frozen=True)
class CPU:
    """The Central Processing Unit (CPU). Consists of an ALU and set of registers, designed to fetch and execute instructions written in the Hack machine language."""

    # inputs
    a_register: REGISTER16
    d_register: REGISTER16
    pc: PC

    # outputs (initially None to allow for random initialization)
    out_m: Optional[tuple[bool, ...]] = None
    write_m: Optional[bool] = None
    zr: Optional[bool] = None
    ng: Optional[bool] = None

    def __post_init__(self) -> None:
        if self.out_m is None:
            object.__setattr__(self, "out_m", sample_bits(16))
            object.__setattr__(self, "write_m", random.choice([True, False]))
            object.__setattr__(self, "zr", self.out_m == ZERO16)
            object.__setattr__(self, "ng", not is_non_negative(self.out_m))  # type: ignore

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
        assert isinstance(self.zr, bool), "zr must be a bool"
        assert isinstance(self.ng, bool), "ng must be a bool"

        # body
        new_a_register_value = MUX16(
            xs=instruction,  # A-instruction
            ys=self.out_m,  # ALU output from current time step
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
            xs=self.out_m,
            load=AND(
                instruction[0],  # is C-instruction
                instruction[11],  # is d2=1
            ),
        )

        selected_register_value = MUX16(
            xs=self.a_register.out,  # A register in current time step
            ys=in_m,  # M register in current time step
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
                x=AND(is_jgt, AND(NOT(self.ng), NOT(self.zr))),
                y=OR(
                    x=AND(is_jeq, self.zr),
                    y=OR(
                        x=AND(is_jge, NOT(self.ng)),
                        y=OR(
                            x=AND(is_jlt, self.ng),
                            y=OR(
                                x=AND(is_jne, NOT(self.zr)),
                                y=OR(
                                    x=AND(is_jle, OR(self.ng, self.zr)),
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
            out_m=new_out_m,
            write_m=new_write_m,
            zr=new_zr,
            ng=new_ng,
        )

        # post-conditions
        assert isinstance(new_cpu, CPU), "output must be a CPU"

        return new_cpu

    @property
    def address_m(self) -> tuple[bool, ...]:
        """Returns the memory address to which `out_m` should be written."""
        return self.a_register.out


@dataclass(frozen=True)
class Memory:
    """The main memory of the computer. Consists of RAM, a screen memory map and a register storing the output of the keyboard."""

    pass


@dataclass(frozen=True)
class Computer:
    """The Hack computer, including the CPU, ROM and RAM. When reset is zero, the program stored in the ROM is executed. When reset is one, the execution of the program restarts."""

    pass
