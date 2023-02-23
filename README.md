# Bakery algorithm

This repo is my implementation of Bakery algorithm for PPDS course at FEI STU.

## What is Bakery algorithm
The Bakery Algorithm is a mutual exclusion algorithm used in computer science to solve the critical section problem in multi-process systems. The critical section problem refers to the issue of multiple processes trying to access critical section (shared resource) at the same time, leading to conflicts and incorrect results.

The Bakery Algorithm provides a way for processes to enter the critical section one at a time, ensuring that only one process is executing the critical section at any given time. It accomplishes this by assigning a unique number to each process that requests entry into the critical section, and then using these numbers to establish a priority order for entry.

The Bakery Algorithm helps to prevent race conditions and ensures that only one process at a time can execute the critical section, leading to correct and predictable results in multi-process systems.

## How to use this project
This project consists of single python script `main.py`. To run this program, you need some prerequisites: 
1. Python 3.10 installed on your system
2. Library `fei.ppds` installed on your system (easiest way is to install globally with `pip install fei.ppds`)

After fulfilling these requirements, you should be able to run this script with command `python main.py` (assuming your shell's working directory is the directory where script is located).
After running the command, the output should be in this format: 
```
thread number: 0 counter value: 1
thread number: 1 counter value: 2
thread number: 2 counter value: 3
thread number: 3 counter value: 4
thread number: 4 counter value: 5
process 5 waiting
thread number: 5 counter value: 6
thread number: 6 counter value: 7
thread number: 7 counter value: 8
thread number: 8 counter value: 9
thread number: 9 counter value: 10
```

Output could contain various numbers of messages in this format: `process {processId} waiting`. This message simply means that process is paused and waiting for synchronization.
The important thing is that numbers of counter value are in sequence. This implies that processes were synchronized before accessing critical section.
The script spawns 10 threads by default, but you can play around with this variable by changing the value of `NUM_THREADS`

## Why does this project work