/*
g++ (Debian 12.2.0-14) 12.2.0
Leiden University
Author: Steffan Radojevic
Email: steffanradojevic@gmail.com
Date: 3 September 2025
Description: Measure throughput of memset (Standard C Library), return average
throughput for the Raspberry Pi 5 equipped with Cortex A-76 Example compile
command: g++ -DSIZEARRAY=23529411 -DREPEATED=5 -O3 -ftree-vectorize
-march=armv8.2-a -mtune=native main_memset.cpp -o program
*/

#include <chrono> // https://www.geeksforgeeks.org/measure-execution-time-function-cpp/
#include <cstring> // memset
#include <iomanip>
#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <sys/mman.h>
#include <unistd.h>

float *allocate_array_with_mmap(size_t sizeArr) {
  size_t page_size = sysconf(_SC_PAGESIZE);
  size_t total_bytes = sizeof(float) * sizeArr;

  // Round off page size
  size_t aligned_size = (total_bytes + page_size - 1) & ~(page_size - 1);

  float *arr =
      static_cast<float *>(mmap(nullptr, aligned_size, PROT_READ | PROT_WRITE,
                                MAP_PRIVATE | MAP_ANONYMOUS, -1, 0));

  if (arr == MAP_FAILED) {
    perror("mmap failed");
    return nullptr;
  }

  return arr;
}

int main() {

#ifdef SIZEARRAY
  size_t sizeArr = SIZEARRAY;
#else
  std::cout << "Macro SIZEARRAY not defined" << std::endl;
#endif

#ifdef REPEATED
  int repeat = REPEATED;
#else
  std::cout << "Macro REPEATED not defined" << std::endl;
#endif

  // Allocate array and initialize with random constant
  float *arr = allocate_array_with_mmap(sizeArr);
  for (int i = 0; i < sizeArr; ++i) {
    arr[i] = static_cast<float>(99999999);
  }

  int result;
  double total_time = 0;
  double total_throughput = 0;
  double max_throughput = 0;

  // Run memset including two warm-ups
  for (int i = 0; i < repeat + 2; ++i) {

    // Run micro-kernel and time duration
    size_t sizeArr_bytes = sizeArr * sizeof(float);
    auto start = std::chrono::high_resolution_clock::now();
    memset(arr, 0, sizeArr_bytes);
    auto stop = std::chrono::high_resolution_clock::now();
    auto duration =
        std::chrono::duration_cast<std::chrono::microseconds>(stop - start);

    if ((i == 0) || (i == 1)) // warm up
    {
      continue;
    }

    total_time += duration.count();

    // Compute throughput in bytes per second
    double current_throughput =
        (sizeArr * 4) / (static_cast<double>(duration.count()) / 1000000);

    total_throughput += current_throughput;

    // Experiments compute average throughput, max throughput may be used later
    if (max_throughput < current_throughput) {
      max_throughput = current_throughput;
    }
  }

  // Output average throughput -> experiments.py catches this output
  std::cout << std::fixed << (total_throughput / repeat);

  return 0;
}
