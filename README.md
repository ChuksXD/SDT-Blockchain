# BlockchainKnapsack
Experimental analysis of weighted knapsack algorithms for transaction selection in blockchain technology.

The algorithms are as follows:

Dynamic_KnapsackBlockchain: Implementation of an offline knapsack algorithm that uses dynamic programming on the transactions in the 
mempool to fill in a block.

KnapsackOffline: Implementation of an offline knapsack algorithm that finds the density of  each transaction in the mempool and arranges 
all the transactions in descending order of thier densities then performs a greedy process of selecting transactions with larger densities
that can fit the block.

KnapsackBlockchain:Implementation of a pure online greedy algorithm that selects or rejects transactions as soon as they arrive.

KnapsackBlockchainwithadvice: Implementation of an online advice model that is given the optimal solution of an offline algorithm (in this
case KnapsackOffline) in order to improve its value by comparing the density of each transaction to the total density of the block formed
in the offline algorithm.

Transaction.txt: Mempool data (for November 2018) in text format obtained from blockchair.com/bitcoin. The data is arranged thus 
#BlockId, #Hash, #date&time, #input_count, #output_count, #output_total(in BTC), #Output_total(in USD),  #Output_fee(in BTC), 
#Output_fee * 10000(in USD), #Size (in bytes)
