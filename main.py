"""Transform image to grayscale using numba.

This module implements an image transformation to grayscale using CPU and 
also using GPU with Numba emulator. The final image is saved to file.
"""

__author__ = "Martin Mecir, Tomáš Vavro"
__licence__ = "MIT"

from numba import cuda
import matplotlib . pyplot as plt
import numpy as np
import time

IMAGE_NAME = 'images-18'

@cuda.jit
def transform_to_grayscale_cuda(in_data, out_data):
    """Transform every RGB pixel to grayscale using formula.

    Also check bounds of data.
    Use grid() instead of manual pos computation.

    Arguments:
        in_data  -- matrix of pixel
        out_data -- transformed matrix
    """
    row, col = cuda.grid(2)  # indices inside the matrix
    if row < len(in_data) and col < len(in_data[row]):  # check array bounds
        [r, g, b] = in_data[row][col]
        out_data[row][col] = 0.299 * r + 0.587 * g + 0.114 * b


def transform_to_grayscale(in_data):
    """
    Transforms in_data to grayscale using formula
    
    Arguments:
        in_data  -- matrix of ones and zeroes

    Returns:
        out_data -- negated matrix
    """
    return np.dot(in_data[..., :3], [0.299, 0.587, 0.114])



def main():
    """Run main."""
    pixels = plt.imread(f'./images/{IMAGE_NAME}.jpeg').copy()
    height, width, _ = pixels.shape
    out_data_cuda = np.zeros((height, width)).copy()
    # This works for 256x256 pixel images
    tpb = (16, 16)
    bpg = (16, 16)
    
    gpu_start = time.time()
    transform_to_grayscale_cuda[bpg, tpb](pixels, out_data_cuda)
    gpu_duration = time.time() - gpu_start

    cpu_start = time.time()
    out_data = transform_to_grayscale(pixels)
    cpu_duration = time.time() - cpu_start

    print("CPU: ", cpu_duration)
    print("GPU: ", gpu_duration)
    plt.imsave(f'{IMAGE_NAME}-grayscale-cpu.jpg', out_data ,format='jpg', cmap=plt.get_cmap('gray'))
    plt.imsave(f'{IMAGE_NAME}-grayscale-gpu.jpg', out_data_cuda ,format='jpg', cmap=plt.get_cmap('gray'))

if __name__ == "__main__":
    main()