# BlockchainKnapsack - transaction selection mining algorithm using SDT 
Comparing our proposed Size-Density table (SDT) strategy to different weighted knapsack algorithms for transaction selection from the mempool.
## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#Setup)

## General info
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

* Heap Sort: 
