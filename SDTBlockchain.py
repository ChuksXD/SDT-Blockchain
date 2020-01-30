'''This program is still a working progress'''
from collections import  defaultdict
import os
import json
import sys
import numpy as np
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
import math
import time
import datetime
from dateutil.parser import parse
from binary_heap import MaxHeap
import copy
''' Item class that represent each transaction'''
class Item:    
    def __init__(self,key,value,weight, alfa):
        self.key = key
        self.value = float(value)
        self.weight = float(weight)  
        self.offset = alfa * 1
        self.density = (self.value- self.offset)/self.weight
    def __str__(self):
        return str(self.density)
    def __repr__(self):
        return (self.density)
    def __eq__(self, other):
        return ((self.density) == (other.density))
    def __lt__(self, other):
        return ((self.density) < (other.density))
    def __le__(self, other):
        return ((self.density) <= (other.density))
    def __gt__(self, other):
        return ((self.density) > (other.density))
    def __ge__(self, other):
        return ((self.density) >= (other.density))
        
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
    def __init__(self,sizeClass, densityClass,sizeUpper,DensitUpper):
        # have different inputs for X and Y (2 dif classes)
        self.sizeClassLimit = sizeClass
        self.densityClassLimit = densityClass
        self.sizeUpper = sizeUpper
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
        sizeScaled = item.weight/self.sizeUpper
        if densityScaled >= 1:
            densityClass = self.densityClassLimit -1
        else:
            densityClass = math.floor(densityScaled*(self.densityClassLimit-1))
        if sizeScaled >=1 :
            sizeClass = self.sizeClassLimit -1
        else:
            sizeClass = math.floor((item.weight/self.sizeUpper)*(self.sizeClassLimit-1))

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
        while not terminated and j >= 0:                     
            index = cap/self.densityUpper                   #empty fraction of the block    
            if index >=1:
                si = self.sizeClassLimit -1
            else:
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
                # for item in self.table[si][j]:
                #     if item.weight <= cap:
                #         block.add(item)
                #         self.table[si][j].remove(item)
                #         selected = True
                #         break            
                for item in range(len(self.table[si][j])):
                    if self.table[si][j][item].weight <= cap:
                        block.add(self.table[si][j][item])
                        self.table[si][j].pop(item)
                        selected = True
                        break            
            if not selected:
                j -= 1
            else:
                cap = blockLimit - block.size
                if cap < 100 :
                    terminated = True                     
        return block

    def fillOpt(self, blockLimit):
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
                if cap <= 100 :
                    terminated = True                     
        return block
    
   
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
        self.memPool = list()
    def add(self, item):
        self.memPool.append(item)

    def fill(self,capacity):
        block = Block()
        cap = capacity - block.size
        lastFewTxs = 0 
        index = 0   
        for item in self.memPool:            
            if item.weight <= cap:
                block.add(item)     
                cap -= item.weight
                self.memPool.pop(index)             
            if block.size > capacity -100 or lastFewTxs > 50:
                break
            elif block.size > capacity - 1000:
                lastFewTxs += 1
            index +=1
        return block
    
class GreedAdvice:
    def __init__(self,advice):
        self.memPool = list()
        self.advice = advice
        self.memPollRejected = list()
    def add(self, item):
        if item.density >= self.advice:
            self.memPool.append(item)
        else:
            self.memPollRejected.append(item)

    def fill(self,capacity):
        block = Block()
        cap = capacity - block.size
        lastFewTxs = 0 
        index = 0      
        for item in self.memPool:            
            if item.weight <= cap:
                block.add(item)     
                cap -= item.weight
                self.memPool.pop(index)             
            if block.size > capacity -100 or lastFewTxs > 50:
                break
            elif block.size > capacity - 1000:
                lastFewTxs += 1
            index += 1
        
        return block



