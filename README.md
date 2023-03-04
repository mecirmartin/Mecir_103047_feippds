# Barber shop problem
This repo is my implementation of second assignment for PPDS course at FEI STU.

## What is Barber shop problem
There is a small town with only one barber shop. The barber in the shop has a strict set of rules that he follows:

1. If there is no one in the shop, the barber goes to sleep.
2. If a customer enters the shop and barber is sleeping, barber will wake up and customer can sit down and get a hair cut from the barber.
3. If a customer enters the shop and barber is currently working, customer can sit in waiting room and wait for his haircut.
4. If all seats in waiting room are occupied, the customer has to return after certain period of time and check if all seats are still occupied.
5. After haircut, customer lets his hair grow and then visits barber shop again.

## How to use this project
This project consists of single python script `main.py`. To run this program, you need some prerequisites: 
1. Python 3.10 installed on your system
2. Library `fei.ppds` installed on your system (easiest way is to install globally with `pip install fei.ppds`)

After fulfilling these requirements, you should be able to run this script with command `python main.py` (assuming your shell's working directory is the directory where script is located).
After running the command, the output should be in this format: 
```
CUSTOMER: 0 is in the room
CUSTOMER: 1 is in the room
CUSTOMER: 2 is in the room
CUSTOMER: 3 waiting room is full
CUSTOMER: 4 waiting room is full
CUSTOMER: 1 gets haircut
BARBER: cuts hair
CUSTOMER: 3 waiting room is full
CUSTOMER: 4 waiting room is full
CUSTOMER: 1 hair is growing
CUSTOMER: 2 gets haircut
BARBER: cuts hair
CUSTOMER: 4 is in the room
CUSTOMER: 3 waiting room is full
CUSTOMER: 3 waiting room is full
CUSTOMER: 1 waiting room is full
CUSTOMER: 2 hair is growing
CUSTOMER: 0 gets haircut
BARBER: cuts hair
CUSTOMER: 3 is in the room
CUSTOMER: 1 waiting room is full
CUSTOMER: 2 waiting room is full
CUSTOMER: 0 hair is growing
CUSTOMER: 3 gets haircut
BARBER: cuts hair
CUSTOMER: 1 is in the room
CUSTOMER: 2 waiting room is full
CUSTOMER: 0 waiting room is full
CUSTOMER: 3 hair is growing
CUSTOMER: 1 gets haircut
BARBER: cuts hair
```

Output could contain various numbers of messages in this format. However the number of processes inside the room should not exceed the `SIZE_OF_WAITING_ROOM`
The script spawns 5 processes by default, but you can play around with this variable by changing the value of `NUM_THREADS`.

## How does this program work
This program represents the solution for barber shop using multiple processes. To ensure correct execution of program processes need to comply to following rules:
1. The number of processes that can enter into critical section (waiting room) has to be limited by constant `SIZE_OF_WAITING_ROOM` (by default set to `3`). To ensure that number of processes inside critical section won't exceed `SIZE_OF_WAITING_ROOM`, synchronization pattern **Multiplex** is used.
2. The integrity of counter is protected by mutex using `shared.mutex.lock()`/`shared.mutex.unlock()`
3. Synchronization pattern **Rendezvous** is used to ensure that only one customer process can enter `get_haircut`, only when barber process is not doing any work
4. Synchronization pattern **Rendezvous** is used after functions `get_haircut` and `cut_hair` are finished to reestablish integrity again.

