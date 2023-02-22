"""
This module contains an implementation of Bakery algorithm.
Bakery algorithm assures mutual exclusion of N threads.
"""

__author__ = "Martin Mečír, Tomáš Vavro"
__email__ = "xmecirm@stuba.sk, xvavro@stuba.sk"
__license__ = "MIT"

from fei.ppds import Thread
from time import sleep

current_number: int = 0
next_number: int = 0


def process(tid: int, num_runs: int):
    """
    Simulates a process.
    
    :param tid: thread id
    :param num_runs: number of executions of the critical section
    """
    global current_number, next_number

    for _ in range(num_runs):
        # process wants to enter critical section
        turn: int = current_number
        current_number += 1

        # wait for other processes to finish their execution of critical section
        while turn != next_number:
            continue

        # execute critical section
        print(f"Process {tid} runs a complicated computation!")
        sleep(1)

        # exit critical section
        next_number += 1


if __name__ == '__main__':
    DEFAULT_NUM_RUNS = 10
    NUM_THREADS = 3
    threads = [Thread(process, i, DEFAULT_NUM_RUNS) for i in range(NUM_THREADS)]
    [t.join() for t in threads]