"""
This program represents my solution of Feasting savages problem (fourth assignment for PPDS course at FEI STU). 

University: STU Slovak Technical University in Bratislava
Faculty: FEI Faculty of Electrical Engineering and Information Technology
Year: 2023
"""


__authors__ = "Martin Mečír"
__email__ = "mecir.martin@gmail.com"
__license__ = "MIT"


from fei.ppds import Mutex, Thread, Semaphore, print
from time import sleep

NUM_OF_SAVAGES = 5
SIZE_OF_COOKING_POT = 3


class Shared(object):

    def __init__(self):
        """
            Init method of Shared class

            :param self: reference to object
        """
        self.pot_mutex = Mutex()
        self.cooking_pot = SIZE_OF_COOKING_POT
        self.empty_pot = Semaphore(0)
        self.full_pot = Semaphore(0)

        self.turnstile = Semaphore(0)
        self.turnstile2 = Semaphore(1)
        self.barrier_mutex = Mutex()
        self.barrier_count = 0


def feast(i: int, shared: Shared):
    """
    Function which represents feasting of a savage.

    :param i: id of a savage
    :param shared: shared object with synchronization ADT
    """
    while True:
        shared.barrier_mutex.lock()
        shared.barrier_count += 1
        if shared.barrier_count == NUM_OF_SAVAGES:
            print(f'SAVAGE: {i} arrived, barrier unlocking')
            shared.turnstile2.wait()
            shared.turnstile.signal()
        shared.barrier_mutex.unlock()
        print(f'SAVAGE: {i} waiting on barrier')
        shared.turnstile.wait()
        shared.turnstile.signal()

        shared.pot_mutex.lock()
        # critical section
        if shared.cooking_pot == 0:
            print(f'SAVAGE: {i} went to take a portion, but pot is empty, waiting for refill')
            shared.empty_pot.signal()
            shared.full_pot.wait()
        shared.cooking_pot -= 1
        print(f'SAVAGE: {i} took a portion')
        shared.pot_mutex.unlock()

        shared.barrier_mutex.lock()
        shared.barrier_count -= 1
        if shared.barrier_count == 0:
            shared.turnstile.wait()
            shared.turnstile2.signal()
        shared.barrier_mutex.unlock()
        shared.turnstile2.wait()
        shared.turnstile2.signal()


def cook_food(shared: Shared):
    """
    Simulate time and print info when chef cooks the food

    :param shared: shared object with synchronization ADT
    """
    print('CHEF: food is cooking')
    sleep(1)
    shared.cooking_pot = SIZE_OF_COOKING_POT


def cook(shared: Shared):
    """
    Function cook represents chef. Chef is sleeping.
    When savage signalizes that pot is empty, chef wakes up and cooks the food.

    :param shared: shared object with synchronization ADT
    """
    while True:
        shared.empty_pot.wait()
        cook_food(shared)
        shared.full_pot.signal()


def main():
    shared = Shared()
    savages = []

    for i in range(NUM_OF_SAVAGES):
        savages.append(Thread(feast, i, shared))
    chef = Thread(cook, shared)

    for t in savages + [chef]:
        t.join()


if __name__ == "__main__":
    main()
