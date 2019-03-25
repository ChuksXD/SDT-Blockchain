'''This program is still a working progress'''
from collections import  defaultdict
import math
import time
''' Item class that represent each transaction'''
class Item:    
    def __init__(self,k,v,w):
        self.key = k
        self.value = float(v)
        self.weight = float(w)
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
            self.fee += item.value/10000 # in order to converter the value to dollars
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
    
    

"""Algorithm to fill the blocks with transactions."""
class SDT:
    def __init__(self,sizeClass, densityClass,sizeLimit,DensitUpper):
        # have different inputs for X and Y (2 dif classes)
        self.sizeClassLimit = sizeClass
        self.densityClassLimit = densityClass
        self.sizeLimit = sizeLimit
        self.densityUpper = DensitUpper
        self.table = [[[] for x in range(self.densityClassLimit)]for y in range(self.sizeClassLimit)]
        self.sizeTable = [[0 for x in range(self.densityClassLimit)]for y in range(self.sizeClassLimit)]

    def add(self, item):
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
        
    def fill(self, blockLimit):
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

           
            classSi = self.table[si][j]
            sorted(classSi, key=lambda item: (item.value/item.weight), reverse=True)
            # some of them fits, but some of them not. So check the size of each one of them.
            if not selected:
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

    """print the table with the amount of transactions in each class"""
    def print(self,):
        for x in reversed(range(self.sizeClassLimit)):
            for y in range(self.densityClassLimit):
                print("<",len(self.table[x][y]),">",end=" ")
            print()

def main ():
    sdt = SDT(1, 1000,1000,40)
    with open('transactions.txt','r') as f:
        for line in f:
            sdt.add(Item(line.split(',')[1],line.split(',')[8],line.split(',')[9]))
    
    #sdt.print()
    mined = sdt.fill1(1000000) # Block size
    mined.print()
    #sdt.print()
"""
    sdt = SDT(25,1000,40)
    with open('transactions.txt','r') as f:
        for line in f:
            sdt.add(Item(line.split(',')[1],line.split(',')[8],line.split(',')[9]))
    
    #sdt.print()
    mined = sdt.fill1(1000000)
    mined.print()
    #sdt.print()
    f.close() 
"""

if __name__ == "__main__":
    start_time = time.time()
    main()
    # time for the algorithm is computed and printed

    elapsed_time_secs = time.time() - start_time

    msg = "Execution took: %s secs " %elapsed_time_secs

    print(msg)
