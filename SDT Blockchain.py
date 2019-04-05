'''This program is still a working progress'''
from collections import  defaultdict
import math
import time
import datetime
from dateutil.parser import parse
from binary_heap import MaxHeap
import copy
''' Item class that represent each transaction'''
class Item:    
    def __init__(self,k,v,w):
        self.key = k
        self.value = float(v)
        self.weight = float(w)
    def __str__(self):
        return str(self.value/self.weight)
    def __repr__(self):
        return (self.value / self.weight)
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
        
''' Block class represents a block with a set of transactions, total fee, size and number of transactions.'''
class Block:
    def __init__(self):
        self.transactions = []
        self.fee = 0
        self.count = 0
        self.size = 0
    def add(self, item):
        result = False
        if isinstance(item, Item):
            self.transactions.append(item)
            self.fee += item.value # in order to converter the value to dollars
            self.count +=1
            self.size += item.weight
            result = True
        return result
            
    def addBulk(self, listItems):
        #self.transactions.extend(listItems)
        #option to improve performance
        for item in listItems:
            if not self.add(item):
                print("error")

    def print(self):
        print("Size = ", self.size)
        print("Value = ", self.fee)
        print("Total = ", self.count)

"""
Class Knapsack has method that simulate the algorithm used in bitcore.
"""
class Knapsack:
    def __init__(self,):
        self.max_heap = MaxHeap()  

    
    def add(self, item):
        self.max_heap.add_element(item)

    #function to fill the knapsack(block) with transactions based on thier density value
    def fillold(self, items, capacity):
        block = Block()
        cap = capacity - block.size()
        items = sorted(items, key=lambda item: (item.value/item.weight), reverse=True)
        for item in items:
            if item.weight <= cap:
                block.add(item)
                cap -= item.weight
        return block
    def fill (self, capacity):
        #add a function that limit the algorithm to check the whole list.
        #max_heap = MaxHeap(items)
        block = Block()
        cap = capacity - block.size
        lastFewTxs = 0        
        for x in range(len(self.max_heap.elements())):
            item = self.max_heap.get_root_value()
            if item.weight <= cap:
                block.add(item)                
                self.max_heap.extract_root()        
                cap -= item.weight                    
            elif block.size > capacity -100 or lastFewTxs > 50:
                break
            if block.size > capacity - 1000:
                lastFewTxs += 1
        return block
               
