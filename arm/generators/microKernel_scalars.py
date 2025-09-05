"""
Python 3.11.2
Leiden University
Author: Steffan Radojevic
Email: steffanradojevic@gmail.com
Date: 3 September 2025 
Description: Generates ARM assembly files for various striding configurations. 
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
        self.kernel = kernel
        self.strides = strides
        self.portions = portions
        self.SEW = SEW  # selected element width
        self.arr_length = arr_length
        self.elementSize = elementSize
        self.MAXVLEN = MAXVLEN
        self.MAXSP = MAXSP  # maximum strides * unrolls
        self.elements_per_instr = 1  # Scalar instruction always 1 element
        self.elements_per_loop = (
            strides * portions * self.elements_per_instr
        )  # Number of elements per loop iteration

        self.formatting = formatting

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
        }

        # Stride memory values
        self.stride_registers = [
            "x3",
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
            - x19-x30
        Initialize loop bounds and loop counters:
            - x1 = loop counter
            - x2 = loop bound
        Initialize/Store stride memory addresses in registers
            - x3-x30 available registers for stride memory addresses

        x0 reserved for start value array
        """

        code = []

        # Determine stride length between each stride unroll
        array_size_bytes = self.arr_length * 4
        stride_len_bytes = int(array_size_bytes / self.strides)

        # Generate assembly header
        code.append(f"\t.text \n")
        code.append(f"\t.global microKernel // ARM \n")
        code.append(f"\n")
        code.append(
            f"microKernel:  // arr_length={self.arr_length} | in bytes={array_size_bytes}\n"
        )

        if self.formatting:
            code.append(f"\n")
            code.append(f"// put registers on stack \n")

        # Store callee-saved registers on the stack
        code.append(f"\tsub sp, sp, #128 \n")
        code.append(f"\tstp x19, x20, [sp, #16]  \n")
        code.append(f"\tstp x21, x22, [sp, #32]  \n")
        code.append(f"\tstp x23, x24, [sp, #48]  \n")
        code.append(f"\tstp x25, x26, [sp, #64]  \n")
        code.append(f"\tstp x27, x28, [sp, #80]  \n")
        code.append(f"\tstp x29, x30, [sp, #96]  \n")

        if self.formatting:
            code.append(f"\n")
            code.append(f"// loop counter and loop bound  \n")

        loops = int(
            self.arr_length / self.elements_per_loop
        )  # Determine number of loops

        code.append(f"\tmovz x1, #0\n")  # Loop counter
        code.append(f"\n")

        # Loop bound
        code.append(f"// loop bound={loops}\n")
        MOVZ, MOVK16, MOVK32, MOVK48 = self.split_immediate_16bit_segments(loops)
        code.append(f"\tmovz x2, #{MOVZ}\n")
        code.append(f"\tmovk x2, #{MOVK16}, LSL #16\n")
        code.append(f"\tmovk x2, #{MOVK32}, LSL #32\n")
        code.append(f"\tmovk x2, #{MOVK48}, LSL #48\n")

        # Generate stride memory addresses
        for stride in range(self.strides):
            # Determine stride address and retrieve 16-bit segments
            stride_address = stride * stride_len_bytes
            MOVZ, MOVK16, MOVK32, MOVK48 = self.split_immediate_16bit_segments(
                stride_address
            )

            if self.formatting:
                code.append(f"\n")
                code.append(
                    f"// stride {stride + 1} | array_id: {int(stride_address/4)} | bytes offset: {stride_address} \n"
                )

            # Load 64-bit immediate stride memory address by combining four 16-bit segments (MOVZ + MOVK with shifts)
            code.append(f"\tmovz {self.stride_registers[self.idx_reg]}, #{MOVZ}\n")
            code.append(
                f"\tmovk {self.stride_registers[self.idx_reg]}, #{MOVK16}, LSL #16\n"
            )
            code.append(
                f"\tmovk {self.stride_registers[self.idx_reg]}, #{MOVK32}, LSL #32\n"
            )
            code.append(
                f"\tmovk {self.stride_registers[self.idx_reg]}, #{MOVK48}, LSL #48\n"
            )
            code.append(
                f"\tadd {self.stride_registers[self.idx_reg]}, {self.stride_registers[self.idx_reg]}, x0\n"
            )

            self.reg_values[
                self.idx_reg
            ] = stride_address  # Keep track of stride memory address
            self.idx_reg += 1  # Point to next available register

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

        # Store loop counter in s0 for the writeKernel
        if self.kernel == "writeKernel":
            code.append(f"\tSCVTF s0, x1\n")

        # For each stride and portion unroll, generate the memory accesses
        for stride in range(self.strides):
            if self.formatting:
                code.append(f"\n")
                code.append(f"\t// stride {stride + 1}\n")
            portion_offset = 0
            for portion in range(self.portions):
                # Reset vreg (vector register) to 0 when exceeding vreg 31
                if vreg_idx > 31:
                    vreg_idx = 0

                # Compute memory access array value in bytes, includes in comments to aid debugging
                array_id_value = self.reg_values[stride] + portion_offset

                # Generate memory access for readKernel LDR scalar instructions
                if self.kernel == "readKernel":
                    code.append(
                        f"\tldr s{vreg_idx},[{self.stride_registers[stride]}], #4 //array id: {int(array_id_value/4)} bytes={array_id_value}\n"
                    )

                # Generate memory access for writeKernel STR scalar instructions
                elif self.kernel == "writeKernel":
                    code.append(
                        f"\tstr s0,[{self.stride_registers[stride]}], #4 //array id: {int(array_id_value/4)} bytes={array_id_value}\n"
                    )

                vreg_idx += 1  # Point to next vector register
                portion_offset += 4  # Point to next portion unroll

        if self.formatting:
            code.append(f"\n")
            code.append(f"// loop condition\n")

        # Loop condition / increment
        code.append(f"\tadd x1, x1, #1\n")
        code.append(f"\tcmp x1, x2\n")
        code.append(f"\tBNE .Loop\n")
        code.append(f"\n")

        return "".join(code)

    def generate_epilogue(self):
        """
        Restore callee-saved registers from stack
            - Restore callee-saved registers x19-x30
        Return function
        """
        code = []

        code.append(f".Eind:\n")

        if self.formatting:
            code.append(f"\n")
            code.append(f"// put registers on stack \n")

        # Restore callee-saved registers
        code.append(f"\tldp x19, x20, [sp, #16]  \n")
        code.append(f"\tldp x21, x22, [sp, #32]  \n")
        code.append(f"\tldp x23, x24, [sp, #48]  \n")
        code.append(f"\tldp x25, x26, [sp, #64]  \n")
        code.append(f"\tldp x27, x28, [sp, #80]  \n")
        code.append(f"\tldp x29, x30, [sp, #96]  \n")
        code.append(f"\tadd sp, sp, #128\n")

        # Return function
        code.append(f"\tret")
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
        self.arr_length = int(
            (self.arr_length // self.elements_per_loop) * (self.elements_per_loop)
        )

        code = []

        # Generate assembly instructions
        code.append(self.generate_prologue())
        code.append(self.generate_loop_body())
        code.append(self.generate_epilogue())

        function_name, file_name = self.create_filename()

        with open(file_name, "w+") as f:
            f.write("".join(code))

    def split_immediate_16bit_segments(self, offset):
        """
        Using bit masks, we extract the 16-bits segments of each equally divided part of the immediate value.
        The first 16-bit segment is for the MOVZ instruction,
        the other 16-bit segments are for the MOVK instructions, later used along their appropriate left shift
        """

        mask0_16 = 0xFFFF
        mask16_32 = 0xFFFF0000
        mask32_48 = 0xFFFF00000000
        mask48_64 = 0xFFFF000000000000

        MOVZ = offset & mask0_16
        MOVK16 = (offset & mask16_32) >> 16
        MOVK32 = (offset & mask32_48) >> 32
        MOVK48 = (offset & mask48_64) >> 48

        return MOVZ, MOVK16, MOVK32, MOVK48

    def return_array_size(self):
        return self.arr_length
