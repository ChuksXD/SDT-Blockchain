# SDTBlockchain - transaction selection mining algorithm using SDT 
Comparing our proposed Size-Density table (SDT) strategy to different weighted knapsack algorithms for transaction selection from the mempool.
## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#Setup)

## GENERAL INFO
We introduce a data structure, SDT that outperforms the widely used transaction selection mining algorithms such as heap-based sorting. It improves performance by supporting insertion & deletion in constant time
and more importantly forms a block without the need to sort transactions.

In addition, the transactions selected by the SDT have a total fee that is comparable and in some cases, better than existing solutions. This enables miners to gain both speed and pofit when adopting our strategy.

The algorithms that we use for comparison are as follows:

* Dynamic_KnapsackBlockchain: Implementation of an offline knapsack algorithm that uses dynamic programming on the transactions in the 
mempool to fill in a block.

* KnapsackOffline: Implementation of an offline knapsack algorithm that finds the density of  each transaction in the mempool and arranges 
all the transactions in descending order of thier densities then performs a greedy process of selecting transactions with larger densities
that can fit the block.

* KnapsackBlockchain:Implementation of a pure online greedy algorithm that selects or rejects transactions as soon as they arrive.

* KnapsackBlockchainwithadvice: Implementation of an online advice model that is given the optimal solution of an offline algorithm (in this
case KnapsackOffline) in order to improve its value by comparing the density of each transaction to the total density of the block formed
in the offline algorithm.

* Heap Sort: An offline algorithm that uses heap-based strategy to sort the transactions. It was implemented using the following library. https://pypi.org/project/binary-heap/
* SDT Blockchain: Implementation of our proposed size-density table based stategy.

These algorithms can be found separately in the sorting algorithms folder.

The dataset used contained about 30,000 pending transactions that were in the Bitcoin mempool on 28th of March, 2019 at 5:04pm and was obtained from blockchair.com/bitcoin. It can be found in the transactions208.txt file.

# Technologies
* Python 3.7
* JSON

# Setup
Clone the repository and execute the SDT Blockchain.py file (It contains all the algorithms used in the comparison as well as SDT). Make sure you set transactions file to the TransactionM2803.txt or your own transactions file with the structure #DTC,#Output_fee * 10000(in USD), #Size (in bytes).

To test the algorithms separately, go to the sorting algorithms folder and execute any of the .py files. To use your own date structure it in this format:
BlockId, #Hash, #date&time, #input_count, #output_count, #output_total(in BTC), #Output_total(in USD),  #Output_fee(in BTC), #Output_fee * 10000(in USD), #Size (in bytes).



