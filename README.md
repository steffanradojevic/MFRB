
# MFRB - Multi-striding Framework 

Multi-platform framework for the Raspberry Pi 5 equipped with an ARM Cortex-A76 processor, and the Banana Pi BPI-F3 equipped with a RISC-V SpacemiT K1 processor. This framework evaluates the effectiveness of multi-striding on these two micro-architectures. 

This project was developed as part of my bachelor thesis: [Evaluating the effectiveness of Multi-striding on the Raspberry Pi 5 and Banana Pi F-3](https://theses.liacs.nl/3407). 

## Performance Highlights

- **ARM Cortex-A76**: up to 83% of theoretical max bandwidth, and compared to the single-strided baselines, we find speedup factors of 1.51× for scalar loads, 1.47× for scalar stores and 1.54× for vector stores. Most notably, when compared to standard C library function `memset`, we achieve a speedup of 1.55x using vector stores.
- **RISC-V SpacemiT K1**: 1.03x speedup for scalar writes vs single-strided baseline

## Project Overview
We implemented two micro-kernels per micro-architecture (`readKernel` for loads, `writeKernel` for stores) to measure memory access throughput under different striding configurations. For each micro-architecture, we produce these micro-kernels in ARM and RISC-V assembly based on various parameters, such as striding configurations. We benchmark these micro-kernels and compare the throughput of the single-strided baseline configurations with multi-strided configurations.

## Project Structure

- **`/analysis`** - Python script to analyze the results from the multi-striding experiments using heatmaps.
- **`/arm`** -  Assembly file generators, benchmarks and validation program for the Cortex-A76. 
- **`/results`** - The results of a large experiment using a wide variety of striding configurations, conducted on the Cortex-A76 and SpacemiT K1.
- **`/risc-v`** - Assembly file generators, benchmarks and validation program for the SpacemiT K1.

## Acknowledgements
This framework and the experiments conducted in this project are based on the paper by Blom et al.: [Multi-Strided Access Patterns to Boost Hardware Prefetching](https://www.researchgate.net/publication/391455066_Multi-Strided_Access_Patterns_to_Boost_Hardware_Prefetching).

I thank the authors for their work on multi-striding and for their help with this project.

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.
