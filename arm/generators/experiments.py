"""
Python 3.11.2
Leiden University
Author: Steffan Radojevic
Email: steffanradojevic@gmail.com
Date: 3 September 2025 
Description: Experiment file for evaluating multi-striding on the ARM Raspberry Pi 5 equipped with a Cortex A-76.
Generate assembly files for each striding configuration and array size, compile, run binaries and store measured throughputs in CSV-files.
"""

from microKernel_scalars import microKernel as microKernelScalar
from microKernel_vectors import microKernel as microKernelVector

# https://www.geeksforgeeks.org/python-subprocess-module/
import subprocess
import os

import csv


class experiment:
    def __init__(self, conf):
        self.type = conf["type"]
        self.kernel = conf["kernel"]
        self.instr_type = conf["instr_type"]
        self.strides = conf["strides"]
        self.portions = conf["portions"]
        self.array_length = conf["array_length"]
        self.repeat_assembly = conf["repeat_assembly"]
        self.repeat_binary = conf["repeat_binary"]
        self.file_name = conf["file_name"]
        self.array_steps = conf["array_steps"]
        self.number_arrays = conf["number_arrays"]
        self.results = []
        self.array_size = {}

    def generate_kernels(self):
        """
        Generate assembly micro-kernels for various configurations and array sizes
        Compiles, run the experiments, measure the throughputs and save the results

        Steps:
            1. Generate arrays with varying sizes, spaced out by a constant
            2. Initialize micro-kernel objects and generate assembly micro-kernels
            3. Compile assembly files with C++ main.cpp
            4. Run binaries, save throughput in throughput_arr[]
            5. Take max throughput, and save this with configuration info in self.results[]

        Raises:
            ValueError: If binary compilation failed
        """

        start = self.array_length
        step = self.array_steps
        count = self.number_arrays

        # Generate array sizes (start, step, count)
        arr_all = [start + step * i for i in range(count)]

        # Run experiment for each array size, stride unroll and portion unroll
        for arr in arr_all:
            for stride in range(self.strides):
                stride += 1  # Convert 0-based index to 1-based index
                for portion in range(self.portions):
                    portion += 1

                    if self.type == "Scalar":
                        gen = microKernelScalar(
                            strides=stride,
                            portions=portion,
                            arr_length=arr,
                            MAXVLEN=128,
                            MAXSP=32,
                            formatting=True,
                            kernel=self.kernel,
                        )

                    elif self.type == "Vector":
                        gen = microKernelVector(
                            strides=stride,
                            portions=portion,
                            arr_length=arr,
                            MAXVLEN=128,
                            MAXSP=32,
                            formatting=True,
                            kernel=self.kernel,
                            instr_type=self.instr_type,
                        )

                    gen.generate_assembly_file()
                    array_size = (
                        gen.return_array_size()
                    )  # Used for -DSIZEARRAY during compilation

                    kernel_file = (
                        f"microKernel{stride}x{portion}.s"  # Assembly file name
                    )
                    output_file = (
                        f"program{stride}x{portion}"  # Compiled binary file name
                    )

                    # Generate compile command
                    # Example = [g++ -DSIZEARRAY=505290240 -DREPEATED=2 -march=armv8.2-a readKernel1x32.s -O0 main_readKernel.cpp -o program1x32]
                    command = [
                        "g++",
                        f"-DSIZEARRAY={array_size}",
                        f"-DREPEATED={self.repeat_assembly}",
                        "-march=armv8.2-a",
                        "-O0",
                        "main.cpp",
                        kernel_file,
                        "-o",
                        output_file,
                    ]

                    # Compile kernel with g++ en check result
                    ans = subprocess.call(command, cwd="../kernels")
                    if ans != 0:
                        raise ValueError(f"Failed command with {command}")

                    throughput_arr = []

                    # Each array consists of multiple binary runs
                    for repeat in range(self.repeat_binary):
                        data, temp = os.pipe()
                        # Write to STDIN as a byte object(convert string
                        # to bytes with encoding utf8)
                        os.write(temp, bytes("5 10\n", "utf-8"))
                        os.close(temp)

                        command = f"./program{stride}x{portion}"

                        # Store output of the program as a byte string in s
                        s = subprocess.check_output(
                            command, cwd="../kernels", stdin=data, shell=True
                        )

                        # Decode s to a normal string
                        result = s.decode("utf-8").split(" ")

                        throughput_arr.append(
                            float(result[0])
                        )  # Store measured throughput

                    self.results.append(
                        [stride, portion, array_size, max(throughput_arr)]
                    )

    def write_result_to_csv(self):
        with open(f"results/{self.file_name}.csv", "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            head = ["stride", "portion", "array_size", "throughput"]
            writer.writerow(head)
            writer.writerows(self.results)

    def run_experiment(self):
        self.generate_kernels()
        self.write_result_to_csv()


conf = {
    "type": "Scalar",
    "kernel": "readKernel",
    "instr_type": "-",
    "strides": 3,
    "portions": 11,
    "array_length": 23529411,
    "repeat_assembly": 1,
    "repeat_binary": 1,
    "array_steps": 771,
    "number_arrays": 1,
    "file_name": "example_scalar_readKernel",
}

experiment = experiment(conf)
experiment.run_experiment()
