"""
Python 3.11.2
Leiden University
Author: Steffan Radojevic
Email: steffanradojevic@gmail.com
Date: 4 September 2025 
Description: Experiment file for evaluating memset (Standard C Library) on the ARM Raspberry Pi 5 equipped with a Cortex A-76.
Memset is identical in the experimental setup and methods as the multi-strided micro-kernels, 
only optimizations compared to these micro-kernels are the compiler flags -O3, -ftree-vectorize and -mtune=native.
"""

# https://www.geeksforgeeks.org/python-subprocess-module/
import subprocess
import os

import csv


class experiment:
    def __init__(self, conf):
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
        Compiles, run the experiments, measure the throughputs and save the results for memset (Standard C Library)
        The experiments are identical to the multi-strided micro-kernel experiments

        Steps:
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

        # Run experiment for each array size
        for arr in arr_all:
            array_size = arr

            output_file = f"program"

            # Generate compile command
            # Example = [g++ -DSIZEARRAY=23529411 -DREPEATED=5 -O3 -ftree-vectorize -march=armv8-a -mtune=native main_memset.cpp -o program]
            command = [
                "g++",
                f"-DSIZEARRAY={array_size}",
                f"-DREPEATED={self.repeat_assembly}",
                "-ftree-vectorize",
                "-mtune=native",
                "-march=armv8.2-a",
                "-O3",
                "main_memset.cpp",
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

                command = f"./program"

                # Store output of the program as a byte string in s
                s = subprocess.check_output(
                    command, cwd="../kernels", stdin=data, shell=True
                )

                # Decode s to a normal string
                result = s.decode("utf-8").split(" ")

                throughput_arr.append(float(result[0]))  # Store measured throughput

            self.results.append([array_size, max(throughput_arr)])

    def write_result_to_csv(self):
        with open(f"results/{self.file_name}.csv", "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            head = ["array_size", "throughput"]
            writer.writerow(head)
            writer.writerows(self.results)

    def run_experiment(self):
        self.generate_kernels()
        self.write_result_to_csv()


conf = {
    "array_length": 23529411,
    "repeat_assembly": 5,
    "repeat_binary": 5,
    "array_steps": 7771,
    "number_arrays": 4,
    "file_name": "example_memset",
}


experiment = experiment(conf)
experiment.run_experiment()
