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

## How does this algorithm work
At first the algorithm initializes helper arrays - `flag` and `number`. These arrays are of length `NUM_THREADS` and are initialized to default values (flag is array of boolean `False` values and number is array of zeros).

To enter the critical section using the Bakery Algorithm, a process starts by setting its `flag[tid]` variable to `True` to signal its intent. Then, it receives a unique number that corresponds to max value in the `number` array. The process then sets its `flag` variable to `False`, indicating it now has an unique number assigned to it.

This part of the algorithm is critical and can be confusing. Essentially, the first three lines are a small critical section that prevents other processes from checking the process's old, obsolete number value while it's being modified. To ensure this, the for loop first checks that all other processes have their `flag` variable set to `False`.

The algorithm then proceeds to check the ticket values of each process, allowing the process with the lowest number to enter the critical section. When a process exits the critical section, it resets its value in `number` array to zero. This allows next process to enter critical section.

## How does this algorithm ensure correctness of parallel program
Correctness of a parallel program depends on meeting several conditions, including:
1. Mutual Exclusion: Only one process or thread can access a shared resource or critical section at a time.
2. Deadlock Freedom: The single process must not block other processes from accessing a shared resource or critical section.
3. Starvation Freedom: The decision whether the process should enter critical section should be made in finite time.
4. Unbiased: Processes have no assumptions about mutual timing when entering the critical section.

This implementation ensures aforementioned conditions in following ways: 
1. As explained previously, processes are assigned unique number and only process with lowest number can access critical section.
2. Each process yields execution to process with next lowest number immediately after exiting critical section.
3. The decision whether the process should enter critical section is made based on boolean value read from `flag` array. Array can be accessed in constant time `(O(1))` - this operation will be completed in finite time. 
4. The algorithm makes no assumptions about mutual timing of processes. Only process with lowest number can access critical section.