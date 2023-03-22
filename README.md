# Dining savages problem
This repo is my implementation of fourth assignment for PPDS course at FEI STU.

## What is Dining savages problem
Community of savages meets every night for a dinner. Savages are eating in companion so everyone has to wait for all savages to arrive first. The last savage to arrive gives a signal and all savages can eat. There is a large pot that can hold M servings of food. When a member of the community wants to eat, they serve themselves from the pot, unless it is empty. If the pot is empty, they wake up the cook and wait until the pot is refilled. Then they can go ahead and take a portion of a meal. Every savage takes one serving. This happens every night, so program has to run indefinitely.

## How to use this project
This project consists of single python script `main.py`. To run this program, you need some prerequisites: 
1. Python 3.10 installed on your system
2. Library `fei.ppds` installed on your system (easiest way is to install globally with `pip install fei.ppds`)

After fulfilling these requirements, you should be able to run this script with command `python main.py` (assuming your shell's working directory is the directory where script is located).
After running the command, the output should be in this format: 
```
SAVAGE: 0 waiting on barrier
SAVAGE: 1 waiting on barrier
SAVAGE: 2 waiting on barrier
SAVAGE: 3 waiting on barrier
SAVAGE: 4 arrived, barrier unlocking
SAVAGE: 4 waiting on barrier
SAVAGE: 4 took a portion
SAVAGE: 2 took a portion
SAVAGE: 0 took a portion
SAVAGE: 3 went to take a portion, but pot is empty, waiting for refill
CHEF: food is cooking
SAVAGE: 3 took a portion
SAVAGE: 1 took a portion
SAVAGE: 1 waiting on barrier
SAVAGE: 4 waiting on barrier
SAVAGE: 0 waiting on barrier
SAVAGE: 3 waiting on barrier
SAVAGE: 2 arrived, barrier unlocking
SAVAGE: 2 waiting on barrier
SAVAGE: 2 took a portion
SAVAGE: 4 went to take a portion, but pot is empty, waiting for refill
CHEF: food is cooking
SAVAGE: 4 took a portion
SAVAGE: 0 took a portion
SAVAGE: 3 took a portion
SAVAGE: 1 went to take a portion, but pot is empty, waiting for refill
CHEF: food is cooking
SAVAGE: 1 took a portion
SAVAGE: 1 waiting on barrier
SAVAGE: 4 waiting on barrier
SAVAGE: 3 waiting on barrier
SAVAGE: 2 waiting on barrier
SAVAGE: 0 arrived, barrier unlocking
SAVAGE: 0 waiting on barrier
SAVAGE: 0 took a portion
SAVAGE: 1 took a portion
SAVAGE: 3 went to take a portion, but pot is empty, waiting for refill
CHEF: food is cooking
SAVAGE: 3 took a portion
SAVAGE: 4 took a portion
SAVAGE: 2 took a portion
SAVAGE: 2 waiting on barrier
SAVAGE: 0 waiting on barrier
SAVAGE: 3 waiting on barrier
SAVAGE: 1 waiting on barrier
SAVAGE: 4 arrived, barrier unlocking
SAVAGE: 4 waiting on barrier
SAVAGE: 4 went to take a portion, but pot is empty, waiting for refill
CHEF: food is cooking
SAVAGE: 4 took a portion
SAVAGE: 3 took a portion
SAVAGE: 0 took a portion
SAVAGE: 2 went to take a portion, but pot is empty, waiting for refill
CHEF: food is cooking
SAVAGE: 2 took a portion
SAVAGE: 1 took a portion
SAVAGE: 1 waiting on barrier
SAVAGE: 0 waiting on barrier
SAVAGE: 3 waiting on barrier
SAVAGE: 4 waiting on barrier
SAVAGE: 2 arrived, barrier unlocking
SAVAGE: 2 waiting on barrier
SAVAGE: 2 took a portion
SAVAGE: 4 went to take a portion, but pot is empty, waiting for refill
```

The script runs indefinitely. The number of servings in the pot is equals `SIZE_OF_COOKING_POT` (default is 3). 
The script spawns 5 processes by default, but you can play around with this variable by changing the value of `NUM_OF_SAVAGES`.

## How does this program work
The script spawns 5 processes by default (can be modified by changing the value of `NUM_OF_SAVAGES`) that run in function `feast` in infinite loop. Script also spawns single process that runs function `cook` in infinite loop.
The most important function in this script is `feast`. 

This function implements reusable barrier to make sure that all process will synchronize at the start of the while loop (all savages are waiting for very last of them to join).
The approach is known as a two-phase barrier since it necessitates the threads to pause twice. Initially, they must wait for all threads to arrive, and then they must wait for all threads to complete the critical section. Learn more about reusable barrier in [Little Book Of Semaphores](https://greenteapress.com/semaphores/LittleBookOfSemaphores.pdf) - section `3.7.5`.
In short we keep count of processes waiting on barrier, we protect the count with the Mutex. Last process to arrive on the barrier first locks the second turnstile and then opens first turnstile and opens critical section for processes waiting on the barrier.
``` 
shared.barrier_mutex.lock()
shared.barrier_count += 1
if shared.barrier_count == NUM_OF_SAVAGES:
    print(f'SAVAGE: {i} arrived, barrier unlocking')
    shared.turnstile2.wait()
    shared.turnstile.signal()
shared.barrier_mutex.unlock()
```
From this code you can see that processes are waiting on barrier until last process opens the turnstile. Processes are going through turnstile one by one.
```
print(f'SAVAGE: {i} waiting on barrier')
shared.turnstile.wait()
shared.turnstile.signal()
```

In next code snippet we keep the count of portions of food inside the pot. The counter is protected with the Mutex. When the counter reaches zero (pot is empty), next synchronization pattern is used - rendezvous. Process signals that the pot is empty and it waits for refill.
```
shared.pot_mutex.lock()
# critical section
if shared.cooking_pot == 0:
    print(f'SAVAGE: {i} went to take a portion, but pot is empty, waiting for refill')
    shared.empty_pot.signal()
    shared.full_pot.wait()
shared.cooking_pot -= 1
print(f'SAVAGE: {i} took a portion')
shared.pot_mutex.unlock()
```

In last part of `feast` function all processes are synchronized very similarly to the start of the while loop. The last process to leave critical section locks the first turnstile and then unlocks the second turnstile. That way we ensure that all processes will leave the critical section at once and all will be synchronized on first barrier at the start of the for loop.
```
shared.barrier_mutex.lock()
shared.barrier_count -= 1
if shared.barrier_count == 0:
    shared.turnstile.wait()
    shared.turnstile2.signal()
shared.barrier_mutex.unlock()
shared.turnstile2.wait()
shared.turnstile2.signal()
```

The script also contains function `cook`. This function represents single cook that cooks meals. This is represented by single process in while loop. This process is synchronized with `feast` function using synchronization pattern rendezvous. The process waits for `shared.empty_pot.wait()`, then cooks food and signals that it is done cooking with `shared.full_pot.signal()`
```
while True:
    shared.empty_pot.wait()
    cook_food(shared)
    shared.full_pot.signal()
```
