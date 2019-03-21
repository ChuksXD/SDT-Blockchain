'''This program is still a working progress'''
from collections import  defaultdict
class item:
    size_class = 0
    density_class=0
    def __init__(self,k,v,w):
        self.key = k
        self.value = v
        self.weight = w
        self.density = self.value/self.weight
        self.scaled_density =self.density/P
        self.size = self.weight/Blocksize

def SDT(k1,k2):

    for x in items:
        for s in range(k1):
            if x .size >  s/k1 & x.size <=(s+1)/k1:
                x.size_class = s
        for d in range(k2-1):
            if x.scaled_density >= d/(k2-1) & x.scaled_density < (d+1)/(k2-1):
                x.density_class = d
            elif x.scaled_density > 1:
                x.density_class = k2-1


    size_table = [[0 for i in range(k1)] for j in range(k2)]
    dict = defaultdict(list)

    for x in items:
        for i in range(k1):
            for j in range(k2):
                if x.size_class == i & x.density_class==j:
                    dict[j].append(x)
                    size_table[i][j]=1


    cap =1
    j=k2-1
    max_number_transactions = 8;
    m=0 #number of selected transactions
    while m < max_number_transactions:
        s1 = cap * k1
        selected = False
        i = s1 - 1







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
knapsack =[]
#define blocksize in terms of bytes
Blocksize = 1000000
No_of_items = len(fee)

P=29.33# value is just temporary and an upper bound density should be calculated
key_count =1;
items=[]
for x in range(len(No_of_items)):
    items.append(item(key_count,fee[x],size[x]))
    key_count+=1
exit(-1)

