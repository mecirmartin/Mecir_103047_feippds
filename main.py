"""
Program represents different sequences of using mutex

University: STU Slovak Technical University in Bratislava
Faculty: FEI Faculty of Electrical Engineering and Information Technology
Year: 2023
"""


__authors__ = "Martin Mečír, Marián Šebeňa"
__email__ = "mecir.martin@gmail.com, mariansebena@stuba.sk, xvavro@stuba.sk"
__license__ = "MIT"


from fei.ppds import Mutex, Thread, Semaphore, print
from time import sleep

NUM_OF_CUSTOMERS = 5
SIZE_OF_WAITING_ROOM = 3


class Shared(object):

    def __init__(self):

        # TODO : Initialize patterns we need and variables
        self.mutex = Mutex()
        self.waiting_room = 0
        self.waiting_room_multiplex = Semaphore(SIZE_OF_WAITING_ROOM)
        self.customer = Semaphore(0)
        self.barber = Semaphore(0)
        self.customer_done = Semaphore(0)
        self.barber_done = Semaphore(0)


def get_haircut(i):
    # TODO: Simulate time and print info when customer gets haircut
    print(f'CUSTOMER: {i} gets haircut')
    sleep(1)
    pass


def cut_hair():
    # TODO: Simulate time and print info when barber cuts customer's hair
    print('BARBER: cuts hair')
    sleep(1)
    pass


def balk(i):
    # TODO: Represents situation when waiting room is full and print info
    print(f'CUSTOMER: {i} waiting room is full')
    sleep(0.5)
    pass


def growing_hair(i):
    # TODO: Represents situation when customer wait after getting haircut. So hair is growing and customer is sleeping for some time
    print(f"CUSTOMER: {i} hair is growing")
    sleep(1)
    pass


def customer(i, shared):
    # TODO: Function represents customers behavior. Customer come to waiting if room is full sleep.
    # TODO: Wake up barber and waits for invitation from barber. Then gets new haircut.
    # TODO: After it both wait to complete their work. At the end waits to hair grow again

    while True:
        # TODO: Access to waiting room. Could customer enter or must wait? Be careful about counter integrity :)
        shared.mutex.lock()
        if (shared.waiting_room == SIZE_OF_WAITING_ROOM):
            shared.mutex.unlock()
            balk(i)
            continue
        shared.mutex.unlock()

        shared.waiting_room_multiplex.wait()
        shared.mutex.lock()
        shared.waiting_room += 1
        shared.mutex.unlock()

        # if(temp <= SIZE_OF_WAITING_ROOM):
        #     shared.waiting_room_multiplex.signal()

        print(f'CUSTOMER: {i} is in the room')
        # TODO: Rendezvous 1
        shared.customer.wait()
        shared.barber.signal()
        get_haircut(i)
        # TODO: Rendezvous 2
        shared.customer_done.wait()
        shared.barber_done.signal()

        # TODO: Leave waiting room. Integrity again
        shared.mutex.lock()
        shared.waiting_room -= 1
        shared.mutex.unlock()
        shared.waiting_room_multiplex.signal()
        growing_hair(i)


def barber(shared):
    # TODO: Function barber represents barber. Barber is sleeping.
    # TODO: When customer come to get new hair wakes up barber.
    # TODO: Barber cuts customer hair and both wait to complete their work.

    while True:
        # TODO: Rendezvous 1
        shared.customer.signal()
        shared.barber.wait()
        cut_hair()
        # TODO: Rendezvous 2
        shared.customer_done.signal()
        shared.barber_done.wait()


def main():

    shared = Shared()
    customers = []

    for i in range(NUM_OF_CUSTOMERS):
        customers.append(Thread(customer, i, shared))
    hair_stylist = Thread(barber, shared)

    for t in customers + [hair_stylist]:
        t.join()


if __name__ == "__main__":
    main()
