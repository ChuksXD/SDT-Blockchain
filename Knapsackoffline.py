''' Offline knapsack algorithm for the blockchain that orders all transactions in the mempool according to thier density value 
(in descending order) and then performs a greedy process''' 
import numpy 
import time
from binary_heap import MaxHeap

# create a class for the transactions
class Item:
    def __init__(self, value, weight):
        self.value = float(value)
        self.weight = float(weight)
    def __repr__(self):
        return str(self.value + self.weight)
    def __eq__(self, other):
        return ((self.value/self.weight) == (other.value/ other.weight))
    def __lt__(self, other):
        return ((self.value/self.weight) < (other.value/ other.weight))
    def __le__(self, other):
        return ((self.value/self.weight) <= (other.value/ other.weight))
    def __gt__(self, other):
        return ((self.value/self.weight) > (other.value/ other.weight))
    def __ge__(self, other):
        return ((self.value/self.weight) >= (other.value/ other.weight))
    
#create a class for the block
class Knapsack:
    def __init__(self, capacity, items_list= []):
        self.capacity = capacity
        self.items_list = items_list
        self.current_value = 0
        self.items_no = 0
        self.current_weight = 0    

    def can_fill(self, item):
        return self.current_weight + item.weight <= self.capacity
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
    def fillh (self, max_heap):
        #add a function that limit the algorithm to check the whole list.
        #max_heap = MaxHeap(items)
        lastFewTxs = 0
        for x in range(len(max_heap.elements())):
            item = max_heap.get_root_value()
            if self.can_fill(item):
                self.items_list.append(item)
                self.current_value += item.value
                self.current_weight += item.weight
                self.items_no+=1
                max_heap.extract_root()                
            elif self.current_weight > self.capacity -100 or lastFewTxs > 50:
                break
            if self.current_weight > self.capacity - 1000:
                lastFewTxs += 1
                
            

def main():
    fee=[]
    size=[]
    #extract neeeded values from mempool data
    max_heap = MaxHeap()    
    with open('transactions.txt','r') as f:
        for line in f:
            values  = line.split(',')
            max_heap.add_element(Item(values[8],values[9]))                        

    f.close()    

#define blocksize in terms of bytes
    Blocksize = 1000000
    No_of_items = len(fee)
    bag = Knapsack(Blocksize)

    items = max_heap.elements()   

    #fill block
    #bag.fill(items)
    bag.fillh(max_heap)
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
