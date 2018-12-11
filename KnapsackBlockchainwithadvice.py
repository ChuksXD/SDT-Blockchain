import time
from datetime import timedelta
from numpy import *
global totalW
class item:
    def __init__(self,id,v,w):
        self.id = id
        self.value= v
        self.weight = w
    def getID(self):
        return self.id
    def getValue(self):
        return self.value
    def getWeight(self):
        return self.weight

    def __str__(self):
        return '<' + self.id + ', ' + str(self.value) + ', ' \
               + str(self.weight) + '>'



def greedy(item, maxWeight,total,knapsack,p):
    global totalW
    totalW= total

    w = item.getWeight()
    if p>= Advice_function:
        if w + totalW <= maxWeight:
            knapsack.append(item)
            totalW += w
            return knapsack
        else:
            return None
    elif p< Advice_function:
        return None

def calc(count,n):
    for x in range(n):

        newitem = item(id[count],fee[count],size[count])
        profit_density= newitem.getValue()/newitem.getWeight()

        greedy(newitem,Blocksize,totalW,knapsack,profit_density)

        count+=1

start_time = time.time()
id = []
fee=[]
size=[]
with open('transactions.txt','r') as f:
    for line in f:
        id.append(line.split(',')[1])
        fee.append(line.split(',')[8])
        size.append(line.split(',')[9])

f.close()
#divide each fee by 10000 to get value in usd
fee = [int(i) for i in fee]
size = [int(i) for i in size]
knapsack =[]
#define blocksize in terms of bytes
Blocksize = 1000000
No_of_items = len(fee)
totalW = 0
count = 0
Advice_function =10.338212

calc(count,No_of_items)
knapsack[:] = [item for item in knapsack if item is not None]
Knapsack_size = len(knapsack)
sum =0
for x in range(0,Knapsack_size):
    sum+=knapsack[x].getValue()
print("Total value from transactions in block is ", sum/10000, ' dollars')
print('Total number of items included in knapsack is ', Knapsack_size)
print('Total number of items available is ', No_of_items)
print('items included are as follows')
print('<id,value,weight>')
for x in knapsack:
    print(' ',x)



# time for the algorithm is computed and printed

elapsed_time_secs = time.time() - start_time

msg = "Execution took: %s secs " %elapsed_time_secs

print(msg)