def main (opt,SDTParam,transactionFile,fineTune):
    
    Tdatetime = "2019-10-20 23:52:45"
    capacity = 1000000
    #initial = datetime.datetime.strptime(Tdatetime,'%Y-%m-%d %H:%M:%S')
    nextblock = datetime.timedelta(minutes=10)    
    delay = datetime.timedelta(minutes=0) 
    blocksMinded = []    
    rounds = 3 # numebr of simulations
    totalTime = 0
    totalFee = 0
    totalTransactions = 0
    simulationTTime = 0
    broadcastTransactions = 0
    startSimulationTime = time.time()        
    container = None
    infos = {}
    minedInfo = {'addExtre':[], 'BlocksFee':[]}
    for i in range(rounds):
        delay = datetime.timedelta(minutes=i)
        initial = parse(Tdatetime) + nextblock
        if opt == 0 :
            container = Greed()
            #greedonly
        elif opt == 1:
            container = GreedAdvice(0.00037)    
        elif opt == 2:
            container = Knapsack()
        elif opt == 3:
            container = SDT(SDTParam[0],SDTParam[1],SDTParam[2],SDTParam[3])
        else:
            print("Invalid Argument")

        extraTrans = 0
        extraTransList = []
        for line in transactionFile:
            fields = line.split(',')
            timeStamp = parse(fields[1])
            if timeStamp < (initial + delay):
                extraTrans += 1
                #sdt.addLog(Item(line.split(',')[0],line.split(',')[1],line.split(',')[2]),1.2)
                broadcastTransactions += 1
                container.add(Item(fields[0],fields[2],fields[3],fineTune))
            else:
                #print(extraTrans)
                extraTransList.append(extraTrans)
                extraTrans = 0
                initial += nextblock
                #print(count)            
                begin = time.time()    
                mined = container.fill(capacity)
                blocksMinded.append(mined)
                totalTime += time.time() - begin
                #mined.print()                
                totalFee += mined.fee
                totalTransactions += mined.count                 
                #print(totalFee, end=',')
                #sdt.print()      
        values = []
        print(extraTransList)
        extraTransList.clear()
        for block in blocksMinded:
            values.append(block.fee)
        print(values)
        print()
        values.clear()
        blocksMinded.clear()
    simulationTTime += time.time() - startSimulationTime
        #mined.print()

    print('Total time = {}, Opcao = {} TransactionsReceived = {}, avgBlock = {}'.format(simulationTTime, opt,broadcastTransactions,totalTime/rounds), end=' ')
    print("Total fee = {} Total transactions = {}".format(totalFee/rounds,totalTransactions))
    return totalFee/rounds,totalTransactions/rounds, totalTime/rounds, simulationTTime

def simulation (capacity):
    #SDT(100,100,1000.0,0.01)
    sizeClass = 100
    densitClass = 100
    sizeUpper = 95000
    densityUpper = 0.0015                 
    result = None 
    best = Block()   
    simulationTime = 0               
    SDTParam = [sizeClass,densitClass,sizeUpper,densityUpper]              
    result, cumulativeTime, simulationTime = main(3, SDTParam)      
    print(simulationTime, cumulativeTime, SDTParam, result.fee, result.count, result.size)                            
    
    
    '''
    for x in range(100):
            SDTParam = [sizeClass,densitClass,sizeUpper,densityUpper]              
            result, cumulativeTime = main(3, SDTParam)      
            print(cumulativeTime/size, SDTParam, result.fee, result.count, result.size)                            
            cumulativeTime = 0
            if result.fee > best.fee:
                best = copy.deepcopy(result)
                best.print()
            sizeUpper +=1000   
    '''
    return result

def simulationGreed (capacity):
    block = Block() 
    best = 0
    count = 0
    advice = 0.00036
    Tdatetime = "2019-10-20 23:52:45"
    capacity = 1000000
    #initial = datetime.datetime.strptime(Tdatetime,'%Y-%m-%d %H:%M:%S')
    nextblock = datetime.timedelta(minutes=10)
    initial = parse(Tdatetime) + nextblock    
    blocksMinded = []
    begin = time.time()
    rounds = 1 # numebr of simulations
    totalTime = 0
    totalFee = 0
    totalTransactions = 0
    simulationTTime = 0
    broadcastTransactions = 0
    startSimulationTime = time.time()    
    container = Greed()        
    oldTotalFee = 0

    for i in range(10):
        with open('../Data/parsedData.csv','r') as f:
            for line in f:
                fields = line.split(',')
                timeStamp = parse(fields[1])
                if timeStamp < initial:
                    #sdt.addLog(Item(line.split(',')[0],line.split(',')[1],line.split(',')[2]),1.2)
                    broadcastTransactions += 1
                    container.add(Item(fields[0],fields[2],fields[3],0))
                else:
                    initial += nextblock
                    #print(rounds)                
                    mined = container.fillAdvice(capacity,advice)
                    totalFee += mined.fee
                    totalTransactions += mined.count
                    rounds +=1
                    #sdt.print()     
        print(rounds)
        rounds = 0     
        count += 1                     
                
        if totalFee > oldTotalFee:
            oldTotalFee = totalFee
            best = advice
            print("Total={} - Advice={}".format(oldTotalFee,best))
        totalFee = 0
        totalTransactions = 0
        initial = parse(Tdatetime) + nextblock

        f.close() 
        print(count)
        advice -= 0.00001
    block.print()
    print('advice =', best)



if __name__ == "__main__":
    
    #simulationGreed(1000000)        
    best = 0 
    transactionFile = open('/Users/dossants/Desktop/knapsack problem /Data/parsedData.csv','r').readlines()
    fineTune = 0.0000
    for option in range (2,4):         
        totalFee,totalTransactions, cumulativeTime , simulationTime= main(option,[100,100,60000,0.00069],transactionFile,fineTune)
            #result = simulation(1000000)
            # time for the algorithm is computed and printed        
            #result.print()
            #print(x) 
        # if totalFee > best:
            
        #     best = totalFee
        #     print("Total ={}, upperboud = {}".format(best,upperbound))  
        #fineTune += 0.001
        print(simulationTime,cumulativeTime, [], totalFee, totalTransactions)
        
    #simulation(1000000)    