"""Algorithm to fill the blocks with transactions. It is based on a matrix of size by densite. Each classe is represented by one index of this matrix."""
class SDT:
    '''
    Method to initialize the class with upperbounds and 
    '''
    def __init__(self,sizeClass, densityClass,sizeLimit,DensitUpper):
        # have different inputs for X and Y (2 dif classes)
        self.sizeClassLimit = sizeClass
        self.densityClassLimit = densityClass
        self.sizeLimit = sizeLimit
        self.densityUpper = DensitUpper
        self.table = [[[] for x in range(self.densityClassLimit)]for y in range(self.sizeClassLimit)]
        self.sizeTable = [[0 for x in range(self.densityClassLimit)]for y in range(self.sizeClassLimit)]
        self.count = 0
    '''
    Method responsible for add transaction into the right classes.
    '''
    def add(self, item):
        self.count +=1
        density = item.value/item.weight
        densityScaled = density/self.densityUpper
        sizeClass = math.floor((item.weight/self.sizeLimit)%self.sizeClassLimit)        
        if densityScaled >= 1:
            self.table[sizeClass][self.densityClassLimit-1].append(item)            
            self.sizeTable[sizeClass][self.densityClassLimit-1] += item.weight
        else:
            densityClass = math.floor(densityScaled*self.densityClassLimit)
            self.table[sizeClass][densityClass].append(item)
            self.sizeTable[sizeClass][densityClass] += item.weight
        return
    
    def addLog(self,item,logbase):
        self.count +=1
        density = item.value/item.weight
        if density >0:
            densityScaledReversed = self.densityUpper/density
        else:
            densityScaledReversed = 1000000
        sizeScaledReversed = self.sizeLimit/item.weight                
        if sizeScaledReversed <=1:
            sizeClass = self.sizeClassLimit -1
        else:
            #print(sizeScaledReversed)
            #print(math.log(sizeScaledReversed,logbase))
            sizeClass = self.sizeClassLimit - math.floor(math.log(sizeScaledReversed,logbase)) -1
            if sizeClass <0 :
                sizeClass = 0
        
        #print(sizeClass)
        if densityScaledReversed <= 1:
            self.table[sizeClass][self.densityClassLimit-1].append(item)            
            self.sizeTable[sizeClass][self.densityClassLimit-1] += item.weight
        else:
            densityClass = self.densityClassLimit - math.floor(math.log(densityScaledReversed,logbase))-2
            if densityClass < 0 :
                densityClass = 0            
            #print(sizeClass)
            #print(densityClass)
            self.table[sizeClass][densityClass].append(item)
            self.sizeTable[sizeClass][densityClass] += item.weight
        return
    '''  
    Method responsible for create a block with the better profit possible.
    '''    
    def fill(self, blockLimit):
        #print(self.count)
        block = Block()        
        cap = blockLimit- block.size
        terminated = False
        j = self.densityClassLimit -1        
        #lastFewTxs = 0
        isSorted = False
        while not terminated and j >= 0:                     
            index = cap/blockLimit        #empty fraction of the block    
            si = math.floor(index * (self.sizeClassLimit-1)) # class which cap belongs
            selected = False
            i = si -1 # any transaction at class I for sizes fits in the remaining capacity. While transaction in SI might fit or might not.
            
            
            # check if all the transactions in this class fit in the remaning portion of the block
            while i >= 0 and not selected:
                if len(self.table[i][j]) > 0:
                    x = self.table[i][j].pop()
                    block.add(x)
                    selected = True
                else:
                    i -= 1
            #classSi = self.table[si][j]
            #sorted(classSi, key=lambda item: (item.value/item.weight), reverse=True)
            if not selected:
                for item in self.table[si][j]:
                    if item.weight <= cap:
                        block.add(item)
                        self.table[si][j].remove(item)
                        selected = True
                        break

            
            if not selected:
                j -= 1
            else:
                cap = blockLimit - block.size
                if cap == 0 :
                    terminated = True                     
        return block

    def fill1(self, blockLimit):
        #print(self.count)
        block = Block()        
        cap = blockLimit- block.size
        terminated = False
        j = self.densityClassLimit -1        
        #lastFewTxs = 0
        while not terminated and j >= 0:                     
            index = cap/blockLimit        #empty fraction of the block    
            si = math.floor(index * (self.sizeClassLimit-1)) # class which cap belongs
            selected = False
            i = si -1 # any transaction at class I for sizes fits in the remaining capacity. While transaction in SI might fit or might not.                
            # check if all the transactions in this class fit in the remaning portion of the block
            if  self.sizeTable[si][j] < cap and self.sizeTable[si][j] != 0:
                block.addBulk(self.table[si][j])                
                selected = True
                self.table[si][j].clear()
                self.sizeTable[si][j] = 0 # clean the list with transaction I just added in the block
            elif self.sizeTable[i][j] < cap and self.sizeTable[i][j] != 0:
                block.addBulk(self.table[i][j])                
                selected = True
                self.table[i][j].clear()
                self.sizeTable[i][j] = 0 # clean the list with transaction I just added in the block 

           
            
            # some of them fits, but some of them not. So check the size of each one of them.
            if not selected:
                classSi = self.table[si][j][:]
                if len(classSi) > 0:
                    #print(*classSi)
                    #classSi.sort(key=lambda item: (item.value/item.weight), reverse=True)
                    #print(*classSi)
                    #input()
                    for item in classSi: #self.table[si][j]:
                        if item.weight <= cap:
                            block.add(item)

                            self.table[si][j].remove(item)                        
                            cap = blockLimit - block.size
                            selected = True
                            break
            
            # maybe sorting by density can help
            # add one by one transactions because any of them fits, but not all of them as whole. 
            while i >= 0 and not selected:
                if len(self.table[i][j]) > 0:
                    x = self.table[i][j].pop()
                    block.add(x)
                    selected = True
                else:
                    i -= 1                       
            if not selected:
                j -= 1
            else:
                cap = blockLimit - block.size                
                if cap == 0 :
                    terminated = True                     
        return block
    
    def fillLog(self, blockLimit,logbase):
        #print(self.count)
        block = Block()        
        cap = blockLimit- block.size
        terminated = False
        j = self.densityClassLimit -1        
        #lastFewTxs = 0
        while not terminated and j >= 0:                     
            #index = cap/blockLimit        #empty fraction of the block    
            sizeScaledReversed = blockLimit/cap # makesure the result is positive ( I am not sure about it)
            #print(cap)
            #print(sizeScaledReversed)
            #self.sizeClassLimit - math.floor(math.log(sizeScaledReversed,logbase)) -1
            si = self.sizeClassLimit - math.floor(math.log(sizeScaledReversed,logbase)) -1 # class which cap belongs
            if si < 0:
                si = 0
            if si <=1:
                si = self.sizeClassLimit -1
            selected = False
            i = si -1 # any transaction at class I for sizes fits in the remaining capacity. While transaction in SI might fit or might not.                
            # check if all the transactions in this class fit in the remaning portion of the block
            #print(si)
            if  self.sizeTable[si][j] < cap and self.sizeTable[si][j] != 0:
                block.addBulk(self.table[si][j])                
                selected = True
                self.table[si][j].clear()
                self.sizeTable[si][j] = 0 # clean the list with transaction I just added in the block
            elif self.sizeTable[i][j] < cap and self.sizeTable[i][j] != 0:
                block.addBulk(self.table[i][j])                
                selected = True
                self.table[i][j].clear()
                self.sizeTable[i][j] = 0 # clean the list with transaction I just added in the block 

           
            
            # some of them fits, but some of them not. So check the size of each one of them.
            if not selected:
                classSi = self.table[si][j][:]
                if len(classSi) > 0:
                    #print(*classSi)
                    #classSi.sort(key=lambda item: (item.value/item.weight), reverse=True)
                    #print(*classSi)
                    #input()
                    for item in classSi: #self.table[si][j]:
                        if item.weight <= cap:
                            block.add(item)
                            self.table[si][j].remove(item)                        
                            cap = blockLimit - block.size
                            selected = True
                            break
            
            # maybe sorting by density can help
            # add one by one transactions because any of them fits, but not all of them as whole. 
            while i >= 0 and not selected:
                if len(self.table[i][j]) > 0:
                    x = self.table[i][j].pop()
                    block.add(x)
                    selected = True                    
                else:
                    i -= 1                       
            if not selected:
                j -= 1
            else:
                cap = blockLimit - block.size                
                if cap <= 0 :
                    terminated = True                     
        return block
    
    def fillLog1(self, blockLimit,logbase):
        block = Block() 
        cap = blockLimit - block.size
        terminated = False
        j = self.densityClassLimit -1
        si = self.sizeClassLimit -1
        while not terminated and j >=0:
            classSi = self.table[si][j][:]
            classSi.sort(key=lambda item: (item.value/item.weight), reverse=True)
            for item in classSi:
                if item.weight <= cap:
                    block.add(item)
                    self.table[si][j].remove(item)
                    cap = blockLimit - block.size
                if cap == 0:
                    break

            if si == 0:
                si = self.sizeClassLimit -1
                j -=1
            else:
                si -= 1
                cap = blockLimit - block.size
                if cap == 0:
                    terminated =True
        return block
    """print the table with the amount of transactions in each class"""
    def print(self,):
        for x in reversed(range(self.sizeClassLimit)):
            for y in range(self.densityClassLimit):
                print("<",len(self.table[x][y]),">",end=" ")
            print()

