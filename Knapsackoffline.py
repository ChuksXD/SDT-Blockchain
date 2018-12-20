''' Offline knapsack algorithm for the blockchain that orders all transactions in the mempool according to thier density value 
(in descending order) and then performs a greedy process''' 
from numpy import *
import time
# create a class for the transactions
class Item:
    def __init__(self, value, weight):
        self.value = value
        self.weight = weight

#create a class for the block
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
    #function to fill the knapsack(block) with transactions based on thier density value
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
    #extract neeeded values from mempool data
    with open('transactions.txt','r') as f:
        for line in f:
            fee.append(line.split(',')[8])
            size.append(line.split(',')[9])

    f.close()
    
    fee = [int(i) for i in fee]
    size = [int(i) for i in size]

#define blocksize in terms of bytes
    Blocksize = 1000000
    No_of_items = len(fee)
    bag = Knapsack(Blocksize)

    items = []

    for x in range(No_of_items):

        items.append(
            Item(fee[x], size[x])
        )
    #fill block
    bag.fill(items)
    total_value = bag.current_value
    #divide by 10000 to get the value in USD
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
