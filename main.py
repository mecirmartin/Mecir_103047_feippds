"""
This module contains an implementation of Bakery algorithm.
Bakery algorithm assures mutual exclusion of N threads.
"""

__author__ = "Martin Mečír, Tomáš Vavro"
__email__ = "xmecirm@stuba.sk, xvavro@stuba.sk"
__license__ = "MIT"

from fei.ppds import Thread

NUM_THREADS = 10

flag = [False] * (NUM_THREADS)
number = [0] * (NUM_THREADS)
value: int = 0  # global counter


def process(tid: int, num_threads: int):
    """
    Simulates a process.

    :param tid: thread id
    :param num_threads: number of executions of the critical section (number of threads)
    """
    global value
    flag[tid] = True
    number[tid] = max(number) + 1
    flag[tid] = False

    for j in range(num_threads):
        while flag[j]:
            print(f'process {tid} waiting')
            pass
        while (number[j] < number[tid] or (number[j] == number[tid] and j < tid)) and number[j] != 0:
            print(f'process {tid} waiting')
            pass

    # critical section
    value += 1
    print(f"thread number: {tid}", f'counter value: {value}')
    number[tid] = 0
    # end of critical section


if __name__ == '__main__':
    threads = [Thread(process, i, NUM_THREADS) for i in range(NUM_THREADS)]
    [t.join() for t in threads]
