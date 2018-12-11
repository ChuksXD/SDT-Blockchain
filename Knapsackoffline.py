from numpy import *
import time
from datetime import timedelta
class Item:
    def __init__(self, value, weight):
        self.value = value
        self.weight = weight


class Knapsack:
    def __init__(self, capacity, items_list= []):
        self.capacity = capacity
        self.items_list = items_list
        self.current_value = 0
        self.items_no = 0

    def current_weight(self):
        return sum(item.weight for item in self.items_list)

    def can_fill(self, item):
        return self.current_weight() + item.weight <= self.capacity

    def fill(self, items):
        items = sorted(items, key=lambda item: (item.value/item.weight), reverse=True)
        for item in items:
            if self.can_fill(item):
                self.items_list.append(item)
                self.current_value += item.value
                self.items_no+=1
    def countitems(self):
        return self.items_no
    def __repr__(self):
        return str(self.current_value)


def main():
    fee=[]
    size=[]
    with open('transactions.txt','r') as f:
        for line in f:
            fee.append(line.split(',')[8])
            size.append(line.split(',')[9])

    f.close()
#divide each fee by 10000 to get value in usd
    fee = [int(i) for i in fee]
    size = [int(i) for i in size]

#define blocksize in terms of bytes
    Blocksize = 1000000
    No_of_items = len(fee)
    #capacity, n = map(int, input().split())
    capacity = 10
    bag = Knapsack(Blocksize)

    items = []

    for x in range(No_of_items):

        items.append(
            Item(fee[x], size[x])
        )

    bag.fill(items)
    total_value = bag.current_value
    value = float(total_value/10000)
    print('Number of items in the knapsack', bag.countitems())
    print('Total value from transactions in block is ', value, 'dollars')


if __name__ == "__main__":
    start_time = time.time()
    main()
    # time for the algorithm is computed and printed

    elapsed_time_secs = time.time() - start_time

    msg = "Execution took: %s secs " %elapsed_time_secs

    print(msg)