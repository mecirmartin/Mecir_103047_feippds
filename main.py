"""
This program represents my solution of Dining philosophers problem (third assignment for PPDS course at FEI STU). 

University: STU Slovak Technical University in Bratislava
Faculty: FEI Faculty of Electrical Engineering and Information Technology
Year: 2023
"""


__author__ = "Martin Mečír, Tomáš Vavro"
__email__ = "mecir.martin@gmail.com"
__license__ = "MIT"


from fei.ppds import Thread, Mutex, Semaphore, print
from time import sleep

NUM_PHILOSOPHERS: int = 5
NUM_RUNS: int = 15  # number of repetitions of think-eat cycle of philosophers
RIGHT_HANDED_PHILOSOPHERS_IDS = [0, 1, 2, 3]
LEFT_HANDED_PHILOSOPHERS_IDS = [4]


class Shared:
    """
    Represent shared data for all threads.
    """

    def __init__(self):
        """
        Initialize an instance of Shared.

        :param self: reference to object
        """
        self.forks = [Mutex() for _ in range(NUM_PHILOSOPHERS)]
        self.waiter: Semaphore = Semaphore(NUM_PHILOSOPHERS - 1)


def think(i: int):
    """
    Simulate thinking.

    :param i: philosopher's id
    """
    print(f"Philosopher {i} is thinking!")
    sleep(0.1)


def eat(i: int):
    """
    Simulate eating.

    :param i: philosopher's id
    """
    print(f"Philosopher {i} is eating!")
    sleep(0.1)


def get_forks_right(i: int, shared: Shared):
    """
    Function to lock resources for right-handed philosopher.

    :param i: philosopher's id
    :param shared: shared object 
    """
    shared.forks[i].lock()
    sleep(0.5)
    shared.forks[(i+1) % NUM_PHILOSOPHERS].lock()


def get_forks_left(i: int, shared: Shared):
    """
    Function to lock resources for left-handed philosopher.

    :param i: philosopher's id
    :param shared: shared object 
    """
    shared.forks[(i+1) % NUM_PHILOSOPHERS].lock()
    sleep(0.5)
    shared.forks[i].lock()


def philosopher(i: int, shared: Shared):
    """
    Run philosopher's code.

    :param i: philosopher's id
    :param shared: shared object
    """
    for _ in range(NUM_RUNS):
        think(i)
        # get forks
        if i in RIGHT_HANDED_PHILOSOPHERS_IDS:
            get_forks_right(i, shared)
        else:
            get_forks_left(i, shared)
        eat(i)
        # put forks
        shared.forks[i].unlock()
        shared.forks[(i + 1) % NUM_PHILOSOPHERS].unlock()


def main():
    """
    Run main.
    """
    shared: Shared = Shared()
    philosophers: list[Thread] = [
        Thread(philosopher, i, shared) for i in range(NUM_PHILOSOPHERS)
    ]
    for p in philosophers:
        p.join()


if __name__ == "__main__":
    main()
