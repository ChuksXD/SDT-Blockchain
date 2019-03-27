
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
    size_table = [[[] for i in range(k1)] for j in range(k2)]

    for x in items:
        for s in range(k1):
            if x .size >  s/k1 and x.size <=(s+1)/k1:
                x.size_class = s
        for d in range(k2-1):
            if x.scaled_density >= d/(k2-1) and x.scaled_density < (d+1)/(k2-1):
                x.density_class = d
            elif x.scaled_density > 1:
                x.density_class = k2-1

    for x in items:
        for i in range(k1):
            for j in range(k2):
                if x.size_class == i and x.density_class==j:
                    size_table[i][j].append(x)

    cap =1
    j=k2-1
    max_number_transactions = 8;
    m=0 #number of selected transactions
    terminate = False
    while m < max_number_transactions and terminate == False:
        s1 = cap * k1
        print(s1)
        selected = False
        i = s1 - 1
        while i > 0 and selected==False:
            print(i)
            print(j)
            if size_table[i][j] == []:
                i-=1
            else:
                transaction = size_table[i][j].pop()
                B.append(transaction)
                cap = cap - transaction.size
                selected = True

        for t in range(0,2):
            if selected == False:
                for transaction in size_table[i][j]:
                    if transaction.size <= cap:
                        B.append(transaction)
                        size_table[s1][j].remove(transaction)
                        cap = cap - transaction.size
                        selected = True

        if selected == False:

            j-=1
            if j == -1:
                terminate = True
        else:
            m+=1



fees=[]
sizes=[]
with open('transactions.txt','r') as f:
    for line in f:
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


P=29.33
key_count =1;
items=[]
B=[]
for x in range(len(fees)):
    items.append(item(key_count,fees[x],sizes[x]))
    key_count+=1
SDT(50,50)




