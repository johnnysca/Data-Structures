# explanations for member functions are provided in requirements.py
# each file that uses a cuckoo hash should import it from this file.
import random as rand
from typing import List


class CuckooHash:
    def __init__(self, init_size: int):
        self.__num_rehashes = 0
        self.CYCLE_THRESHOLD = 10

        self.table_size = init_size
        self.tables = [[None] * init_size for _ in range(2)]

    def hash_func(self, key: int, table_id: int) -> int:
        key = int(str(key) + str(self.__num_rehashes) + str(table_id))
        rand.seed(key)
        return rand.randint(0, self.table_size - 1)

    def get_table_contents(self) -> List[List[int]]:
        return self.tables

    # you should *NOT* change any of the existing code above this line
    # you may however define additional instance variables inside the __init__ method.

    def insert(self, key: int) -> bool:
        index = self.hash_func(key, 0)
        if self.tables[0][index] == None:
            self.tables[0][index] = key
            return True
        else:

            prev = self.tables[0][index]
            self.tables[0][index] = key
            evictions = 1
            idx = 1
            index = self.hash_func(prev, idx)
            while self.tables[idx][index] != None:
                if(evictions > self.CYCLE_THRESHOLD):
                    return False
                prev2 = self.tables[idx][index]
                self.tables[idx][index] = prev
                evictions += 1
                idx = (idx + 1) % 2
                prev = prev2
                index = self.hash_func(prev, idx)
            self.tables[idx][index] = prev
            return True



    def lookup(self, key: int) -> bool:
        index1, index2 = self.hash_func(key, 0), self.hash_func(key, 1)
        return self.tables[0][index1] == key or self.tables[1][index2] == key

    def delete(self, key: int) -> None:
        if self.lookup(key):
            index1, index2 = self.hash_func(key, 0), self.hash_func(key, 1)
            if self.tables[0][index1] == key:
                self.tables[0][index1] = None
            else:
                self.tables[1][index2] = None

    def rehash(self, new_table_size: int) -> None:
        self.__num_rehashes += 1;
        self.table_size = new_table_size  # do not modify this line

        existing_elements = []
        for i in range(2):
            for j in range(len(self.tables[i])):
                if self.tables[i][j] != None:
                    existing_elements.append(self.tables[i][j])

        self.tables = [[None] * new_table_size for _ in range(2)]

        for num in existing_elements:
            self.insert(num)

# feel free to define new methods in addition to the above
# fill in the definitions of each required member function (above),
# and for any additional member functions you define

