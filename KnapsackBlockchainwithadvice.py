'''An  online advice model for the knapsack blockchain problem that is given the value from the offline optimal algorithm
(knapsackoffline) as advice and uses it as the optimal solution'''
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


#online greedy function with advice value of optimal solution
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
#function that creates each transaction object and sends each one to the greedy function
def calc(count,n):
    for x in range(n):

        newitem = item(id[count],fee[count],size[count])
        profit_density= newitem.getValue()/newitem.getWeight()

        greedy(newitem,Blocksize,totalW,knapsack,profit_density)

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
fee = [int(i) for i in fee]
size = [int(i) for i in size]
#create a block(knapsack)
knapsack =[]
#define blocksize in terms of bytes
Blocksize = 1000000
No_of_items = len(fee)
totalW = 0
count = 0
#advice bit from offline algorithm (Note that our optimal solution was divided by 10000 to get the value in USD)
optimal_solution = 2033.8212
'''Calculate advice function using the density (total value obtained / total size of block in bytes which is 1000000).
The total value has to be multiplied by 10000 before the division is done'''
total_value = optimal_solution * 10000
Advice_function = total_value/1000000

calc(count,No_of_items)
knapsack[:] = [item for item in knapsack if item is not None]
Knapsack_size = len(knapsack)
#get total value of all transactions in the block
sum =0
for x in range(0,Knapsack_size):
    sum+=knapsack[x].getValue()
print("Total value from transactions in block is ", sum/10000, ' dollars')
print('Total number of items included in knapsack is ', Knapsack_size)
print('Total number of items available is ', No_of_items)
print('items included are as follows')
print('<id,value,weight>')
#for x in knapsack:
#    print(' ',x)



# time for the algorithm is computed and printed

elapsed_time_secs = time.time() - start_time

msg = "Execution took: %s secs " %elapsed_time_secs

print(msg)
