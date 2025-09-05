/*
g++ (Bianbu) 13.2.0
Leiden University
Author: Steffan Radojevic
Email: steffanradojevic@gmail.com
Date: 5 September 2025
Description: Validation of the writeKernels scalars and vectors. The kernels
write the loop counter to array. After kernel function call, validate array to
check if everything went succesfull. Example compile command: g++
-DSIZEARRAY=505290240 -DSCALAR=1 -DSTRIDES=2 -DPORTIONS=4 -march=rv64gcv_zba_zbb_zbs
microKernel2x4.s -O0 validation_writeKernel.cpp -o program2x4
*/

#include <bit>
#include <cassert>
#include <cstdint>
#include <iostream>

#define MAXVLEN 256 // Vector register size
#define SEW 32      // Selected Element Width (single-precision floating points)

extern "C" int microKernel(float *arr);

/*
Compare check_value (value we increase manually) with array_value.
If they differ, the writeKernel did not correctly wrote the loop counter to the
array
*/
bool unit_test_loop(float *arr, size_t sizeArr, int strides, int portion,
                    int scalar) {
  int check_value = 0;
  int ids_per_stride = portion;
  int stride_switch = int(sizeArr / strides);

  // Vector: multiple elements per memory access
  if (scalar == 0) {
    ids_per_stride = ids_per_stride * int(MAXVLEN / SEW);
  };

  for (int i = 0; i < sizeArr; ++i) {
    // Retrieve array_value from written array
    float array_value;
    array_value = arr[i];

    // Increment check each loop itteration
    if ((i % ids_per_stride == 0) && (i != 0)) {
      check_value += 1;
    }

    // Next stride, reset check
    if ((i % stride_switch) == 0) {
      check_value = 0;
    }

    if (array_value != check_value) {
      // Aid in debugging
      std::cout << "check_value=" << check_value
                << " array_value=" << array_value << " i=" << i << std::endl;
      return false;
    }
  }

  return true;
}

int main() {

#ifdef SIZEARRAY
  size_t sizeArr = SIZEARRAY;
#else
  std::cout << "Macro SIZEARRAY not defined" << std::endl;
#endif

#ifdef STRIDES
  int strides = STRIDES;
#else
  std::cout << "Macro STRIDES not defined" << std::endl;
#endif

#ifdef PORTIONS
  int portions = PORTIONS;
#else
  std::cout << "Macro PORTIONS not defined" << std::endl;
#endif

#ifdef SCALAR
  int scalar = SCALAR;
#else
  std::cout << "Macro SCALAR not defined" << std::endl;
#endif

  // Allocate array and initialize with random constant
  float *arr = new float[sizeArr];
  int result;
  for (int i = 0; i < sizeArr; ++i) {
    arr[i] = 99999999;
  }

  // Run writeKernel and check result
  microKernel(arr);
  assert(unit_test_loop(arr, sizeArr, strides, portions, scalar) == true);

  // Utilized for Python unit test to check if succesfull
  // Not part of the framework, send an email to request this feature
  std::cout << "OK" << std::endl;

  return 0;
}