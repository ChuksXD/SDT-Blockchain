#Pure online greedy knapsack algorithm for the blockchain transactions 
from numpy import *
import time
#A variable that holds the total capacity of the block at a given time
global totalW
#Create a class for the transactions
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


#Online knapsack greedy funnction that processes each transaction sequentially without knowing the future transactions
def greedy(item, maxWeight,total,knapsack):
    global totalW
    totalW= total

    w = item.getWeight()

    if w + totalW <= maxWeight:
        knapsack.append(item)
        totalW += w
        return knapsack
    else:
        return None
#function that creates each transaction object and sends each one to the greedy function
def calc(count,n):
    for x in range(n):

        newitem = item(id[count],fee[count],size[count])
        greedy(newitem,Blocksize,totalW,knapsack)

        count+=1
#start timing of driver program
start_time = time.time()
#Extract needed values from mempool data
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
fee = [float(i)/10000 for i in fee]
size = [float(i) for i in size]
#create a block(knapsack array)
knapsack =[]
#define blocksize in terms of bytes
Blocksize = 1000000
No_of_items = len(fee)
totalW = 0
count = 0
calc(count,No_of_items)
knapsack[:] = [item for item in knapsack if item is not None]
Knapsack_size = len(knapsack)
sum =0
#get total value of all transactions in the block
for x in range(0,Knapsack_size):
    sum+=knapsack[x].getValue()
print("Total value from transactions in block is ", sum, ' dollars')
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
