from queue import Queue
import time
import threading
import random


class Table:
    def __init__(self, number:int):
        self.number = number
        self.guest = None

class Guest(threading.Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self):
        time.sleep(random.randint(3,10))


class Cafe:
    def __init__(self, *tables):
        self.queue = Queue()
        self.tables = tables

    def guest_arrival(self, *guests):
        for guest in guests:
            guest_seat = False
            for table in self.tables:
                if table.guest is None:
                    table.guest = guest
                    guest.start()
                    print(f'{guest.name} сел(-а) за стол номер {table.number}')
                    guest_seat = True
                    break

            if not guest_seat:
                    self.queue.put(guest)
                    print(f'{guest.name} в очереди')

    def discuss_guests(self):
        while self.queue.empty() or any(table.guest is not None for table in self.tables):
            for table in self.tables:
                if table.guest is not None:
                    if table.guest.is_alive():
                        pass
                    else:
                        print(f'{table.guest.name} покушал(-а) и ушёл(ушла).\nСтол номер {table.number} свободен')
                        table.guest = None

                        if not self.queue.empty() and table.guest is None:
                            queue_guest = self.queue.get()
                            table.guest = queue_guest
                            print(f'{queue_guest.name} вышел(-ла) из очереди и сел(-а) за стол номер {table.number}')
                            queue_guest.start()




# Создание столов
tables = [Table(number) for number in range(1, 6)]
# Имена гостей
guests_names = [
'Maria', 'Oleg', 'Vakhtang', 'Sergey', 'Darya', 'Arman',
'Vitoria', 'Nikita', 'Galina', 'Pavel', 'Ilya', 'Alexandra'
]
# Создание гостей
guests = [Guest(name) for name in guests_names]
# Заполнение кафе столами
cafe = Cafe(*tables)
# Приём гостей
cafe.guest_arrival(*guests)
# Обслуживание гостей
cafe.discuss_guests()