class Greed:
    def __init__(self,):
        self.memPool =[]
    def add(self, item):
        self.memPool.append(item)
    def fill(self,capacity):
        block = Block()
        cap = capacity - block.size
        lastFewTxs = 0        
        for item in self.memPool:            
            if item.weight <= cap:
                block.add(item)     
                cap -= item.weight                    
            elif block.size > capacity -100 or lastFewTxs > 50:
                break
            if block.size > capacity - 1000:
                lastFewTxs += 1
        return block
    def fillAdvice(self,capacity, advice):
        block = Block()
        cap = capacity - block.size
        lastFewTxs = 0        
        for item in self.memPool:            
            if item.weight <= cap and item.fee >= advice:
                block.add(item)     
                cap -= item.weight                    
            elif block.size > capacity -100 or lastFewTxs > 50:
                break
            if block.size > capacity - 1000:
                lastFewTxs += 1
        return block


def main (opt):
    """
    Tdatetime = "2017-11-06 00:00:00"
    #initial = datetime.datetime.strptime(Tdatetime,'%Y-%m-%d %H:%M:%S')
    nextblock = datetime.timedelta(minutes=10)
    initial = parse(Tdatetime) + nextblock
    sdt = SDT(25, 25,1000,0.1)
    count = 0
    with open('transactions061117.txt','r') as f:
        for line in f:
            fields = line.split(',')
            timeStamp = parse(fields[0])
            if timeStamp < initial:
                #sdt.addLog(Item(line.split(',')[0],line.split(',')[1],line.split(',')[2]),1.2)
                sdt.add(Item(fields[0],fields[1],fields[2]))
            else:
                initial += nextblock
                count +=1
                print(count)
                sdt.print()
                mined = sdt.fill1(1000000) # Block size
                mined.print()
                #sdt.print()                
    """
    container = None
    if opt == 0 or opt == 1:
        container = Greed()
        #greedonly    
    elif opt == 2:
        container = Knapsack()
    elif opt == 3:
        container = SDT(170,170,1000.0,0.003)
    else:
        print("Invalid Argument")
    capacity = 1000000    
    with open('transactionsM2803.txt','r') as f:
        for line in f:               
            # item (value, weight)
            container.add(Item(line.split(',')[0],line.split(',')[1],line.split(',')[2]))         
    #start_time = time.time()
    #container.print()
    if opt == 1:
        mined = container.fillAdvice(capacity,1)
    else:
        mined = container.fill(capacity)
    f.close() 
    return mined

