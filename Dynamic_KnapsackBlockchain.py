# A Dynamic Programming based Python Program for the Knapsack Blockchain problem
# Returns the maximum value that can be put in a Block of capacity 1mb

import time

#dynamic programming function obtained from geeksforgeeks
def knapSack(W, wt, val, n):
    K = [[0 for x in range(W+1)] for x in range(n+1)]

    # Build table K[][] in bottom up manner
    for i in range(n+1):
        for w in range(W+1):
            if i==0 or w==0:
                K[i][w] = 0
            elif wt[i-1] <= w:
                K[i][w] = max(val[i-1] + K[i-1][w-wt[i-1]], K[i-1][w])
            else:
                K[i][w] = K[i-1][w]

    return K[n][W]
#end knapsack function
#start timer
start_time = time.time()
#extract values from mempool data
id = []
fee=[]
size=[]
with open('transactions.txt','r') as f:
    for line in f:
        id.append(line.split(',')[1])
        fee.append(line.split(',')[8])
        size.append(line.split(',')[9])

f.close()
# Main Program to test dynamic function

#divide each fee by 10000 to get value in usd
fee = [float(i)/10000 for i in fee]
size = [float(i) for i in size]
#define blocksize in terms of bytes
Blocksize = 1000000
No_of_items = len(fee)
print("Total Value (in dollars) from transactions in the block",knapSack(Blocksize, size, fee, No_of_items))
# time for the algorithm is computed and printed
elapsed_time_secs = time.time() - start_time

msg = "Execution took: %s secs " %elapsed_time_secs
print(msg)

