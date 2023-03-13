# Dining Philosophers problem
This repo is my implementation of third assignment for PPDS course at FEI STU.

## What is Dining philosophers problem
The Dining Philosophers problem is a problem that illustrates synchronization issues in concurrent programming. It is a thought experiment that involves five philosophers who are sitting around a circular table, with a bowl of food and a single fork between each pair of philosophers. The philosophers spend their time thinking and eating, but they need two forks to eat.

The problem arises when all five philosophers reach for the fork on their right at the same time. They will each have one fork and will be waiting for the fork on their left to become available, which is held by their neighbor. This results in a deadlock, where none of the philosophers can proceed with eating.

The Dining Philosophers problem is used to illustrate the challenges of managing shared resources in a multi-threaded system, and the need for proper synchronization mechanisms to avoid deadlocks and other issues.

## How to use this project
This project consists of single python script `main.py`. To run this program, you need some prerequisites: 
1. Python 3.10 installed on your system
2. Library `fei.ppds` installed on your system (easiest way is to install globally with `pip install fei.ppds`)

After fulfilling these requirements, you should be able to run this script with command `python main.py` (assuming your shell's working directory is the directory where script is located).
After running the command, the output should be in this format: 
```
Philosopher 0 is thinking!
Philosopher 1 is thinking!
Philosopher 2 is thinking!
Philosopher 3 is thinking!
Philosopher 4 is thinking!
Philosopher 3 is eating!
Philosopher 3 is thinking!
Philosopher 2 is eating!
Philosopher 2 is thinking!
Philosopher 1 is eating!
Philosopher 1 is thinking!
Philosopher 0 is eating!
Philosopher 0 is thinking!
Philosopher 3 is eating!
Philosopher 3 is thinking!
Philosopher 2 is eating!
Philosopher 2 is thinking!
Philosopher 1 is eating!
Philosopher 4 is eating!
Philosopher 4 is thinking!
Philosopher 1 is thinking!
Philosopher 3 is eating!
Philosopher 3 is thinking!
Philosopher 2 is eating!
Philosopher 2 is thinking!
Philosopher 1 is eating!
Philosopher 1 is thinking!
Philosopher 0 is eating!
Philosopher 0 is thinking!
Philosopher 3 is eating!
Philosopher 3 is thinking!
Philosopher 2 is eating!
Philosopher 2 is thinking!
Philosopher 1 is eating!
Philosopher 4 is eating!
Philosopher 1 is thinking!
Philosopher 4 is thinking!
Philosopher 3 is eating!
Philosopher 2 is eating!
Philosopher 1 is eating!
Philosopher 0 is eating!
Philosopher 0 is thinking!
Philosopher 4 is eating!
Philosopher 4 is thinking!
Philosopher 0 is eating!
Philosopher 0 is thinking!
Philosopher 4 is eating!
Philosopher 4 is thinking!
Philosopher 0 is eating!
Philosopher 4 is eating!
```

The script runs in a loop for 5 times by default, but you can play around with this variable by changing the value of `NUM_RUNS`.

## How does this program work
This program is a solution to the Dining Philosophers problem that accounts for left-handed philosophers. The solution assigns each philosopher(process) a unique id number and prevents deadlock. Since we have `N` philosophers and `N` resources, assuming that at least one of the philosophers is left handed, we can conclude, that there won't be a deadlock in the program (there won't be a situation in which all processes are holding lock over one resource).
This program assumes that we have `NUM_PHILOSOPHERS` philosophers (and same number of resources). This constant is set to `5`.
The solution is to simply assume that four philosophers are right-handed and one is left handed. That way at least one process will always be able to acquire lock over two resources (at least one philosopher will be able to eat).

## How does this solution compare to solution using waiter
In the solution that accounts for left-handed philosophers, there is a chance of starvation if a philosopher is unable to acquire the fork they need. This can happen if the philosopher is right-handed and the fork on their right is already taken by another philosopher. In this case, the philosopher will have to wait until the fork on their right becomes available, which may take some time if the other philosopher is taking a long time to eat. This can cause the right-handed philosopher to starve, especially if there are multiple right-handed philosophers competing for the same fork.
This solution greatly depends on distribution of left and right handed philosophers in system. For example my implementation introduces only one left-handed philosopher - process with id `4`.
Left-handed philosopher with id `4` acquires lock over semaphore with id `0` first (blocking right-handed philosopher with id `0` from accessing the semaphore).
Accordingly right-handed philosopher with id `0` acquires lock over semaphore with id `0` first (blocking left-handed philosopher with id `4` from accessing the semaphore).
You can observe in logs provided that in each iteration of loop either philosopher with id `0` is eating or philosophers with id `1` and `4` are eating (parallelism).
This results in starvation of philosophers with ids `4` and `0`. You can observe the end of the logs where the fact that philosophers with ids `1`, `2`, `3` leave the loop and philosophers with ids `0` and `4` are still eating and thinking to finish the five iterations.
This works because we have finite number of iteration, in real program which is running in infinite loop, there will be problem of starvation.

In the solution that uses a waiter, there is a lower chance of starvation because the waiter ensures that only a certain number of philosophers can pick up forks at once. This prevents deadlock and ensures that each philosopher gets a turn to eat. However, the waiter solution may still be prone to starvation if the system is heavily loaded or if there are long wait times for the waiter. Also this introduces additional synchronization mechanism (waiter) and may increase complexity of final solution.

Ultimately, the choice between the two solutions depends on the specific requirements of the project, such as the number of philosophers, the likelihood of deadlock, and the desired level of parallelism and performance.

## Compare solutions using experiment
In this experiment i've compared my solution with only left-handed philosopher and [solution using waiter.](https://github.com/tj314/ppds-2023-cvicenia/blob/master/seminar4/04_philosophers.py)
I've compared these two solution on `5`, `10` and `15` runs of loop. I ran and compared two solutions with aforementioned parameters, measured time that took each script to finish and then processed results into a table.  You can see that using my approach each iteration of loop either philosopher with id `0` or philosopher with id `4` is starving as described in preceding paragraph.
The time difference only increases with higher number of loops (said processes are becoming increasingly starved). In conclusion, the solution using waiter behaves better for this use case. My solution could be improved by experimenting with distribution of left and right-handed philosophers in system.

| NUM_RUNS | left-handed |   waiter  |
|----------|-------------|-----------|
|     5    |     6.94    |    4.36   |
|    10    |    13.42    |    8.13   |
|    15    |    20.13    |   11.89   |