def simulation (capacity):
    #SDT(100,100,1000.0,0.01)
    sizeClass = 170
    densitClass = 170
    sizeUpper = 1000
    densityUpper = 0.001
    block = Block()
    param = []
    count = 0
    for isize in range(10):
        sizeClass += 0
        densitClass = 170
        for idensity in range(10):
            densitClass += 0
            sizeUpper = 1000
            for isizeUpper in range(10):
                sizeUpper += 0    
                densityUpper = 170            
                for idensityUpper in range(10):
                    count +=1                                                
                    densityUpper += 0.001
                    sdt = SDT(sizeClass,densitClass,sizeUpper, densityUpper)    
                    with open('transactionsM2803.txt','r') as f:
                        for line in f:               
                            # item (value, weight)
                            sdt.add(Item(line.split(',')[0],line.split(',')[1],line.split(',')[2]))         
                    #start_time = time.time()
                    #container.print()
                    mined = sdt.fill(capacity)
                    f.close() 
                    if mined.fee > block.fee:
                        block = copy.deepcopy(mined)
                        param = [sizeClass,densitClass,sizeUpper,densityUpper]
                    print(count)
    block.print()
    print(param)
    return block


if __name__ == "__main__":

    for x in range(1):
        start_time = time.time()
        result = main(3)
        #result = simulation(1000000)
    # time for the algorithm is computed and printed        
        result.print()
        print( time.time() - start_time)
        
        
