# Project Overview
The `experiments.py` file generates the assembly files (micro-kernels) using `microKernel_scalars.py` and `microKernel_vectors.py` and stores them in the folder `/kernels`. These generated assembly files are then compiled together with `/main.cpp`, creating a binary `programSxP` (S=stride unroll, P=portion unroll). Depending on the experiment configurations, we measure the throughput of all these binaries and save the results as a CSV in `/results`.

## Project Structure
- **`/examples`** 
    -  Examples of the generated multi-strided assembly files using various striding configurations in RISC-V. 
- **`/generators`**
    - `/results` The results of the experiments in CSV format.
  - `/experiments.py` The main experiment file. Experiments for scalar and vector loads/stores instructions can be conducted using various paramaters.
  - `/microKernel_scalars.py` The micro-kernel assembly file generator for the scalar loads and stores. 
  - `/microKernel_vectors.py` The micro-kernel assembly file generator for the vector loads and stores. 

- **`/kernels`**
    - `/main.cpp` Array initialization, start timer, assembly function call, stop timer and calculation of the throughput.  
    - `makefile` Remove all the generated assembly files and program binaries produced by the experiments files.
    - `validation_writeKernel.cpp` Program to validate if all values written by the `writeKernel` for scalar and vectors are executed correctly.

