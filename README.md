# Transform images to gray scale using CPU and GPU
This repo is my implementation of fifth assignment for PPDS course at FEI STU.

## What does this code do
This repo contains implementation of gray scale transformation in Python. This code is ran on CPU.
However this repo also contains implementation of said transformation using Numba compiler and CUDA
parallel computing platform.

## What is Numba and CUDA
According to [official site](https://numba.pydata.org):
Numba translates Python functions to optimized machine code at runtime using the industry-standard LLVM compiler library. Numba-compiled numerical algorithms in Python can approach the speeds of C or FORTRAN.

In this project Numba is used to run CUDA code in Python.
According to [official site](https://blogs.nvidia.com/blog/2012/09/10/what-is-cuda-2/):
CUDA is a parallel computing platform and programming model created by NVIDIA. CUDA helps developers speed up their applications by harnessing the power of GPU accelerators.


## How is CUDA used in this project
In this project CUDA is used to speed up the transformation of images. The image transformation to gray scale is 
ideal problem for demonstration of CUDA capabilities since it is fundamentally SIMD (Single instruction multiple data) problem. 
Thus we can take advantage of GPU architecture as it can spawn multiple processes. Every process can then compute transformation
for one pixel.

## How to use this project
This project consists of single python script `main.py`. To run this program, you need some prerequisites: 
1. Python 3.10 installed on your system
2. Matlplotlib installed on your system
3. Numpy installed on your system

After fulfilling these requirements, you should be able to run this script with command `python main.py` (assuming your shell's working directory is the directory where script is located).
After running the command, the script will generate two files `face_grayscale.jpg` and `face_grayscale_cuda.jpg`. Those are the images transformed to gray scale.


## What computation is used to perform gray scale transformation
The formula used for gray scale transformation is `Y = 0.299R + 0.587G + 0.114B`. You can read more about 
this formula [here](https://en.wikipedia.org/wiki/Grayscale#Converting_color_to_grayscale).
