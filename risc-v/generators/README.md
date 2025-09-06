## RISC-V Instructions
We conduct on the experiment on the RISC-V SpacemiT K1 on 4 scalar and vector load/store instructions. These instructions are shown in the table below.

| Instruction | Type | Kernel |
|------------|----------------|-------------------|
| `flw` | `Scalar` | `readKernel` |
| `fsw` | `Scalar` | `writeKernel` |
| `vle32.v` | `Vector` | `readKernel` |
| `vse32.v` | `Vector` | `writeKernel` |

## Run experiments
In the **`experiments.py`** file we only have to set the configuration dictionary in python and run the following function:
```bash
experiment = experiment(conf)
experiment.run_experiment()
```
Run **`experiments.py`** and the experiment will start.

The configuration file is as follow:

```python
conf = {
    "type": "Scalar",
    "kernel": "writeKernel",
    "strides": 20,
    "portions": 32,
    "array_length": 23529411,
    "repeat_assembly": 5,
    "repeat_binary": 5,
    "array_steps": 7771,
    "number_arrays": 10,
    "file_name": "example_scalar_writeKernel",
}

```
- `type` - Kernel type: [`Scalar`] or [`Vector`].
- `kernel` - Micro-kernel: [`readKernel`] or [`writeKernel`].
- `strides` - Range of strides we want to conduct the experiment on. In the config example we will have a range of [1-20].
- `portions` - Range of portions we want to conduct the experiment on. In the config example we will have a range of [1-32].
- `array_length` - (Starting) array length in elements. For the RISC-V experiments, array sizes in bytes cannot exceed 32-bit in value. Support for larger array sizes have to be implemented.
- `repeat_assembly` - How many times we call the micro-kernel function within a single binary. We take the mean throughput over these calls.
- `repeat_binary` - How many times do we call the binary. We take the max throughput over these calls.
- `array_steps` - If we experiment on multiple arrays to reduce address collisions, what is the increment between these arrays. All the measurements from each arrays will be stored as a CSV file.
- `number_arrays` - How many arrays do we want to generate using the `array_steps` as increment. 
- `file_name` - The CSV file name of the results of the experiments. The file will be stored in `\results`.

