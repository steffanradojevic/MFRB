"""
Python 3.12.3
Leiden University
Author: Steffan Radojevic
Email: steffanradojevic@gmail.com
Date: 5 September 2025
Description: Generates RISC-V assembly files for various striding configurations.
Each assembly files consists of a prologue, loop body and epilogue.
"""

import os


class microKernel:
    def __init__(
        self,
        strides,
        portions,
        arr_length,
        SEW=32,
        elementSize=4,
        MAXVLEN=256,
        MAXSP=32,
        formatting=False,
        kernel="readKernel",
    ):
        self.strides = strides
        self.portions = portions
        self.SEW = SEW  # Selected element width
        self.arr_length = arr_length
        self.elementSize = elementSize
        self.MAXVLEN = MAXVLEN
        self.MAXSP = MAXSP  # Maximum strides * unrolls
        self.elements_per_instr = int(
            MAXVLEN / SEW
        )  # Number of elements per vector instruction
        self.elements_per_loop = int(
            strides * portions * self.elements_per_instr
        )  # Number of elements per loop iteration

        self.formatting = formatting

        self.kernel = kernel

        self.idx_reg = 0

        # Keep track of register values
        self.reg_values = {
            "x0": 0,
            "x1": 0,
            "x2": 0,
            "x3": 0,
            "x4": 0,
            "x5": 0,
            "x6": 0,
            "x7": 0,
            "x8": 0,
            "x9": 0,
            "x10": 0,
            "x11": 0,
            "x12": 0,
            "x13": 0,
            "x14": 0,
            "x15": 0,
            "x16": 0,
            "x17": 0,
            "x18": 0,
            "x19": 0,
            "x20": 0,
            "x21": 0,
            "x22": 0,
            "x23": 0,
            "x24": 0,
            "x25": 0,
            "x26": 0,
            "x27": 0,
            "x28": 0,
            "x29": 0,
            "x30": 0,
            "x31": 0,
        }

        # Stride memory values
        self.stride_registers = [
            "x4",
            "x5",
            "x6",
            "x7",
            "x8",
            "x9",
            "x10",
            "x11",
            "x12",
            "x13",
            "x14",
            "x15",
            "x16",
            "x17",
            "x18",
            "x19",
            "x20",
            "x21",
            "x22",
            "x23",
            "x24",
            "x25",
            "x26",
            "x27",
            "x28",
            "x29",
            "x30",
        ]

    def create_filename(self):
        function_name = f"microKernel"
        file_name_postfix = function_name + str(self.strides) + "x" + str(self.portions)
        file_name = f"../kernels/{file_name_postfix}.s"

        return function_name, file_name

    def generate_prologue(self):
        """
        Store callee-saved registers on the stack:
            - x1, x3, x4, x8-10, x18-27
        Initialize loop bounds and loop counters:
            - x3 = loop counter
            - x1 = loop bound
        Initialize/Store stride memory addresses in registers
            - x4-x30 available registers for stride memory addresses

        x0 reserved for start value array
        """

        code = []

        # Determine stride length between each stride unroll
        array_size_bytes = self.arr_length * 4
        stride_len_bytes = int(array_size_bytes / self.strides)

        # Generate assembly header
        code.append(f"\t.text \n")
        code.append(f"\t.global microKernel # Vector\n")
        code.append(f"\n")
        code.append(
            f"microKernel:  # arr_length={self.arr_length} | in bytes={array_size_bytes}\n"
        )

        if self.formatting:
            code.append(f"\n")
            code.append(f"# put registers on stack \n")

        # Store callee-saved registers on the stack
        code.append(f"\taddi sp, sp, -128\n")
        code.append(f"\tsd x1, 0(sp)\n")
        code.append(f"\tsd x3, 8(sp)\n")
        code.append(f"\tsd x4, 16(sp)\n")
        code.append(f"\tsd x8, 24(sp)\n")
        code.append(f"\tsd x9, 32(sp)\n")
        code.append(f"\tsd x10, 40(sp)\n")
        code.append(f"\tsd x18, 48(sp)\n")
        code.append(f"\tsd x19, 56(sp)\n")
        code.append(f"\tsd x20, 64(sp)\n")
        code.append(f"\tsd x21, 72(sp)\n")
        code.append(f"\tsd x22, 80(sp)\n")
        code.append(f"\tsd x23, 88(sp)\n")
        code.append(f"\tsd x24, 96(sp)\n")
        code.append(f"\tsd x25, 104(sp)\n")
        code.append(f"\tsd x26, 112(sp)\n")
        code.append(f"\tsd x27, 120(sp)\n")

        if self.formatting:
            code.append(f"\n")
            code.append(f"# loop counter and loop bound  \n")

        loops = int(
            self.arr_length / self.elements_per_loop
        )  # Determine number of loops

        code.append(f"\taddi x3, x0, 0\n")  # Loop counter
        code.append(f"\n")

        # Loop bound
        code.append(f"# loop bound={loops}\n")
        lui_offset, addi_offset = self.split_immediate_lui_addi(loops)
        code.append(f"\tlui x1, {lui_offset}\n")
        code.append(f"\taddi x1, x1, {addi_offset}\n")

        # Generate stride memory addresses
        for stride in range(self.strides):

            # Determine stride address and retrieve lui and addi segments
            stride_address = stride * stride_len_bytes
            lui_offset, addi_offset = self.split_immediate_lui_addi(stride_address)

            if self.formatting:
                code.append(f"\n")
                code.append(
                    f"# stride {stride + 1} | bytes offset: {stride_address} \n"
                )

            # Load 32-bit immediate stride memory address by combining two lui and addi segments
            code.append(f"\tlui {self.stride_registers[self.idx_reg]}, {lui_offset}\n")
            code.append(
                f"\taddi {self.stride_registers[self.idx_reg]}, {self.stride_registers[self.idx_reg]}, {addi_offset}\n"
            )

            # x4 = array base address
            if stride == 0:
                code.append(f"\tadd x4, x4, a0\n")

            else:
                code.append(
                    f"\tadd {self.stride_registers[self.idx_reg]}, {self.stride_registers[self.idx_reg]}, x4\n"
                )

            self.reg_values[self.idx_reg] = (
                stride_address  # Keep track of stride memory address
            )
            self.idx_reg += 1  # Point to next available register

        code.append(f"\n")

        # Vector configuration for RVV 1.0 standard
        code.append(f"\tvsetivli x0, 8, e32, m1\n")
        code.append(f"\n")

        return "".join(code)

    def generate_loop_body(self):
        """
        Memory accesses for each striding configurations
            - Loop over each stride and portion unroll
            - Generate memory access for either readKernel or writeKernel
        Loop condition / increment
        """

        code = []
        idx_reg = 0
        vreg_idx = 0

        code.append(f".Loop:\n")

        # Store loop counter in v0 for the writeKernel
        if self.kernel == "writeKernel":
            code.append(f"\tfcvt.s.w f0, x3 \n")
            code.append(f"\tvfmv.v.f v0, f0\n")

        # Calculate increment each memory access (portion unroll)
        bytes_per_instr = int(self.MAXVLEN / self.SEW) * 4

        # For each stride and portion unroll, generate the memory accesses
        for stride in range(self.strides):
            if self.formatting:
                code.append(f"\n")
                code.append(f"\t# stride {stride + 1}\n")
            portion_offset = 0
            for portion in range(self.portions):
                # Reset vreg (vector register) to 0 when exceeding vreg 31
                if vreg_idx > 31:
                    vreg_idx = 0

                # Compute memory access array value in bytes, includes in comments to aid debugging
                array_id_value = self.reg_values[self.stride_registers[stride]] + (
                    portion_offset
                )

                # Generate memory access for readKernel vle32.v vector instructions
                if self.kernel == "readKernel":
                    code.append(
                        f"\tvle32.v v{vreg_idx}, ({self.stride_registers[stride]})  #array id: {int(array_id_value/4)} bytes={array_id_value}\n"
                    )
                    code.append(
                        f"\taddi {self.stride_registers[stride]}, {self.stride_registers[stride]}, {bytes_per_instr}\n"
                    )

                # Generate memory access for writeKernel vse32.v vector instructions
                elif self.kernel == "writeKernel":
                    code.append(
                        f"\tvse32.v v0, ({self.stride_registers[stride]})  #array id: {int(array_id_value/4)} bytes={array_id_value}\n"
                    )
                    code.append(
                        f"\taddi {self.stride_registers[stride]}, {self.stride_registers[stride]}, {bytes_per_instr}\n"
                    )

                vreg_idx += 1  # Point to next vector register
                portion_offset += 32  # Point to next portion unroll

        if self.formatting:
            code.append(f"\n")
            code.append(f"# loop control\n")

        # Loop condition / increment
        code.append(f"\taddi x3, x3, 1\n")
        code.append(f"\tbne x3, x1, .Loop\n")
        code.append(f"\n")

        return "".join(code)

    def generate_epilogue(self):
        """
        Restore callee-saved registers from stack
            - Restore callee-saved registers x19-x30
        Return function
        """

        code = []

        if self.formatting:
            code.append(f"\n")
            code.append(f"# put registers on stack \n")

        # Restore callee-saved registers
        code.append(f".Epilogue:\n")
        code.append(f"\tld x1, 0(sp)\n")
        code.append(f"\tld x3, 8(sp)\n")
        code.append(f"\tld x4, 16(sp)\n")
        code.append(f"\tld x8, 24(sp)\n")
        code.append(f"\tld x9, 32(sp)\n")
        code.append(f"\tld x10, 40(sp)\n")
        code.append(f"\tld x18, 48(sp)\n")
        code.append(f"\tld x19, 56(sp)\n")
        code.append(f"\tld x20, 64(sp)\n")
        code.append(f"\tld x21, 72(sp)\n")
        code.append(f"\tld x22, 80(sp)\n")
        code.append(f"\tld x23, 88(sp)\n")
        code.append(f"\tld x24, 96(sp)\n")
        code.append(f"\tld x25, 104(sp)\n")
        code.append(f"\tld x26, 112(sp)\n")
        code.append(f"\tld x27, 120(sp)\n")
        code.append(f"\taddi sp, sp, 128\n")

        # Return function
        code.append(f"\tret\n")
        code.append(f"\n")

        return "".join(code)

    def generate_assembly_file(self):
        """
        Generate assembly files along with the set configurations
        Assembly file consists of three parts.

        Assembly Prologue:
            - Store callee-saved registers on stack
            - Initialize loop bounds and loop counters
            - Store stride memory addresses in registers

        Assembly Loop Body:
            - Memory accesses for each striding configurations
            - Loop condition / increment

        Assembly Epilogue:
            - Restore callee-saved registers from stack
            - Return function
        """

        # Resize the array depended on striding configurations and memory access size
        self.arr_length = (self.arr_length // self.elements_per_loop) * (
            self.elements_per_loop
        )

        code = []

        # Generate assembly instructions
        code.append(self.generate_prologue())
        code.append(self.generate_loop_body())
        code.append(self.generate_epilogue())

        function_name, file_name = self.create_filename()

        with open(file_name, "w+") as f:
            f.write("".join(code))

    def split_immediate_lui_addi(self, offset):
        """
        We will use lui and addi to load in every immediate
        To reduce complexity, maximum immediate value is 32 bits
        With lui we can load in the upper 20 bits
        with addi we can load the lower 12 bits
        For lui we dont need bitmasking, we can just shift 12 right e.g.
        lui we want lui x1, (integer >> 12)
        For addi we can not shift like ((integer << 20) >> 12) because it will generate very big numbers
        We can use a simpel bitmask to get the first 12 bits
        Addi can only add 11 bit, so if the 12 bit is set we have to to something different
        We add 1 to lui, and then substract the different between 2048 (12 bit) and the first 11 bits

        example:
        decimal: 123060208  binary: 111010101011011111111110000
        lui: 111010101011011 31:12 (30043) (it will get shifted left 12 times when loading)
        so actually it is: 111010101011011000000000000

        addi: 111111110000 12 bit is set so we transform it into 11 bits: 11111110000

        because the 12th bit is set, we add 1 to lui
        111010101011011
                      1 +
        -----------------
        111010101011100 (decimal = 30044)

        And when these get loaded in the upper 20 bits it is:
        111010101011100000000000000 (decimal = 123060224)

        Then we take the difference of 2048 and the 11 bits of addi:
        111111111111
         11111110000  -
        --------------
                1111  (decimal 16)

        We substract this from lui so 123060224 - 16 = 123060208
        So when the 12 bit is set, this is how we load it
        """

        copy_offset = offset
        lui_offset = copy_offset >> 12

        # Bit 12 is set, different calculation
        if (0b100000000000 & offset) != 0:

            bitmask_addi = 0b11111111111
            addi_offset = bitmask_addi & offset

            lui_offset += 1
            addi_offset = (2048 - addi_offset) * -1

            return lui_offset, addi_offset

        # Normal approach
        else:
            bitmask_addi = 0b111111111111
            addi_offset = bitmask_addi & offset

        return lui_offset, addi_offset

    def return_array_size(self):
        return self.arr_length
