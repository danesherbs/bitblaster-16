from dataclasses import dataclass
from typing import Callable
from utils import is_n_bit_vector, sample_bits
from gates import MUX16
from arithmetic import ALU
from memory import BIT, REGISTER16, PC


@dataclass(frozen=True)
class CPU:
    """The Central Processing Unit (CPU). Consists of an ALU and set of registers, designed to fetch and execute instructions written in the Hack machine language."""

    a_register: REGISTER16
    d_register: REGISTER16
    pc: PC

    def __call__(
        self,
        instruction: tuple[bool, ...],
        in_m: tuple[bool, ...],
        reset: bool,
    ) -> "CPU":
        """Returns the next state of the CPU."""
        # pre-conditions
        assert is_n_bit_vector(instruction, n=16), "instruction must be a 16-bit tuple"
        assert is_n_bit_vector(in_m, n=16), "in_m must be a 16-bit tuple"
        assert isinstance(reset, bool), "reset must be a bool"

        # body
        out_m, write_m, address_m, pc = self.out  # outputs in current time step

        new_a_register_value = MUX16(
            xs=instruction,
            ys=out_m,
            sel=instruction[0],
        )

        new_a_register = self.a_register(  # A register in next time step
            xs=new_a_register_value,
            load=True,
        )

        new_pc = self.pc(
            xs=sample_bits(16),  # TODO: implement
            load=False,  # TODO: implement
            inc=True,  # TODO: implement
            reset=reset,
        )

        new_cpu = CPU(
            a_register=new_a_register,
            d_register=self.d_register,
            pc=new_pc,
        )
        
        # post-conditions
        assert isinstance(new_cpu, CPU), "output must be a CPU"
        assert new_a_register.out == new_a_register_value, "A register must be updated"

        return new_cpu

    @property
    def out(self) -> tuple[tuple[bool, ...], bool, tuple[bool, ...], tuple[bool, ...]]:
        out_m = sample_bits(16)
        write_m = False
        address_m = None

        return out_m, write_m, address_m, self.pc.out


@dataclass(frozen=True)
class Memory:
    """The main memory of the computer. Consists of RAM, a screen memory map and a register storing the output of the keyboard."""

    pass


@dataclass(frozen=True)
class Computer:
    """The Hack computer, including the CPU, ROM and RAM. When reset is zero, the program stored in the ROM is executed. When reset is one, the execution of the program restarts."""

    pass
